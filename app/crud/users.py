"""User CRUD operations"""
from datetime import datetime, timezone
from typing import Any, List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get(self, db: Session, id: Any) -> Optional[User]:
        return db.query(self.model).filter(
            self.model.id == id,
            self.model.deleted_at.is_(None),
        ).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(self.model).filter(
            self.model.deleted_at.is_(None),
        ).offset(skip).limit(limit).all()

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(self.model).filter(
            self.model.username == username,
            self.model.deleted_at.is_(None),
        ).first()

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(self.model).filter(
            self.model.email == email,
            self.model.deleted_at.is_(None),
        ).first()

    def remove(self, db: Session, *, id: Any) -> Optional[User]:
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            obj.deleted_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(obj)
        return obj


users = CRUDUser(User)
