from typing import List, Dict

# -------------------------
# CATEGORY MAPPING
# -------------------------
CATEGORY_TO_SPECIALIST: Dict[str, str] = {
    "neurological": "Neurologist",
    "respiratory": "Pulmonologist",
    "cardiovascular": "Cardiologist",
    "digestive": "Gastroenterologist",
    "dermatological": "Dermatologist",
    "musculoskeletal": "Orthopedic",
    "general": "General Physician"
}

# -------------------------
# CANONICAL SYMPTOM TO SPECIALIST OVERRIDE
# -------------------------
CANONICAL_SYMPTOM_TO_SPECIALIST: Dict[str, str] = {
    "CHEST_PAIN": "Cardiologist",
    "BREATHLESSNESS": "Pulmonologist",
    "SKIN_RASH": "Dermatologist",
    "JOINT_PAIN": "Orthopedic",
    "SEVERE_HEADACHE": "Neurologist"
}


def get_specialist_from_symptoms(symptoms: List[Dict[str, str]], category: str) -> str:
    """
    Determines specialist based on canonical symptom codes first,
    fallback to category.
    
    symptoms: List of dicts with {"name": raw_name, "code": canonical_code}
    """
    for symptom in symptoms:
        code = symptom.get("code")
        if code in CANONICAL_SYMPTOM_TO_SPECIALIST:
            return CANONICAL_SYMPTOM_TO_SPECIALIST[code]

    # fallback to category
    return CATEGORY_TO_SPECIALIST.get(category, "General Physician")