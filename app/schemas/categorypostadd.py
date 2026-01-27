"""Category post add schema — body for POST /categories/{id}/posts"""
from pydantic import BaseModel
from typing import Literal, Optional


class CategoryPostAdd(BaseModel):
    post_id: int
    relation_type: Optional[Literal["submission", "reference"]] = "submission"
