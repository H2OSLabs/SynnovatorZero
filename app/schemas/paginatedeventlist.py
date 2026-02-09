"""Paginated event list schema"""
from pydantic import BaseModel
from typing import List
from app.schemas.event import Event


class PaginatedEventList(BaseModel):
    items: List[Event]
    total: int
    skip: int
    limit: int
