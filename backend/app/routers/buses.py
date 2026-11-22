from fastapi import APIRouter, Depends, HTTPException
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
    existing = db.query(crud.models.Bus).filter(
        crud.models.Bus.line_number == bus.line_number
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


@router.put("/{bus_id}", response_model=schemas.BusResponse)
def edit_bus(
    bus_id: int,
    bus: schemas.BusUpdate,
    db: Session = Depends(get_db)
):
    updated = crud.update_bus(db, bus_id, bus)

    if not updated:
        raise HTTPException(status_code=404, detail="Bus not found")

    return updated


@router.delete("/{bus_id}")
def remove_bus(
    bus_id: int,
    db: Session = Depends(get_db)
):
    deleted = crud.delete_bus(db, bus_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Bus not found")

    return {"message": "Bus deleted successfully"}
