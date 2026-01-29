"""CategoryGroup CRUD — category:group relationship (team registration)"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.category_group import CategoryGroup


class CRUDCategoryGroup:
    def get(self, db: Session, *, id: int) -> Optional[CategoryGroup]:
        return db.query(CategoryGroup).filter(CategoryGroup.id == id).first()

    def get_by_category_and_group(self, db: Session, *, category_id: int, group_id: int) -> Optional[CategoryGroup]:
        return db.query(CategoryGroup).filter(
            CategoryGroup.category_id == category_id,
            CategoryGroup.group_id == group_id,
        ).first()

    def get_multi_by_category(self, db: Session, *, category_id: int) -> List[CategoryGroup]:
        return db.query(CategoryGroup).filter(
            CategoryGroup.category_id == category_id,
        ).all()

    def get_multi_by_group(self, db: Session, *, group_id: int) -> List[CategoryGroup]:
        return db.query(CategoryGroup).filter(
            CategoryGroup.group_id == group_id,
        ).all()

    def is_user_in_category(self, db: Session, *, category_id: int, user_id: int) -> bool:
        """Check if a user is already in any group registered to this category."""
        from app.models.member import Member
        return db.query(CategoryGroup).join(
            Member, CategoryGroup.group_id == Member.group_id,
        ).filter(
            CategoryGroup.category_id == category_id,
            Member.user_id == user_id,
            Member.status == "accepted",
        ).first() is not None

    def create(self, db: Session, *, category_id: int, group_id: int) -> CategoryGroup:
        obj = CategoryGroup(category_id=category_id, group_id=group_id)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def remove(self, db: Session, *, id: int) -> Optional[CategoryGroup]:
        obj = db.query(CategoryGroup).filter(CategoryGroup.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def remove_by_category_and_group(self, db: Session, *, category_id: int, group_id: int) -> Optional[CategoryGroup]:
        obj = self.get_by_category_and_group(db, category_id=category_id, group_id=group_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


    def remove_all_by_category(self, db: Session, *, category_id: int) -> int:
        count = db.query(CategoryGroup).filter(CategoryGroup.category_id == category_id).delete()
        db.commit()
        return count

    def remove_all_by_group(self, db: Session, *, group_id: int) -> int:
        count = db.query(CategoryGroup).filter(CategoryGroup.group_id == group_id).delete()
        db.commit()
        return count


category_groups = CRUDCategoryGroup()
