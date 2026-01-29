"""TargetInteraction CRUD — target:interaction polymorphic binding + cache update"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.target_interaction import TargetInteraction
from app.models.interaction import Interaction


class CRUDTargetInteraction:
    def get(self, db: Session, *, id: int) -> Optional[TargetInteraction]:
        return db.query(TargetInteraction).filter(TargetInteraction.id == id).first()

    def get_by_target_and_interaction(
        self, db: Session, *, target_type: str, target_id: int, interaction_id: int,
    ) -> Optional[TargetInteraction]:
        return db.query(TargetInteraction).filter(
            TargetInteraction.target_type == target_type,
            TargetInteraction.target_id == target_id,
            TargetInteraction.interaction_id == interaction_id,
        ).first()

    def get_multi_by_target(
        self, db: Session, *, target_type: str, target_id: int,
        interaction_type: Optional[str] = None,
    ) -> List[TargetInteraction]:
        q = db.query(TargetInteraction).filter(
            TargetInteraction.target_type == target_type,
            TargetInteraction.target_id == target_id,
        )
        if interaction_type:
            q = q.join(Interaction, TargetInteraction.interaction_id == Interaction.id).filter(
                Interaction.type == interaction_type,
            )
        return q.all()

    def has_like_by_user(
        self, db: Session, *, target_type: str, target_id: int, user_id: int,
    ) -> bool:
        """Check if user already liked this target (for dedup)."""
        return db.query(TargetInteraction).join(
            Interaction, TargetInteraction.interaction_id == Interaction.id,
        ).filter(
            TargetInteraction.target_type == target_type,
            TargetInteraction.target_id == target_id,
            Interaction.type == "like",
            Interaction.created_by == user_id,
        ).first() is not None

    def get_like_by_user(
        self, db: Session, *, target_type: str, target_id: int, user_id: int,
    ) -> Optional[TargetInteraction]:
        """Get the like target_interaction for a user on a target."""
        return db.query(TargetInteraction).join(
            Interaction, TargetInteraction.interaction_id == Interaction.id,
        ).filter(
            TargetInteraction.target_type == target_type,
            TargetInteraction.target_id == target_id,
            Interaction.type == "like",
            Interaction.created_by == user_id,
        ).first()

    def create(
        self, db: Session, *, target_type: str, target_id: int, interaction_id: int,
    ) -> TargetInteraction:
        obj = TargetInteraction(
            target_type=target_type, target_id=target_id, interaction_id=interaction_id,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def remove(self, db: Session, *, id: int) -> Optional[TargetInteraction]:
        obj = db.query(TargetInteraction).filter(TargetInteraction.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def count_by_target_and_type(
        self, db: Session, *, target_type: str, target_id: int, interaction_type: str,
    ) -> int:
        """Count interactions of a type on a target (for cache update)."""
        return db.query(TargetInteraction).join(
            Interaction, TargetInteraction.interaction_id == Interaction.id,
        ).filter(
            TargetInteraction.target_type == target_type,
            TargetInteraction.target_id == target_id,
            Interaction.type == interaction_type,
            Interaction.deleted_at.is_(None),
        ).count()


    def get_all_by_target(
        self, db: Session, *, target_type: str, target_id: int,
    ) -> List[TargetInteraction]:
        return db.query(TargetInteraction).filter(
            TargetInteraction.target_type == target_type,
            TargetInteraction.target_id == target_id,
        ).all()

    def remove_all_by_target(
        self, db: Session, *, target_type: str, target_id: int,
    ) -> List[int]:
        """Remove all bindings for a target, return interaction_ids for cascade."""
        tis = self.get_all_by_target(db, target_type=target_type, target_id=target_id)
        interaction_ids = [ti.interaction_id for ti in tis]
        for ti in tis:
            db.delete(ti)
        db.commit()
        return interaction_ids

    def get_all_by_interaction(
        self, db: Session, *, interaction_id: int,
    ) -> List[TargetInteraction]:
        return db.query(TargetInteraction).filter(
            TargetInteraction.interaction_id == interaction_id,
        ).all()

    def remove_all_by_interaction(
        self, db: Session, *, interaction_id: int,
    ) -> int:
        count = db.query(TargetInteraction).filter(
            TargetInteraction.interaction_id == interaction_id,
        ).delete()
        db.commit()
        return count


target_interactions = CRUDTargetInteraction()
