# backend/app/utils/pricing.py

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .. import models
from ..config import settings


def compute_dynamic_price(db: Session, flight: models.Flight):
    """
    Public wrapper to compute surge pricing using rules:

    - Surge triggers when >=SURGE_ATTEMPTS attempts occur inside SURGE_WINDOW_MINUTES.
    - Surge lasts SURGE_DURATION_MINUTES (price = base_price * SURGE_MULTIPLIER).
    """
    now = datetime.utcnow()

    lookback = timedelta(minutes=settings.SURGE_DURATION_MINUTES)
    window = timedelta(minutes=settings.SURGE_WINDOW_MINUTES)

    attempts = (
        db.query(models.PricingAttempt.attempt_time)
        .filter(models.PricingAttempt.flight_id == flight.id)
        .filter(models.PricingAttempt.attempt_time >= now - lookback)
        .order_by(models.PricingAttempt.attempt_time.asc())
        .all()
    )

    attempt_times = [a[0] for a in attempts]

    trigger_time = _find_surge_trigger_time(
        attempt_times,
        threshold=settings.SURGE_ATTEMPTS,
        window_minutes=settings.SURGE_WINDOW_MINUTES
    )

    if trigger_time:
        expires_at = trigger_time + timedelta(minutes=settings.SURGE_DURATION_MINUTES)
        if now <= expires_at:
            return round(flight.base_price * settings.SURGE_MULTIPLIER, 2)

    return flight.base_price


def _find_surge_trigger_time(attempt_times, threshold: int, window_minutes: int):
    """
    Returns the timestamp when surge triggered or None.
    A surge triggers when threshold attempts occur within window_minutes.
    """
    if not attempt_times:
        return None

    window = timedelta(minutes=window_minutes)
    start = 0

    for end in range(len(attempt_times)):
        while attempt_times[end] - attempt_times[start] > window:
            start += 1

        if end - start + 1 >= threshold:
            # Trigger time is time of latest attempt in window
            return attempt_times[end]

    return None
