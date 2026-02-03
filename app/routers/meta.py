from fastapi import APIRouter
from pydantic import BaseModel

from app.schemas.enums import PostType

router = APIRouter()


class PostTypeListResponse(BaseModel):
    items: list[PostType]
    default: PostType


@router.get("/meta/post-types", response_model=PostTypeListResponse)
def get_post_types():
    return {"items": list(PostType), "default": PostType.general}

