"""EventPost CRUD — event:post relationship"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.event_post import EventPost


class CRUDEventPost:
    def get(self, db: Session, *, id: int) -> Optional[EventPost]:
        return db.query(EventPost).filter(EventPost.id == id).first()

    def get_by_category_and_post(self, db: Session, *, event_id: int, post_id: int) -> Optional[EventPost]:
        return db.query(EventPost).filter(
            EventPost.event_id == event_id,
            EventPost.post_id == post_id,
        ).first()

    def get_multi_by_category(
        self, db: Session, *, event_id: int,
        relation_type: Optional[str] = None, skip: int = 0, limit: int = 100,
    ) -> List[EventPost]:
        q = db.query(EventPost).filter(EventPost.event_id == event_id)
        if relation_type:
            q = q.filter(EventPost.relation_type == relation_type)
        return q.offset(skip).limit(limit).all()

    def count_by_category(
        self, db: Session, *, event_id: int, relation_type: Optional[str] = None,
    ) -> int:
        q = db.query(EventPost).filter(EventPost.event_id == event_id)
        if relation_type:
            q = q.filter(EventPost.relation_type == relation_type)
        return q.count()

    def count_submissions_by_user(
        self, db: Session, *, event_id: int, user_id: int,
    ) -> int:
        """Count submissions by a specific user in a event (for max_submissions check)."""
        from app.models.post import Post
        return db.query(EventPost).join(Post, EventPost.post_id == Post.id).filter(
            EventPost.event_id == event_id,
            EventPost.relation_type == "submission",
            Post.created_by == user_id,
        ).count()

    def create(
        self, db: Session, *, event_id: int, post_id: int,
        relation_type: str = "submission",
    ) -> EventPost:
        obj = EventPost(event_id=event_id, post_id=post_id, relation_type=relation_type)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def remove(self, db: Session, *, id: int) -> Optional[EventPost]:
        obj = db.query(EventPost).filter(EventPost.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj


    def remove_all_by_category(self, db: Session, *, event_id: int) -> int:
        count = db.query(EventPost).filter(EventPost.event_id == event_id).delete()
        db.commit()
        return count

    def remove_all_by_post(self, db: Session, *, post_id: int) -> int:
        count = db.query(EventPost).filter(EventPost.post_id == post_id).delete()
        db.commit()
        return count


event_posts = CRUDEventPost()
