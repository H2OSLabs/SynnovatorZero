"""Event group add schema"""
from pydantic import BaseModel


class EventGroupAdd(BaseModel):
    group_id: int
