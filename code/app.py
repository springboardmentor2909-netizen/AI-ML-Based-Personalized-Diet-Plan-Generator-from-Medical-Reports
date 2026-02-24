import streamlit as st
import json
import tempfile
import os

from ollama_diet_generation import generate_diet_advice
from single_input_inference import predict_health_status
from rule_based_medical_intent_extraction import extract_medical_intents


# PAGE CONFIG

st.set_page_config(
    page_title="AI Health & Diet Assistant",
    layout="wide"
)

# HEADER

st.title("🩺 AI Health Condition & Diet Recommendation System")
st.markdown(
    """
    Upload a **medical report (PDF / Image / Text)**.  
    The system will:
    - Predict health condition (**Normal / Abnormal**)
    - Detect major health risks
    - Understand medical context
    - Generate a **personalized diet plan**
    """
)

# SIDEBAR OPTIONS

st.sidebar.header("🍽 Diet Preferences")

num_days = st.sidebar.selectbox(
    "Number of days",
    options=[1, 2, 3],
    index=1
)

diet_pref = st.sidebar.radio(
    "Diet Preference",
    options=["Vegetarian", "Non-Vegetarian"]
)

# FILE UPLOAD

uploaded_file = st.file_uploader(
    "Upload Medical Report",
    type=["pdf", "png", "jpg", "jpeg", "txt"]
)

run_button = st.button("🔍 Analyze Report")


# MAIN PIPELINE

if uploaded_file and run_button:

    with st.spinner("Analyzing medical report..."):


        # SAVE FILE TEMPORARILY
        suffix = uploaded_file.name.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
            tmp.write(uploaded_file.read())
            temp_path = tmp.name

        # SINGLE INPUT ML INFERENCE
        inference_result = predict_health_status(temp_path)

        health_status = inference_result["final_health_label"]
        risk_flags = inference_result["risk_factors"]

        # Convert risk flags to list
        risk_factors = [k for k, v in risk_flags.items() if v == 1]
        doctor_comments = inference_result["doctor_comments"]

        # MEDICAL INTENT LOGIC
        medical_intents = []

        if "Diabetes" in risk_factors:
            medical_intents.append("LOW_SUGAR_DIET")
        if "Hypertension" in risk_factors:
            medical_intents.append("LOW_SODIUM_DIET")
        if "Obesity" in risk_factors:
            medical_intents.append("WEIGHT_MANAGEMENT")

        if not medical_intents:
            medical_intents = ["GENERAL_HEALTHY_DIET"]

        bert_intents = []

        if doctor_comments and isinstance(doctor_comments, str):
            bert_intents = extract_medical_intents([], doctor_comments)

        medical_intents.extend(bert_intents)
        all_intents = medical_intents

        medical_intents = [
            intent
            for item in medical_intents
            for intent in (item if isinstance(item, list) else [item])
        ]


        # DIET GENERATION (OLLAMA)
        diet_text = generate_diet_advice(
            medical_intents=medical_intents,
            health_status=health_status,
            days=num_days,
            diet_preference=diet_pref
        )

        # DISPLAY RESULTS
        st.success("✅ Analysis Complete")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🩺 Health Status")
            if health_status == "Normal":
                st.success("NORMAL")
            else:
                st.error("ABNORMAL")

        with col2:
            st.subheader("⚠️ Detected Risk Factors")
            if risk_factors:
                for r in risk_factors:
                    st.warning(r)
            else:
                st.success("No significant risk detected")

        st.subheader("🧠 Medical Insight")
        st.write(", ".join(medical_intents))

        st.subheader("🥗 Personalized Diet Recommendation")
        st.markdown(diet_text)

        # JSON OUTPUT
        final_json = {
            "health_status": health_status,
            "risk_factors": risk_factors,
            "medical_intents": medical_intents,
            "diet_preferences": {
                "days": num_days,
                "type": diet_pref
            },
            "diet_plan": diet_text
        }

        st.subheader("📄 Download Result")
        st.download_button(
            label="Download JSON",
            data=json.dumps(final_json, indent=4),
            file_name="health_analysis_result.json",
            mime="application/json"
        )

        # CLEAN TEMP FILE
        os.remove(temp_path)

# FOOTER

st.markdown("---")
st.caption(
    "⚕️ This AI system provides dietary guidance only and does not replace professional medical advice."
)
