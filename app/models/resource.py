"""Resource SQLAlchemy 模型"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text
from sqlalchemy.sql import func



from app.database import Base


class Resource(Base):
    """"""
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False, default=None)
    display_name = Column(String, nullable=True, default=None)
    description = Column(String, nullable=True, default=None)
    mime_type = Column(String, nullable=True, default=None)
    size = Column(Integer, nullable=True, default=None)
    url = Column(String, nullable=True, default=None)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    