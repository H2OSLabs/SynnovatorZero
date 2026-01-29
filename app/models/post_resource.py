"""PostResource SQLAlchemy model — post:resource relationship"""
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class PostResource(Base):
    __tablename__ = "post_resources"
    __table_args__ = (
        UniqueConstraint("post_id", "resource_id", name="uq_post_resource"),
    )

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, nullable=False, index=True)
    resource_id = Column(Integer, nullable=False, index=True)
    display_type = Column(String, nullable=False, default="attachment")  # attachment | inline
    position = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
