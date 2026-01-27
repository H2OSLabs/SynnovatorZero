"""Paginated category list schema"""
from pydantic import BaseModel
from typing import List
from app.schemas.category import Category


class PaginatedCategoryList(BaseModel):
    items: List[Category]
    total: int
    skip: int
    limit: int
