# backend/app/routers/bookings.py

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from .. import schemas, crud, models
from ..database import get_db

router = APIRouter(prefix="/bookings", tags=["bookings"])


# ============================================================
# Utility → Inject price into nested flight
# ============================================================
def attach_price(booking: models.Booking):
    """Ensures booking.flight always contains price field."""
    if booking.flight:
        booking.flight.price = booking.flight.base_price  # simple pricing logic
    return booking


# ============================================================
# CREATE BOOKING (AUTH REQUIRED)
# ============================================================
@router.post("", response_model=schemas.BookingOut, status_code=status.HTTP_201_CREATED)
def create_booking(payload: schemas.BookingCreate, request: Request, db: Session = Depends(get_db)):
    """
    Rules:
    - user_id is REQUIRED
    - user must exist
    """

    if not payload.user_id:
        raise HTTPException(status_code=401, detail="Login required to book a flight")

    user = db.query(models.User).filter(models.User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user. Please login again.")

    ip = request.client.host if request.client else None

    try:
        booking = crud.create_booking(
            db=db,
            passenger_name=payload.passenger_name,
            flight_id=payload.flight_id,
            user_id=payload.user_id,
            ip_address=ip,
        )

        return attach_price(booking)

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Booking failed: {str(e)}")


# ============================================================
# LIST BOOKINGS (AUTH REQUIRED)
# ============================================================
@router.get("", response_model=List[schemas.BookingOut])
def list_bookings(user_id: Optional[int] = None, db: Session = Depends(get_db)):

    if not user_id:
        raise HTTPException(status_code=401, detail="Login required to view bookings")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")

    try:
        bookings = crud.get_bookings(db, user_id=user_id)

        # attach price to each booking
        return [attach_price(b) for b in bookings]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not fetch bookings: {str(e)}")


# ============================================================
# DOWNLOAD TICKET (USER CAN ONLY DOWNLOAD OWN TICKET)
# ============================================================
@router.get("/ticket/{pnr}")
def download_ticket(pnr: str, user_id: int, db: Session = Depends(get_db)):

    if not user_id:
        raise HTTPException(status_code=401, detail="Login required")

    booking = db.query(models.Booking).filter(models.Booking.pnr == pnr).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    try:
        from ..utils.pdf_generator import generate_ticket_pdf

        pdf_path = generate_ticket_pdf(booking=booking, flight=booking.flight)
        return FileResponse(pdf_path, filename=f"{pnr}.pdf", media_type="application/pdf")

    except ImportError:
        raise HTTPException(
            status_code=501,
            detail="PDF generator missing. Implement backend/app/utils/pdf_generator.py",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not generate ticket: {str(e)}")
