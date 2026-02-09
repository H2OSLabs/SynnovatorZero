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
from app.schemas.user import UserCreate

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: Optional[str] = None  # 可选，兼容旧前端


class LoginResponse(BaseModel):
    user_id: int
    username: str
    role: str
    # TODO: Add access_token and refresh_token when JWT is implemented


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str = "participant"  # participant 或 organizer


class RegisterResponse(BaseModel):
    user_id: int
    username: str
    role: str


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    refresh_token: str


@router.post("/auth/register", response_model=RegisterResponse, tags=["auth"])
def register(
    body: RegisterRequest,
    db: Session = Depends(get_db),
):
    """
    Register a new user.

    角色只能是 participant 或 organizer。
    """
    # 验证角色
    if body.role not in ("participant", "organizer"):
        raise HTTPException(status_code=400, detail="Role must be 'participant' or 'organizer'")

    # 检查用户名是否已存在
    existing_user = crud.users.get_by_username(db, username=body.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # 检查邮箱是否已存在
    existing_email = db.query(crud.users.model).filter(
        crud.users.model.email == body.email,
        crud.users.model.deleted_at.is_(None)
    ).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    # 创建用户
    user_create = UserCreate(
        username=body.username,
        email=body.email,
        password=body.password,
        role=body.role,
    )
    user = crud.users.create(db, obj_in=user_create)

    return RegisterResponse(
        user_id=user.id,
        username=user.username,
        role=user.role,
    )


@router.post("/auth/login", response_model=LoginResponse, tags=["auth"])
def login(
    body: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Authenticate user and return session info.

    密码验证逻辑（明文比对，仅开发用）：
    - 如果用户有密码且请求提供了密码：必须匹配
    - 如果用户没有密码：跳过验证（兼容旧数据）
    """
    user = crud.users.get_by_username(db, username=body.username)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # 密码验证（明文比对）
    if user.password:
        if not body.password or body.password != user.password:
            raise HTTPException(status_code=401, detail="Invalid username or password")

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
