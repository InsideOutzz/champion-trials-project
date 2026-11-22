from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas, models

router = APIRouter(
    prefix="/reports",
    tags=["Crowd Reports"]
)


@router.post("/", response_model=schemas.ReportResponse)
def submit_report(
    report: schemas.ReportCreate,
    db: Session = Depends(get_db)
):
    bus = db.query(models.Bus).filter(
        models.Bus.id == report.bus_id
    ).first()

    if not bus:
        raise HTTPException(
            status_code=404,
            detail="Bus line not found"
        )

    return crud.create_report(db, report)


@router.get("/", response_model=list[schemas.ReportResponse])
def list_reports(
    bus_id: int = None,
    db: Session = Depends(get_db)
):
    return crud.get_reports(db, bus_id)