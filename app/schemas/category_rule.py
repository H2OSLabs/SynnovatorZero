"""CategoryRule Pydantic schemas — category:rule relationship"""
from pydantic import BaseModel
from datetime import datetime


class CategoryRuleResponse(BaseModel):
    id: int
    category_id: int
    rule_id: int
    priority: int
    created_at: datetime

    model_config = {"from_attributes": True}
