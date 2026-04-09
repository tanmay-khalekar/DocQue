from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import crud
from app.api.dependencies import get_db
from app.services.trend_analyzer import analyze_trend

from fastapi.responses import StreamingResponse
from app.services.pdf_generator import generate_pdf

from app.schemas.report_schema import ReportResponse

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/{user_id}", response_model=ReportResponse)
def get_report(user_id: int, db: Session = Depends(get_db)):

    records = crud.get_entries_with_analysis(db, user_id)

    if not records:
        raise HTTPException(status_code=404, detail="No data found")

    # -------------------------
    # Build timeline input
    # -------------------------
    trend_input = []

    risk_summary = {"High": 0, "Medium": 0, "Low": 0}

    latest_specialist = None

    for entry, analysis in records:
        trend_input.append({
            "created_at": entry.created_at,
            "severity_score": analysis.severity_score
        })

        # risk summary
        if analysis.risk_level:
            risk_summary[analysis.risk_level] += 1

        # latest specialist
        if analysis.specialist_id:
            specialist = crud.get_specialist_by_id(db, analysis.specialist_id)
            latest_specialist = specialist.name if specialist else None

    # -------------------------
    # Trend analysis
    # -------------------------
    trend_data = analyze_trend(trend_input)

    return {
        "user_id": user_id,
        "trend": trend_data["trend"],
        "timeline": trend_data["timeline"],
        "risk_summary": risk_summary,
        "latest_specialist": latest_specialist,
        "total_entries": len(records)
    }

@router.get("/{user_id}/download")
def download_report(user_id: int, db: Session = Depends(get_db)):

    # reuse your existing logic
    report_data = get_report(user_id, db)

    pdf_buffer = generate_pdf(report_data)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=report_{user_id}.pdf"
        }
    )