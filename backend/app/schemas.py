# backend/app/schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ======================================================
# FLIGHT SCHEMAS
# ======================================================

class FlightBase(BaseModel):
    flight_id: str
    airline: str
    departure_city: str
    arrival_city: str
    base_price: float


class FlightCreate(FlightBase):
    pass


class FlightOut(BaseModel):
    id: int
    flight_id: str
    airline: str
    departure_city: str
    arrival_city: str
    base_price: float
    price: float  # dynamic price

    class Config:
        from_attributes = True  # REQUIRED for ORM → Pydantic v2


# ======================================================
# USER SCHEMAS (AUTH)
# ======================================================

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str]
    wallet_balance: float
    created_at: datetime

    class Config:
        from_attributes = True


# ======================================================
# BOOKING SCHEMAS
# ======================================================

class BookingCreate(BaseModel):
    user_id: Optional[int] = None
    passenger_name: str
    flight_id: int


class BookingOut(BaseModel):
    id: int
    pnr: str
    passenger_name: str
    flight_id: int
    final_price: float
    booking_time: datetime
    user_id: Optional[int] = None

    flight: Optional[FlightOut] = None  # nested flight

    class Config:
        from_attributes = True


# ======================================================
# OPTIONAL — Pricing Attempt
# ======================================================

class PricingAttemptCreate(BaseModel):
    flight_id: int
    ip_address: Optional[str] = None
