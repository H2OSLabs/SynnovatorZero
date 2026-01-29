"""Interaction Pydantic schemas — unified for like/comment/rating"""
from pydantic import BaseModel
from datetime import datetime
from typing import Any, Dict, Literal, Optional


INTERACTION_TYPES = ("like", "comment", "rating")


class InteractionBase(BaseModel):
    type: Literal["like", "comment", "rating"]
    value: Optional[Any] = None  # comment→str, rating→dict, like→None
    parent_id: Optional[int] = None  # for nested comments


class InteractionCreate(InteractionBase):
    pass


class InteractionUpdate(BaseModel):
    value: Optional[Any] = None


class InteractionInDBBase(InteractionBase):
    id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class Interaction(InteractionInDBBase):
    pass
