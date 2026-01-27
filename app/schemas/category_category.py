"""CategoryCategory Pydantic schemas — category:category relationship"""
from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional


class CategoryCategoryAdd(BaseModel):
    target_category_id: int
    relation_type: Literal["stage", "track", "prerequisite"]
    stage_order: Optional[int] = None


class CategoryCategoryResponse(BaseModel):
    id: int
    source_category_id: int
    target_category_id: int
    relation_type: str
    stage_order: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}
