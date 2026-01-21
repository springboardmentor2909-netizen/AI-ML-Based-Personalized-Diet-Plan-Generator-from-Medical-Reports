<<<<<<< HEAD
# ==============================
# Imports
# ==============================
import streamlit as st
from fpdf import FPDF
from ai_diet_generator import generate_diet
import re

# ==============================
# Custom CSS
# ==============================
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #0f1e1c, #192924);
    color: #e0ffe0;
    font-family: 'Segoe UI', sans-serif;
}
.stApp h1 {
    color: #00ff7f;
    text-align: center;
    font-size: 42px;
}
div.stButton > button {
    background: linear-gradient(90deg, #10b981, #34d399);
    color: white;
    font-size: 18px;
    padding: 10px 25px;
    border-radius: 12px;
    border: none;
}
.stTextInput input {
    border-radius: 12px;
    padding: 10px;
    border: 2px solid #10b981;
    background-color: #0f1e1c;
    color: #e0ffe0;
}
.diet-card {
    background-color: #1f3d28;
    color: #e0ffe0;
    padding: 18px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    font-size: 16px;
    line-height: 1.6;
}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==============================
# Remove emojis for PDF
# ==============================
def remove_emojis(text):
    emoji_pattern = re.compile(
        "[" 
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA70-\U0001FAFF"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# ==============================
# PDF Generator
# ==============================
def create_pdf(patient_id, diet_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "AI Diet Plan", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "", 11)

    clean_text = remove_emojis(diet_text)
    for line in clean_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    file_name = f"diet_plan_{patient_id}.pdf"
    pdf.output(file_name)
    return file_name

# ==============================
# Title
# ==============================
st.title("🥗 AI Diet Planner 🍎")
st.image(
    "https://images.unsplash.com/photo-1600891964599-f61ba0e24092",
    use_container_width=True

)

# ==============================
# Layout
# ==============================
col1, col2 = st.columns([2, 1])

with col1:
    patient_id = st.text_input("Enter Patient ID", placeholder="e.g. 101")

    if st.button("Generate Diet Plan"):
        if patient_id.isdigit():

            with st.spinner("Generating diet plan..."):
                diet_text = generate_diet(patient_id)

            if diet_text:
                st.success("✅ Diet Generated Successfully!")

                meals = {
                    "Breakfast 🥣": "",
                    "Lunch 🥗": "",
                    "Snacks 🍎": "",
                    "Dinner 🍛": ""
                }

                current_meal = None

                for raw_line in diet_text.split("\n"):
                    line = raw_line.strip()
                    lower = line.lower()

                    if lower.startswith("breakfast"):
                        current_meal = "Breakfast 🥣"
                        continue
                    if lower.startswith("lunch"):
                        current_meal = "Lunch 🥗"
                        continue
                    if lower.startswith("snack"):
                        current_meal = "Snacks 🍎"
                        continue
                    if lower.startswith("dinner"):
                        current_meal = "Dinner 🍛"
                        continue

                    if current_meal and line:
                        meals[current_meal] += f"- {line}<br>"

                st.subheader("Your Diet Plan 🥗")

                for meal, content in meals.items():
                    if content:
                        st.markdown(f"""
                            <div class="diet-card">
                                <b>{meal}</b><br><br>
                                {content}
                            </div>
                        """, unsafe_allow_html=True)

                pdf = create_pdf(patient_id, diet_text)
                with open(pdf, "rb") as f:
                    st.download_button(
                        "📄 Download PDF",
                        f,
                        file_name=pdf,
                        mime="application/pdf"
                    )

            else:
                st.error("❌ Diet generation failed")

        else:
            st.warning("⚠️ Enter numeric ID only")

with col2:
    st.image(
        "https://images.unsplash.com/photo-1567306226416-28f0efdc88ce",
        use_container_width=True

    )
    st.caption("Healthy Eating = Healthy Life 🥗")

# ==============================
# Footer
# ==============================
st.markdown("""
<div style="text-align:center; font-size:14px; margin-top:20px; color:#00ff7f;">
💡 Tip: Drink water & walk 30 minutes daily
</div>
""", unsafe_allow_html=True)




https://ai-diet-planner-vjmgltvwuegdxoudqq9kvx.streamlit.app/#your-diet-plan
https://share.streamlit.io/
=======

import streamlit as st
import json
import pandas as pd

from nlp.text_cleaning import TextCleaner
from nlp.intent_parser import IntentParser
from nlp.ner_model import MedicalNER

from ml.feature_extractor import FeatureExtractor, FEATURE_COLUMNS
from ml.predictor import Predictor

from llm.rule_generator import LocalLlama
from llm.json_normalizer import JSONNormalizer

from utils.pdf_utils import extract_text_from_pdf
from utils.ocr_utils import extract_text_from_image
from reports.pdf_generator import generate_pdf


# --------------------------
# Initialize components
# --------------------------
text_cleaner = TextCleaner()
ner_model = MedicalNER()
intent_parser = IntentParser()
feature_extractor = FeatureExtractor()

predictor = Predictor(
    model_path="models/lightgbm_patient_model.pkl",
    feature_path="models/lightgbm_features.pkl"
)

rule_generator = LocalLlama(model="llama3.1:8b")
json_normalizer = JSONNormalizer()


# --------------------------
# Streamlit UI
# --------------------------
st.set_page_config(
    page_title="AI Medical Diet Assistant",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 AI Medical Diet Assistant")
st.write(
    "Upload lab reports, doctor notes, or medical prescriptions "
    "to get personalized diet guidelines."
)


# --------------------------
# File upload
# --------------------------
uploaded_file = st.file_uploader(
    "Upload PDF, Image, or Text file",
    type=["pdf", "png", "jpg", "jpeg", "txt"]
)

if uploaded_file:
    st.info(f"Processing **{uploaded_file.name}**...")

    file_ext = uploaded_file.name.split(".")[-1].lower()

    # --------------------------
    # Text extraction
    # --------------------------
    if file_ext == "pdf":
        raw_text = extract_text_from_pdf(uploaded_file)
    elif file_ext in ["png", "jpg", "jpeg"]:
        raw_text = extract_text_from_image(uploaded_file)
    else:
        raw_text = uploaded_file.read().decode("utf-8")

    cleaned_text = text_cleaner.clean_text(raw_text)

    # --------------------------
    # NLP
    # --------------------------
    entities = ner_model.extract_entities(cleaned_text)
    medical_intent = intent_parser.parse_intent(cleaned_text, entities)

    # --------------------------
    # Feature extraction
    # --------------------------
    features = feature_extractor.extract_features_from_texts([cleaned_text])

    # --------------------------
    # Auto-fill missing features (NO user input)
    # --------------------------
    default_values = {
        "age": 30,
        "bmi": 22.0,
        "blood_sugar": 90.0,
        "cholesterol": 180.0,
        "hemoglobin": 13.5,
        "blood_pressure": 120.0,
        "heart_rate": 72.0,
        "weight": 70.0
    }

    for col in FEATURE_COLUMNS:
        if pd.isna(features.at[0, col]) or features.at[0, col] == 0:
            features.at[0, col] = default_values[col]

    features = features.astype(float)

    # --------------------------
    # Show extracted features
    # --------------------------
    st.subheader("🔍 Extracted Clinical Features")
    for col in FEATURE_COLUMNS:
        st.success(f"{col}: {features.at[0, col]}")

    # --------------------------
    # ML Prediction (ONLY ONCE)
    # --------------------------
    patient_status, model_diet_plan = predictor.predict(
        features.iloc[0].to_dict()
    )

    st.info(f"🩺 Patient Status: **{patient_status}**")

    # --------------------------
    # LLM Diet Generation
    # --------------------------
    patient_data = {
        "patient_status": patient_status,
        "medical_intent": medical_intent,
        "entities": entities,
        "model_diet_hints": model_diet_plan
    }

    diet_rules = rule_generator.generate_diet(patient_data)
    diet_json = json_normalizer.normalize(diet_rules)

    # --------------------------
    # Output
    # --------------------------
    st.subheader("✅ Personalized Diet Guidelines")
    st.json(diet_json)

    format_choice = st.radio("Select output format:", ["PDF", "JSON", "Both"])

    if format_choice in ["JSON", "Both"]:
        st.download_button(
            "Download JSON",
            data=json.dumps(diet_json, indent=2),
            file_name="diet_guidelines.json",
            mime="application/json"
        )

    if format_choice in ["PDF", "Both"]:
        pdf_path = generate_pdf(
            patient_id=uploaded_file.name.split(".")[0],
            medical_intent=medical_intent,
            diet_json=diet_json
        )
        with open(pdf_path, "rb") as f:
            st.download_button(
                "Download PDF",
                data=f.read(),
                file_name="diet_guidelines.pdf",
                mime="application/pdf"
            )
>>>>>>> 213f33e (Initial commit: full project code)
