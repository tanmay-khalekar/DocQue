from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# -----------------------------
# USER SCHEMAS
# -----------------------------

class UserBase(BaseModel):
    name: str
    email: str
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# -----------------------------
# SYMPTOM ENTRY SCHEMAS
# -----------------------------

class SymptomEntryBase(BaseModel):
    symptom_text: str = Field(..., min_length=3)
    severity: Optional[int] = Field(None, ge=1, le=10)


class SymptomEntryCreate(SymptomEntryBase):
    user_id: int


class SymptomEntryUpdate(BaseModel):
    symptom_text: Optional[str]
    severity: Optional[int]


class SymptomEntryResponse(SymptomEntryBase):
    entry_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# -----------------------------
# SYMPTOM ANALYSIS SCHEMAS
# -----------------------------

class SymptomAnalysisBase(BaseModel):
    structured_symptoms: Optional[dict]
    risk_level: Optional[str]
    specialist_id: Optional[int]
    severity_score: Optional[int] = Field(None, ge=1, le=10)


class SymptomAnalysisCreate(SymptomAnalysisBase):
    entry_id: int


class SymptomAnalysisResponse(SymptomAnalysisBase):
    analysis_id: int
    entry_id: int

    class Config:
        from_attributes = True

class SymptomWithAnalysisResponse(BaseModel):
    entry: SymptomEntryResponse
    analysis: Optional[SymptomAnalysisResponse]
    analysis_status: str

    class Config:
        from_attributes = True