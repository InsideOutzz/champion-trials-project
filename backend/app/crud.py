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
    return db.query(models.Bus).all()


def get_bus(db: Session, bus_id: int):
    return db.query(models.Bus).filter(
        models.Bus.id == bus_id
    ).first()


def update_bus(db: Session, bus_id: int, bus_data: schemas.BusUpdate):
    db_bus = get_bus(db, bus_id)

    if db_bus:
        db_bus.line_number = bus_data.line_number
        db_bus.route_name = bus_data.route_name

        db.commit()
        db.refresh(db_bus)

    return db_bus


def delete_bus(db: Session, bus_id: int):
    db_bus = get_bus(db, bus_id)

    if db_bus:
        db.delete(db_bus)
        db.commit()
        return True

    return False


# REPORT CRUD

def create_report(db: Session, report: schemas.ReportCreate, user_id: int):
    db_report = models.CrowdReport(
        bus_id=report.bus_id,
        crowd_level=report.crowd_level,
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


def update_report(
    db: Session,
    report_id: int,
    crowd_level: schemas.CrowdLevel
):
    report = get_report(db, report_id)

    if report:
        report.crowd_level = crowd_level
        db.commit()
        db.refresh(report)

    return report


def delete_report(db: Session, report_id: int):
    report = get_report(db, report_id)

    if report:
        db.delete(report)
        db.commit()
        return True

    return False