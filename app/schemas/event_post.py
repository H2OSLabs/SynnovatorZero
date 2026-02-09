"""EventPost Pydantic schemas — event:post relationship"""
from pydantic import BaseModel
from datetime import datetime


class EventPostResponse(BaseModel):
    id: int
    event_id: int
    post_id: int
    relation_type: str
    created_at: datetime

    model_config = {"from_attributes": True}
