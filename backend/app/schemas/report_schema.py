from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# -----------------------------
# REPORT CREATION
# -----------------------------

class ReportCreate(BaseModel):
    user_id: int
    report_file: Optional[str] = None


# -----------------------------
# REPORT RESPONSE
# -----------------------------

class ReportResponse(BaseModel):
    report_id: int
    user_id: int
    generated_at: datetime
    report_file: Optional[str]

    class Config:
        from_attributes = True


# -----------------------------
# TIMELINE ENTRY
# -----------------------------

class SymptomTimelineEntry(BaseModel):
    entry_id: int
    symptom_text: str
    severity: Optional[int]
    risk_level: Optional[str]
    created_at: datetime


# -----------------------------
# AGGREGATED REPORT DATA
# -----------------------------

class SymptomReportResponse(BaseModel):
    user_id: int
    generated_at: datetime

    total_entries: int

    severity_trend: Optional[str]
    risk_summary: Optional[str]
    recommended_specialist: Optional[str]

    timeline: List[SymptomTimelineEntry]