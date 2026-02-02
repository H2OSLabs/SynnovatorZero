"""共享依赖

认证模式:
- MOCK_AUTH=true (默认): 开发模式，使用 X-User-Id header 或自动创建 mock 用户
- MOCK_AUTH=false: 生产模式，需要真实的 OAuth/JWT 认证 (未实现)
"""
from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.core.config import settings


def _get_or_create_mock_user(db: Session) -> int:
    """在 mock 模式下获取或创建默认用户。"""
    from app import crud
    from app.schemas.user import UserCreate

    # 尝试获取已存在的 mock 用户
    user = crud.users.get(db, id=settings.mock_user_id)
    if user:
        return user.id

    # 创建 mock 用户
    mock_user_data = UserCreate(
        username=f"mock_user_{settings.mock_user_id}",
        email=f"mock_user_{settings.mock_user_id}@example.com",
        role=settings.mock_user_role,
    )
    mock_user = crud.users.create(db, obj_in=mock_user_data)
    return mock_user.id


def get_current_user_id(
    x_user_id: Optional[int] = Header(None),
    db: Session = Depends(get_db),
) -> Optional[int]:
    """从 X-User-Id header 获取当前用户 ID。

    Mock 模式下:
    - 如果提供了 X-User-Id，验证用户存在后返回
    - 如果未提供，返回 None (用于可选认证的端点)

    生产模式下:
    - TODO: 从 JWT token 解析用户 ID
    """
    if settings.mock_auth:
        if x_user_id is not None:
            from app import crud
            user = crud.users.get(db, id=x_user_id)
            if user:
                return user.id
        return None
    else:
        # TODO: 实现 JWT 解析
        raise HTTPException(status_code=501, detail="OAuth authentication not implemented")


def require_current_user_id(
    x_user_id: Optional[int] = Header(None),
    db: Session = Depends(get_db),
) -> int:
    """要求必须有当前用户 ID。

    Mock 模式下:
    - 如果提供了 X-User-Id，验证用户存在后返回
    - 如果未提供，自动创建并返回 mock 用户

    生产模式下:
    - TODO: 从 JWT token 解析用户 ID，token 无效则返回 401
    """
    if settings.mock_auth:
        if x_user_id is not None:
            from app import crud
            user = crud.users.get(db, id=x_user_id)
            if user:
                return user.id
            # 用户 ID 无效，但在 mock 模式下我们仍然接受它
            # 这允许测试代码使用任意 ID
            raise HTTPException(status_code=401, detail="User not found")

        # 未提供 header，自动创建 mock 用户
        return _get_or_create_mock_user(db)
    else:
        # TODO: 实现 JWT 解析
        if x_user_id is None:
            raise HTTPException(status_code=401, detail="Authentication required")
        raise HTTPException(status_code=501, detail="OAuth authentication not implemented")


def require_role(*allowed_roles: str):
    """Factory: return a dependency that checks the current user has one of the allowed roles."""
    def _check_role(
        x_user_id: Optional[int] = Header(None),
        db: Session = Depends(get_db),
    ) -> int:
        if settings.mock_auth:
            if x_user_id is None:
                # 自动创建 mock 用户
                user_id = _get_or_create_mock_user(db)
            else:
                user_id = x_user_id

            from app import crud
            user = crud.users.get(db, id=user_id)
            if user is None:
                raise HTTPException(status_code=401, detail="User not found")
            if user.role not in allowed_roles:
                raise HTTPException(
                    status_code=403,
                    detail=f"Role '{user.role}' not allowed. Requires: {', '.join(allowed_roles)}"
                )
            return user_id
        else:
            # TODO: 实现 JWT 解析
            if x_user_id is None:
                raise HTTPException(status_code=401, detail="Authentication required")
            raise HTTPException(status_code=501, detail="OAuth authentication not implemented")

    return _check_role


def is_mock_auth_enabled() -> bool:
    """检查是否启用了 mock 认证模式。"""
    return settings.mock_auth
