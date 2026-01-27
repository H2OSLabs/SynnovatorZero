"""Post relation add schema — body for POST /posts/{id}/related"""
from pydantic import BaseModel
from typing import Literal, Optional


class PostRelationAdd(BaseModel):
    target_post_id: int
    relation_type: Optional[Literal["reference", "reply", "embed"]] = "reference"
    position: Optional[int] = None
