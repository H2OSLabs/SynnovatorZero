"""Paginated rating list schema"""
from pydantic import BaseModel
from typing import List
from app.schemas.rating import Rating


class PaginatedRatingList(BaseModel):
    items: List[Rating]
    total: int
    skip: int
    limit: int
