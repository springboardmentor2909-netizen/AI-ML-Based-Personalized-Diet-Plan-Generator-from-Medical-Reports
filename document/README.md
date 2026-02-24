🩺 AI-Powered Health Risk Analysis & Personalized Diet Planning System

An end-to-end AI Health & Diet Recommendation System that processes medical reports (PDF, image, or text), predicts health abnormality using trained ML models, extracts medical intent using BERT, and generates personalized diet plans using a local LLaMA 3 model — without any paid APIs.

🚀 Project Overview

This project integrates:

Numerical Machine Learning for health abnormality detection

BERT-based NLP for understanding doctor notes

Rule-based medical reasoning for safety and interpretability

Local LLaMA 3 reasoning for diet plan generation

The system is designed as a decision-support system, not a diagnostic replacement.

🧠 Complete Pipeline
Medical Report (PDF / Image / Text)
            ↓
Text & Numeric Feature Extraction
            ↓
Trained ML Model (LightGBM)
            ↓
Normal / Abnormal Health Prediction
            ↓
Doctor Notes Cleaning & Segmentation
            ↓
BERT (NER + Intent Classification – Pretrained)
            ↓
Rule-Based Medical Intent Extraction
            ↓
LLaMA 3 (Local Reasoning Engine)
            ↓
Personalized Diet Plan (JSON)

🔍 Key Features

✅ Supports PDF / Image / Text medical reports
✅ Uses pretrained ML model (no retraining at inference)
✅ BERT for clinical language understanding
✅ Rule-based medical intent extraction (safe & explainable)
✅ Local LLaMA 3 (no OpenAI / paid APIs)
✅ Generates meal-wise diet plans
✅ Supports veg / non-veg preference
✅ Frontend-ready JSON output

🧪 Core Technologies Used
🔢 Numerical Health Risk Prediction (ML)

LightGBM (final selected model)

Random Forest & XGBoost (baseline evaluation)

Predicts combined abnormality from:

Diabetes

Hypertension

Obesity

Anemia

Final output:

Normal / Abnormal

🧠 BERT-Based Medical NLP

Pretrained BERT models are used without fine-tuning, as recommended for clinical text tasks.

BERT is used for:

Named Entity Recognition (NER)

Sentence-level medical intent classification

Understanding doctor prescriptions and notes

⚠️ BERT is not used for diagnosis, only for language understanding.

📐 Rule-Based Medical Intent Extraction

Intent categories include:

LOW_SODIUM_DIET

DIABETIC_FRIENDLY_DIET

IRON_RICH_DIET

LIFESTYLE_MODIFICATION

GENERAL_HEALTHY_DIET

Rules ensure:

Medical safety

Deterministic behavior

Explainability for mentors and evaluation

🍽️ Diet Plan Generation (LLaMA 3)

Model: LLaMA 3 (local, via Ollama)

Usage:

Takes numerical predictions + medical intents

Generates structured diet recommendations

Provides meal-wise plans (Breakfast / Lunch / Dinner)

Includes nutrient considerations

LLaMA 3 is used only for reasoning, after medical constraints are applied.


📊 Model Performance Summary

Accuracy: >97%

ROC-AUC: ≈ 0.99

Reduced overfitting (train vs test aligned)

Medically interpretable outputs

🛡️ Design Justification
Component	Reason
Machine Learning	Objective health risk prediction
BERT	Clinical language understanding
Rule-Based Logic	Medical safety & explainability
LLaMA 3	Flexible diet reasoning
Local Models	Privacy + zero API cost
⚠️ Disclaimer

This system is intended for educational and decision-support purposes only.
It does not replace medical professionals.

👨‍💻 Author

Abhijit Manna