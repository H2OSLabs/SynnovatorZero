"""Resource CRUD operations"""
from datetime import datetime, timezone
from typing import Any, List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.resource import Resource
from app.schemas.resource import ResourceCreate, ResourceUpdate


class CRUDResource(CRUDBase[Resource, ResourceCreate, ResourceUpdate]):
    def get(self, db: Session, id: Any) -> Optional[Resource]:
        return db.query(self.model).filter(
            self.model.id == id,
            self.model.deleted_at.is_(None),
        ).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Resource]:
        return db.query(self.model).filter(
            self.model.deleted_at.is_(None),
        ).offset(skip).limit(limit).all()

    def remove(self, db: Session, *, id: Any) -> Optional[Resource]:
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            obj.deleted_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(obj)
        return obj


resources = CRUDResource(Resource)
