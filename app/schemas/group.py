"""Group Pydantic schemas"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional



# Shared properties
class GroupBase(BaseModel):
    """Group 基础 schema"""
    name: str
    description: Optional[str] = None
    visibility: str
    max_members: Optional[int] = None
    require_approval: Optional[bool] = None
    

# Properties to receive on creation
class GroupCreate(GroupBase):
    """创建 Group 的请求 schema"""
    name: str
    visibility: str
    

# Properties to receive on update
class GroupUpdate(BaseModel):
    """更新 Group 的请求 schema"""
    name: Optional[str] = None
    description: Optional[str] = None
    visibility: Optional[str] = None
    max_members: Optional[int] = None
    require_approval: Optional[bool] = None
    

# Properties shared by models stored in DB
class GroupInDBBase(GroupBase):
    """数据库中的 Group 基础 schema"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Properties to return to client
class Group(GroupInDBBase):
    """Group 响应 schema"""
    pass

# Properties stored in DB
class GroupInDB(GroupInDBBase):
    """数据库中存储的 Group schema"""
    pass