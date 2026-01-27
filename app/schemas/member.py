"""Member Pydantic schemas — group:user relationship"""
from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional


class MemberBase(BaseModel):
    role: Literal["owner", "admin", "member"] = "member"
    status: Literal["pending", "accepted", "rejected"] = "pending"


class MemberCreate(MemberBase):
    group_id: int
    user_id: int


class MemberUpdate(BaseModel):
    role: Optional[Literal["owner", "admin", "member"]] = None
    status: Optional[Literal["pending", "accepted", "rejected"]] = None


class MemberInDBBase(MemberBase):
    id: int
    group_id: int
    user_id: int
    joined_at: Optional[datetime] = None
    status_changed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class Member(MemberInDBBase):
    pass
