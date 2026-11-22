from sqlalchemy import (
    Column, Integer, String, DateTime,
    ForeignKey, Enum
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class CrowdLevel(str, enum.Enum):
    empty = "empty"
    low = "low"
    medium = "medium"
    high = "high"
    full = "full"


class Bus(Base):
    __tablename__ = "buses"

    id = Column(Integer, primary_key=True, index=True)
    line_number = Column(String, unique=True, nullable=False)
    route_name = Column(String, nullable=False)

    reports = relationship("CrowdReport", back_populates="bus")


class CrowdReport(Base):
    __tablename__ = "crowd_reports"

    id = Column(Integer, primary_key=True, index=True)

    bus_id = Column(Integer, ForeignKey("buses.id"))
    crowd_level = Column(Enum(CrowdLevel), nullable=False)

    reported_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    bus = relationship("Bus", back_populates="reports")