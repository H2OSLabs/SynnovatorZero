"""Paginated member list schema"""
from pydantic import BaseModel
from typing import List
from app.schemas.member import Member


class PaginatedMemberList(BaseModel):
    items: List[Member]
    total: int
    skip: int
    limit: int
