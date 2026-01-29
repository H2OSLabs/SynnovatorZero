"""Paginated resource list schema"""
from pydantic import BaseModel
from typing import List
from app.schemas.resource import Resource


class PaginatedResourceList(BaseModel):
    items: List[Resource]
    total: int
    skip: int
    limit: int
