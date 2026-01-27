"""Post resource add schema"""
from pydantic import BaseModel
from typing import Optional


class PostResourceAdd(BaseModel):
    resource_id: int
    display_type: Optional[str] = "attachment"
    position: Optional[int] = None
