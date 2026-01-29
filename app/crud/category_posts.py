"""CategoryPost CRUD — category:post relationship"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.category_post import CategoryPost


class CRUDCategoryPost:
    def get(self, db: Session, *, id: int) -> Optional[CategoryPost]:
        return db.query(CategoryPost).filter(CategoryPost.id == id).first()

    def get_by_category_and_post(self, db: Session, *, category_id: int, post_id: int) -> Optional[CategoryPost]:
        return db.query(CategoryPost).filter(
            CategoryPost.category_id == category_id,
            CategoryPost.post_id == post_id,
        ).first()

    def get_multi_by_category(
        self, db: Session, *, category_id: int,
        relation_type: Optional[str] = None, skip: int = 0, limit: int = 100,
    ) -> List[CategoryPost]:
        q = db.query(CategoryPost).filter(CategoryPost.category_id == category_id)
        if relation_type:
            q = q.filter(CategoryPost.relation_type == relation_type)
        return q.offset(skip).limit(limit).all()

    def count_by_category(
        self, db: Session, *, category_id: int, relation_type: Optional[str] = None,
    ) -> int:
        q = db.query(CategoryPost).filter(CategoryPost.category_id == category_id)
        if relation_type:
            q = q.filter(CategoryPost.relation_type == relation_type)
        return q.count()

    def count_submissions_by_user(
        self, db: Session, *, category_id: int, user_id: int,
    ) -> int:
        """Count submissions by a specific user in a category (for max_submissions check)."""
        from app.models.post import Post
        return db.query(CategoryPost).join(Post, CategoryPost.post_id == Post.id).filter(
            CategoryPost.category_id == category_id,
            CategoryPost.relation_type == "submission",
            Post.created_by == user_id,
        ).count()

    def create(
        self, db: Session, *, category_id: int, post_id: int,
        relation_type: str = "submission",
    ) -> CategoryPost:
        obj = CategoryPost(category_id=category_id, post_id=post_id, relation_type=relation_type)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def remove(self, db: Session, *, id: int) -> Optional[CategoryPost]:
        obj = db.query(CategoryPost).filter(CategoryPost.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj


    def remove_all_by_category(self, db: Session, *, category_id: int) -> int:
        count = db.query(CategoryPost).filter(CategoryPost.category_id == category_id).delete()
        db.commit()
        return count

    def remove_all_by_post(self, db: Session, *, post_id: int) -> int:
        count = db.query(CategoryPost).filter(CategoryPost.post_id == post_id).delete()
        db.commit()
        return count


category_posts = CRUDCategoryPost()
