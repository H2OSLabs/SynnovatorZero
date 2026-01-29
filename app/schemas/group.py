"""Group Pydantic schemas"""
from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional


VISIBILITY_VALUES = ("public", "private")


class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    visibility: Literal["public", "private"] = "public"
    max_members: Optional[int] = None
    require_approval: Optional[bool] = False


class GroupCreate(GroupBase):
    name: str


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    visibility: Optional[Literal["public", "private"]] = None
    max_members: Optional[int] = None
    require_approval: Optional[bool] = None


class GroupInDBBase(GroupBase):
    id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class Group(GroupInDBBase):
    pass
