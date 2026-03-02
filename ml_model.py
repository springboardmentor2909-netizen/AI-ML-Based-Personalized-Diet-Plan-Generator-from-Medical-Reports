import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "xgboost_diet_model.pkl")

def load_model():
    return joblib.load(MODEL_PATH)

def predict_risk(model, features):
    """
    features: list -> [[Pregnancies, Glucose, BP, SkinThickness,
                         Insulin, BMI, DPF, Age]]
    """
    prediction = model.predict(features)
    return "high" if prediction[0] == 1 else "normal"
