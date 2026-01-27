"""Post SQLAlchemy 模型"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func

from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)
    tags = Column(JSON, nullable=True, default=[])
    status = Column(String, nullable=False)
    like_count = Column(Integer, nullable=True, default=0)
    comment_count = Column(Integer, nullable=True, default=0)
    average_rating = Column(Float, nullable=True)
    content = Column(Text, nullable=True)
    created_by = Column(String, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
