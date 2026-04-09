from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

logger = logging.getLogger(__name__)

from app.api.dependencies import get_db
from app.db import crud
from app.db import models
from app.schemas.symptom_schema import (
    SymptomEntryCreate,
    SymptomEntryUpdate,
    SymptomEntryResponse,
    SymptomAnalysisResponse,
    SymptomWithAnalysisResponse,
    SymptomAnalysisCreate
)

from app.services.llm_service import analyze_symptom_text

from app.services.rule_engine import evaluate_risk_and_specialist

router = APIRouter(
    prefix="/api/symptoms",
    tags=["Symptoms"]
)

# ---------------------------------------------------------
# CREATE SYMPTOM ENTRY
# ---------------------------------------------------------

@router.post("/", response_model=SymptomWithAnalysisResponse, status_code=201)
def create_symptom_entry(entry_data: SymptomEntryCreate, db: Session = Depends(get_db)):

    user = crud.get_user_by_id(db, entry_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    entry = crud.create_symptom_entry(db, entry_data)

    analysis = None
    analysis_status = "success"

    try:
        llm_data = analyze_symptom_text(entry.symptom_text) 

        rule_output = evaluate_risk_and_specialist(llm_data)

        specialist_obj = crud.get_specialist_by_name(
            db, rule_output["specialist"]
            )

        specialist_id = specialist_obj.specialist_id if specialist_obj else None

        analysis_payload = SymptomAnalysisCreate(
            entry_id=entry.entry_id,
            structured_symptoms=llm_data,
            severity_score=llm_data.get("severity_score"),
            risk_level=rule_output["risk_level"],
            specialist_id=specialist_id
        )

        analysis = crud.create_symptom_analysis(db, analysis_payload)

    except Exception as e:
        logger.error(
            f"LLM processing failed for entry_id={entry.entry_id}, user_id={entry.user_id}", exc_info=True
        )
        analysis_status = "failed"

    return {
        "entry": entry,
        "analysis": analysis,
        "analysis_status": analysis_status
    }
# ---------------------------------------------------------
# GET USER SYMPTOM HISTORY
# ---------------------------------------------------------

@router.get(
    "/user/{user_id}",
    response_model=List[SymptomEntryResponse]
)
def get_user_entries(
    user_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Retrieve all symptom entries for a user.
    """

    user = crud.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    entries = crud.get_entries_by_user(db, user_id, skip, limit)

    return entries


# ---------------------------------------------------------
# GET SINGLE SYMPTOM ENTRY
# ---------------------------------------------------------

@router.get(
    "/{entry_id}",
    response_model=SymptomEntryResponse
)
def get_entry(
    entry_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a single symptom entry.
    """

    entry = crud.get_entry_by_id(db, entry_id)

    if not entry:
        raise HTTPException(
            status_code=404,
            detail="Symptom entry not found"
        )

    return entry


# ---------------------------------------------------------
# UPDATE SYMPTOM ENTRY
# ---------------------------------------------------------

@router.put(
    "/{entry_id}",
    response_model=SymptomEntryResponse
)
def update_entry(
    entry_id: int,
    entry_update: SymptomEntryUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a symptom entry.
    """

    entry = crud.get_entry_by_id(db, entry_id)

    if not entry:
        raise HTTPException(
            status_code=404,
            detail="Entry not found"
        )

    updated_entry = crud.update_symptom_entry(
        db,
        entry,
        entry_update.model_dump(exclude_unset=True)
    )

    return updated_entry


# ---------------------------------------------------------
# DELETE SYMPTOM ENTRY
# ---------------------------------------------------------

@router.delete(
    "/{entry_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_entry(
    entry_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a symptom entry.
    """

    entry = crud.get_entry_by_id(db, entry_id)

    if not entry:
        raise HTTPException(
            status_code=404,
            detail="Entry not found"
        )

    crud.delete_symptom_entry(db, entry)

    return


# ---------------------------------------------------------
# GET ANALYSIS FOR ENTRY
# ---------------------------------------------------------

@router.get(
    "/{entry_id}/analysis",
    response_model=SymptomAnalysisResponse
)
def get_analysis(
    entry_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve AI analysis for a symptom entry.
    """

    analysis = crud.get_analysis_by_entry(db, entry_id)

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )

    return analysis