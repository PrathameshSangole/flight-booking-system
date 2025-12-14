# backend/app/main.py
import os
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .database import engine, Base, get_db
from . import models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(title="Flight Booking API - FastAPI + MySQL")

# Routers
from .routers import flights, bookings, users
app.include_router(flights.router)
app.include_router(bookings.router)
app.include_router(users.router)


# ---------------------------------------------------
# CORS CONFIG  (Fix for "No Access-Control-Allow-Origin")
# ---------------------------------------------------
origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # IMPORTANT: allow all — solves CORS error
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------
# STARTUP → Create tables & seed demo user + flights
# ---------------------------------------------------
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

    db = next(get_db())
    try:
        # ----------------------------
        # DEMO USER
        # ----------------------------
        demo_username = os.getenv("DEMO_USERNAME", "demo_user")

        user = db.query(models.User).filter_by(username=demo_username).first()

        if not user:
            user = models.User(
                username=demo_username,
                email="demo@example.com",
                password_hash=pwd_context.hash("demo123"),
                full_name="Demo User",
                wallet_balance=50000.0,
            )
            db.add(user)
            db.commit()

        # ----------------------------
        # SEED FLIGHTS
        # ----------------------------
        if db.query(models.Flight).count() == 0:
            seed_flights = [
                ("AI-101", "Air India", "Mumbai", "Delhi", random.uniform(2000, 3000)),
                ("AI-202", "Air India", "Delhi", "Bengaluru", random.uniform(2000, 3000)),
                ("6E-303", "IndiGo", "Mumbai", "Bengaluru", random.uniform(2000, 3000)),
                ("6E-404", "IndiGo", "Chennai", "Mumbai", random.uniform(2000, 3000)),
                ("UK-505", "Vistara", "Hyderabad", "Delhi", random.uniform(2000, 3000)),
                ("UK-606", "Vistara", "Mumbai", "Kolkata", random.uniform(2000, 3000)),
                ("G8-707", "GoAir", "Pune", "Ahmedabad", random.uniform(2000, 3000)),
                ("SG-808", "SpiceJet", "Chennai", "Kochi", random.uniform(2000, 3000)),
                ("AI-909", "Air India", "Jaipur", "Delhi", random.uniform(2000, 3000)),
                ("6E-110", "IndiGo", "Delhi", "Goa", random.uniform(2000, 3000)),
                ("UK-211", "Vistara", "Bengaluru", "Hyderabad", random.uniform(2000, 3000)),
                ("G8-312", "GoAir", "Kolkata", "Pune", random.uniform(2000, 3000)),
            ]

            for f in seed_flights:
                db.add(
                    models.Flight(
                        flight_id=f[0],
                        airline=f[1],
                        departure_city=f[2],
                        arrival_city=f[3],
                        base_price=round(f[4], 2),
                    )
                )
            db.commit()

    finally:
        db.close()


# --------------------------------------------------------------------
# IMPORTANT: REMOVE OLD ENDPOINTS
#          (React must use routers, not duplicates)
# --------------------------------------------------------------------
# ❌ REMOVE:
#   /flights  (duplicate)
#   /book     (old, no surge)
#   /bookings (duplicate)
#
# These caused React to hit the wrong route → Network error.
#
# NOTHING BELOW THIS LINE.
