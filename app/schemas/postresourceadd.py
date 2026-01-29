"""Post resource add schema — body for POST /posts/{id}/resources"""
from pydantic import BaseModel
from typing import Literal, Optional


class PostResourceAdd(BaseModel):
    resource_id: int
    display_type: Optional[Literal["attachment", "inline"]] = "attachment"
    position: Optional[int] = None
