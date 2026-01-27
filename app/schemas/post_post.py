"""PostPost Pydantic schemas — post:post relationship"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PostPostResponse(BaseModel):
    id: int
    source_post_id: int
    target_post_id: int
    relation_type: str
    position: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}
