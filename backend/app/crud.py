from sqlalchemy.orm import Session
from app import models, schemas


def create_bus(db: Session, bus: schemas.BusCreate):
    db_bus = models.Bus(**bus.model_dump())

    db.add(db_bus)
    db.commit()
    db.refresh(db_bus)

    return db_bus


def get_buses(db: Session):
    return db.query(models.Bus).all()


def create_report(db: Session, report: schemas.ReportCreate):
    db_report = models.CrowdReport(
        bus_id=report.bus_id,
        crowd_level=report.crowd_level
    )

    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    return db_report


def get_reports(db: Session, bus_id=None):
    query = db.query(models.CrowdReport)

    if bus_id is not None:
        query = query.filter(
            models.CrowdReport.bus_id == bus_id
        )

    return query.order_by(
        models.CrowdReport.reported_at.desc()
    ).all()