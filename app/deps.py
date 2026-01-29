"""共享依赖"""
from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db


def get_current_user_id(x_user_id: Optional[int] = Header(None)) -> Optional[int]:
    """从 X-User-Id header 获取当前用户 ID (临时方案，后续替换为 JWT auth)"""
    return x_user_id


def require_current_user_id(x_user_id: Optional[int] = Header(None)) -> int:
    """要求必须有当前用户 ID"""
    if x_user_id is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return x_user_id


def require_role(*allowed_roles: str):
    """Factory: return a dependency that checks the current user has one of the allowed roles."""
    def _check_role(
        x_user_id: Optional[int] = Header(None),
        db: Session = Depends(get_db),
    ) -> int:
        if x_user_id is None:
            raise HTTPException(status_code=401, detail="Authentication required")
        from app import crud
        user = crud.users.get(db, id=x_user_id)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        if user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail=f"Role '{user.role}' not allowed. Requires: {', '.join(allowed_roles)}")
        return x_user_id
    return _check_role
