"""Authentication routes."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.auth import (
    JWT_EXPIRES_SECONDS,
    create_access_token,
    get_current_user,
    verify_password,
)
from app.db import connect

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: str
    email: str
    role: str
    hedera_account_id: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserOut


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest) -> TokenResponse:
    email = body.email.strip().lower()
    with connect() as conn:
        row = conn.execute(
            "SELECT id, email, password_hash, role, hedera_account_id "
            "FROM users WHERE email = %s",
            (email,),
        ).fetchone()
    if row is None or not verify_password(body.password, row[2]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    user = {
        "id": str(row[0]),
        "email": row[1],
        "role": row[3],
        "hedera_account_id": row[4],
    }
    return TokenResponse(
        access_token=create_access_token(user),
        expires_in=JWT_EXPIRES_SECONDS,
        user=UserOut(**user),
    )


@router.get("/me", response_model=UserOut)
def me(user: dict = Depends(get_current_user)) -> UserOut:
    return UserOut(**user)
