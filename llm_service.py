from typing import Dict, List
import re

# Rule-based diet generation system (no external LLM required)

MEAL_DATABASE = {
    "breakfast_options": {
        "diabetes_safe": [
            "Oatmeal with berries and almonds (low glycemic)",
            "Greek yogurt with flaxseeds",
            "Vegetable omelet with whole wheat toast",
            "Chia seed pudding with unsweetened almond milk"
        ],
        "hypertension_safe": [
            "Oatmeal with bananas (potassium rich)",
            "Egg whites with whole grain bread",
            "Smoothie with leafy greens and berries",
            "Whole grain toast with avocado"
        ],
        "cholesterol_safe": [
            "Oat bran with walnuts and blueberries",
            "Smoothie with plant-based milk and chia seeds",
            "Whole wheat toast with almond butter",
            "Greek yogurt with ground flaxseed"
        ],
        "thyroid_safe": [
            "Scrambled eggs with iodized salt",
            "Oatmeal with Brazil nuts (selenium)",
            "Whole grain bread with tuna",
            "Cottage cheese with berries"
        ],
        "heart_disease_safe": [
            "Mediterranean oatmeal with olive oil drizzle",
            "Whole grain toast with sardines",
            "Vegetable smoothie with unsweetened milk",
            "Eggs with whole wheat and herbs"
        ],
        "general": [
            "Scrambled eggs with whole grain toast",
            "Fruit smoothie with yogurt",
            "Oatmeal with fresh fruits",
            "Whole grain cereal with milk"
        ]
    },
    "lunch_options": {
        "diabetes_safe": [
            "Grilled chicken with brown rice and steamed broccoli",
            "Lentil soup with vegetable salad",
            "Baked salmon with sweet potato and green beans",
            "Quinoa bowl with roasted vegetables and lean protein"
        ],
        "hypertension_safe": [
            "Turkey and vegetable wrap with low-sodium sauce",
            "Potassium-rich salad with chickpeas",
            "Grilled fish with herbs and steamed vegetables",
            "Vegetable stir-fry with brown rice"
        ],
        "cholesterol_safe": [
            "Grilled chicken with olive oil and whole wheat pasta",
            "Baked white fish with omega-3 rich sides",
            "Plant-based protein bowl with nuts",
            "Mediterranean salad with olive oil dressing"
        ],
        "thyroid_safe": [
            "Grilled chicken with iodine-rich seaweed salad",
            "Baked fish with Brazil nuts and vegetables",
            "Lean beef with selenium-rich mushrooms",
            "Chicken soup with whole grain crackers"
        ],
        "heart_disease_safe": [
            "Mediterranean grilled fish with olive oil",
            "Lean meat with heart-healthy vegetable sides",
            "Plant-based protein with herbs and spices",
            "Vegetable soup with whole grain bread"
        ],
        "general": [
            "Grilled chicken with rice and vegetables",
            "Fish with sweet potato and greens",
            "Vegetable stir-fry with lean protein",
            "Salad with grilled chicken or tofu"
        ]
    },
    "dinner_options": {
        "diabetes_safe": [
            "Baked salmon with roasted cauliflower and asparagus",
            "Lean turkey meatballs with zucchini noodles",
            "Grilled tilapia with steamed broccoli and quinoa",
            "Chicken breast with spinach and brown rice"
        ],
        "hypertension_safe": [
            "Baked white fish with potassium-rich potatoes",
            "Low-sodium vegetable curry with grilled chicken",
            "Herb-roasted turkey breast with vegetables",
            "Pasta with olive oil and herbs (no added salt)"
        ],
        "cholesterol_safe": [
            "Omega-3 rich salmon with olive oil vegetables",
            "Plant-based protein with whole grain sides",
            "Skinless chicken with fiber-rich vegetables",
            "Mediterranean vegetable stew with lean meat"
        ],
        "thyroid_safe": [
            "Grilled shrimp with seaweed and vegetables",
            "Baked chicken with Brazil nut crust",
            "Fish with selenium-rich mushrooms",
            "Lean beef with thyroid-supporting vegetables"
        ],
        "heart_disease_safe": [
            "Mediterranean baked fish with vegetables",
            "Lean poultry with heart-healthy sides",
            "Plant-based dinner with nuts and seeds",
            "Vegetable-based soup with lean protein"
        ],
        "general": [
            "Grilled chicken with vegetables and rice",
            "Baked fish with steamed vegetables",
            "Lean meat with salad and whole grain sides",
            "Vegetable stir-fry with protein"
        ]
    },
    "snack_options": {
        "diabetes_safe": [
            "Apple with peanut butter",
            "Mixed nuts (unsalted)",
            "Greek yogurt with berries",
            "Carrots with hummus"
        ],
        "hypertension_safe": [
            "Banana with almonds",
            "Potassium-rich dried fruit",
            "Low-sodium cheese with fruit",
            "Unsalted nuts with berries"
        ],
        "cholesterol_safe": [
            "Handful of walnuts",
            "Apple with almond butter",
            "Berries with Greek yogurt",
            "Raw almonds and fruit"
        ],
        "thyroid_safe": [
            "Brazil nuts (2-3 daily)",
            "Seaweed snacks",
            "Cheese with whole grain crackers",
            "Eggs and whole grain bread"
        ],
        "heart_disease_safe": [
            "Olive oil crackers with tomato",
            "Mixed Mediterranean nuts",
            "Avocado with whole grain bread",
            "Omega-3 rich seeds and berries"
        ],
        "general": [
            "Fresh fruit",
            "Yogurt with berries",
            "Nuts and seeds",
            "Vegetable sticks with dip"
        ]
    }
}

FOODS_TO_AVOID = {
    "diabetes": [
        "Refined sugars and sweets",
        "White bread and pasta",
        "Processed snacks",
        "Sugary drinks and fruit juices",
        "High-fat processed meats"
    ],
    "hypertension": [
        "High-sodium processed foods",
        "Cured and processed meats",
        "High-sodium condiments",
        "Alcohol (excessive)",
        "Caffeinated beverages (excessive)"
    ],
    "cholesterol": [
        "Saturated fats and trans fats",
        "Full-fat dairy products",
        "Processed meats",
        "Fried foods",
        "Egg yolks (in excess)"
    ],
    "thyroid": [
        "Goitrogen vegetables (raw, in excess)",
        "High iodine foods (if hyperthyroid)",
        "Soy products (in excess)",
        "Calcium supplements with medications"
    ],
    "heart_disease": [
        "Trans fats and saturated fats",
        "Processed and cured meats",
        "High-sodium foods",
        "Refined carbohydrates",
        "Sugary drinks"
    ]
}

def generate_natural_diet(diet_rules: List[str], medical_conditions: List[str], patient_info: Dict = None, biomarkers: Dict = None) -> str:
    """
    Generate a personalized 7-day meal plan using rule-based logic (no external LLM).
    """
    if not diet_rules and not medical_conditions:
        medical_conditions = ["general"]

    # Determine primary condition for meal selection
    primary_condition = None
    if medical_conditions:
        condition_lower = medical_conditions[0].lower()
        if "diabetes" in condition_lower:
            primary_condition = "diabetes_safe"
        elif "hypertension" in condition_lower or "blood pressure" in condition_lower:
            primary_condition = "hypertension_safe"
        elif "cholesterol" in condition_lower:
            primary_condition = "cholesterol_safe"
        elif "thyroid" in condition_lower:
            primary_condition = "thyroid_safe"
        elif "heart" in condition_lower or "cardiac" in condition_lower:
            primary_condition = "heart_disease_safe"
    
    if not primary_condition:
        primary_condition = "general"

    # Build 7-day meal plan
    plan_text = f"🥗 **7-DAY PERSONALIZED DIET PLAN**\n"
    plan_text += f"Medical Conditions: {', '.join(medical_conditions)}\n"
    plan_text += f"Based on: {', '.join(diet_rules[:3])}...\n\n"

    for day in range(1, 8):
        plan_text += f"**DAY {day}:**\n"
        
        # Get meals from database
        breakfast = MEAL_DATABASE["breakfast_options"].get(primary_condition, MEAL_DATABASE["breakfast_options"]["general"])[day % 4]
        lunch = MEAL_DATABASE["lunch_options"].get(primary_condition, MEAL_DATABASE["lunch_options"]["general"])[day % 4]
        dinner = MEAL_DATABASE["dinner_options"].get(primary_condition, MEAL_DATABASE["dinner_options"]["general"])[day % 4]
        snack1 = MEAL_DATABASE["snack_options"].get(primary_condition, MEAL_DATABASE["snack_options"]["general"])[day % 4]
        snack2 = MEAL_DATABASE["snack_options"].get(primary_condition, MEAL_DATABASE["snack_options"]["general"])[(day + 1) % 4]
        
        plan_text += f"  🌅 Breakfast: {breakfast}\n"
        plan_text += f"  🍽️ Lunch: {lunch}\n"
        plan_text += f"  🥗 Dinner: {dinner}\n"
        plan_text += f"  🍎 Snack 1: {snack1}\n"
        plan_text += f"  🥜 Snack 2: {snack2}\n\n"

    # Add foods to avoid
    avoid_list = []
    for condition in medical_conditions:
        condition_key = None
        if "diabetes" in condition.lower():
            condition_key = "diabetes"
        elif "hypertension" in condition.lower() or "blood pressure" in condition.lower():
            condition_key = "hypertension"
        elif "cholesterol" in condition.lower():
            condition_key = "cholesterol"
        elif "thyroid" in condition.lower():
            condition_key = "thyroid"
        elif "heart" in condition.lower() or "cardiac" in condition.lower():
            condition_key = "heart_disease"
        
        if condition_key and condition_key in FOODS_TO_AVOID:
            avoid_list.extend(FOODS_TO_AVOID[condition_key])

    if avoid_list:
        plan_text += f"**⚠️ FOODS TO AVOID:**\n"
        for food in list(set(avoid_list))[:8]:  # Remove duplicates, show top 8
            plan_text += f"  • {food}\n"
        plan_text += "\n"

    # Add biomarker-specific notes
    if biomarkers:
        plan_text += f"**📊 BIOMARKER CONSIDERATIONS:**\n"
        for marker, data in biomarkers.items():
            if data.get("abnormal"):
                value = data.get("value", "N/A")
                unit = data.get("unit", "")
                plan_text += f"  • {marker}: {value} {unit} - Requires dietary adjustment\n"
        plan_text += "\n"

    # Add general guidelines
    plan_text += "**✅ GENERAL GUIDELINES:**\n"
    plan_text += "  • Maintain consistent meal times\n"
    plan_text += "  • Stay hydrated (8-10 glasses of water daily)\n"
    plan_text += "  • Include plenty of vegetables and whole grains\n"
    plan_text += "  • Monitor portion sizes\n"
    plan_text += "  • Consult with a healthcare provider or registered dietitian\n"

    return plan_text

def extract_patient_info(text: str) -> Dict:
    """
    Extract patient information from medical report text.
    """
    info = {}
    text_lower = text.lower()

    # Extract age
    if "age" in text_lower:
        age_match = re.search(r'age[:\s]*(\d+)', text_lower)
        if age_match:
            info["age"] = int(age_match.group(1))

    # Extract gender
    if "female" in text_lower or "/f" in text_lower:
        info["gender"] = "female"
    elif "male" in text_lower or "/m" in text_lower:
        info["gender"] = "male"

    return info
