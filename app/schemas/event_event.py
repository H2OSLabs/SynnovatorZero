"""EventEvent Pydantic schemas — event:event relationship"""
from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional


class EventEventAdd(BaseModel):
    target_event_id: int
    relation_type: Literal["stage", "track", "prerequisite"]
    stage_order: Optional[int] = None


class EventEventResponse(BaseModel):
    id: int
    source_event_id: int
    target_event_id: int
    relation_type: str
    stage_order: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}
