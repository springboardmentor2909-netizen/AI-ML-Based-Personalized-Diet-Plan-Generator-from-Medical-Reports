import random

def generate_weekly_diet(intent, preference):
    risk = intent["risk_level"]
    conditions = intent["conditions"]
    features = intent["ml_features_used"]

    # ---------- CONDITION IDENTIFICATION ----------
    if "hypertension" in conditions:
        case = "hypertension"
    elif "Glucose" in features:
        case = "diabetes"
    elif "BMI" in features:
        case = "obesity"
    else:
        case = "normal"

    # ---------- BASE DIET RULES ----------
    rules = {
        "hypertension": {
            "avoid": ["salt", "pickles", "processed foods"],
            "limits": {"salt_per_day": "≤ 5g"},
            "notes": ["low sodium diet", "monitor blood pressure"]
        },
        "diabetes": {
            "avoid": ["sweets", "refined carbs", "sugary drinks"],
            "limits": {"sugar": "minimal"},
            "notes": ["low glycemic diet", "monitor glucose levels"]
        },
        "obesity": {
            "avoid": ["fried foods", "junk food", "high calorie snacks"],
            "limits": {"calories": "controlled"},
            "notes": ["weight loss focused diet"]
        },
        "normal": {
            "avoid": ["excess sugar", "junk food"],
            "limits": {},
            "notes": ["balanced healthy diet"]
        }
    }

    # ---------- MEAL TEMPLATES ----------
    veg_meals = {
        "Breakfast": ["Oats", "Idli", "Vegetable upma"],
        "Lunch": ["Brown rice & dal", "Vegetable curry"],
        "Snack": ["Fruits", "Nuts"],
        "Dinner": ["Chapati & sabzi"]
    }

    nonveg_meals = {
        "Breakfast": ["Boiled eggs", "Vegetable omelette"],
        "Lunch": ["Grilled chicken", "Fish curry"],
        "Snack": ["Roasted peanuts"],
        "Dinner": ["Chicken soup", "Egg curry"]
    }

    meal_source = veg_meals if preference == "veg" else nonveg_meals

    # ---------- WEEKLY PLAN ----------
    weekly_plan = {}
    days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]

    for i, day in enumerate(days):
        weekly_plan[day] = {
            meal: meal_source[meal][i % len(meal_source[meal])]
            for meal in meal_source
        }

    return {
        "risk_level": risk,
        "condition": case,
        "preference": preference,
        "weekly_diet_plan": weekly_plan,
        "foods_to_avoid": rules[case]["avoid"],
        "limits": rules[case]["limits"],
        "notes": rules[case]["notes"]
    }

