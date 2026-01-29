"""Interaction SQLAlchemy 模型 — unified model for like/comment/rating"""
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func

from app.database import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)  # like | comment | rating
    value = Column(JSON, nullable=True)  # comment→text, rating→scores object, like→null
    parent_id = Column(Integer, nullable=True)  # for nested comments
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
