"""notifications API 路由"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app import crud, schemas
from app.database import get_db
from app.deps import require_current_user_id

router = APIRouter()


@router.get("/notifications", response_model=schemas.PaginatedNotificationList, tags=["notifications"])
def list_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_read: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(require_current_user_id),
):
    """List current user's notifications."""
    items = crud.notifications.get_multi_by_user(
        db, user_id=current_user_id, is_read=is_read, skip=skip, limit=limit
    )
    total = crud.notifications.count_by_user(db, user_id=current_user_id, is_read=is_read)
    return {"items": items, "total": total, "skip": skip, "limit": limit}


@router.get("/notifications/unread-count", tags=["notifications"])
def get_unread_count(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(require_current_user_id),
):
    """Get count of unread notifications."""
    count = crud.notifications.count_unread(db, user_id=current_user_id)
    return {"unread_count": count}


@router.get("/notifications/{notification_id}", response_model=schemas.Notification, tags=["notifications"])
def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(require_current_user_id),
):
    """Get a specific notification."""
    item = crud.notifications.get(db, id=notification_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    # Permission check: only owner can view
    if item.user_id != current_user_id:
        raise HTTPException(status_code=404, detail="Notification not found")
    return item


@router.patch("/notifications/{notification_id}", response_model=schemas.Notification, tags=["notifications"])
def update_notification(
    notification_id: int,
    body: schemas.NotificationUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(require_current_user_id),
):
    """Mark a notification as read."""
    item = crud.notifications.get(db, id=notification_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    # Permission check: only owner can update
    if item.user_id != current_user_id:
        raise HTTPException(status_code=404, detail="Notification not found")

    if body.is_read is not None and body.is_read and not item.is_read:
        item = crud.notifications.mark_as_read(db, db_obj=item)

    return item


@router.post("/notifications/read-all", status_code=status.HTTP_200_OK, tags=["notifications"])
def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(require_current_user_id),
):
    """Mark all notifications as read."""
    count = crud.notifications.mark_all_as_read(db, user_id=current_user_id)
    return {"marked_count": count}
