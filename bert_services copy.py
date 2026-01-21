from transformers import BertTokenizer, BertForSequenceClassification
import torch
import re

import os
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "bert_disease_classifier")

# Load the trained model and tokenizer
tokenizer = BertTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = BertForSequenceClassification.from_pretrained(MODEL_PATH, local_files_only=True)
model.eval()

# Label mapping (should match training)
label_map = {0: 'cholesterol', 1: 'thyroid', 2: 'diabetes', 3: 'hypertension', 4: 'healthy'}
id_to_label = {v: k for k, v in label_map.items()}

# Strong keyword indicators for each disease (for fallback/augmentation)
DISEASE_KEYWORDS = {
    'diabetes': {
        'keywords': ['glucose', 'blood sugar', 'hba1c', 'fasting', 'random glucose', 'diabetes'],
        'biomarkers': ['glucose', 'hba1c', 'fasting_glucose', 'random_glucose']
    },
    'hypertension': {
        'keywords': ['blood pressure', 'bp', 'hypertension', 'hypertensive', 'systolic', 'diastolic'],
        'biomarkers': ['blood_pressure']
    },
    'cholesterol': {
        'keywords': ['cholesterol', 'lipid', 'hdl', 'ldl', 'triglyceride', 'lipids', 'dyslipidemia'],
        'biomarkers': ['total_cholesterol', 'hdl', 'ldl', 'triglycerides']
    },
    'thyroid': {
        'keywords': ['thyroid', 'tsh', 't3', 't4', 'hypothyroid', 'hyperthyroid', 'tpo'],
        'biomarkers': ['tsh', 't3', 't4', 'tpo_antibodies']
    },
    'heart_disease': {
        'keywords': ['heart', 'cardiac', 'troponin', 'ck-mb', 'ck mb', 'myocardial', 'infarction', 'chest pain'],
        'biomarkers': ['ck_mb', 'troponin', 'ldh']
    }
}

def predict_disease(text: str, biomarkers: dict = None) -> list[str]:
    """
    Predict diseases using BERT model + keyword-based augmentation + biomarker detection.
    """
    diseases = []
    text_lower = text.lower()
    
    # Step 1: Check biomarker-based detection first (most reliable)
    if biomarkers:
        biomarker_diseases = detect_diseases_from_biomarkers(biomarkers)
        if biomarker_diseases:
            diseases.extend(biomarker_diseases)
    
    # Step 2: BERT model prediction
    try:
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
        with torch.no_grad():
            outputs = model(**inputs)
            predictions = torch.softmax(outputs.logits, dim=-1)
            predicted_label = label_map[torch.argmax(predictions, dim=-1).item()]
            
            # Get confidence score
            confidence = predictions.max().item()
            
            # Only trust BERT if confidence is > 0.6
            if confidence > 0.6 and predicted_label != "healthy":
                if predicted_label not in diseases:
                    diseases.append(predicted_label)
    except Exception as e:
        print(f"BERT prediction error: {e}")
    
    # Step 3: Keyword-based detection (fallback/augmentation)
    for disease, indicators in DISEASE_KEYWORDS.items():
        if disease not in diseases:
            keyword_count = sum(1 for keyword in indicators['keywords'] if keyword in text_lower)
            if keyword_count >= 1:  # At least one keyword match
                diseases.append(disease)
    
    # Step 4: Additional pattern-based detection
    additional_diseases = detect_patterns_in_text(text_lower)
    for disease in additional_diseases:
        if disease not in diseases:
            diseases.append(disease)
    
    # If no diseases detected, return empty list or 'healthy'
    if not diseases:
        return []
    
    return list(set(diseases))

def detect_diseases_from_biomarkers(biomarkers: dict) -> list[str]:
    """
    Detect diseases based on abnormal biomarker values.
    """
    diseases = []
    
    # Diabetes indicators
    if 'fasting_glucose' in biomarkers and biomarkers['fasting_glucose'].get('value', 0) >= 126:
        diseases.append('diabetes')
    elif 'hba1c' in biomarkers and biomarkers['hba1c'].get('value', 0) >= 6.5:
        diseases.append('diabetes')
    elif 'random_glucose' in biomarkers and biomarkers['random_glucose'].get('value', 0) >= 200:
        diseases.append('diabetes')
    
    # Hypertension indicators
    if 'blood_pressure' in biomarkers:
        bp_value = str(biomarkers['blood_pressure'].get('value', ''))
        try:
            systolic, diastolic = map(int, bp_value.split('/'))
            if systolic >= 140 or diastolic >= 90:
                diseases.append('hypertension')
        except:
            pass
    
    # Cholesterol/Lipid indicators
    if 'total_cholesterol' in biomarkers and biomarkers['total_cholesterol'].get('value', 0) >= 240:
        diseases.append('cholesterol')
    elif 'ldl' in biomarkers and biomarkers['ldl'].get('value', 0) >= 160:
        diseases.append('cholesterol')
    
    # Thyroid indicators
    if 'tsh' in biomarkers:
        tsh_value = biomarkers['tsh'].get('value', 0)
        if tsh_value < 0.4 or tsh_value > 4.0:
            diseases.append('thyroid')
    
    # Cardiac indicators
    if 'ck_mb' in biomarkers and biomarkers['ck_mb'].get('value', 0) > 24:
        diseases.append('heart_disease')
    elif 'troponin' in biomarkers:
        diseases.append('heart_disease')
    
    return list(set(diseases))

def detect_patterns_in_text(text_lower: str) -> list[str]:
    """
    Detect diseases using advanced pattern matching.
    """
    diseases = []
    
    # Diabetes patterns
    if re.search(r'diabetes|diabetic|blood sugar|glucose level', text_lower):
        diseases.append('diabetes')
    
    # Hypertension patterns
    if re.search(r'hypertension|high blood pressure|elevated bp', text_lower):
        diseases.append('hypertension')
    
    # Cholesterol patterns
    if re.search(r'hyperlipidemia|dyslipidemia|high cholesterol', text_lower):
        diseases.append('cholesterol')
    
    # Thyroid patterns
    if re.search(r'thyroid|hypothyroid|hyperthyroid|goiter', text_lower):
        diseases.append('thyroid')
    
    # Cardiac patterns
    if re.search(r'cardiac|myocardial infarction|mi|cad|coronary', text_lower):
        diseases.append('heart_disease')
    
    return list(set(diseases))
