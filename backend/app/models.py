from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum
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

    reports = relationship(
        "CrowdReport",
        back_populates="bus"
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    reports = relationship(
        "CrowdReport",
        back_populates="user"
    )


class CrowdReport(Base):
    __tablename__ = "crowd_reports"

    id = Column(Integer, primary_key=True, index=True)

    bus_id = Column(
        Integer,
        ForeignKey("buses.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    crowd_level = Column(
        Enum(CrowdLevel),
        nullable=False
    )

    reported_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    bus = relationship(
        "Bus",
        back_populates="reports"
    )

    user = relationship(
        "User",
        back_populates="reports"
    )


class DeveloperKey(Base):
    __tablename__ = "developer_keys"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    key_hash = Column(
        String(64),
        nullable=False,
        unique=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
