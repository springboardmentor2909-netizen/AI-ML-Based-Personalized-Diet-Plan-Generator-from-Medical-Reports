import os
import pdfplumber
import pytesseract
from PIL import Image
import io
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


PDF_FOLDER = r"C:\Users\Suman\Project\datasets\pdf_reports"
OUTPUT = r"C:\Users\Suman\Project\datasets\pdf_reports_structured_data.csv"

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(pdf_path):
    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text and text.strip():
                all_text += text + "\n"
            else:
                # page image fallback: convert to image and OCR
                pil_img_obj = page.to_image(resolution=300).original
                # page.to_image().original returns a PIL.Image or bytes depending on pdfplumber version
                if isinstance(pil_img_obj, bytes):
                    pil_img = Image.open(io.BytesIO(pil_img_obj))
                else:
                    pil_img = pil_img_obj
                ocr_text = pytesseract.image_to_string(pil_img)
                all_text += ocr_text + "\n"
    return all_text

records = []
files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith(".pdf")]
print("PDF files found:", len(files))

for i, file_name in enumerate(files, start=1):
    pdf_path = os.path.join(PDF_FOLDER, file_name)
    print("Processing:", file_name)
    try:
        text = extract_text_from_pdf(pdf_path)
    except Exception as e:
        print("Error reading PDF:", e)
        text = ""

    text = text.replace("\r", "\n")

    # Height & Weight
    height = extract_height(text)
    weight = extract_weight(text)

    # BMI (extracted OR auto-calculated)
    bmi_value = extract_bmi(text)
    if bmi_value is None:
        bmi_value = calculate_bmi(height, weight)

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
print("PDF extraction finished. Saved at:", OUTPUT)
