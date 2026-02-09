"""EventGroup Pydantic schemas — event:group relationship"""
from pydantic import BaseModel
from datetime import datetime


class EventGroupResponse(BaseModel):
    id: int
    event_id: int
    group_id: int
    registered_at: datetime

    model_config = {"from_attributes": True}
