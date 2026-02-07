"""EventEvent SQLAlchemy model — event:event relationship (stage/track/prerequisite)"""
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class EventEvent(Base):
    __tablename__ = "event_events"
    __table_args__ = (
        UniqueConstraint("source_event_id", "target_event_id", name="uq_event_event"),
    )

    id = Column(Integer, primary_key=True, index=True)
    source_event_id = Column(Integer, nullable=False, index=True)
    target_event_id = Column(Integer, nullable=False, index=True)
    relation_type = Column(String, nullable=False)  # stage | track | prerequisite
    stage_order = Column(Integer, nullable=True)  # only for stage type
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
