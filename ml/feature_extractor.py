import re
import pandas as pd
import numpy as np

FEATURE_COLUMNS = [
    "age",
    "bmi",
    "blood_sugar",
    "cholesterol",
    "hemoglobin",
    "blood_pressure",
    "heart_rate",
    "weight"
]

FEATURE_ALIASES = {
    "age": ["age", "years", "yrs", "patient age", "dob"],
    "bmi": ["bmi", "body mass index", "b.m.i", "body index"],
    "blood_sugar": [
        "blood sugar", "fbs", "glucose", "sugar", "random blood sugar",
        "rbs", "fasting blood sugar", "fasting glucose", "fbg", "bs", "blood glucose"
    ],
    "cholesterol": [
        "cholesterol", "t.c.", "total cholesterol", "tc", "serum cholesterol",
        "hdl", "ldl", "vldl", "lipid profile", "chol"
    ],
    "hemoglobin": [
        "hemoglobin", "hb", "hgb", "hb level", "hemoglobin concentration", "hb conc"
    ],
    "blood_pressure": [
        "blood pressure", "bp", "systolic", "diastolic", "systolic bp", "diastolic bp",
        "b.p.", "arterial pressure", "bp systolic", "bp diastolic"
    ],
    "heart_rate": [
        "heart rate", "pulse", "pr", "pulse rate", "heart beat", "beats per minute", "bpm"
    ],
    "weight": [
        "weight", "wt", "body weight", "patient weight", "mass", "body mass", "wgt"
    ]
}


class FeatureExtractor:
    def __init__(self):
        pass

    def extract_numbers(self, text: str) -> dict:
        features = {}

        for feature, aliases in FEATURE_ALIASES.items():

            # ---------- FIX FOR BLOOD PRESSURE ----------
            if feature == "blood_pressure":
                # Extract ONLY systolic BP (e.g. 148 from 148/96)
                match = re.search(
                    r'(blood pressure|bp|systolic)\s*[:=]?\s*(\d{2,3})',
                    text,
                    re.IGNORECASE
                )
                if match:
                    features[feature] = float(match.group(2))
                    print(f"✅ Extracted blood_pressure (systolic): {features[feature]}")
                else:
                    features[feature] = None
                    print("❌ Missing blood_pressure")
                continue

            # ---------- ALL OTHER FEATURES ----------
            pattern = r'(' + '|'.join(aliases) + r')\s*[:=]?\s*(\d+\.?\d*)'
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                features[feature] = float(match.group(2))
                print(f"✅ Extracted {feature}: {features[feature]}")
            else:
                features[feature] = None
                print(f"❌ Missing {feature}")

        return features

    def extract_features_from_texts(self, texts: list) -> pd.DataFrame:
        all_features = [self.extract_numbers(t) for t in texts]
        df = pd.DataFrame(all_features)

        # Ensure all expected columns are present
        for col in FEATURE_COLUMNS:
            if col not in df.columns:
                df[col] = np.nan

        df = df[FEATURE_COLUMNS]  # Reorder columns
        return df
