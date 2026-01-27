"""CategoryRule CRUD — category:rule relationship"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.category_rule import CategoryRule


class CRUDCategoryRule:
    def get(self, db: Session, *, id: int) -> Optional[CategoryRule]:
        return db.query(CategoryRule).filter(CategoryRule.id == id).first()

    def get_by_category_and_rule(self, db: Session, *, category_id: int, rule_id: int) -> Optional[CategoryRule]:
        return db.query(CategoryRule).filter(
            CategoryRule.category_id == category_id,
            CategoryRule.rule_id == rule_id,
        ).first()

    def get_multi_by_category(self, db: Session, *, category_id: int) -> List[CategoryRule]:
        return db.query(CategoryRule).filter(
            CategoryRule.category_id == category_id,
        ).order_by(CategoryRule.priority.asc()).all()

    def create(self, db: Session, *, category_id: int, rule_id: int, priority: int = 0) -> CategoryRule:
        obj = CategoryRule(category_id=category_id, rule_id=rule_id, priority=priority)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update_priority(self, db: Session, *, db_obj: CategoryRule, priority: int) -> CategoryRule:
        db_obj.priority = priority
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[CategoryRule]:
        obj = db.query(CategoryRule).filter(CategoryRule.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def remove_by_category_and_rule(self, db: Session, *, category_id: int, rule_id: int) -> Optional[CategoryRule]:
        obj = self.get_by_category_and_rule(db, category_id=category_id, rule_id=rule_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


    def remove_all_by_category(self, db: Session, *, category_id: int) -> int:
        count = db.query(CategoryRule).filter(CategoryRule.category_id == category_id).delete()
        db.commit()
        return count

    def remove_all_by_rule(self, db: Session, *, rule_id: int) -> int:
        count = db.query(CategoryRule).filter(CategoryRule.rule_id == rule_id).delete()
        db.commit()
        return count


category_rules = CRUDCategoryRule()
