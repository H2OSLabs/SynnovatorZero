"""Paginated rule list schema"""
from pydantic import BaseModel
from typing import List
from app.schemas.rule import Rule


class PaginatedRuleList(BaseModel):
    items: List[Rule]
    total: int
    skip: int
    limit: int
