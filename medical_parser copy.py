import re
from typing import Dict, List, Tuple

def build_medical_intent(diseases: list[str], extracted_text: str) -> dict:
    """
    Build a comprehensive medical intent from diseases and extracted text.
    """
    # Extract numerical values and conditions
    biomarkers = extract_biomarkers(extracted_text)
    patient_info = extract_patient_info(extracted_text)

    # Determine risk level based on conditions and biomarkers
    risk_level = calculate_risk_level(diseases, biomarkers)

    return {
        "conditions": diseases,
        "biomarkers": biomarkers,
        "patient_info": patient_info,
        "risk_level": risk_level
    }

def extract_biomarkers(text: str) -> Dict[str, Dict]:
    """
    Extract biomarker values from medical report text with comprehensive patterns.
    """
    biomarkers = {}
    text_lower = text.lower()

    # Comprehensive biomarker patterns (order matters - more specific first)
    biomarker_patterns = {
        # Glucose & Diabetes markers
        "fasting_glucose": r"(?:fasting\s+)?glucose\s*(?:[:\-]?\s*)(\d+\.?\d*)\s*(?:mg/dl|mg\/dl)",
        "hba1c": r"hba1c\s*(?:[:\-]?\s*)(\d+\.?\d*)\s*(?:%)?",
        "random_glucose": r"random\s+(?:blood\s+)?glucose\s*(?:[:\-]?\s*)(\d+\.?\d*)",
        
        # Lipid panel
        "total_cholesterol": r"(?:total\s+)?cholesterol\s*(?:[:\-]?\s*)(\d+\.?\d*)\s*(?:mg/dl|mg\/dl)",
        "hdl": r"hdl\s*(?:[:\-]?\s*)(\d+\.?\d*)\s*(?:mg/dl|mg\/dl)",
        "ldl": r"ldl\s*(?:[:\-]?\s*)(\d+\.?\d*)\s*(?:mg/dl|mg\/dl)",
        "triglycerides": r"triglycerides?\s*(?:[:\-]?\s*)(\d+\.?\d*)\s*(?:mg/dl|mg\/dl)",
        
        # Thyroid markers
        "tsh": r"tsh\s*(?:[:\-]?\s*)(\d+\.?\d*)\s*(?:miu/l|miu\/l|μiu/ml)?",
        "t3": r"(?:free\s+)?t3\s*(?:[:\-]?\s*)(\d+\.?\d*)\s*(?:pg/ml|pg\/ml)?",
        "t4": r"(?:free\s+)?t4\s*(?:[:\-]?\s*)(\d+\.?\d*)\s*(?:ng/dl|ng\/dl)?",
        "tpo_antibodies": r"tpo\s+antibodies?\s*(?:[:\-]?\s*)(\d+\.?\d*)",
        
        # Cardiac markers
        "ck_mb": r"ck\s*-?\s*mb\s*(?:[:\-]?\s*)(\d+\.?\d*)\s*(?:u/l|u\/l)?",
        "troponin": r"troponin\s*(?:[:\-]?\s*)(\d+\.?\d*)",
        "ldh": r"ldh\s*(?:[:\-]?\s*)(\d+\.?\d*)",
        
        # Hemoglobin & Blood
        "hemoglobin": r"hemoglobin\s*(?:[:\-]?\s*)(\d+\.?\d*)\s*(?:gm/dl|g/dl|g\/dl)",
        "hematocrit": r"hematocrit\s*(?:[:\-]?\s*)(\d+\.?\d*)\s*(?:%)?",
        
        # Renal function
        "creatinine": r"creatinine\s*(?:[:\-]?\s*)(\d+\.?\d*)\s*(?:mg/dl|mg\/dl)",
        "bun": r"(?:blood\s+)?urea\s+nitrogen|bun\s*(?:[:\-]?\s*)(\d+\.?\d*)\s*(?:mg/dl|mg\/dl)",
        "gfr": r"gfr\s*(?:[:\-]?\s*)(\d+\.?\d*)",
        
        # Hepatic function
        "alt": r"alt\s*(?:[:\-]?\s*)(\d+\.?\d*)\s*(?:u/l|u\/l)?",
        "ast": r"ast\s*(?:[:\-]?\s*)(\d+\.?\d*)\s*(?:u/l|u\/l)?",
        "bilirubin": r"(?:total\s+)?bilirubin\s*(?:[:\-]?\s*)(\d+\.?\d*)",
        
        # Electrolytes
        "sodium": r"sodium\s*(?:[:\-]?\s*)(\d+\.?\d*)\s*(?:mmol/l|mmol\/l|meq/l)",
        "potassium": r"potassium\s*(?:[:\-]?\s*)(\d+\.?\d*)\s*(?:mmol/l|mmol\/l|meq/l)",
        "calcium": r"calcium\s*(?:[:\-]?\s*)(\d+\.?\d*)\s*(?:mg/dl|mmol/l)",
        "phosphorus": r"phosphorus\s*(?:[:\-]?\s*)(\d+\.?\d*)",
        
        # Blood pressure (special case - two values)
        "blood_pressure": r"blood\s+pressure\s*(?:[:\-]?\s*)(\d+/\d+)",
    }

    for biomarker, pattern in biomarker_patterns.items():
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            value_str = match.group(1)
            # Handle blood pressure separately
            if biomarker == "blood_pressure":
                value = value_str
            else:
                try:
                    value = float(value_str)
                except ValueError:
                    continue
            
            biomarkers[biomarker] = {
                "value": value, 
                "unit": get_unit(biomarker),
                "abnormal": is_abnormal(biomarker, value) if biomarker != "blood_pressure" else False
            }

    return biomarkers

def extract_patient_info(text: str) -> Dict:
    """
    Extract patient demographic information.
    """
    info = {}
    text_lower = text.lower()

    # Age - try several robust patterns and prefer plausible values
    candidates: List[int] = []

    # Pattern: 'Age' or 'Age/Sex' followed by digits (e.g. 'Age/Sex : 50 Yr /F')
    for m in re.finditer(r'age(?:/sex)?\s*[:\s]*([0-9]{1,3})', text_lower, re.IGNORECASE):
        try:
            candidates.append(int(m.group(1)))
        except ValueError:
            pass

    # Pattern: number followed by 'yr' or 'years' (e.g. '50 Yr')
    for m in re.finditer(r'([0-9]{1,3})\s*(?:yr|y|years)\b', text_lower, re.IGNORECASE):
        try:
            candidates.append(int(m.group(1)))
        except ValueError:
            pass

    # Fallback: simple 'Age: 50' style
    age_match = re.search(r'age[:\s]*([0-9]{1,3})', text_lower)
    if age_match:
        try:
            candidates.append(int(age_match.group(1)))
        except ValueError:
            pass

    # Choose the best candidate: prefer values between 2 and 120 (exclude likely OCR '1' errors)
    chosen = None
    for c in candidates:
        if 2 <= c <= 120:
            chosen = c
            break
    if chosen is None and candidates:
        # If no preferred candidate, accept any reasonable value 0-120
        for c in candidates:
            if 0 < c <= 120:
                chosen = c
                break
    if chosen is not None:
        info["age"] = int(chosen)

    # Gender
    if "/f" in text_lower or "female" in text_lower:
        info["gender"] = "female"
    elif "/m" in text_lower or "male" in text_lower:
        info["gender"] = "male"

    # Patient name
    name_match = re.search(r'patient name\s*:\s*([^\n]+)', text_lower)
    if name_match:
        info["name"] = name_match.group(1).strip().title()

    return info

def calculate_risk_level(diseases: List[str], biomarkers: Dict) -> str:
    """
    Calculate risk level based on conditions and biomarker values.
    """
    risk_score = 0

    # Disease-based risk
    high_risk_diseases = ["diabetes", "hypertension", "heart_disease"]
    for disease in diseases:
        if any(hrd in disease.lower() for hrd in high_risk_diseases):
            risk_score += 2

    # Biomarker-based risk
    if "glucose" in biomarkers and biomarkers["glucose"]["value"] > 126:
        risk_score += 2
    if "hba1c" in biomarkers and biomarkers["hba1c"]["value"] > 6.5:
        risk_score += 2
    if "cholesterol" in biomarkers and biomarkers["cholesterol"]["value"] > 240:
        risk_score += 1
    if "blood_pressure" in biomarkers:
        systolic, diastolic = map(int, biomarkers["blood_pressure"]["value"].split('/'))
        if systolic > 140 or diastolic > 90:
            risk_score += 2

    if risk_score >= 4:
        return "high"
    elif risk_score >= 2:
        return "medium"
    else:
        return "low"

def get_unit(biomarker: str) -> str:
    """
    Get the standard unit for a biomarker.
    """
    units = {
        # Glucose & Diabetes
        "fasting_glucose": "mg/dl",
        "random_glucose": "mg/dl",
        "hba1c": "%",
        
        # Lipids
        "total_cholesterol": "mg/dl",
        "cholesterol": "mg/dl",
        "hdl": "mg/dl",
        "ldl": "mg/dl",
        "triglycerides": "mg/dl",
        
        # Thyroid
        "tsh": "mIU/L",
        "t3": "pg/ml",
        "t4": "ng/dl",
        "tpo_antibodies": "IU/ml",
        
        # Cardiac
        "ck_mb": "U/L",
        "troponin": "ng/ml",
        "ldh": "U/L",
        
        # Blood
        "hemoglobin": "g/dl",
        "hematocrit": "%",
        
        # Renal
        "creatinine": "mg/dl",
        "bun": "mg/dl",
        "gfr": "ml/min",
        
        # Hepatic
        "alt": "U/L",
        "ast": "U/L",
        "bilirubin": "mg/dl",
        
        # Electrolytes
        "sodium": "mEq/L",
        "potassium": "mEq/L",
        "calcium": "mg/dl",
        "phosphorus": "mg/dl",
        
        # Blood Pressure
        "blood_pressure": "mmHg"
    }
    return units.get(biomarker, "")

def is_abnormal(biomarker: str, value: float) -> bool:
    """
    Check if a biomarker value is abnormal based on standard reference ranges.
    """
    abnormal_ranges = {
        "fasting_glucose": (70, 100),  # Normal range
        "random_glucose": (70, 140),
        "hba1c": (4.0, 5.6),
        "total_cholesterol": (0, 200),
        "hdl": (40, 1000),  # Higher is better
        "ldl": (0, 100),
        "triglycerides": (0, 150),
        "tsh": (0.4, 4.0),
        "hemoglobin": (12.0, 17.5),
        "creatinine": (0.6, 1.2),
        "ck_mb": (0, 24),
    }
    
    if biomarker not in abnormal_ranges:
        return False
    
    min_val, max_val = abnormal_ranges[biomarker]
    if biomarker == "hdl":  # HDL higher is better
        return value < min_val or value > max_val
    return value < min_val or value > max_val
