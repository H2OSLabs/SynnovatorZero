"""PostResource Pydantic schemas — post:resource relationship"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PostResourceResponse(BaseModel):
    id: int
    post_id: int
    resource_id: int
    display_type: str
    position: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}
