"""CategoryGroup Pydantic schemas — category:group relationship"""
from pydantic import BaseModel
from datetime import datetime


class CategoryGroupResponse(BaseModel):
    id: int
    category_id: int
    group_id: int
    registered_at: datetime

    model_config = {"from_attributes": True}
