"""User Pydantic schemas"""
from pydantic import BaseModel, EmailStr, AnyUrl
from datetime import datetime
from typing import Optional



# Shared properties
class UserBase(BaseModel):
    """User 基础 schema"""
    username: str
    email: EmailStr
    display_name: Optional[str] = None
    avatar_url: Optional[AnyUrl] = None
    bio: Optional[str] = None
    role: str
    

# Properties to receive on creation
class UserCreate(UserBase):
    """创建 User 的请求 schema"""
    username: str
    email: EmailStr
    role: str
    

# Properties to receive on update
class UserUpdate(BaseModel):
    """更新 User 的请求 schema"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    display_name: Optional[str] = None
    avatar_url: Optional[AnyUrl] = None
    bio: Optional[str] = None
    role: Optional[str] = None
    

# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    """数据库中的 User 基础 schema"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Properties to return to client
class User(UserInDBBase):
    """User 响应 schema"""
    pass

# Properties stored in DB
class UserInDB(UserInDBBase):
    """数据库中存储的 User schema"""
    pass