"""Resource Pydantic schemas"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ResourceBase(BaseModel):
    filename: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    mime_type: Optional[str] = None
    size: Optional[int] = None
    url: Optional[str] = None


class ResourceCreate(ResourceBase):
    created_by: Optional[int] = None


class ResourceUpdate(BaseModel):
    display_name: Optional[str] = None
    description: Optional[str] = None


class ResourceInDBBase(ResourceBase):
    model_config = {"from_attributes": True}

    id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class Resource(ResourceInDBBase):
    pass


class ResourceInDB(ResourceInDBBase):
    pass