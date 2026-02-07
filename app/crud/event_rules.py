"""EventRule CRUD — event:rule relationship"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.event_rule import EventRule


class CRUDEventRule:
    def get(self, db: Session, *, id: int) -> Optional[EventRule]:
        return db.query(EventRule).filter(EventRule.id == id).first()

    def get_by_category_and_rule(self, db: Session, *, event_id: int, rule_id: int) -> Optional[EventRule]:
        return db.query(EventRule).filter(
            EventRule.event_id == event_id,
            EventRule.rule_id == rule_id,
        ).first()

    def get_multi_by_category(self, db: Session, *, event_id: int) -> List[EventRule]:
        return db.query(EventRule).filter(
            EventRule.event_id == event_id,
        ).order_by(EventRule.priority.asc()).all()

    def create(self, db: Session, *, event_id: int, rule_id: int, priority: int = 0) -> EventRule:
        obj = EventRule(event_id=event_id, rule_id=rule_id, priority=priority)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update_priority(self, db: Session, *, db_obj: EventRule, priority: int) -> EventRule:
        db_obj.priority = priority
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[EventRule]:
        obj = db.query(EventRule).filter(EventRule.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def remove_by_category_and_rule(self, db: Session, *, event_id: int, rule_id: int) -> Optional[EventRule]:
        obj = self.get_by_category_and_rule(db, event_id=event_id, rule_id=rule_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


    def remove_all_by_category(self, db: Session, *, event_id: int) -> int:
        count = db.query(EventRule).filter(EventRule.event_id == event_id).delete()
        db.commit()
        return count

    def remove_all_by_rule(self, db: Session, *, rule_id: int) -> int:
        count = db.query(EventRule).filter(EventRule.rule_id == rule_id).delete()
        db.commit()
        return count


event_rules = CRUDEventRule()
