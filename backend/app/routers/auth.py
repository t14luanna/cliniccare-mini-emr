import sqlite3

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import create_access_token, get_current_doctor, verify_password
from app.database import get_db
from app.schemas import Doctor, LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: sqlite3.Connection = Depends(get_db)):
    row = db.execute(
        "SELECT username, full_name, password_hash FROM doctor WHERE username = ?",
        (payload.username,),
    ).fetchone()

    # don't reveal if it's the username or the password
    if row is None or not verify_password(payload.password, row["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return {
        "access_token": create_access_token(row["username"]),
        "doctor": {"username": row["username"], "full_name": row["full_name"]},
    }


@router.get("/me", response_model=Doctor)
def me(doctor: dict = Depends(get_current_doctor)):
    return doctor
