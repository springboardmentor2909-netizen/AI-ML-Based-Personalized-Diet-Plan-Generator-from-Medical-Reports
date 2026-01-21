def normalize_rules(medical_intent: dict) -> dict:
    """
    Generate specific, biomarker-aware diet rules based on conditions and biomarkers.
    """
    conditions = medical_intent.get("conditions", [])
    biomarkers = medical_intent.get("biomarkers", {})
    rules = set()

    # DIABETES - Specific rules based on glucose levels
    if any(c.lower() in ["diabetes", "diabetes mellitus"] for c in conditions):
        rules.update([
            "low glycemic index diet",
            "limit refined carbohydrates",
            "increase fiber intake (30+ grams daily)",
            "consistent meal timing",
            "monitor portion sizes",
            "include lean proteins at each meal"
        ])
        if "hba1c" in biomarkers and biomarkers["hba1c"].get("abnormal"):
            rules.add("strict carbohydrate control")

    # HYPERTENSION - DASH diet principles
    if any(c.lower() in ["hypertension", "high blood pressure"] for c in conditions):
        rules.update([
            "DASH diet approach",
            "limit sodium to <1500mg daily",
            "increase potassium-rich foods",
            "limit alcohol",
            "reduce caffeine",
            "maintain healthy weight"
        ])

    # CHOLESTEROL/DYSLIPIDEMIA - Lipid management
    if any(c.lower() in ["cholesterol", "dyslipidemia", "high cholesterol"] for c in conditions):
        rules.update([
            "increase omega-3 fatty acids",
            "limit saturated fats to <7% of calories",
            "eliminate trans fats",
            "increase soluble fiber",
            "include plant sterols",
            "choose lean proteins"
        ])

    # THYROID - Iodine and selenium management
    if any(c.lower() in ["thyroid", "hypothyroidism", "hyperthyroidism"] for c in conditions):
        rules.update([
            "adequate iodine intake",
            "include selenium-rich foods",
            "separate medications from meals",
            "consistent iodine levels"
        ])

    # HEART DISEASE - Cardiac protection
    if any(c.lower() in ["heart disease", "cardiac", "coronary"] for c in conditions):
        rules.update([
            "Mediterranean diet approach",
            "limit sodium",
            "increase heart-healthy fats",
            "avoid processed meats",
            "increase fiber",
            "maintain DASH principles"
        ])

    # General healthy guidelines (always include)
    rules.update([
        "adequate hydration (8-10 glasses daily)",
        "regular meal schedule",
        "moderate portion sizes"
    ])

    return {
        "conditions": conditions,
        "biomarkers": biomarkers,
        "diet_rules": sorted(list(rules))  # Sort for consistency
    }
