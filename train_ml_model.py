import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import joblib

# Load data
df = pd.read_csv("training/data/medical_numeric.csv")

# 👇 Correct target column
TARGET_COL = "Diabetes_012"   # change ONLY if your CSV differs

X = df.drop(TARGET_COL, axis=1)
y = df[TARGET_COL]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# Train model with better params
model = RandomForestClassifier(
    n_estimators=500,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1,
    class_weight='balanced'
)
model.fit(X_train, y_train)

# Cross-validation
cv_scores = cross_val_score(model, X_train, y_train, cv=5)
print(f"Cross-validation scores: {cv_scores}")
print(f"Mean CV accuracy: {cv_scores.mean():.4f}")

# Evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"✅ Test Accuracy: {acc * 100:.2f}%")
print(classification_report(y_test, y_pred))

# Save model and scaler
joblib.dump(model, "training/models/ml_model.pkl")
joblib.dump(scaler, "training/models/scaler.pkl")
print("✅ Model and scaler saved to training/models/")
