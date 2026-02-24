import requests
import json
import time

# OLLAMA CONFIGURATION

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"   # You can switch to mistral / phi3 / medllama

REQUEST_TIMEOUT = 300  # seconds


# PROMPT BUILDER

def build_prompt(
    medical_intents,
    health_status,
    age=None,
    gender=None,
    days=3,
    diet_preference="Non-Vegetarian"
):
    intents_text = ", ".join(medical_intents)

    prompt = f"""
You are a clinical diet planning assistant.

Patient profile:
- Health status: {health_status}
- Age: {age if age else "Not specified"}
- Gender: {gender if gender else "Not specified"}
- Dietary preference: {diet_preference}
- Medical dietary concerns: {intents_text}

Task:
Create a {days}-day structured diet plan.

Rules:
- Follow the dietary preference strictly
- Meals per day: Breakfast, Lunch, Snack, Dinner
- Mention approximate nutrients for each meal
  (Calories, Protein, Carbohydrates, Fat)
- Use simple, commonly available foods
- Avoid sugar, excess salt, and unhealthy fats
- Do NOT prescribe medicines or supplements
- Do NOT diagnose diseases
- Keep language clear and professional

Output format EXACTLY like this:

Day 1:
Breakfast: <food> (Calories: X kcal, Protein: X g, Carbs: X g, Fat: X g)
Lunch: ...
Snack: ...
Dinner: ...

Repeat for all days.

Now generate the diet plan.
"""

    return prompt.strip()


# OLLAMA CALL FUNCTION

def call_ollama(prompt):
    """
    Calls the Ollama local API and returns generated text.
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,      # lower = safer, more deterministic
            "top_p": 0.9,
            "num_predict": 180       # limit verbosity
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()

        result = response.json()
        return result.get("response", "").strip()

    except requests.exceptions.RequestException as e:
        print("❌ Ollama API error:", e)
        return "Diet advice unavailable due to system error."


# MAIN PUBLIC FUNCTION

def generate_diet_advice(
    medical_intents,
    health_status,
    age=None,
    gender=None,
    days=3,
    diet_preference="Non-Vegetarian"
):
    if not medical_intents:
        medical_intents = ["GENERAL_HEALTHY_DIET"]

    prompt = build_prompt(
        medical_intents=medical_intents,
        health_status=health_status,
        age=age,
        gender=gender,
        days=days,
        diet_preference=diet_preference
    )

    return call_ollama(prompt)


# TEST BLOCK (OPTIONAL)

if __name__ == "__main__":
    # Quick sanity test
    test_intents = [
        "LOW_SUGAR_DIET",
        "LOW_FAT_DIET",
        "LIFESTYLE_MODIFICATION"
    ]

    advice = generate_diet_advice(
        medical_intents=test_intents,
        health_status="Abnormal",
        age=45,
        gender="Male"
    )

    print("\nGenerated Diet Recommendation:\n")
    print(advice)