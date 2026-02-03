"""Notification schemas"""
from datetime import datetime
from typing import Optional, List
from enum import Enum

from pydantic import BaseModel, ConfigDict


class NotificationType(str, Enum):
    award = "award"
    comment = "comment"
    team_request = "team_request"
    follow = "follow"
    mention = "mention"
    system = "system"


class NotificationBase(BaseModel):
    type: NotificationType
    title: Optional[str] = None
    content: str
    related_url: Optional[str] = None


class NotificationCreate(NotificationBase):
    user_id: int
    actor_id: Optional[int] = None


class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None


class NotificationInDBBase(NotificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    actor_id: Optional[int] = None
    is_read: bool
    created_at: datetime


class Notification(NotificationInDBBase):
    pass


class PaginatedNotificationList(BaseModel):
    items: List[Notification]
    total: int
    skip: int
    limit: int
    unread_count: Optional[int] = None
