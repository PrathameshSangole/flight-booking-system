# backend/app/routers/flights.py

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas, crud, models
from ..database import get_db

router = APIRouter(prefix="/flights", tags=["flights"])


@router.get("", response_model=List[schemas.FlightOut])
def list_flights(
    departure_city: Optional[str] = None,
    arrival_city: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    List flights with optional search filters.
    Each flight returned includes the computed dynamic price.
    """
    try:
        flights = crud.get_flights(
            db,
            departure_city=departure_city,
            arrival_city=arrival_city
        )
        return flights
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not fetch flights: {str(e)}")


@router.post("/seed", status_code=status.HTTP_201_CREATED)
def seed_flights(db: Session = Depends(get_db)):
    """
    Seed default flights into the database.
    """
    try:
        count = crud.seed_flights(db)
        return {"seeded": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not seed flights: {str(e)}")


@router.get("/{flight_id}", response_model=schemas.FlightOut)
def get_flight(flight_id: int, db: Session = Depends(get_db)):
    """
    Fetch a single flight by its DB ID.
    Dynamic price is recalculated every time.
    """
    flight = crud.get_flight_by_id(db, flight_id)
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    # Compute surge-adjusted price
    try:
        price = crud.compute_dynamic_price(db, flight)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pricing error: {str(e)}")

    return {
        "id": flight.id,
        "flight_id": flight.flight_id,
        "airline": flight.airline,
        "departure_city": flight.departure_city,
        "arrival_city": flight.arrival_city,
        "base_price": flight.base_price,
        "price": round(price, 2),
    }
