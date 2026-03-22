import json
import logging
from typing import Dict, Any, Set, List

from app.services.specialist_mapper import get_specialist_from_symptoms

logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# LOAD RULE CONFIG
# ---------------------------------------------------------
import os

BASE_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(BASE_DIR, "rule_config.json")


try:
    with open(CONFIG_PATH, "r") as f:
        RULES = json.load(f)
except Exception as e:
    logger.error(f"Failed to load rule config: {e}")
    RULES = {}

RED_FLAG_COMBINATIONS: List[Set[str]] = [set(combo) for combo in RULES.get("red_flag_combinations", [])]
RED_FLAG_SINGLE: Set[str] = set(RULES.get("red_flag_single", []))
SEVERITY_RULES: Dict[str, int] = RULES.get("severity_rules", {"HIGH":7, "MEDIUM":4})

# ---------------------------------------------------------
# MAIN RULE ENGINE
# ---------------------------------------------------------

def evaluate_risk_and_specialist(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Takes validated LLM output (with canonical codes) and returns:
    - risk_level
    - specialist
    - reason (why this level was assigned)
    """

    # -------------------------
    # Extract canonical codes from LLM output
    # -------------------------
    symptoms_with_codes = data.get("symptoms", [])

    if not symptoms_with_codes:
        return {
            "risk_level": "Low",
            "specialist": "General Physician",
            "reason": "no_symptoms"
        }

    symptom_codes = {s.get("code") for s in symptoms_with_codes if s.get("code")}

    severity = int(data.get("severity_score", 5))

    # -------------------------
    # 1. Default risk (based on severity thresholds from config)
    # -------------------------
    if severity >= SEVERITY_RULES.get("HIGH", 7):
        risk_level = "High"
    elif severity >= SEVERITY_RULES.get("MEDIUM", 4):
        risk_level = "Medium"
    else:
        risk_level = "Low"

    reason = "severity_based"

    # -------------------------
    # 2. Single red flag override
    # -------------------------
    if symptom_codes & RED_FLAG_SINGLE:
        logger.warning(f"Single red flag detected: {symptom_codes & RED_FLAG_SINGLE}")
        risk_level = "High"
        reason = "red_flag_single"

    # -------------------------
    # 3. Red flag combinations
    # -------------------------
    for combo in RED_FLAG_COMBINATIONS:
        if combo.issubset(symptom_codes):
            logger.warning(f"Red flag combination detected: {combo}")
            risk_level = "High"
            reason = "red_flag_combination"
            break

    # -------------------------
    # 4. Specialist mapping
    # -------------------------
    specialist = get_specialist_from_symptoms(symptoms_with_codes, data.get("category", "general"))

    return {
        "risk_level": risk_level,
        "specialist": specialist,
        "reason": reason
    }