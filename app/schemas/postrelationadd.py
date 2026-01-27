"""Post relation add schema"""
from pydantic import BaseModel
from typing import Optional


class PostRelationAdd(BaseModel):
    target_post_id: int
    relation_type: Optional[str] = "reference"
    position: Optional[int] = None
