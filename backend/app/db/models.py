from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    date_of_birth = Column(Date)
    gender = Column(Enum("Male", "Female", "Other", name="gender_enum"))
    created_at = Column(DateTime, default=datetime.utcnow)

    symptom_entries = relationship("SymptomEntry", back_populates="user")
    reports = relationship("Report", back_populates="user")


class SymptomEntry(Base):
    __tablename__ = "symptom_entries"

    entry_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), index=True)
    symptom_text = Column(Text, nullable=False)
    severity = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="symptom_entries")
    analysis = relationship("SymptomAnalysis", back_populates="entry", uselist=False)


class SymptomAnalysis(Base):
    __tablename__ = "symptom_analysis"

    analysis_id = Column(Integer, primary_key=True)
    entry_id = Column(Integer, ForeignKey("symptom_entries.entry_id"), index=True)

    structured_symptoms = Column(JSONB)
    risk_level = Column(String)
    specialist_id = Column(Integer, ForeignKey("specialists.specialist_id"), index=True)
    severity_score = Column(Integer)

    entry = relationship("SymptomEntry", back_populates="analysis")
    specialist = relationship("Specialist", back_populates="analyses")


class Specialist(Base):
    __tablename__ = "specialists"

    specialist_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    field = Column(String)
    description = Column(Text)

    analyses = relationship("SymptomAnalysis", back_populates="specialist")


class Report(Base):
    __tablename__ = "reports"

    report_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), index=True)

    generated_at = Column(DateTime, default=datetime.utcnow)
    report_file = Column(Text)

    user = relationship("User", back_populates="reports")