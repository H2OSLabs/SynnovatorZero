"""Comment Pydantic schemas"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class CommentBase(BaseModel):
    content: str
    parent_id: Optional[int] = None


class CommentCreate(CommentBase):
    target_id: int
    target_type: str
    created_by: str


class CommentUpdate(BaseModel):
    content: Optional[str] = None


class CommentInDBBase(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    target_id: int
    target_type: str
    created_by: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class Comment(CommentInDBBase):
    pass
