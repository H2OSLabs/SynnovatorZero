"""EventRule Pydantic schemas — event:rule relationship"""
from pydantic import BaseModel
from datetime import datetime


class EventRuleResponse(BaseModel):
    id: int
    event_id: int
    rule_id: int
    priority: int
    created_at: datetime

    model_config = {"from_attributes": True}
