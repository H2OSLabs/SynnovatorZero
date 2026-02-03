"""admin API 路由"""
from datetime import datetime, timezone
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.deps import require_role
from app.models.post import Post
from app.models.user import User

router = APIRouter()

# Admin role dependency
require_admin = require_role("admin")

# Valid post statuses
VALID_POST_STATUSES = {"draft", "pending_review", "published", "rejected"}

# Valid user roles
VALID_USER_ROLES = {"participant", "organizer", "admin"}


@router.post("/admin/posts/batch-delete", response_model=schemas.BatchResult, tags=["admin"])
def batch_delete_posts(
    body: schemas.BatchIds,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(require_admin),
):
    """Batch soft-delete posts (admin only)"""
    success_count = 0
    failed_ids: List[int] = []
    errors: Dict[str, str] = {}

    for post_id in body.ids:
        post = db.query(Post).filter(
            Post.id == post_id,
            Post.deleted_at.is_(None)
        ).first()

        if not post:
            failed_ids.append(post_id)
            errors[str(post_id)] = "Post not found or already deleted"
            continue

        post.deleted_at = datetime.now(timezone.utc)
        success_count += 1

    db.commit()

    return {
        "success_count": success_count,
        "failed_count": len(failed_ids),
        "failed_ids": failed_ids if failed_ids else None,
        "errors": errors if errors else None,
    }


@router.post("/admin/posts/batch-update-status", response_model=schemas.BatchResult, tags=["admin"])
def batch_update_post_status(
    body: schemas.BatchStatusUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(require_admin),
):
    """Batch update post status (admin only)"""
    if body.status not in VALID_POST_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid status. Must be one of: {', '.join(VALID_POST_STATUSES)}"
        )

    success_count = 0
    failed_ids: List[int] = []
    errors: Dict[str, str] = {}

    for post_id in body.ids:
        post = db.query(Post).filter(
            Post.id == post_id,
            Post.deleted_at.is_(None)
        ).first()

        if not post:
            failed_ids.append(post_id)
            errors[str(post_id)] = "Post not found or deleted"
            continue

        post.status = body.status
        success_count += 1

    db.commit()

    return {
        "success_count": success_count,
        "failed_count": len(failed_ids),
        "failed_ids": failed_ids if failed_ids else None,
        "errors": errors if errors else None,
    }


@router.post("/admin/users/batch-update-roles", response_model=schemas.BatchResult, tags=["admin"])
def batch_update_user_roles(
    body: schemas.BatchRoleUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(require_admin),
):
    """Batch update user roles (admin only)"""
    if body.role not in VALID_USER_ROLES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid role. Must be one of: {', '.join(VALID_USER_ROLES)}"
        )

    success_count = 0
    failed_ids: List[int] = []
    errors: Dict[str, str] = {}

    for user_id in body.ids:
        user = db.query(User).filter(
            User.id == user_id,
            User.deleted_at.is_(None)
        ).first()

        if not user:
            failed_ids.append(user_id)
            errors[str(user_id)] = "User not found or deleted"
            continue

        user.role = body.role
        success_count += 1

    db.commit()

    return {
        "success_count": success_count,
        "failed_count": len(failed_ids),
        "failed_ids": failed_ids if failed_ids else None,
        "errors": errors if errors else None,
    }
