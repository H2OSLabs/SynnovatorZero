"""UserUser CRUD — user:user relationship (follow/block)"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.user_user import UserUser


class CRUDUserUser:
    def get(self, db: Session, *, id: int) -> Optional[UserUser]:
        return db.query(UserUser).filter(UserUser.id == id).first()

    def get_relation(
        self, db: Session, *, source_user_id: int, target_user_id: int, relation_type: str,
    ) -> Optional[UserUser]:
        return db.query(UserUser).filter(
            UserUser.source_user_id == source_user_id,
            UserUser.target_user_id == target_user_id,
            UserUser.relation_type == relation_type,
        ).first()

    def has_block(self, db: Session, *, blocker_id: int, blocked_id: int) -> bool:
        """Check if blocker has blocked blocked_id."""
        return db.query(UserUser).filter(
            UserUser.source_user_id == blocker_id,
            UserUser.target_user_id == blocked_id,
            UserUser.relation_type == "block",
        ).first() is not None

    def get_following(self, db: Session, *, user_id: int) -> List[UserUser]:
        """Get all users this user follows."""
        return db.query(UserUser).filter(
            UserUser.source_user_id == user_id,
            UserUser.relation_type == "follow",
        ).all()

    def get_followers(self, db: Session, *, user_id: int) -> List[UserUser]:
        """Get all users who follow this user."""
        return db.query(UserUser).filter(
            UserUser.target_user_id == user_id,
            UserUser.relation_type == "follow",
        ).all()

    def count_followers(self, db: Session, *, user_id: int) -> int:
        """Count users who follow this user."""
        return db.query(UserUser).filter(
            UserUser.target_user_id == user_id,
            UserUser.relation_type == "follow",
        ).count()

    def count_following(self, db: Session, *, user_id: int) -> int:
        """Count users this user follows."""
        return db.query(UserUser).filter(
            UserUser.source_user_id == user_id,
            UserUser.relation_type == "follow",
        ).count()

    def is_mutual_follow(self, db: Session, *, user_a: int, user_b: int) -> bool:
        """Check if two users follow each other (friends)."""
        a_follows_b = self.get_relation(db, source_user_id=user_a, target_user_id=user_b, relation_type="follow")
        b_follows_a = self.get_relation(db, source_user_id=user_b, target_user_id=user_a, relation_type="follow")
        if not (a_follows_b and b_follows_a):
            return False
        # Block overrides friendship
        if self.has_block(db, blocker_id=user_a, blocked_id=user_b):
            return False
        if self.has_block(db, blocker_id=user_b, blocked_id=user_a):
            return False
        return True

    def create(self, db: Session, *, source_user_id: int, target_user_id: int, relation_type: str) -> UserUser:
        obj = UserUser(
            source_user_id=source_user_id,
            target_user_id=target_user_id,
            relation_type=relation_type,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def remove(self, db: Session, *, source_user_id: int, target_user_id: int, relation_type: str) -> Optional[UserUser]:
        obj = self.get_relation(db, source_user_id=source_user_id, target_user_id=target_user_id, relation_type=relation_type)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def remove_all_for_user(self, db: Session, *, user_id: int) -> int:
        """Remove all relations where user is source or target (for cascade delete)."""
        count = db.query(UserUser).filter(
            (UserUser.source_user_id == user_id) | (UserUser.target_user_id == user_id)
        ).delete(synchronize_session="fetch")
        db.commit()
        return count


user_users = CRUDUserUser()
