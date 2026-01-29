"""PostResource CRUD — post:resource relationship"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.post_resource import PostResource


class CRUDPostResource:
    def get(self, db: Session, *, id: int) -> Optional[PostResource]:
        return db.query(PostResource).filter(PostResource.id == id).first()

    def get_by_post_and_resource(self, db: Session, *, post_id: int, resource_id: int) -> Optional[PostResource]:
        return db.query(PostResource).filter(
            PostResource.post_id == post_id,
            PostResource.resource_id == resource_id,
        ).first()

    def get_multi_by_post(self, db: Session, *, post_id: int) -> List[PostResource]:
        return db.query(PostResource).filter(
            PostResource.post_id == post_id,
        ).order_by(PostResource.position.asc().nulls_last()).all()

    def create(
        self, db: Session, *, post_id: int, resource_id: int,
        display_type: str = "attachment", position: Optional[int] = None,
    ) -> PostResource:
        obj = PostResource(
            post_id=post_id, resource_id=resource_id,
            display_type=display_type, position=position,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, *, db_obj: PostResource, display_type: Optional[str] = None, position: Optional[int] = None) -> PostResource:
        if display_type is not None:
            db_obj.display_type = display_type
        if position is not None:
            db_obj.position = position
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[PostResource]:
        obj = db.query(PostResource).filter(PostResource.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj


    def remove_all_by_post(self, db: Session, *, post_id: int) -> int:
        count = db.query(PostResource).filter(PostResource.post_id == post_id).delete()
        db.commit()
        return count


post_resources = CRUDPostResource()
