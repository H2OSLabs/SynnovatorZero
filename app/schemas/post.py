"""Post Pydantic schemas"""
from pydantic import BaseModel
from datetime import datetime
from typing import List, Literal, Optional

from app.schemas.enums import PostType


POST_TYPES = tuple(t.value for t in PostType)
POST_STATUSES = ("draft", "pending_review", "published", "rejected")
POST_VISIBILITIES = ("public", "private")

# Valid status transitions:
#   draft → pending_review → published | rejected
#   rejected → draft (resubmit after revision)
#   private posts: draft → published (skip pending_review)
VALID_POST_STATUS_TRANSITIONS = {
    "draft": ("pending_review", "published"),
    "pending_review": ("published", "rejected"),
    "published": (),
    "rejected": ("draft",),
}


class PostBase(BaseModel):
    title: str
    type: PostType = PostType.general
    tags: Optional[List[str]] = None
    status: Literal["draft", "pending_review", "published", "rejected"] = "draft"
    visibility: Literal["public", "private"] = "public"
    content: Optional[str] = None


class PostCreate(PostBase):
    title: str


class PostUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[PostType] = None
    tags: Optional[List[str]] = None
    status: Optional[Literal["draft", "pending_review", "published", "rejected"]] = None
    visibility: Optional[Literal["public", "private"]] = None
    content: Optional[str] = None


class PostInDBBase(PostBase):
    id: int
    created_by: Optional[int] = None
    like_count: int = 0
    comment_count: int = 0
    average_rating: Optional[float] = None
    deleted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class Post(PostInDBBase):
    pass
