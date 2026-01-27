"""Resource Pydantic schemas"""
from pydantic import BaseModel, AnyUrl
from datetime import datetime
from typing import Optional



# Shared properties
class ResourceBase(BaseModel):
    """Resource 基础 schema"""
    filename: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    mime_type: Optional[str] = None
    size: Optional[int] = None
    url: Optional[AnyUrl] = None
    

# Properties to receive on creation
class ResourceCreate(ResourceBase):
    """创建 Resource 的请求 schema"""
    filename: str
    

# Properties to receive on update
class ResourceUpdate(BaseModel):
    """更新 Resource 的请求 schema"""
    filename: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    mime_type: Optional[str] = None
    size: Optional[int] = None
    url: Optional[AnyUrl] = None
    

# Properties shared by models stored in DB
class ResourceInDBBase(ResourceBase):
    """数据库中的 Resource 基础 schema"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Properties to return to client
class Resource(ResourceInDBBase):
    """Resource 响应 schema"""
    pass

# Properties stored in DB
class ResourceInDB(ResourceInDBBase):
    """数据库中存储的 Resource schema"""
    pass