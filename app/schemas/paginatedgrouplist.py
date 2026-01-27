"""Paginated group list schema"""
from pydantic import BaseModel
from typing import List
from app.schemas.group import Group


class PaginatedGroupList(BaseModel):
    items: List[Group]
    total: int
    skip: int
    limit: int
