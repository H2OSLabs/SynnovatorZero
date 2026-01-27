"""Paginated comment list schema"""
from pydantic import BaseModel
from typing import List
from app.schemas.comment import Comment


class PaginatedCommentList(BaseModel):
    items: List[Comment]
    total: int
    skip: int
    limit: int
