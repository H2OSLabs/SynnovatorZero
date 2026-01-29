"""UserUser Pydantic schemas — user:user relationship (follow/block)"""
from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional


class UserUserCreate(BaseModel):
    source_user_id: int
    target_user_id: int
    relation_type: Literal["follow", "block"]


class UserUserResponse(BaseModel):
    id: int
    source_user_id: int
    target_user_id: int
    relation_type: str
    created_at: datetime

    model_config = {"from_attributes": True}
