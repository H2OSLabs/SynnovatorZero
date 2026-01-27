"""Category rule add schema"""
from pydantic import BaseModel
from typing import Optional


class CategoryRuleAdd(BaseModel):
    rule_id: int
    priority: Optional[int] = None
