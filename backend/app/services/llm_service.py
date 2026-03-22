import os
import json
import logging
import re
from typing import Dict, Any, List

from groq import Groq
from app.validators import validate_symptom_data  # your external validator

logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise RuntimeError("GROQ_API_KEY not set")

MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

client = Groq(api_key=API_KEY)

MAX_RETRIES = 3


# ---------------------------------------------------------
# CANONICAL SYMPTOMS
# ---------------------------------------------------------

# # Map LLM symptom text to standard codes
# CANONICAL_SYMPTOMS = {
#     "CHEST_PAIN": ["chest pain", "chest discomfort", "tightness in chest"],
#     "BREATHLESSNESS": ["breathlessness", "shortness of breath", "dyspnea"],
#     "LEFT_ARM_PAIN": ["left arm pain", "pain in left arm"],
#     "SEVERE_HEADACHE": ["severe headache", "intense headache", "migraine"],
#     "BLURRED_VISION": ["blurred vision", "vision disturbance"],
#     "HIGH_FEVER": ["high fever", "temperature above 38.5C"],
#     "STIFF_NECK": ["stiff neck", "neck rigidity"],
#     # Add more canonical mappings as needed
# }

# def map_to_canonical(symptoms: List[str]) -> List[Dict[str, str]]:
#     """
#     Convert raw LLM symptom strings to canonical codes.
#     Returns a list of dicts: [{"name": raw_name, "code": canonical_code}, ...]
#     """
#     mapped = []
#     for s in symptoms:
#         lower_s = s.lower()
#         code_found = None
#         for code, aliases in CANONICAL_SYMPTOMS.items():
#             if lower_s in [a.lower() for a in aliases]:
#                 code_found = code
#                 break
#         mapped.append({"name": s, "code": code_found or "UNKNOWN"})
#     return mapped

# ---------------------------------------------------------
# PROMPTS
# ---------------------------------------------------------
SYSTEM_PROMPT = """
You are a medical symptom parser.

Your task is to extract structured information from user symptom descriptions.

IMPORTANT RULES:
1. Only extract information explicitly mentioned.
2. Do NOT provide diagnosis.
3. Output STRICT JSON only.
4. Do NOT include explanations or extra text.

SYMPTOM FORMAT:
Each symptom MUST be an object with:
- "name": original symptom text (lowercase)
- "code": standardized UPPERCASE code with underscores

EXAMPLES:
"chest pain" → "CHEST_PAIN"
"shortness of breath" → "BREATHLESSNESS"
"high fever" → "HIGH_FEVER"

JSON FORMAT:
{
 "symptoms": [
   {"name": "symptom", "code": "SYMBOLIC_CODE"}
 ],
 "category": "one of: neurological, respiratory, cardiovascular, digestive, dermatological, musculoskeletal, general",
 "duration": "duration mentioned or null",
 "severity_score": integer from 1 to 10,
 "summary": "short summary"
}
"""

# ---------------------------------------------------------
# JSON PARSER
# ---------------------------------------------------------

def extract_json(response_text: str) -> Dict[str, Any]:
    """
    Extract JSON safely from LLM output.
    """

    try:
        return json.loads(response_text)

    except json.JSONDecodeError:
        logger.warning("Direct JSON parse failed, attempting regex extraction")

        # Extract first JSON object using regex
        match = re.search(r"\{.*?\}", response_text, re.DOTALL)

        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError as e:
                logger.error(f"Regex JSON parse failed: {e}")

        raise ValueError("Invalid JSON from LLM")


# ---------------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------------

def analyze_symptom_text(user_text: str) -> Dict[str, Any]:
    """
    Main entry point for symptom analysis.
    """

    for attempt in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_text}
                ],
                temperature=0,
                max_tokens=300,
                timeout=10
            )

            content = response.choices[0].message.content
            if not content:  # to avoid squiggles i added these two lines
                raise ValueError("Empty response from LLM")

            logger.debug(f"LLM raw response: {content}")
            logger.error(f"RAW LLM OUTPUT: {content}")

            data = extract_json(content)

            validated_data = validate_symptom_data(data)

            return validated_data

        except Exception as e:
            logger.warning(
                f"Attempt {attempt + 1} failed | Input: {user_text} | Error: {str(e)}"
            )

    logger.error("All retries failed")
    raise RuntimeError("LLM processing failed after retries")