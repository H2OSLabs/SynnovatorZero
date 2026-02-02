"""Rating Pydantic schemas"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Any, Dict, Optional


class RatingBase(BaseModel):
    scores: Dict[str, Any]
    comment: Optional[str] = None


class RatingCreate(RatingBase):
    target_id: int
    target_type: str
    created_by: str


class RatingUpdate(BaseModel):
    scores: Optional[Dict[str, Any]] = None
    comment: Optional[str] = None


class RatingInDBBase(RatingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    target_id: int
    target_type: str
    created_by: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class Rating(RatingInDBBase):
    pass
