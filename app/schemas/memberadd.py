"""Member add schema"""
from pydantic import BaseModel
from typing import Optional


class MemberAdd(BaseModel):
    user_id: int
    role: Optional[str] = "member"
