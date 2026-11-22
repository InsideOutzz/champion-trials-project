
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas, models
from app.auth.security import get_current_user
from app.models import User

router = APIRouter(
    prefix="/buses",
    tags=["Buses"]
)


@router.post("/", response_model=schemas.BusResponse)
def add_bus(
    bus: schemas.BusCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(models.Bus).filter(
        models.Bus.line_number == bus.line_number
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="This bus line already exists."
        )

    return crud.create_bus(db, bus)


@router.get("/", response_model=list[schemas.BusResponse])
def list_buses(db: Session = Depends(get_db)):
    return crud.get_buses(db)
