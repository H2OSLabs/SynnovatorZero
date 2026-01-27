"""Paginated interaction list schema"""
from pydantic import BaseModel
from typing import List
from app.schemas.interaction import Interaction


class PaginatedInteractionList(BaseModel):
    items: List[Interaction]
    total: int
    skip: int
    limit: int
