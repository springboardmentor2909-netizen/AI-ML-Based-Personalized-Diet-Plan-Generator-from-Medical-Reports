import streamlit as st
import pdfplumber
import pytesseract
import cv2
import numpy as np
import pandas as pd
import pickle
import json
from openai import OpenAI

# =====================================================
# CONFIG
# =====================================================
import os
if os.name == "nt":
    import pytesseract
st.set_page_config(page_title="AI Personalized Diet Planner", layout="wide")

import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# =====================================================
# LOAD ML MODEL
# =====================================================
with open("combined_numerical_model.bkl", "rb") as f:
    model = pickle.load(f)

with open("combined_numerical_features.bkl", "rb") as f:
    feature_names = pickle.load(f)

# =====================================================
# FILE TEXT EXTRACTION (RAW ONLY)
# =====================================================
def extract_pdf_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_image_text(file):
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return pytesseract.image_to_string(gray)

# =====================================================
# GPT MEDICAL EXTRACTION (CORE LOGIC)
# =====================================================
def gpt_extract_medical_values(report_text):
    prompt = f"""
You are a medical data extraction AI.

The following text is from a medical report.
The text may be noisy, scanned, incomplete, or unstructured.

Your task:
Extract ONLY these values if present:
- HbA1c (%)
- Blood glucose (mg/dL)
- BMI
- Total cholesterol (mg/dL)
- Blood pressure (systolic/diastolic)
- Hypertension (1 if BP >=140/90 else 0)
- Heart disease (1 if mentioned else 0)

Rules:
- If value is missing, use null
- Do NOT guess
- Return ONLY valid JSON
- No explanation text

JSON format:
{{
  "hba1c_level": null,
  "blood_glucose_level": null,
  "bmi": null,
  "cholesterol": null,
  "systolic_bp": null,
  "diastolic_bp": null,
  "hypertension": 0,
  "heart_disease": 0
}}

Report Text:
\"\"\"{report_text}\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content[content.find("{"):content.rfind("}") + 1])
    except:
        return {
            "hba1c_level": None,
            "blood_glucose_level": None,
            "bmi": None,
            "cholesterol": None,
            "systolic_bp": None,
            "diastolic_bp": None,
            "hypertension": 0,
            "heart_disease": 0
        }

# =====================================================
# GPT DIET PLAN
# =====================================================
def generate_diet_plan(status, preferences):
    prompt = f"""
You are a certified Indian clinical dietitian.

Generate a personalized 3-day Indian diet plan.

Health Status:
{status}

Diet Preferences:
{preferences}

Rules:
- Indian food only
- No sugar if diabetic
- Simple home meals
- Return ONLY JSON

{{
  "Day 1": {{"Breakfast": "", "Lunch": "", "Dinner": ""}},
  "Day 2": {{"Breakfast": "", "Lunch": "", "Dinner": ""}},
  "Day 3": {{"Breakfast": "", "Lunch": "", "Dinner": ""}}
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    text = response.choices[0].message.content
    try:
        return json.loads(text[text.find("{"):text.rfind("}") + 1])
    except:
        return {}

# =====================================================
# STREAMLIT UI
# =====================================================
st.title("🩺 AI-Based Personalized Diet Plan System")

uploaded = st.file_uploader("Upload Medical Report (PDF / Image)", type=["pdf", "png", "jpg", "jpeg"])
preferences = st.text_input("Diet Preferences (optional)")

if uploaded:
    if uploaded.type == "application/pdf":
        raw_text = extract_pdf_text(uploaded)
    else:
        raw_text = extract_image_text(uploaded)

    st.subheader("Raw Extracted Text")
    st.text_area("", raw_text, height=300)

    # GPT extraction
    extracted = gpt_extract_medical_values(raw_text)

    st.subheader("Extracted Medical Values (GPT)")
    st.json(extracted)

    # Prepare ML input
    ml_input = {
        "hba1c_level": extracted["hba1c_level"] or 0,
        "blood_glucose_level": extracted["blood_glucose_level"] or 0,
        "bmi": extracted["bmi"] or 0,
        "cholesterol": extracted["cholesterol"] or 0,
        "hypertension": extracted["hypertension"],
        "heart_disease": extracted["heart_disease"]
    }

    X = pd.DataFrame([ml_input]).reindex(columns=feature_names, fill_value=0)
    ml_pred = model.predict(X)[0]

    # Final health status (hybrid rule)
    if extracted["hba1c_level"] and extracted["hba1c_level"] >= 6.5:
        status = "Diabetic (HbA1c clinical rule)"
    elif extracted["blood_glucose_level"] and extracted["blood_glucose_level"] >= 200:
        status = "Diabetic (Glucose clinical rule)"
    else:
        status = "Diabetic" if ml_pred == 1 else "Non-Diabetic"

    st.subheader("Health Status")
    if "Non" in status:
        st.success(status)
    else:
        st.error(status)

    # Diet plan
    st.subheader("🍱 3-Day Personalized Diet Plan")
    diet = generate_diet_plan(status, preferences)

    for day, meals in diet.items():
        st.markdown(f"### {day}")
        for meal, food in meals.items():
            st.write(f"**{meal}:** {food}")

    st.download_button(
        "Download JSON",
        json.dumps({
            "health_status": status,
            "extracted_values": extracted,
            "diet_plan": diet
        }, indent=2),
        file_name="diet_plan.json",
        mime="application/json"
    )
