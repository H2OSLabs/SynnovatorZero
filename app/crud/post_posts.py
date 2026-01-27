"""PostPost CRUD — post:post relationship (reference/reply/embed)"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.post_post import PostPost


class CRUDPostPost:
    def get(self, db: Session, *, id: int) -> Optional[PostPost]:
        return db.query(PostPost).filter(PostPost.id == id).first()

    def get_relation(
        self, db: Session, *, source_post_id: int, target_post_id: int, relation_type: str,
    ) -> Optional[PostPost]:
        return db.query(PostPost).filter(
            PostPost.source_post_id == source_post_id,
            PostPost.target_post_id == target_post_id,
            PostPost.relation_type == relation_type,
        ).first()

    def get_multi_by_source(
        self, db: Session, *, source_post_id: int, relation_type: Optional[str] = None,
    ) -> List[PostPost]:
        q = db.query(PostPost).filter(PostPost.source_post_id == source_post_id)
        if relation_type:
            q = q.filter(PostPost.relation_type == relation_type)
        return q.order_by(PostPost.position.asc().nulls_last()).all()

    def create(
        self, db: Session, *, source_post_id: int, target_post_id: int,
        relation_type: str = "reference", position: Optional[int] = None,
    ) -> PostPost:
        obj = PostPost(
            source_post_id=source_post_id, target_post_id=target_post_id,
            relation_type=relation_type, position=position,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(
        self, db: Session, *, db_obj: PostPost,
        relation_type: Optional[str] = None, position: Optional[int] = None,
    ) -> PostPost:
        if relation_type is not None:
            db_obj.relation_type = relation_type
        if position is not None:
            db_obj.position = position
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[PostPost]:
        obj = db.query(PostPost).filter(PostPost.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj


    def remove_all_by_post(self, db: Session, *, post_id: int) -> int:
        """Remove all relations where post is source or target."""
        count = db.query(PostPost).filter(
            (PostPost.source_post_id == post_id) |
            (PostPost.target_post_id == post_id)
        ).delete(synchronize_session="fetch")
        db.commit()
        return count


post_posts = CRUDPostPost()
