"""Paginated user list schema"""
from pydantic import BaseModel
from typing import List
from app.schemas.user import User


class PaginatedUserList(BaseModel):
    items: List[User]
    total: int
    skip: int
    limit: int
