"""Interaction CRUD operations (unified model + legacy Comment/Rating)"""
from datetime import datetime, timezone
from typing import Any, List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.interaction import Interaction
from app.models.comment import Comment
from app.models.rating import Rating
from app.schemas.interaction import InteractionCreate, InteractionUpdate
from app.schemas.comment import CommentCreate, CommentUpdate
from app.schemas.rating import RatingCreate, RatingUpdate


class CRUDInteraction(CRUDBase[Interaction, InteractionCreate, InteractionUpdate]):
    def get(self, db: Session, id: Any) -> Optional[Interaction]:
        return db.query(self.model).filter(
            self.model.id == id,
            self.model.deleted_at.is_(None),
        ).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Interaction]:
        return db.query(self.model).filter(
            self.model.deleted_at.is_(None),
        ).offset(skip).limit(limit).all()

    def remove(self, db: Session, *, id: Any) -> Optional[Interaction]:
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            obj.deleted_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(obj)
        return obj


interactions = CRUDInteraction(Interaction)


# Legacy CRUD (used by existing interaction router stubs)
class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):
    pass


class CRUDRating(CRUDBase[Rating, RatingCreate, RatingUpdate]):
    pass


comments = CRUDComment(Comment)
ratings = CRUDRating(Rating)
