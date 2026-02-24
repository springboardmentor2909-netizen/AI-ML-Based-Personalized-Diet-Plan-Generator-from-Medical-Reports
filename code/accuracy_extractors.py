import re

def try_float(s):
    try:
        return float(s)
    except:
        return None

def extract_number(pattern, text, min_val=None, max_val=None):
    """
    Generic extractor that captures the first numeric group and validates range.
    """
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        return None
    val = try_float(match.group(1))
    if val is None:
        return None
    if min_val is not None and val < min_val:
        return None
    if max_val is not None and val > max_val:
        return None
    return val

# Specific convenience wrappers 
def extract_glucose(text):
    return extract_number(r"(?:glucose|blood sugar)[^\d\-]{0,10}([0-9]{2,3})", text, 50, 500)

def extract_total_chol(text):
    return extract_number(r"(?:total cholesterol|cholesterol)[^\d\-]{0,10}([0-9]{2,3})", text, 50, 400)

def extract_ldl(text):
    return extract_number(r"\bldl\b[^\d\-]{0,10}([0-9]{2,3})", text, 20, 300)

def extract_hdl(text):
    return extract_number(r"\bhdl\b[^\d\-]{0,10}([0-9]{2,3})", text, 10, 120)

def extract_triglycerides(text):
    return extract_number(r"(?:triglycerides|tg)[^\d\-]{0,10}([0-9]{2,3})", text, 40, 600)

def extract_hemoglobin(text):
    return extract_number(r"(?:hemoglobin|hb)[^\d\-]{0,10}([0-9]+(?:\.[0-9]+)?)", text, 5, 20)

def extract_creatinine(text):
    return extract_number(r"(?:creatinine)[^\d\-]{0,10}([0-9]+(?:\.[0-9]+)?)", text, 0.2, 6)

def extract_bmi(text):
    return extract_number(r"\bbmi\b[^\d\-]{0,10}([0-9]+(?:\.[0-9]+)?)", text, 10, 80)


def extract_bp_strict(text):
    # Normalize common OCR separators
    text = text.replace("—", "/").replace("-", "/")

    # Priority 1: Explicit "Blood Pressure" label
    m = re.search(
        r"blood\s*pressure[^\d]{0,20}([0-9]{2,3})\s*/\s*([0-9]{2,3})",
        text,
        re.IGNORECASE
    )
    if m:
        sys = int(m.group(1))
        dia = int(m.group(2))
        if 70 <= sys <= 200 and 40 <= dia <= 130:
            return f"{sys}/{dia}"

    # Priority 2: Generic BP pattern with spaces and optional mmHg
    matches = re.findall(
        r"([0-9]{2,3})\s*/\s*([0-9]{2,3})\s*(?:mmhg)?",
        text,
        re.IGNORECASE
    )

    for sys, dia in matches:
        sys = int(sys)
        dia = int(dia)

        # Reject dates like 12/08
        if sys <= 31 and dia <= 31:
            continue

        if 70 <= sys <= 200 and 40 <= dia <= 130:
            return f"{sys}/{dia}"

    return None


def extract_doctor_comments(text):
    """
    Search for common headings and capture the following block.
    Return a cleaned, truncated string (max 2000 chars).
    """
    patterns = [
        r"(doctor'?s?\s*comments?)\s*[:\-\—]\s*(.+)",
        r"(doctor'?s?\s*notes?)\s*[:\-\—]\s*(.+)",
        r"(clinical\s*notes?)\s*[:\-\—]\s*(.+)",
        r"(remarks?)\s*[:\-\—]\s*(.+)",
        r"(impression[s]?)\s*[:\-\—]\s*(.+)",
        r"(advice)\s*[:\-\—]\s*(.+)",
        r"(recommendation[s]?)\s*[:\-\—]\s*(.+)",
        r"(summary)\s*[:\-\—]\s*(.+)",
    ]
    # Try each pattern with DOTALL so multi-line comments are captured
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE | re.DOTALL)
        if m:
            comment = m.group(2)
            # Trim at next uppercase heading-like token (e.g., "TESTS:" or "SUMMARY:")
            next_heading = re.search(r"\n?[A-Z\s]{3,}[:\n]", comment)
            if next_heading:
                comment = comment[:next_heading.start()]
            # Normalize whitespace
            comment = re.sub(r"\s+", " ", comment).strip()
            return comment[:2000]
    return None

def extract_age(text):
    # Matches: Age: 45 | AGE - 32 | Age 28 Years
    m = re.search(r"\bage\b[^\d]{0,10}([0-9]{1,3})", text, re.IGNORECASE)
    if m:
        age = int(m.group(1))
        if 0 < age < 120:
            return age
    return None

import re

def extract_gender(text):
    text = text.lower()

    # OTHERS / THIRD GENDER
    if re.search(r"\b(transgender|third gender|non[-\s]?binary|other|others)\b", text):
        return "Others"

    # FEMALE
    if re.search(r"\bfemale\b", text):
        return "Female"

    # MALE
    if re.search(r"\bmale\b", text):
        return "Male"

    # SINGLE-LETTER NOTATION
    m = re.search(r"\bsex\b[^\w]{0,10}([mf])\b", text)
    if m:
        return "Male" if m.group(1) == "m" else "Female"

    return None


def extract_height(text):
    # Height in cm 
    m = re.search(r"\bheight\b[^\d]{0,10}([0-9]{2,3}(?:\.[0-9]+)?)\s*cm", text, re.IGNORECASE)
    if m:
        h = float(m.group(1))
        if 50 <= h <= 250:
            return round(h, 1)
    return None


def extract_weight(text):
    # Weight in kg 
    m = re.search(r"\bweight\b[^\d]{0,10}([0-9]{2,3}(?:\.[0-9]+)?)\s*kg", text, re.IGNORECASE)
    if m:
        w = float(m.group(1))
        if 10 <= w <= 300:
            return round(w, 1)
    return None


def calculate_bmi(height_cm, weight_kg):
    if height_cm is None or weight_kg is None:
        return None

    try:
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        if 10 <= bmi <= 80:   # realistic BMI range
            return round(bmi, 1)
    except:
        pass

    return None

def extract_pulse(text):
    m = re.search(
        r"(pulse|pulse rate|heart rate|pr)[^\d]{0,15}([0-9]{2,3})",
        text,
        re.IGNORECASE
    )
    if m:
        pulse = int(m.group(2))
        if 30 <= pulse <= 200:   # realistic pulse range
            return pulse
    return None

