"""Category post add schema"""
from pydantic import BaseModel
from typing import Optional


class CategoryPostAdd(BaseModel):
    post_id: int
    relation_type: Optional[str] = "submission"
