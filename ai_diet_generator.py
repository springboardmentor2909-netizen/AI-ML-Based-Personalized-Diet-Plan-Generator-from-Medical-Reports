from google import genai
import streamlit as st

# Configure client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def generate_diet(patient_id):

    prompt = f"""
You are a professional Indian dietician.

Create a simple, clear, diabetic-friendly Indian diet plan
for Patient ID {patient_id}.

Strictly follow this format:

Breakfast:
- item 1
- item 2

Lunch:
- item 1
- item 2

Snacks:
- item 1
- item 2

Dinner:
- item 1
- item 2
"""

    response = client.models.generate_content(
        model="models/gemini-flash-lite-latest",
        contents=prompt
    )

    return response.text
