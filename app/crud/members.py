"""Member CRUD — group:user relationship with approval flow"""
from datetime import datetime, timezone
from typing import Any, List, Optional

from sqlalchemy.orm import Session

from app.models.member import Member


class CRUDMember:
    def get(self, db: Session, *, id: int) -> Optional[Member]:
        return db.query(Member).filter(Member.id == id).first()

    def get_by_group_and_user(self, db: Session, *, group_id: int, user_id: int) -> Optional[Member]:
        return db.query(Member).filter(
            Member.group_id == group_id,
            Member.user_id == user_id,
        ).first()

    def get_multi_by_group(
        self, db: Session, *, group_id: int, status: Optional[str] = None,
        skip: int = 0, limit: int = 100,
    ) -> List[Member]:
        q = db.query(Member).filter(Member.group_id == group_id)
        if status:
            q = q.filter(Member.status == status)
        return q.offset(skip).limit(limit).all()

    def count_by_group(self, db: Session, *, group_id: int, status: Optional[str] = None) -> int:
        q = db.query(Member).filter(Member.group_id == group_id)
        if status:
            q = q.filter(Member.status == status)
        return q.count()

    def create(
        self, db: Session, *, group_id: int, user_id: int,
        role: str = "member", status: str = "pending",
    ) -> Member:
        now = datetime.now(timezone.utc)
        joined = now if status == "accepted" else None
        obj = Member(
            group_id=group_id, user_id=user_id, role=role,
            status=status, joined_at=joined, status_changed_at=now,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update_status(self, db: Session, *, db_obj: Member, new_status: str) -> Member:
        now = datetime.now(timezone.utc)
        db_obj.status = new_status
        db_obj.status_changed_at = now
        if new_status == "accepted" and db_obj.joined_at is None:
            db_obj.joined_at = now
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_role(self, db: Session, *, db_obj: Member, new_role: str) -> Member:
        db_obj.role = new_role
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[Member]:
        obj = db.query(Member).filter(Member.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def remove_by_group_and_user(self, db: Session, *, group_id: int, user_id: int) -> Optional[Member]:
        obj = self.get_by_group_and_user(db, group_id=group_id, user_id=user_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


    def remove_all_by_group(self, db: Session, *, group_id: int) -> int:
        count = db.query(Member).filter(Member.group_id == group_id).delete()
        db.commit()
        return count

    def remove_all_by_user(self, db: Session, *, user_id: int) -> int:
        count = db.query(Member).filter(Member.user_id == user_id).delete()
        db.commit()
        return count


members = CRUDMember()
