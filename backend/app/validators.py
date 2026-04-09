import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

ALLOWED_CATEGORIES = {
    "neurological",
    "respiratory",
    "cardiovascular",
    "digestive",
    "dermatological",
    "musculoskeletal",
    "general"
}


def validate_symptom_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates and sanitizes LLM output.

    Strategy:
    - symptoms: strict (must exist and be valid)
    - category: fallback to 'general'
    - severity_score: fallback to 5
    - summary: fallback string
    - duration: optional
    """

    if not isinstance(data, dict):
        raise ValueError("LLM output must be a dictionary")

    validated = {}

# -------------------------
# symptoms (STRICT)
# -------------------------

    symptoms = data.get("symptoms")

    if not isinstance(symptoms, list):
        raise ValueError("Invalid or missing 'symptoms'")

    cleaned_symptoms = []

    for s in symptoms:
        if not isinstance(s, dict):
            continue

        name = s.get("name")
        code = s.get("code")

        if not isinstance(name, str) or not isinstance(code, str):
            continue

        name = name.lower().strip()
        code = code.upper().strip()

        if not name or not code:
            continue

        cleaned_symptoms.append({
            "name": name,
            "code": code
        })

    # 🔥 fallback instead of crash
    if not cleaned_symptoms:
        logger.warning("No valid structured symptoms, using fallback")
        cleaned_symptoms = [{
            "name": "unspecified symptom",
            "code": "GENERAL_SYMPTOM"
        }]

    validated["symptoms"] = cleaned_symptoms

    # -------------------------
    # category (SOFT)
    # -------------------------
    category = str(data.get("category", "")).strip().lower()

    if category not in ALLOWED_CATEGORIES:
        logger.warning(f"Invalid category '{category}', defaulting to 'general'")
        category = "general"

    validated["category"] = category

    # -------------------------
    # duration (OPTIONAL)
    # -------------------------
    duration = data.get("duration")

    if duration is None:
        validated["duration"] = None
    else:
        duration = str(duration).strip()
        validated["duration"] = duration if duration else None

    # -------------------------
    # severity_score (SOFT)
    # -------------------------
    severity = data.get("severity_score")

# Ensure severity is not None
    if severity is None:
        severity = 5

    try:
        severity = int(severity)
    except (TypeError, ValueError):
        logger.warning("Invalid severity_score, defaulting to 5")
        severity = 5

# Clamp between 1 and 10
    severity = max(1, min(10, severity))
    validated["severity_score"] = severity


    # -------------------------
    # summary (SOFT)
    # -------------------------
    summary = data.get("summary")

    summary = str(summary).strip() if summary else ""

    if not summary:
        summary = "No summary provided"

    validated["summary"] = summary

    return validated