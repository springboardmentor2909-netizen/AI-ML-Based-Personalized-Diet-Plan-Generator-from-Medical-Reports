from app.services.llm_service import generate_natural_diet, extract_patient_info

def generate_diet_plan(gpt_output: dict) -> dict:
    """
    Generate a comprehensive, personalized diet plan using LLM based on medical conditions, 
    biomarkers, and patient information.
    """
    rules = gpt_output.get("diet_rules", [])
    conditions = gpt_output.get("medical_condition", [])
    patient_info = gpt_output.get("patient_info", {})
    biomarkers = gpt_output.get("biomarkers", {})
    medical_intent = gpt_output.get("medical_intent", {})

    # Generate natural language diet plan using LLM
    # Pass biomarkers for more specific recommendations
    diet_plan_text = generate_natural_diet(
        rules, 
        conditions, 
        patient_info,
        biomarkers or medical_intent.get("biomarkers", {})
    )

    # Structure the response
    plan = {
        "patient": gpt_output.get("patient", "Patient"),
        "medical_condition": conditions,
        "diet_rules": rules,
        "biomarkers": biomarkers or medical_intent.get("biomarkers", {}),
        "risk_level": medical_intent.get("risk_level", "unknown"),
        "diet_plan": diet_plan_text,
        "generated_by": "AI Nutritionist",
        "notes": "This personalized diet plan is generated based on your medical report analysis and lab values. Please consult with your healthcare provider or a registered dietitian before making significant dietary changes."
    }

    return plan
