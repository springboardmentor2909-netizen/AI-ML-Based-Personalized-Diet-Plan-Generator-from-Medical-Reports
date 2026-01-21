from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import json

def generate_pdf(patient_id, medical_intent, diet_json):
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, f"{patient_id}_diet_report.pdf")

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "AI Medical Diet Report")
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Patient ID: {patient_id}")
    y -= 20
    c.drawString(50, y, f"Medical Intent: {medical_intent}")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Diet Recommendations:")
    y -= 20

    c.setFont("Helvetica", 11)
    for rec in diet_json.get("recommendation", []):
        c.drawString(60, y, f"- {rec}")
        y -= 15

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Foods to Avoid:")
    y -= 20

    c.setFont("Helvetica", 11)
    for item in diet_json.get("avoid", []):
        c.drawString(60, y, f"- {item}")
        y -= 15

    c.save()

    return file_path
