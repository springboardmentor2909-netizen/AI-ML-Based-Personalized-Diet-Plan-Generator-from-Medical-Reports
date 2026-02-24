import os
import cv2
import pytesseract
import pandas as pd

from accuracy_extractors import (
    extract_glucose,
    extract_total_chol,
    extract_ldl,
    extract_hdl,
    extract_triglycerides,
    extract_hemoglobin,
    extract_creatinine,
    extract_bmi,
    extract_bp_strict,
    extract_doctor_comments,
    extract_age,
    extract_gender,
    extract_height,
    extract_weight,
    calculate_bmi,
    extract_pulse
)

IMAGE_FOLDER = r"C:\Users\Suman\Project\datasets\png_reports"
OUTPUT = r"C:\Users\Suman\Project\datasets\png_reports_structured_data.csv"

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Tesseract config (IMPORTANT)
TESSERACT_CONFIG = r"--oem 3 --psm 6"

records = []
files = [f for f in os.listdir(IMAGE_FOLDER)
         if f.lower().endswith((".png", ".jpg", ".jpeg"))]

print("Image files found:", len(files))

for i, file_name in enumerate(files, start=1):
    path = os.path.join(IMAGE_FOLDER, file_name)
    print(f"Processing {i}/{len(files)}:", file_name)

    img = cv2.imread(path)
    if img is None:
        print("could not read image:", file_name)
        continue

    # IMAGE PREPROCESSING (FIXED)
    img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)

    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        2
    )

    # OCR 
    raw_text = pytesseract.image_to_string(thresh, config=TESSERACT_CONFIG)
    text = raw_text.replace("\r", "\n")

    # OCR NORMALIZATION (CRITICAL) 
    text = (
        text.replace("H8ight", "Height")
            .replace("We1ght", "Weight")
            .replace("B1ood", "Blood")
            .replace("|", "/")
            .replace("—", "/")
            .replace("-", "/")
            .replace("mmHq", "mmHg")
    )

    # HEIGHT / WEIGHT
    height = extract_height(text)
    weight = extract_weight(text)

    # BMI (AUTO FALLBACK)
    bmi_value = extract_bmi(text)
    if bmi_value is None:
        bmi_value = calculate_bmi(height, weight)

    # RECORD
    record = {
        "report_id": i,
        "age": extract_age(text),
        "gender": extract_gender(text),
        "height_cm": height,
        "weight_kg": weight,
        "bmi": bmi_value,
        "pulse": extract_pulse(text),

        "glucose": extract_glucose(text),
        "cholesterol_total": extract_total_chol(text),
        "ldl": extract_ldl(text),
        "hdl": extract_hdl(text),
        "triglycerides": extract_triglycerides(text),
        "hemoglobin": extract_hemoglobin(text),
        "creatinine": extract_creatinine(text),
        "bp": extract_bp_strict(text),

        "doctor_comments": extract_doctor_comments(text)
    }

    records.append(record)

# SAVE CSV
df = pd.DataFrame(records)
df.to_csv(OUTPUT, index=False, encoding="utf-8")

print("IMAGE extraction finished. Saved at:", OUTPUT)
