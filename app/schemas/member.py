"""Member Pydantic schemas"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MemberBase(BaseModel):
    role: str
    status: str


class MemberCreate(MemberBase):
    group_id: int
    user_id: int


class MemberUpdate(BaseModel):
    role: Optional[str] = None
    status: Optional[str] = None


class MemberInDBBase(MemberBase):
    id: int
    group_id: int
    user_id: int
    joined_at: Optional[datetime] = None
    status_changed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Member(MemberInDBBase):
    pass
