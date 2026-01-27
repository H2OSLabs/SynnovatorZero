"""User SQLAlchemy 模型"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text
from sqlalchemy.sql import func



from app.database import Base


class User(Base):
    """"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, default=None)
    email = Column(String, nullable=False, unique=True, index=True, default=None)
    display_name = Column(String, nullable=True, default=None)
    avatar_url = Column(String, nullable=True, default=None)
    bio = Column(String, nullable=True, default=None)
    role = Column(String, nullable=False, default=None)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    