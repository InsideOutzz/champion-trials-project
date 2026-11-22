from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.analytics import (
    generate_heatmap,
    get_quietest_times
)

router = APIRouter(
    prefix="/heatmap",
    tags=["Heatmap Analytics"]
)


@router.get("/")
def get_heatmap(db: Session = Depends(get_db)):
    return generate_heatmap(db)


@router.get("/quietest")
def quietest_times(db: Session = Depends(get_db)):
    return get_quietest_times(db)