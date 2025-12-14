# backend/app/models.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship
from .database import Base


# --------------------------
# FLIGHT MODEL
# --------------------------
class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    flight_id = Column(String(50), unique=True, nullable=False, index=True)
    airline = Column(String(100), nullable=False)
    departure_city = Column(String(100), nullable=False)
    arrival_city = Column(String(100), nullable=False)
    base_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=func.now())

    bookings = relationship("Booking", back_populates="flight")

    # Dynamic pricing state (one-to-one)
    attempt_state = relationship("FlightAttempt", back_populates="flight", uselist=False)


# --------------------------
# USER MODEL (AUTH READY)
# --------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # login fields
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(200), unique=True, nullable=False, index=True)
    password_hash = Column(String(300), nullable=False)

    # optional fields
    full_name = Column(String(150), nullable=True)

    # wallet
    wallet_balance = Column(Float, nullable=False, default=50000.0)
    created_at = Column(DateTime, default=func.now())

    bookings = relationship("Booking", back_populates="user")


# --------------------------
# BOOKING MODEL
# --------------------------
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    pnr = Column(String(50), unique=True, nullable=False, index=True)
    passenger_name = Column(String(150), nullable=False)

    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    final_price = Column(Float, nullable=False)
    booking_time = Column(DateTime, default=func.now())

    flight = relationship("Flight", back_populates="bookings")
    user = relationship("User", back_populates="bookings")


# --------------------------
# FLIGHT ATTEMPT (Surge Engine)
# --------------------------
class FlightAttempt(Base):
    __tablename__ = "flight_attempts"

    id = Column(Integer, primary_key=True, index=True)
    flight_id = Column(Integer, ForeignKey("flights.id", ondelete="CASCADE"), nullable=False, unique=True)

    attempt_count = Column(Integer, default=0)
    first_attempt_at = Column(DateTime, nullable=True)
    surge_expires_at = Column(DateTime, nullable=True)

    flight = relationship("Flight", back_populates="attempt_state")
