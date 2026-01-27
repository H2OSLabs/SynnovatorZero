"""Rule CRUD operations"""
from datetime import datetime, timezone
from typing import Any, List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.rule import Rule
from app.schemas.rule import RuleCreate, RuleUpdate


class CRUDRule(CRUDBase[Rule, RuleCreate, RuleUpdate]):
    def get(self, db: Session, id: Any) -> Optional[Rule]:
        return db.query(self.model).filter(
            self.model.id == id,
            self.model.deleted_at.is_(None),
        ).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Rule]:
        return db.query(self.model).filter(
            self.model.deleted_at.is_(None),
        ).offset(skip).limit(limit).all()

    def remove(self, db: Session, *, id: Any) -> Optional[Rule]:
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            obj.deleted_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(obj)
        return obj


rules = CRUDRule(Rule)
