"""Member add schema — lightweight body for POST /groups/{id}/members"""
from pydantic import BaseModel
from typing import Literal, Optional


class MemberAdd(BaseModel):
    user_id: int
    role: Optional[Literal["owner", "admin", "member"]] = "member"
