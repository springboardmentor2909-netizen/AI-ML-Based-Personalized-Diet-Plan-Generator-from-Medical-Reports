import pandas as pd
import joblib
from sklearn.metrics import accuracy_score

df = pd.read_csv("training/data/medical_numeric_processed.csv")

X = df.drop("Diabetes_012", axis=1)
y = df["Diabetes_012"]

model = joblib.load("training/models/ml_model.pkl")
pred = model.predict(X)

print("Accuracy:", accuracy_score(y, pred))
