"""Rule SQLAlchemy 模型"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func

from app.database import Base


class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    allow_public = Column(Boolean, nullable=True, default=False)
    require_review = Column(Boolean, nullable=True, default=False)
    reviewers = Column(JSON, nullable=True)
    submission_start = Column(DateTime, nullable=True)
    submission_deadline = Column(DateTime, nullable=True)
    submission_format = Column(JSON, nullable=True)
    max_submissions = Column(Integer, nullable=True)
    min_team_size = Column(Integer, nullable=True)
    max_team_size = Column(Integer, nullable=True)
    scoring_criteria = Column(JSON, nullable=True)
    checks = Column(JSON, nullable=True)
    content = Column(Text, nullable=True)
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
