"""Post CRUD operations"""
from datetime import datetime, timezone
from typing import Any, List, Optional, Tuple

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.category_post import CategoryPost
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    def get(self, db: Session, id: Any) -> Optional[Post]:
        return db.query(self.model).filter(
            self.model.id == id,
            self.model.deleted_at.is_(None),
        ).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        post_type: Optional[str] = None,
        post_status: Optional[str] = None,
        category_id: Optional[int] = None,
        tags: Optional[list[str]] = None,
        order_by: str = "created_at",
        order: str = "desc",
    ) -> Tuple[List[Post], int]:
        query = db.query(self.model).filter(self.model.deleted_at.is_(None))

        if post_type:
            query = query.filter(self.model.type == post_type)
        if post_status:
            query = query.filter(self.model.status == post_status)
        if category_id is not None:
            query = (
                query.join(CategoryPost, CategoryPost.post_id == self.model.id)
                .filter(CategoryPost.category_id == category_id)
            )

        orderable = {
            "id": self.model.id,
            "created_at": self.model.created_at,
            "updated_at": self.model.updated_at,
            "like_count": self.model.like_count,
            "comment_count": self.model.comment_count,
        }
        col = orderable.get(order_by, self.model.created_at)
        query = query.order_by(col.asc() if order == "asc" else col.desc())

        if tags:
            items = query.all()
            filtered = [
                post
                for post in items
                if post.tags and any(tag in post.tags for tag in tags)
            ]
            total = len(filtered)
            return filtered[skip : skip + limit], total

        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total

    def remove(self, db: Session, *, id: Any) -> Optional[Post]:
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            obj.deleted_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(obj)
        return obj


posts = CRUDPost(Post)
