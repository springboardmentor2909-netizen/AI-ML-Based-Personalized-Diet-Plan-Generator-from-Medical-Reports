import os
import re
import numpy as np
import pandas as pd
import joblib
import pdfplumber
import pytesseract
from PIL import Image

# PATHS

MODEL_PATH = r"C:\Users\Suman\Project\models\best_diet_planning_model.pkl"
TRAIN_COLUMNS_PATH = r"C:\Users\Suman\Project\models\train_columns.csv"

# TEXT EXTRACTION

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif ext in [".png", ".jpg", ".jpeg"]:
        img = Image.open(file_path)
        return pytesseract.image_to_string(img)

    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    else:
        raise ValueError("Unsupported file format")

def extract_doctor_comments(text):
    """
    Extracts doctor's impressions / remarks / advice from the report text.
    """

    patterns = [
        r"(impression|conclusion|remarks|doctor.?s note|comments|advice)\s*[:\-]?\s*(.*)"
    ]

    for pat in patterns:
        match = re.search(pat, text, re.I | re.S)
        if match:
            return match.group(2).strip()[:1000]  # limit junk text

    return ""

# FEATURE EXTRACTION (BASIC)

def extract_numeric_features(text):
    features = {}

    def find(pattern):
        match = re.search(pattern, text)
        return float(match.group(1)) if match else np.nan

    features["age"] = find(r"age\s*[:\-]?\s*(\d+)")
    features["bmi"] = find(r"bmi\s*[:\-]?\s*(\d+\.?\d*)")
    features["glucose"] = find(r"glucose\s*[:\-]?\s*(\d+\.?\d*)")
    features["hemoglobin"] = find(
        r"(?:hb|hemoglobin)\s*[:\-]?\s*(\d+\.?\d*)"
    )


    bp_match = re.search(r"(\d{2,3})\s*/\s*(\d{2,3})", text)
    if bp_match:
        features["bp_systolic"] = int(bp_match.group(1))
        features["bp_diastolic"] = int(bp_match.group(2))
    else:
        features["bp_systolic"] = np.nan
        features["bp_diastolic"] = np.nan

    if re.search(r"\bmale\b", text, re.I):
        features["gender_encoded"] = 0
    elif re.search(r"\bfemale\b", text, re.I):
        features["gender_encoded"] = 1
    else:
        features["gender_encoded"] = 2

    return pd.DataFrame([features])


# PREPROCESSING (MINIMAL)

def preprocess_features(df):
    df.loc[(df["bp_systolic"] < 70) | (df["bp_systolic"] > 200), "bp_systolic"] = np.nan
    df.loc[(df["bp_diastolic"] < 40) | (df["bp_diastolic"] > 130), "bp_diastolic"] = np.nan

    df.loc[(df["bmi"] < 10) | (df["bmi"] > 60), "bmi"] = np.nan
    df.loc[(df["glucose"] < 50) | (df["glucose"] > 400), "glucose"] = np.nan
    df.loc[(df["hemoglobin"] < 5) | (df["hemoglobin"] > 25), "hemoglobin"] = np.nan

    df["diabetic_risk"] = (df["glucose"] >= 126).astype(int)
    df["hypertension_risk"] = (
        (df["bp_systolic"] >= 140) |
        (df["bp_diastolic"] >= 90)
    ).astype(int)
    df["obesity_risk"] = (df["bmi"] >= 30).astype(int)
    df["anemia_risk"] = (df["hemoglobin"] < 12).astype(int)

    df.fillna(0, inplace=True)
    return df


# PREDICTION

def predict_health_status(file_path):
    text = extract_text(file_path)
    doctor_comments = extract_doctor_comments(text)

    df = extract_numeric_features(text)
    df = preprocess_features(df)

    # ---- STORE RISK FACTORS BEFORE COLUMN FILTERING ----
    risk_factors = {
        "Diabetes": int(df.get("diabetic_risk", 0)),
        "Hypertension": int(df.get("hypertension_risk", 0)),
        "Obesity": int(df.get("obesity_risk", 0)),
        "Anemia": int(df.get("anemia_risk", 0)),
    }

    train_cols = pd.read_csv(TRAIN_COLUMNS_PATH)["feature"].tolist()

    for col in train_cols:
        if col not in df.columns:
            df[col] = 0

    df = df[train_cols]

    model = joblib.load(MODEL_PATH)
    prediction = model.predict(df)[0]

    return {
        "final_health_label": "Normal" if prediction == 0 else "Abnormal",
        "risk_factors": risk_factors,
        "doctor_comments": doctor_comments
    }


