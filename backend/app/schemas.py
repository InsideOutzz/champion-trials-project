from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum


class CrowdLevel(str, Enum):
    empty = "empty"
    low = "low"
    medium = "medium"
    high = "high"
    full = "full"


class BusCreate(BaseModel):
    line_number: str
    route_name: str


class BusResponse(BaseModel):
    id: int
    line_number: str
    route_name: str

    model_config = ConfigDict(from_attributes=True)


class ReportCreate(BaseModel):
    bus_id: int
    crowd_level: CrowdLevel


class ReportResponse(BaseModel):
    id: int
    bus_id: int
    crowd_level: CrowdLevel
    reported_at: datetime

    model_config = ConfigDict(from_attributes=True)