import ollama

class LocalLlama:
    def __init__(self, model="llama3.1:8b"):
        self.model = model

    def generate_diet(self, structured_medical_data: dict) -> dict:
        prompt = f"""
You are a clinical nutritionist AI.

Given patient medical data below, generate a SAFE, PRACTICAL diet plan.
Rules:
- No medical diagnosis
- No dangerous advice
- Output STRICT JSON

Patient Data:
{structured_medical_data}

JSON format:
{{
  "diet_plan": {{
    "morning": [],
    "afternoon": [],
    "evening": [],
    "avoid": []
  }},
  "notes": ""
}}
"""
        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        return response["message"]["content"]
