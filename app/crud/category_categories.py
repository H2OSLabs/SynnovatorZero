"""CategoryCategory CRUD — category:category relationship (stage/track/prerequisite + cycle detection)"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.category_category import CategoryCategory


class CRUDCategoryCategory:
    def get(self, db: Session, *, id: int) -> Optional[CategoryCategory]:
        return db.query(CategoryCategory).filter(CategoryCategory.id == id).first()

    def get_by_source_and_target(
        self, db: Session, *, source_category_id: int, target_category_id: int,
    ) -> Optional[CategoryCategory]:
        return db.query(CategoryCategory).filter(
            CategoryCategory.source_category_id == source_category_id,
            CategoryCategory.target_category_id == target_category_id,
        ).first()

    def get_multi_by_source(
        self, db: Session, *, source_category_id: int,
        relation_type: Optional[str] = None,
    ) -> List[CategoryCategory]:
        q = db.query(CategoryCategory).filter(
            CategoryCategory.source_category_id == source_category_id,
        )
        if relation_type:
            q = q.filter(CategoryCategory.relation_type == relation_type)
        return q.order_by(CategoryCategory.stage_order.asc().nullslast()).all()

    def get_multi_by_target(
        self, db: Session, *, target_category_id: int,
        relation_type: Optional[str] = None,
    ) -> List[CategoryCategory]:
        q = db.query(CategoryCategory).filter(
            CategoryCategory.target_category_id == target_category_id,
        )
        if relation_type:
            q = q.filter(CategoryCategory.relation_type == relation_type)
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
            edges = db.query(CategoryCategory).filter(
                CategoryCategory.source_category_id == current,
                CategoryCategory.relation_type == relation_type,
            ).all()
            for edge in edges:
                stack.append(edge.target_category_id)
        return False

    def create(
        self, db: Session, *, source_category_id: int, target_category_id: int,
        relation_type: str, stage_order: Optional[int] = None,
    ) -> CategoryCategory:
        obj = CategoryCategory(
            source_category_id=source_category_id,
            target_category_id=target_category_id,
            relation_type=relation_type,
            stage_order=stage_order,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def remove(self, db: Session, *, id: int) -> Optional[CategoryCategory]:
        obj = db.query(CategoryCategory).filter(CategoryCategory.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def remove_by_source_and_target(
        self, db: Session, *, source_category_id: int, target_category_id: int,
    ) -> Optional[CategoryCategory]:
        obj = self.get_by_source_and_target(
            db, source_category_id=source_category_id,
            target_category_id=target_category_id,
        )
        if obj:
            db.delete(obj)
            db.commit()
        return obj


    def remove_all_by_category(self, db: Session, *, category_id: int) -> int:
        """Remove all associations where category is source or target."""
        count = db.query(CategoryCategory).filter(
            (CategoryCategory.source_category_id == category_id) |
            (CategoryCategory.target_category_id == category_id)
        ).delete(synchronize_session="fetch")
        db.commit()
        return count


category_categories = CRUDCategoryCategory()
