import re
from ml_model import predict_risk

# ---------------- TEXT CLEANING ----------------
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9/\s\.]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ---------------- EXTRACTION FUNCTIONS ----------------
def extract_bp(text):
    patterns = [
        r"bp\s*(?:today\s*)?(\d+)\s*/\s*(\d+)",
        r"blood pressure\s*(?:is\s*)?(\d+)\s*/\s*(\d+)"
    ]
    for p in patterns:
        match = re.search(p, text)
        if match:
            return int(match.group(1)), int(match.group(2))
    return None, None


def extract_bmi(text):
    match = re.search(r"bmi\s*(?:is\s*)?(\d+\.?\d*)", text)
    return float(match.group(1)) if match else None


def extract_glucose(text):
    match = re.search(r"glucose\s*(?:level\s*)?(?:is\s*)?(\d+)", text)
    return int(match.group(1)) if match else None


# ---------------- STRUCTURED MEDICAL INTENT ----------------
def build_structured_medical_intent(text, model, default_features):
    intent = {
        "conditions": [],
        "measurements": {},
        "diet_advice": [],
        "risk_level": "normal",
        "ml_features_used": []
    }

    user_inputs = {}

    # ---- Blood Pressure ----
    systolic, diastolic = extract_bp(text)
    if systolic and diastolic:
        intent["measurements"]["blood_pressure"] = f"{systolic}/{diastolic}"
        user_inputs["BloodPressure"] = systolic
        intent["ml_features_used"].append("BloodPressure")

        if systolic >= 140 or diastolic >= 90:
            intent["conditions"].append("hypertension")

    # ---- BMI ----
    bmi = extract_bmi(text)
    if bmi is not None:
        intent["measurements"]["bmi"] = bmi
        user_inputs["BMI"] = bmi
        intent["ml_features_used"].append("BMI")

    # ---- Glucose ----
    glucose = extract_glucose(text)
    if glucose is not None:
        intent["measurements"]["glucose"] = glucose
        user_inputs["Glucose"] = glucose
        intent["ml_features_used"].append("Glucose")

    # ---- Build ML Input ----
    features = default_features.copy()
    features.update(user_inputs)

    ml_input = [[
        features["Pregnancies"],
        features["Glucose"],
        features["BloodPressure"],
        features["SkinThickness"],
        features["Insulin"],
        features["BMI"],
        features["DiabetesPedigreeFunction"],
        features["Age"]
    ]]

    intent["risk_level"] = predict_risk(model, ml_input)

    # ---- Diet Advice from text ----
    if "low salt" in text:
        intent["diet_advice"].append("low salt diet")

    return intent
