import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ---------- JSON EXPORT ----------
def save_diet_json(diet_data, filename="weekly_diet_plan.json"):
    with open(filename, "w") as f:
        json.dump(diet_data, f, indent=4)
    return filename

# ---------- PDF EXPORT ----------
def save_diet_pdf(diet_data, filename="weekly_diet_plan.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(BASE_DIR, "assets", "image", "logo.png")

    def new_page():
        c.showPage()
        c.setFont("Helvetica", 12)
        return height - 40

    y = height - 40

    # -------- LOGO AT TOP --------
    if os.path.exists(logo_path):
        c.drawImage(
            logo_path,
            width / 2 - 40,   # center
            y - 60,
            width=80,
            height=80,
            mask='auto'
        )
        y -= 90

    # -------- TITLE --------
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, y, "Weekly Personalized Diet Plan")
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(40, y, f"Diet Preference: {diet_data['preference']}")
    y -= 20
    c.drawString(40, y, f"Risk Level: {diet_data['risk_level']}")
    y -= 30

    # -------- WEEKLY PLAN --------
    for day, meals in diet_data["weekly_diet_plan"].items():
        if y < 120:
            y = new_page()

        c.setFont("Helvetica-Bold", 13)
        c.drawString(40, y, day)
        y -= 20

        c.setFont("Helvetica", 12)
        for meal, food in meals.items():
            if y < 80:
                y = new_page()
            c.drawString(60, y, f"{meal}: {food}")
            y -= 15

        y -= 10

    # -------- FOODS TO AVOID --------
    if y < 120:
        y = new_page()

    c.setFont("Helvetica-Bold", 13)
    c.drawString(40, y, "Foods to Avoid:")
    y -= 20
    c.setFont("Helvetica", 12)

    for item in diet_data["foods_to_avoid"]:
        if y < 80:
            y = new_page()
        c.drawString(60, y, f"- {item}")
        y -= 15

    # -------- LIMITS --------
    if diet_data["limits"]:
        if y < 120:
            y = new_page()

        c.setFont("Helvetica-Bold", 13)
        c.drawString(40, y, "Limits:")
        y -= 20
        c.setFont("Helvetica", 12)

        for k, v in diet_data["limits"].items():
            if y < 80:
                y = new_page()
            c.drawString(60, y, f"{k}: {v}")
            y -= 15

    # -------- NOTES --------
    if y < 120:
        y = new_page()

    c.setFont("Helvetica-Bold", 13)
    c.drawString(40, y, "Notes:")
    y -= 20
    c.setFont("Helvetica", 12)

    for note in diet_data["notes"]:
        if y < 80:
            y = new_page()
        c.drawString(60, y, f"- {note}")
        y -= 15

    c.save()
    return filename
