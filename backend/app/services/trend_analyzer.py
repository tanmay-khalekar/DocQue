from typing import List, Dict
from datetime import datetime


def analyze_trend(entries: List[Dict]) -> Dict:
    """
    entries: list of dicts with:
    {
        "created_at": datetime,
        "severity_score": int
    }
    """

    if not entries:
        return {
            "trend": "No Data",
            "timeline": []
        }

    # -------------------------
    # Sort chronologically
    # -------------------------
    entries_sorted = sorted(entries, key=lambda x: x["created_at"])

    # -------------------------
    # Build timeline
    # -------------------------
    timeline = [
        {
            "date": entry["created_at"].isoformat(),
            "severity": entry["severity_score"]
        }
        for entry in entries_sorted
    ]

    # -------------------------
    # Trend logic
    # -------------------------
    first = entries_sorted[0]["severity_score"]
    last = entries_sorted[-1]["severity_score"]

    if last > first:
        trend = "Worsening"
    elif last < first:
        trend = "Improving"
    else:
        trend = "Stable"

    return {
        "trend": trend,
        "timeline": timeline
    }