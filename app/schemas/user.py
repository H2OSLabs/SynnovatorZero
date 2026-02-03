"""User Pydantic schemas"""
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Literal, Optional

VALID_ROLES = ("participant", "organizer", "admin")


class UserBase(BaseModel):
    username: str
    email: EmailStr
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    role: Literal["participant", "organizer", "admin"] = "participant"


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    role: Optional[Literal["participant", "organizer", "admin"]] = None


class UserInDBBase(UserBase):
    model_config = {"from_attributes": True}

    id: int
    follower_count: int = 0
    following_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    pass