"""CategoryGroup SQLAlchemy model — category:group relationship (team registration)"""
from sqlalchemy import Column, Integer, DateTime, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class CategoryGroup(Base):
    __tablename__ = "category_groups"
    __table_args__ = (
        UniqueConstraint("category_id", "group_id", name="uq_category_group"),
    )

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, nullable=False, index=True)
    group_id = Column(Integer, nullable=False, index=True)
    registered_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
