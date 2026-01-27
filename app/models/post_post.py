"""PostPost SQLAlchemy model — post:post relationship (reference/reply/embed)"""
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class PostPost(Base):
    __tablename__ = "post_posts"
    __table_args__ = (
        UniqueConstraint("source_post_id", "target_post_id", "relation_type", name="uq_post_post"),
    )

    id = Column(Integer, primary_key=True, index=True)
    source_post_id = Column(Integer, nullable=False, index=True)
    target_post_id = Column(Integer, nullable=False, index=True)
    relation_type = Column(String, nullable=False)  # reference | reply | embed
    position = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
