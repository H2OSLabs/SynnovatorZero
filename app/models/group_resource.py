"""GroupResource SQLAlchemy model — group:resource relationship"""
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class GroupResource(Base):
    __tablename__ = "group_resources"
    __table_args__ = (
        UniqueConstraint("group_id", "resource_id", name="uq_group_resource"),
    )

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, nullable=False, index=True)
    resource_id = Column(Integer, nullable=False, index=True)
    access_level = Column(String, nullable=False, default="read_only")  # read_only | read_write
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
