"""Event Pydantic schemas"""
from pydantic import BaseModel
from datetime import datetime
from typing import List, Literal, Optional


CATEGORY_TYPES = ("competition", "operation")
CATEGORY_STATUSES = ("draft", "published", "closed")

# Valid status transitions: draft → published → closed
VALID_STATUS_TRANSITIONS = {
    "draft": ("published",),
    "published": ("closed",),
    "closed": (),
}


class EventBase(BaseModel):
    name: str
    description: str
    type: Literal["competition", "operation"]
    status: Literal["draft", "published", "closed"] = "draft"
    cover_image: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    tags: Optional[List[str]] = None
    content: Optional[str] = None


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[Literal["competition", "operation"]] = None
    status: Optional[Literal["draft", "published", "closed"]] = None
    cover_image: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    tags: Optional[List[str]] = None
    content: Optional[str] = None


class EventInDBBase(EventBase):
    id: int
    created_by: Optional[int] = None
    participant_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class Event(EventInDBBase):
    pass
