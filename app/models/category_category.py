"""CategoryCategory SQLAlchemy model — category:category relationship (stage/track/prerequisite)"""
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class CategoryCategory(Base):
    __tablename__ = "category_categories"
    __table_args__ = (
        UniqueConstraint("source_category_id", "target_category_id", name="uq_category_category"),
    )

    id = Column(Integer, primary_key=True, index=True)
    source_category_id = Column(Integer, nullable=False, index=True)
    target_category_id = Column(Integer, nullable=False, index=True)
    relation_type = Column(String, nullable=False)  # stage | track | prerequisite
    stage_order = Column(Integer, nullable=True)  # only for stage type
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
