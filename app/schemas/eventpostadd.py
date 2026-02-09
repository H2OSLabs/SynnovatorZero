"""Event post add schema — body for POST /events/{id}/posts"""
from pydantic import BaseModel
from typing import Literal, Optional


class EventPostAdd(BaseModel):
    post_id: int
    relation_type: Optional[Literal["submission", "reference"]] = "submission"
