import os
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

TEXT_FOLDER = r"C:\Users\Suman\Project\datasets\text_reports"
OUTPUT = r"C:\Users\Suman\Project\datasets\text_reports_structured_data.csv"

records = []
files = [f for f in os.listdir(TEXT_FOLDER) if f.lower().endswith(".txt")]
print("Text files found:", len(files))

for i, file_name in enumerate(files, start=1):
    path = os.path.join(TEXT_FOLDER, file_name)
    with open(path, "r", encoding="latin1", errors="ignore") as f:
        raw = f.read()
    text = raw.replace("\r", "\n")  # normalize

    # Height & Weight
    height = extract_height(text)
    weight = extract_weight(text)

    # BMI (extracted OR auto-calculated)
    bmi_value = extract_bmi(text)
    if bmi_value is None:
        bmi_value = calculate_bmi(height, weight)

    # Build record using accurate extractors
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

df = pd.DataFrame(records)
df.to_csv(OUTPUT, index=False, encoding="utf-8")
print("TEXT extraction finished. Saved at:", OUTPUT)
