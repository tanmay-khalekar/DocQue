import logging
from typing import Optional, List

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db import models
from app.schemas.symptom_schema import SymptomEntryCreate, SymptomAnalysisCreate, UserCreate  # assuming schemas live here
from app.schemas.report_schema import ReportCreate

logger = logging.getLogger(__name__)



# HELPER FUNCTIONS

def _save(db: Session, instance):
    """Safely save an instance to the database."""
    try:
        db.add(instance)
        db.commit()
        db.refresh(instance)
        logger.info(f"Saved {instance.__class__.__name__} with ID {getattr(instance, 'id', None)}")
        return instance
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error while saving {instance.__class__.__name__}: {e}")
        raise


# USER CRUD

def create_user(db: Session, user_data: UserCreate) -> models.User:
    logger.info("Creating new user")
    user = models.User(**user_data.model_dump())
    return _save(db, user)


def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    logger.info(f"Fetching user by id={user_id}")
    return db.get(models.User, user_id)


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    logger.info(f"Fetching user by email={email}")
    return db.query(models.User).filter(models.User.email == email).first()

def update_user(
    db: Session, user: models.User, update_data: dict
) -> models.User:
    logger.info(f"Updating user id={user.user_id}")
    for key, value in update_data.items():
        setattr(user, key, value)
    return _save(db, user)


def delete_user(db: Session, user: models.User) -> None:
    try:
        logger.info(f"Deleting user id={user.user_id}")
        db.delete(user)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error deleting user id={user.user_id}: {e}")
        raise


# SYMPTOM ENTRY CRUD

def create_symptom_entry(
    db: Session, entry_data: SymptomEntryCreate
) -> models.SymptomEntry:
    logger.info("Creating symptom entry")
    entry = models.SymptomEntry(**entry_data.model_dump())
    return _save(db, entry)


def get_entries_by_user(
    db: Session, user_id: int, skip: int = 0, limit: int = 20
) -> List[models.SymptomEntry]:
    logger.info(f"Fetching symptom entries for user_id={user_id}")
    return (
        db.query(models.SymptomEntry)
        .filter(models.SymptomEntry.user_id == user_id)
        .order_by(models.SymptomEntry.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_entry_by_id(db: Session, entry_id: int) -> Optional[models.SymptomEntry]:
    logger.info(f"Fetching symptom entry id={entry_id}")
    return db.get(models.SymptomEntry, entry_id)

def get_entries_with_analysis(db: Session, user_id: int):
    return (
        db.query(models.SymptomEntry, models.SymptomAnalysis)
        .join(models.SymptomAnalysis, models.SymptomEntry.entry_id == models.SymptomAnalysis.entry_id)
        .filter(models.SymptomEntry.user_id == user_id)
        .order_by(models.SymptomEntry.created_at.asc())
        .all()
    )

def update_symptom_entry(
    db: Session, entry: models.SymptomEntry, update_data: dict
) -> models.SymptomEntry:
    logger.info(f"Updating symptom entry id={entry.entry_id}")
    for key, value in update_data.items():
        setattr(entry, key, value)
    return _save(db, entry)


def delete_symptom_entry(db: Session, entry: models.SymptomEntry) -> None:
    try:
        logger.info(f"Deleting symptom entry id={entry.entry_id}")
        db.delete(entry)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error deleting symptom entry id={entry.entry_id}: {e}")
        raise


# -----------------------------
# SYMPTOM ANALYSIS CRUD
# -----------------------------

def create_symptom_analysis(
    db: Session, analysis_data: SymptomAnalysisCreate
) -> models.SymptomAnalysis:
    logger.info("Creating symptom analysis")
    analysis = models.SymptomAnalysis(**analysis_data.model_dump())
    return _save(db, analysis)


def get_analysis_by_entry(
    db: Session, entry_id: int
) -> Optional[models.SymptomAnalysis]:
    logger.info(f"Fetching analysis for entry_id={entry_id}")
    return (
        db.query(models.SymptomAnalysis)
        .filter(models.SymptomAnalysis.entry_id == entry_id)
        .first()
    )

def update_symptom_analysis(
    db: Session, analysis: models.SymptomAnalysis, update_data: dict
) -> models.SymptomAnalysis:
    logger.info(f"Updating analysis id={analysis.analysis_id}")
    for key, value in update_data.items():
        setattr(analysis, key, value)
    return _save(db, analysis)


def delete_symptom_analysis(db: Session, analysis: models.SymptomAnalysis) -> None:
    try:
        logger.info(f"Deleting analysis id={analysis.analysis_id}")
        db.delete(analysis)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error deleting analysis id={analysis.analysis_id}: {e}")
        raise

# -----------------------------
# SPECIALIST CRUD
# -----------------------------

def get_specialist_by_id(
    db: Session, specialist_id: int
) -> Optional[models.Specialist]:
    logger.info(f"Fetching specialist id={specialist_id}")
    return db.get(models.Specialist, specialist_id)


def get_all_specialists(db: Session) -> List[models.Specialist]:
    logger.info("Fetching all specialists")
    return db.query(models.Specialist).all()


def update_specialist(
    db: Session, specialist: models.Specialist, update_data: dict
) -> models.Specialist:
    logger.info(f"Updating specialist id={specialist.specialist_id}")
    for key, value in update_data.items():
        setattr(specialist, key, value)
    return _save(db, specialist)


def delete_specialist(db: Session, specialist: models.Specialist) -> None:
    try:
        logger.info(f"Deleting specialist id={specialist.specialist_id}")
        db.delete(specialist)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error deleting specialist id={specialist.specialist_id}: {e}")
        raise

def get_specialist_by_name(db: Session, name: str) -> Optional[models.Specialist]:
    return db.query(models.Specialist).filter(models.Specialist.name == name).first()
# -----------------------------
# REPORT CRUD
# -----------------------------

def create_report(
    db: Session, report_data: ReportCreate
) -> models.Report:
    logger.info("Creating report")
    report = models.Report(**report_data.model_dump())
    return _save(db, report)


def get_reports_by_user(
    db: Session, user_id: int, skip: int = 0, limit: int = 20
) -> List[models.Report]:
    logger.info(f"Fetching reports for user_id={user_id}")
    return (
        db.query(models.Report)
        .filter(models.Report.user_id == user_id)
        .order_by(models.Report.generated_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def update_report(
    db: Session, report: models.Report, update_data: dict
) -> models.Report:
    logger.info(f"Updating report id={report.report_id}")
    for key, value in update_data.items():
        setattr(report, key, value)
    return _save(db, report)


def delete_report(db: Session, report: models.Report) -> None:
    try:
        logger.info(f"Deleting report id={report.report_id}")
        db.delete(report)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error deleting report id={report.report_id}: {e}")
        raise


# new additions
def get_all_entries(db: Session, skip: int = 0, limit: int = 50):
    return (
        db.query(models.SymptomEntry)
        .order_by(models.SymptomEntry.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )