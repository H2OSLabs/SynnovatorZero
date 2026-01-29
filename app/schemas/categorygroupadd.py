"""Category group add schema"""
from pydantic import BaseModel


class CategoryGroupAdd(BaseModel):
    group_id: int
