"""admin API 路由"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.deps import require_role

router = APIRouter()

# Admin role dependency
require_admin = require_role("admin")


@router.delete("/admin/posts", response_model=schemas.BatchResult, tags=["admin"])
def batch_delete_posts(
    body: schemas.BatchIds,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(require_admin),
):
    # TODO: Implement batch delete
    return {"success_count": 0, "failed_count": 0}


@router.patch("/admin/posts/status", response_model=schemas.BatchResult, tags=["admin"])
def batch_update_post_status(
    body: schemas.BatchStatusUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(require_admin),
):
    # TODO: Implement batch status update
    return {"success_count": 0, "failed_count": 0}


@router.patch("/admin/users/role", response_model=schemas.BatchResult, tags=["admin"])
def batch_update_user_roles(
    body: schemas.BatchRoleUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(require_admin),
):
    # TODO: Implement batch role update
    return {"success_count": 0, "failed_count": 0}
