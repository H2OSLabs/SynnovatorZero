"""EventPost SQLAlchemy model — event:post relationship"""
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class EventPost(Base):
    __tablename__ = "category_posts"
    __table_args__ = (
        UniqueConstraint("event_id", "post_id", name="uq_category_post"),
    )

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, nullable=False, index=True)
    post_id = Column(Integer, nullable=False, index=True)
    relation_type = Column(String, nullable=False, default="submission")  # submission | reference
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
