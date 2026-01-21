import ollama
import json

class LocalLlama:
    def __init__(self, model="llama3.1:8b"):
        self.model = model

    def generate_diet(self, patient_data: dict) -> str:
        prompt = f"""
You are a senior clinical dietitian.

RULES:
- If patient_status is "Abnormal", recommendations MUST NOT be empty
- Give condition-specific diet
- Output MUST be valid JSON
- Do NOT explain anything

OUTPUT FORMAT (MANDATORY):
{{
  "recommendation": [string, string, string],
  "avoid": [string, string]
}}

Patient data:
{json.dumps(patient_data, indent=2)}
"""

        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.2}
        )

        return response["message"]["content"]
