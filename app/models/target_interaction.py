"""TargetInteraction SQLAlchemy model — target:interaction polymorphic binding"""
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class TargetInteraction(Base):
    __tablename__ = "target_interactions"
    __table_args__ = (
        UniqueConstraint("target_type", "target_id", "interaction_id", name="uq_target_interaction"),
    )

    id = Column(Integer, primary_key=True, index=True)
    target_type = Column(String, nullable=False)  # post | event | resource
    target_id = Column(Integer, nullable=False, index=True)
    interaction_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
