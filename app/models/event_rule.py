"""EventRule SQLAlchemy model — event:rule relationship"""
from sqlalchemy import Column, Integer, DateTime, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class EventRule(Base):
    __tablename__ = "category_rules"
    __table_args__ = (
        UniqueConstraint("event_id", "rule_id", name="uq_category_rule"),
    )

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, nullable=False, index=True)
    rule_id = Column(Integer, nullable=False, index=True)
    priority = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
