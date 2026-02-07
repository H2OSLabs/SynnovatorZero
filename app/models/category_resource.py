"""CategoryResource SQLAlchemy model — category:resource relationship"""
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class CategoryResource(Base):
    __tablename__ = "category_resources"
    __table_args__ = (
        UniqueConstraint("category_id", "resource_id", name="uq_category_resource"),
    )

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, nullable=False, index=True)
    resource_id = Column(Integer, nullable=False, index=True)
    display_type = Column(String, nullable=False, default="attachment")  # banner | attachment | inline
    position = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
