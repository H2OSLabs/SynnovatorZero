"""CategoryPost Pydantic schemas — category:post relationship"""
from pydantic import BaseModel
from datetime import datetime


class CategoryPostResponse(BaseModel):
    id: int
    category_id: int
    post_id: int
    relation_type: str
    created_at: datetime

    model_config = {"from_attributes": True}
