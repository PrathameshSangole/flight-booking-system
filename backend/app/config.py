# backend/app/config.py
import os

class SimpleSettings:
    # -----------------------------
    # DATABASE SETTINGS
    # -----------------------------
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_NAME: str = os.getenv("DB_NAME", "flight_booking_db")

    # -----------------------------
    # WALLET SETTINGS
    # -----------------------------
    DEFAULT_WALLET_BALANCE: float = float(
        os.getenv("DEFAULT_WALLET_BALANCE", 50000.0)
    )

    # -----------------------------
    # DYNAMIC PRICING SETTINGS
    # -----------------------------
    SURGE_ATTEMPTS: int = int(os.getenv("SURGE_ATTEMPTS", 3))
    SURGE_WINDOW_MINUTES: int = int(os.getenv("SURGE_WINDOW_MINUTES", 5))
    SURGE_DURATION_MINUTES: int = int(os.getenv("SURGE_DURATION_MINUTES", 10))
    SURGE_MULTIPLIER: float = float(os.getenv("SURGE_MULTIPLIER", 1.10))

    # -----------------------------
    # PAGE LIMITING
    # -----------------------------
    DEFAULT_PAGE_LIMIT: int = int(os.getenv("DEFAULT_PAGE_LIMIT", 10))

    # -----------------------------
    # SESSION AUTHENTICATION
    # -----------------------------
    SESSION_SECRET_KEY: str = os.getenv(
        "SESSION_SECRET_KEY",
        "super-secret-session-key-change-this"
    )

    # Name of the cookie stored in frontend browser
    SESSION_COOKIE_NAME: str = os.getenv(
        "SESSION_COOKIE_NAME", "flight_app_session"
    )

# Export the settings instance
settings = SimpleSettings()
