"""auth API 路由

Temporary implementation using header-based auth.
TODO: Replace with proper JWT authentication in Phase 4.4.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app import crud
from app.database import get_db
from app.deps import require_current_user_id

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    user_id: int
    username: str
    role: str
    # TODO: Add access_token and refresh_token when JWT is implemented


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    refresh_token: str


@router.post("/auth/login", response_model=LoginResponse, tags=["auth"])
def login(
    body: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Authenticate user and return session info.

    NOTE: This is a temporary implementation. Password verification is NOT implemented.
    Use this endpoint to get the user_id for the X-User-Id header.

    TODO: Implement proper password hashing and JWT token generation.
    """
    user = crud.users.get_by_username(db, username=body.username)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # TODO: Verify password hash
    # if not verify_password(body.password, user.password_hash):
    #     raise HTTPException(status_code=401, detail="Invalid username or password")

    return LoginResponse(
        user_id=user.id,
        username=user.username,
        role=user.role,
    )


@router.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT, tags=["auth"])
def logout(
    current_user_id: int = Depends(require_current_user_id),
):
    """
    Logout current user.

    NOTE: This is a placeholder. With header-based auth, there's no session to invalidate.

    TODO: Implement token blacklisting when JWT is implemented.
    """
    # TODO: Add token to blacklist
    return None


@router.post("/auth/refresh", response_model=RefreshResponse, tags=["auth"])
def refresh_token(
    body: RefreshRequest,
    db: Session = Depends(get_db),
):
    """
    Refresh access token.

    NOTE: This is a placeholder. Returns dummy tokens.

    TODO: Implement proper token refresh when JWT is implemented.
    """
    # TODO: Verify refresh token and issue new tokens
    raise HTTPException(
        status_code=501,
        detail="Token refresh not implemented. Use X-User-Id header for authentication."
    )
