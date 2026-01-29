"""Paginated post list schema"""
from pydantic import BaseModel
from typing import List
from app.schemas.post import Post


class PaginatedPostList(BaseModel):
    items: List[Post]
    total: int
    skip: int
    limit: int
