"""Group CRUD operations"""
from datetime import datetime, timezone
from typing import Any, List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.group import Group
from app.schemas.group import GroupCreate, GroupUpdate


class CRUDGroup(CRUDBase[Group, GroupCreate, GroupUpdate]):
    def get(self, db: Session, id: Any) -> Optional[Group]:
        return db.query(self.model).filter(
            self.model.id == id,
            self.model.deleted_at.is_(None),
        ).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Group]:
        return db.query(self.model).filter(
            self.model.deleted_at.is_(None),
        ).offset(skip).limit(limit).all()

    def remove(self, db: Session, *, id: Any) -> Optional[Group]:
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            obj.deleted_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(obj)
        return obj


groups = CRUDGroup(Group)
