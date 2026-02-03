"""Notification CRUD operations."""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate


class CRUDNotification:
    def get(self, db: Session, *, id: int) -> Optional[Notification]:
        return db.query(Notification).filter(
            Notification.id == id,
        ).first()

    def get_multi_by_user(
        self,
        db: Session,
        *,
        user_id: int,
        is_read: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Notification]:
        query = db.query(Notification).filter(Notification.user_id == user_id)
        if is_read is not None:
            query = query.filter(Notification.is_read == is_read)
        return query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()

    def count_by_user(
        self,
        db: Session,
        *,
        user_id: int,
        is_read: Optional[bool] = None,
    ) -> int:
        query = db.query(Notification).filter(Notification.user_id == user_id)
        if is_read is not None:
            query = query.filter(Notification.is_read == is_read)
        return query.count()

    def count_unread(self, db: Session, *, user_id: int) -> int:
        return self.count_by_user(db, user_id=user_id, is_read=False)

    def create(
        self,
        db: Session,
        *,
        user_id: int,
        type: str,
        content: str,
        title: Optional[str] = None,
        related_url: Optional[str] = None,
        actor_id: Optional[int] = None,
    ) -> Notification:
        obj = Notification(
            user_id=user_id,
            type=type,
            content=content,
            title=title,
            related_url=related_url,
            actor_id=actor_id,
            is_read=False,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def mark_as_read(self, db: Session, *, db_obj: Notification) -> Notification:
        db_obj.is_read = True
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def mark_all_as_read(self, db: Session, *, user_id: int) -> int:
        """Mark all notifications for a user as read. Returns count updated."""
        count = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False,
        ).update({"is_read": True})
        db.commit()
        return count

    def remove(self, db: Session, *, id: int) -> Optional[Notification]:
        obj = db.query(Notification).filter(Notification.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj


notifications = CRUDNotification()
