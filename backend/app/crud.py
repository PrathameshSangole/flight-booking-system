# backend/app/crud.py

from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from . import models
from .config import settings


# ---------------------------
# SURGE CONFIG
# ---------------------------
SURGE_ATTEMPTS = 3
SURGE_WINDOW_MIN = 5
SURGE_DURATION_MIN = 10
SURGE_MULTIPLIER = 1.10


# ============================================================
# INTERNAL SURGE ENGINE
# ============================================================
def _update_attempt_state(db: Session, flight: models.Flight):
    now = datetime.utcnow()
    state = flight.attempt_state

    # Create first attempt row
    if not state:
        state = models.FlightAttempt(
            flight_id=flight.id,
            attempt_count=1,
            first_attempt_at=now,
            surge_expires_at=None
        )
        db.add(state)
        db.commit()
        db.refresh(state)
        return state

    # Reset window
    if (state.first_attempt_at is None) or (
        now - state.first_attempt_at > timedelta(minutes=SURGE_WINDOW_MIN)
    ):
        state.first_attempt_at = now
        state.attempt_count = 1
        state.surge_expires_at = None
        db.commit()
        return state

    # Increment attempt
    state.attempt_count += 1

    # Trigger surge
    if state.attempt_count >= SURGE_ATTEMPTS:
        state.surge_expires_at = now + timedelta(minutes=SURGE_DURATION_MIN)

    db.commit()
    return state


def compute_dynamic_price(db: Session, flight: models.Flight):
    now = datetime.utcnow()
    state = flight.attempt_state

    if not state:
        return flight.base_price

    # Surge expired
    if state.surge_expires_at and now > state.surge_expires_at:
        state.first_attempt_at = None
        state.attempt_count = 0
        state.surge_expires_at = None
        db.commit()
        return flight.base_price

    # Surge active
    if state.surge_expires_at and now <= state.surge_expires_at:
        return round(flight.base_price * SURGE_MULTIPLIER, 2)

    return flight.base_price


# ============================================================
# FLIGHT CRUD
# ============================================================
def get_flights(db: Session, departure_city=None, arrival_city=None, limit=None):
    if limit is None:
        limit = settings.DEFAULT_PAGE_LIMIT

    query = db.query(models.Flight)

    if departure_city:
        query = query.filter(models.Flight.departure_city.ilike(f"%{departure_city}%"))

    if arrival_city:
        query = query.filter(models.Flight.arrival_city.ilike(f"%{arrival_city}%"))

    flights = query.limit(limit).all()

    # Return enriched data
    out = []
    for f in flights:
        price = compute_dynamic_price(db, f)
        out.append({
            "id": f.id,
            "flight_id": f.flight_id,
            "airline": f.airline,
            "departure_city": f.departure_city,
            "arrival_city": f.arrival_city,
            "base_price": f.base_price,
            "price": round(price, 2)
        })

    return out


def get_flight_by_id(db: Session, flight_id: int):
    return db.query(models.Flight).filter(models.Flight.id == flight_id).first()


# ============================================================
# CREATE BOOKING
# ============================================================
def create_booking(db: Session, passenger_name: str, flight_id: int, user_id: int = None, ip_address: str = None):
    flight = get_flight_by_id(db, flight_id)
    if not flight:
        raise ValueError("Flight not found")

    # update surge and compute price
    _update_attempt_state(db, flight)
    final_price = compute_dynamic_price(db, flight)

    # User wallet deduction
    if user_id:
        user = db.query(models.User).filter(models.User.id == user_id).with_for_update().first()
        if not user:
            raise ValueError("User not found")
        if user.wallet_balance < final_price:
            raise ValueError("Insufficient wallet balance")

        user.wallet_balance -= final_price
        db.commit()
        db.refresh(user)

    # Generate unique PNR
    def new_pnr():
        return f"PNR{random.randint(100000, 999999)}"

    pnr = new_pnr()
    while db.query(models.Booking).filter_by(pnr=pnr).first():
        pnr = new_pnr()

    booking = models.Booking(
        pnr=pnr,
        passenger_name=passenger_name,
        flight_id=flight.id,
        user_id=user_id,
        final_price=round(final_price, 2)
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


# ============================================================
# GET USER BOOKINGS
# IMPORTANT: RETURN ORM OBJECTS (NOT DICTS)
# ============================================================
def get_bookings(db: Session, user_id: int = None):
    query = db.query(models.Booking).order_by(models.Booking.booking_time.desc())

    if user_id:
        query = query.filter(models.Booking.user_id == user_id)

    bookings = query.all()

    # RETURN RAW ORM → FastAPI + Pydantic will serialize nested Flight automatically.
    return bookings


# ============================================================
# SEED SAMPLE FLIGHTS
# ============================================================
def seed_flights(db: Session):
    if db.query(models.Flight).count() > 0:
        return 0

    sample = [
        ("AI-101", "Air India", "Mumbai", "Delhi", 2500),
        ("AI-202", "Air India", "Delhi", "Bengaluru", 2600),
        ("6E-303", "IndiGo", "Mumbai", "Bengaluru", 2550),
        ("6E-404", "IndiGo", "Chennai", "Mumbai", 2400),
        ("UK-505", "Vistara", "Hyderabad", "Delhi", 2300),
    ]

    for s in sample:
        db.add(models.Flight(
            flight_id=s[0],
            airline=s[1],
            departure_city=s[2],
            arrival_city=s[3],
            base_price=s[4]
        ))

    db.commit()
    return len(sample)
