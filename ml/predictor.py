import joblib
import pandas as pd

class Predictor:
    def __init__(self, model_path, feature_path):
        self.model = joblib.load(model_path)
        self.feature_order = joblib.load(feature_path)

    def predict(self, extracted_features: dict):
        # --------------------------
        # Prepare input for model
        # --------------------------
        input_data = [
            extracted_features.get(feature, 0.0)
            for feature in self.feature_order
        ]

        input_df = pd.DataFrame([input_data], columns=self.feature_order)

        # --------------------------
        # ML prediction (class)
        # --------------------------
        model_pred = int(self.model.predict(input_df)[0])

        # --------------------------
        # CLINICAL OVERRIDE RULES (DOCTOR FIRST)
        # --------------------------
        if (
            extracted_features.get("blood_sugar", 0) >= 126 or
            extracted_features.get("cholesterol", 0) >= 200 or
            extracted_features.get("blood_pressure", 0) >= 140 or
            extracted_features.get("bmi", 0) >= 30 or
            extracted_features.get("hemoglobin", 99) < 11
        ):
            status = "Abnormal"
        else:
            status = "Abnormal" if model_pred == 1 else "Normal"

        # --------------------------
        # Diet Plan (ALWAYS GENERATED)
        # --------------------------
        diet_plan = []

        if extracted_features.get("blood_sugar", 0) >= 126:
            diet_plan.append(
                "Limit refined carbohydrates and sugars. Prefer whole grains, legumes, and vegetables."
            )

        if extracted_features.get("cholesterol", 0) >= 200:
            diet_plan.append(
                "Reduce saturated fats. Include oats, nuts, seeds, and omega-3 rich foods."
            )

        if extracted_features.get("blood_pressure", 0) >= 140:
            diet_plan.append(
                "Adopt a low-sodium DASH-style diet. Increase potassium-rich foods."
            )

        if extracted_features.get("bmi", 0) >= 30:
            diet_plan.append(
                "Focus on calorie control, high-fiber foods, and regular physical activity."
            )

        if extracted_features.get("hemoglobin", 99) < 11:
            diet_plan.append(
                "Increase iron-rich foods like leafy greens, legumes, dates, and lean proteins."
            )

        if not diet_plan:
            diet_plan.append(
                "Maintain a balanced diet with fruits, vegetables, whole grains, and adequate hydration."
            )

        return status, diet_plan
