"""Rule Pydantic schemas"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List



# Shared properties
class RuleBase(BaseModel):
    """Rule 基础 schema"""
    name: str
    description: str
    allow_public: Optional[bool] = None
    require_review: Optional[bool] = None
    reviewers: Optional[List] = None
    submission_start: Optional[datetime] = None
    submission_deadline: Optional[datetime] = None
    submission_format: Optional[List] = None
    max_submissions: Optional[int] = None
    min_team_size: Optional[int] = None
    max_team_size: Optional[int] = None
    scoring_criteria: Optional[List] = None
    content: Optional[str] = None
    

# Properties to receive on creation
class RuleCreate(RuleBase):
    """创建 Rule 的请求 schema"""
    name: str
    description: str
    

# Properties to receive on update
class RuleUpdate(BaseModel):
    """更新 Rule 的请求 schema"""
    name: Optional[str] = None
    description: Optional[str] = None
    allow_public: Optional[bool] = None
    require_review: Optional[bool] = None
    reviewers: Optional[List] = None
    submission_start: Optional[datetime] = None
    submission_deadline: Optional[datetime] = None
    submission_format: Optional[List] = None
    max_submissions: Optional[int] = None
    min_team_size: Optional[int] = None
    max_team_size: Optional[int] = None
    scoring_criteria: Optional[List] = None
    content: Optional[str] = None
    

# Properties shared by models stored in DB
class RuleInDBBase(RuleBase):
    """数据库中的 Rule 基础 schema"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Properties to return to client
class Rule(RuleInDBBase):
    """Rule 响应 schema"""
    pass

# Properties stored in DB
class RuleInDB(RuleInDBBase):
    """数据库中存储的 Rule schema"""
    pass