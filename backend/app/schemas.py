
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime
from enum import Enum


class CrowdLevel(str, Enum):
    empty = "empty"
    low = "low"
    medium = "medium"
    high = "high"
    full = "full"


# BUS SCHEMAS

class BusCreate(BaseModel):
    line_number: str = Field(min_length=1, max_length=20)
    route_name: str = Field(min_length=2, max_length=150)


class BusUpdate(BaseModel):
    line_number: str = Field(min_length=1, max_length=20)
    route_name: str = Field(min_length=2, max_length=150)


class BusResponse(BaseModel):
    id: int
    line_number: str
    route_name: str

    model_config = ConfigDict(from_attributes=True)


# REPORT SCHEMAS

class ReportCreate(BaseModel):
    bus_id: int
    crowd_level: CrowdLevel


class ReportUpdate(BaseModel):
    crowd_level: CrowdLevel


class ReportResponse(BaseModel):
    id: int
    bus_id: int
    crowd_level: CrowdLevel
    reported_at: datetime

    model_config = ConfigDict(from_attributes=True)


# USER SCHEMAS

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
