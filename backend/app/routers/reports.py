
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas
from app.auth.security import get_current_user
from app.models import User

router = APIRouter(
    prefix="/reports",
    tags=["Crowd Reports"]
)


# SUBMIT REPORT
@router.post("/", response_model=schemas.ReportResponse)
def submit_report(
    report: schemas.ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bus = crud.get_bus(db, report.bus_id)

    if not bus:
        raise HTTPException(
            status_code=404,
            detail="Bus line not found"
        )

    return crud.create_report(db, report, current_user.id)


# VIEW ALL REPORTS
@router.get("/", response_model=list[schemas.ReportResponse])
def list_reports(
    bus_id: int = None,
    db: Session = Depends(get_db)
):
    return crud.get_reports(db, bus_id)


# VIEW MY REPORTS
@router.get("/my", response_model=list[schemas.ReportResponse])
def list_my_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.get_user_reports(db, current_user.id)


# EDIT MY REPORT
@router.put("/{report_id}", response_model=schemas.ReportResponse)
def edit_report(
    report_id: int,
    report_data: schemas.ReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_report = crud.update_report(
        db,
        report_id,
        report_data.crowd_level,
        current_user.id
    )

    if not updated_report:
        raise HTTPException(
            status_code=404,
            detail="Report not found or you do not own this report"
        )

    return updated_report


# DELETE MY REPORT
@router.delete("/{report_id}")
def remove_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = crud.delete_report(
        db,
        report_id,
        current_user.id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Report not found or you do not own this report"
        )

    return {
        "message": "Report deleted successfully"
    }
