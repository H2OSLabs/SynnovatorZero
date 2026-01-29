"""TargetInteraction Pydantic schemas — target:interaction polymorphic binding"""
from pydantic import BaseModel
from datetime import datetime
from typing import Literal


class TargetInteractionCreate(BaseModel):
    target_type: Literal["post", "category", "resource"]
    target_id: int
    interaction_id: int


class TargetInteractionResponse(BaseModel):
    id: int
    target_type: str
    target_id: int
    interaction_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
