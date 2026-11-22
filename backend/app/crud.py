
from sqlalchemy.orm import Session
from app import models, schemas


# BUS CRUD

def create_bus(db: Session, bus: schemas.BusCreate):
    db_bus = models.Bus(**bus.model_dump())

    db.add(db_bus)
    db.commit()
    db.refresh(db_bus)

    return db_bus


def get_buses(db: Session):
    return db.query(models.Bus).order_by(
        models.Bus.line_number
    ).all()


def get_bus(db: Session, bus_id: int):
    return db.query(models.Bus).filter(
        models.Bus.id == bus_id
    ).first()


# REPORT CRUD

def create_report(
    db: Session,
    report: schemas.ReportCreate,
    user_id: int
):
    db_report = models.CrowdReport(
        bus_id=report.bus_id,
        crowd_level=models.CrowdLevel(report.crowd_level.value),
        user_id=user_id
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


def get_report(db: Session, report_id: int):
    return db.query(models.CrowdReport).filter(
        models.CrowdReport.id == report_id
    ).first()


def get_user_reports(db: Session, user_id: int):
    return db.query(models.CrowdReport).filter(
        models.CrowdReport.user_id == user_id
    ).order_by(
        models.CrowdReport.reported_at.desc()
    ).all()


def update_report(
    db: Session,
    report_id: int,
    crowd_level: schemas.CrowdLevel,
    user_id: int
):
    report = db.query(models.CrowdReport).filter(
        models.CrowdReport.id == report_id,
        models.CrowdReport.user_id == user_id
    ).first()

    if not report:
        return None

    report.crowd_level = models.CrowdLevel(crowd_level.value)

    db.commit()
    db.refresh(report)

    return report


def delete_report(
    db: Session,
    report_id: int,
    user_id: int
):
    report = db.query(models.CrowdReport).filter(
        models.CrowdReport.id == report_id,
        models.CrowdReport.user_id == user_id
    ).first()

    if not report:
        return False

    db.delete(report)
    db.commit()

    return True
