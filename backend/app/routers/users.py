# backend/app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext

from .. import schemas, models
from ..database import get_db

router = APIRouter(prefix="/users", tags=["users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Utility: hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Utility: verify password
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ======================================================
# REGISTER USER
# ======================================================

@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register_user(payload: schemas.UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user.
    Fields: username, email, full_name, password
    """
    # check if username exists
    if db.query(models.User).filter(models.User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    # check if email exists
    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(
        username=payload.username,
        email=payload.email,
        full_name=payload.full_name,
        password_hash=hash_password(payload.password),
        wallet_balance=50000.0,   # default wallet
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ======================================================
# LOGIN USER (NO TOKENS)
# ======================================================

@router.post("/login", response_model=schemas.UserOut)
def login_user(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Simple login:
    - verify email
    - verify password
    - return user object (no JWT token)
    """
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect password")

    return user


# ======================================================
# GET USER BY ID
# ======================================================

@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ======================================================
# LIST USERS
# ======================================================

@router.get("", response_model=List[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.created_at.desc()).all()
    return users


# ======================================================
# WALLET TOP-UP (requires user ID)
# ======================================================

@router.post("/{user_id}/topup")
def top_up_wallet(user_id: int, amount: float, db: Session = Depends(get_db)):
    """
    Add balance to user wallet.
    """
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be > 0")

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.wallet_balance += amount
    db.commit()
    db.refresh(user)

    return {
        "message": "Wallet updated",
        "user_id": user.id,
        "new_balance": user.wallet_balance,
    }
