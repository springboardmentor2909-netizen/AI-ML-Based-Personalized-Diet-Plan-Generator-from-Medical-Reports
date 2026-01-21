import re
import numpy as np

def extract_numeric_features(text: str):
    features = {
        "glucose": None,
        "bp": None,
        "bmi": None
    }

    glucose = re.search(r'glucose[:\s]+(\d+)', text.lower())
    bp = re.search(r'(\d{2,3})\/(\d{2,3})', text)
    bmi = re.search(r'bmi[:\s]+(\d+\.?\d*)', text.lower())

    if glucose:
        features["glucose"] = int(glucose.group(1))
    if bp:
        features["bp"] = int(bp.group(1))
    if bmi:
        features["bmi"] = float(bmi.group(1))

    return np.array([features["glucose"], features["bp"], features["bmi"]])
