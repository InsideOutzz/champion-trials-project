from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(
    prefix="/buses",
    tags=["Buses"]
)


@router.post("/", response_model=schemas.BusResponse)
def add_bus(
    bus: schemas.BusCreate,
    db: Session = Depends(get_db)
):
    return crud.create_bus(db, bus)


@router.get("/", response_model=list[schemas.BusResponse])
def list_buses(db: Session = Depends(get_db)):
    return crud.get_buses(db)