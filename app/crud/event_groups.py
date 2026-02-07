"""EventGroup CRUD — event:group relationship (team registration)"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.event_group import EventGroup


class CRUDEventGroup:
    def get(self, db: Session, *, id: int) -> Optional[EventGroup]:
        return db.query(EventGroup).filter(EventGroup.id == id).first()

    def get_by_category_and_group(self, db: Session, *, event_id: int, group_id: int) -> Optional[EventGroup]:
        return db.query(EventGroup).filter(
            EventGroup.event_id == event_id,
            EventGroup.group_id == group_id,
        ).first()

    def get_multi_by_category(self, db: Session, *, event_id: int) -> List[EventGroup]:
        return db.query(EventGroup).filter(
            EventGroup.event_id == event_id,
        ).all()

    def get_multi_by_group(self, db: Session, *, group_id: int) -> List[EventGroup]:
        return db.query(EventGroup).filter(
            EventGroup.group_id == group_id,
        ).all()

    def count_by_category(self, db: Session, *, event_id: int) -> int:
        """Count groups registered to a event."""
        return db.query(EventGroup).filter(
            EventGroup.event_id == event_id,
        ).count()

    def is_user_in_category(self, db: Session, *, event_id: int, user_id: int) -> bool:
        """Check if a user is already in any group registered to this event."""
        from app.models.member import Member
        return db.query(EventGroup).join(
            Member, EventGroup.group_id == Member.group_id,
        ).filter(
            EventGroup.event_id == event_id,
            Member.user_id == user_id,
            Member.status == "accepted",
        ).first() is not None

    def create(self, db: Session, *, event_id: int, group_id: int) -> EventGroup:
        obj = EventGroup(event_id=event_id, group_id=group_id)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def remove(self, db: Session, *, id: int) -> Optional[EventGroup]:
        obj = db.query(EventGroup).filter(EventGroup.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def remove_by_category_and_group(self, db: Session, *, event_id: int, group_id: int) -> Optional[EventGroup]:
        obj = self.get_by_category_and_group(db, event_id=event_id, group_id=group_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


    def remove_all_by_category(self, db: Session, *, event_id: int) -> int:
        count = db.query(EventGroup).filter(EventGroup.event_id == event_id).delete()
        db.commit()
        return count

    def remove_all_by_group(self, db: Session, *, group_id: int) -> int:
        count = db.query(EventGroup).filter(EventGroup.group_id == group_id).delete()
        db.commit()
        return count


event_groups = CRUDEventGroup()
