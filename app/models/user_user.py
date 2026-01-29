"""UserUser SQLAlchemy model — user:user relationship (follow/block)"""
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class UserUser(Base):
    __tablename__ = "user_users"
    __table_args__ = (
        UniqueConstraint("source_user_id", "target_user_id", "relation_type", name="uq_user_user"),
    )

    id = Column(Integer, primary_key=True, index=True)
    source_user_id = Column(Integer, nullable=False, index=True)
    target_user_id = Column(Integer, nullable=False, index=True)
    relation_type = Column(String, nullable=False)  # follow | block
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
