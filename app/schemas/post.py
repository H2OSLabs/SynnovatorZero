"""Post Pydantic schemas"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List



# Shared properties
class PostBase(BaseModel):
    """Post 基础 schema"""
    title: str
    type: str
    tags: Optional[List] = None
    status: str
    like_count: Optional[int] = None
    comment_count: Optional[int] = None
    average_rating: Optional[float] = None
    content: Optional[str] = None
    

# Properties to receive on creation
class PostCreate(PostBase):
    """创建 Post 的请求 schema"""
    title: str
    type: str
    status: str
    

# Properties to receive on update
class PostUpdate(BaseModel):
    """更新 Post 的请求 schema"""
    title: Optional[str] = None
    type: Optional[str] = None
    tags: Optional[List] = None
    status: Optional[str] = None
    like_count: Optional[int] = None
    comment_count: Optional[int] = None
    average_rating: Optional[float] = None
    content: Optional[str] = None
    

# Properties shared by models stored in DB
class PostInDBBase(PostBase):
    """数据库中的 Post 基础 schema"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Properties to return to client
class Post(PostInDBBase):
    """Post 响应 schema"""
    pass

# Properties stored in DB
class PostInDB(PostInDBBase):
    """数据库中存储的 Post schema"""
    pass