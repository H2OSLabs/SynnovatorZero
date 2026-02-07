"""EventEvent CRUD — event:event relationship (stage/track/prerequisite + cycle detection)"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.event_event import EventEvent


class CRUDEventEvent:
    def get(self, db: Session, *, id: int) -> Optional[EventEvent]:
        return db.query(EventEvent).filter(EventEvent.id == id).first()

    def get_by_source_and_target(
        self, db: Session, *, source_event_id: int, target_event_id: int,
    ) -> Optional[EventEvent]:
        return db.query(EventEvent).filter(
            EventEvent.source_event_id == source_event_id,
            EventEvent.target_event_id == target_event_id,
        ).first()

    def get_multi_by_source(
        self, db: Session, *, source_event_id: int,
        relation_type: Optional[str] = None,
    ) -> List[EventEvent]:
        q = db.query(EventEvent).filter(
            EventEvent.source_event_id == source_event_id,
        )
        if relation_type:
            q = q.filter(EventEvent.relation_type == relation_type)
        return q.order_by(EventEvent.stage_order.asc().nullslast()).all()

    def get_multi_by_target(
        self, db: Session, *, target_event_id: int,
        relation_type: Optional[str] = None,
    ) -> List[EventEvent]:
        q = db.query(EventEvent).filter(
            EventEvent.target_event_id == target_event_id,
        )
        if relation_type:
            q = q.filter(EventEvent.relation_type == relation_type)
        return q.all()

    def has_cycle(
        self, db: Session, *, source_id: int, target_id: int, relation_type: str,
    ) -> bool:
        """Detect circular dependency for stage/prerequisite types.
        Starting from target_id, walk the graph following same relation_type.
        If we reach source_id, there's a cycle.
        """
        if relation_type == "track":
            return False  # tracks are parallel, no cycle concern
        visited = set()
        stack = [target_id]
        while stack:
            current = stack.pop()
            if current == source_id:
                return True
            if current in visited:
                continue
            visited.add(current)
            # Follow outgoing edges of same relation_type from current
            edges = db.query(EventEvent).filter(
                EventEvent.source_event_id == current,
                EventEvent.relation_type == relation_type,
            ).all()
            for edge in edges:
                stack.append(edge.target_event_id)
        return False

    def create(
        self, db: Session, *, source_event_id: int, target_event_id: int,
        relation_type: str, stage_order: Optional[int] = None,
    ) -> EventEvent:
        obj = EventEvent(
            source_event_id=source_event_id,
            target_event_id=target_event_id,
            relation_type=relation_type,
            stage_order=stage_order,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def remove(self, db: Session, *, id: int) -> Optional[EventEvent]:
        obj = db.query(EventEvent).filter(EventEvent.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def remove_by_source_and_target(
        self, db: Session, *, source_event_id: int, target_event_id: int,
    ) -> Optional[EventEvent]:
        obj = self.get_by_source_and_target(
            db, source_event_id=source_event_id,
            target_event_id=target_event_id,
        )
        if obj:
            db.delete(obj)
            db.commit()
        return obj


    def remove_all_by_category(self, db: Session, *, event_id: int) -> int:
        """Remove all associations where event is source or target."""
        count = db.query(EventEvent).filter(
            (EventEvent.source_event_id == event_id) |
            (EventEvent.target_event_id == event_id)
        ).delete(synchronize_session="fetch")
        db.commit()
        return count


event_events = CRUDEventEvent()
