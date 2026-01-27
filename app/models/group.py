"""Group SQLAlchemy 模型"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text
from sqlalchemy.sql import func



from app.database import Base


class Group(Base):
    """"""
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, default=None)
    description = Column(String, nullable=True, default=None)
    visibility = Column(String, nullable=False, default=None)
    max_members = Column(Integer, nullable=True, default=None)
    require_approval = Column(Boolean, nullable=True, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    