"""GroupPost SQLAlchemy model — group:post relationship"""
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class GroupPost(Base):
    __tablename__ = "group_posts"
    __table_args__ = (
        UniqueConstraint("group_id", "post_id", name="uq_group_post"),
    )

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, nullable=False, index=True)
    post_id = Column(Integer, nullable=False, index=True)
    relation_type = Column(String, nullable=False, default="team_submission")  # team_submission | announcement | reference
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
