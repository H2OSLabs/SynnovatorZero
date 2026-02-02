"""posts API 路由"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app import crud, schemas
from app.database import get_db
from app.deps import get_current_user_id, require_current_user_id, require_role
from app.schemas.post import VALID_POST_STATUS_TRANSITIONS

router = APIRouter()


@router.get("/posts", response_model=schemas.PaginatedPostList, tags=["posts"])
def list_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    type: Optional[str] = Query(None),
    post_status: Optional[str] = Query(None, alias="status"),
    tags: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    items = crud.posts.get_multi(db, skip=skip, limit=limit)
    total = len(items)
    return {"items": items, "total": total, "skip": skip, "limit": limit}


@router.post("/posts", response_model=schemas.Post, status_code=status.HTTP_201_CREATED, tags=["posts"])
def create_post(
    post_in: schemas.PostCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_current_user_id),
):
    obj_data = post_in.model_dump()
    obj_data["created_by"] = user_id
    from app.models.post import Post as PostModel
    db_obj = PostModel(**obj_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/posts/{post_id}", response_model=schemas.Post, tags=["posts"])
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user_id: Optional[int] = Depends(get_current_user_id),
):
    item = crud.posts.get(db, id=post_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Post not found")
    # Visibility: draft posts only visible to author
    if item.status == "draft" and item.created_by != current_user_id:
        raise HTTPException(status_code=404, detail="Post not found")
    # Visibility: private posts only visible to author
    if item.visibility == "private" and item.created_by != current_user_id:
        raise HTTPException(status_code=404, detail="Post not found")
    return item


@router.patch("/posts/{post_id}", response_model=schemas.Post, tags=["posts"])
def update_post(
    post_id: int,
    post_in: schemas.PostUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_current_user_id),
):
    item = crud.posts.get(db, id=post_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Post not found")

    # Permission check: author or admin
    user = crud.users.get(db, id=user_id)
    if user.role != "admin" and item.created_by != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")

    # Validate status transition
    if post_in.status is not None and post_in.status != item.status:
        current_status = item.status
        new_status = post_in.status
        allowed = VALID_POST_STATUS_TRANSITIONS.get(current_status, ())
        if new_status not in allowed:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid status transition: {current_status} → {new_status}. "
                       f"Allowed: {current_status} → {', '.join(allowed) if allowed else '(none, terminal state)'}",
            )

    return crud.posts.update(db, db_obj=item, obj_in=post_in)


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["posts"])
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_current_user_id),
):
    item = crud.posts.get(db, id=post_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Post not found")

    # Permission check: author or admin
    user = crud.users.get(db, id=user_id)
    if user.role != "admin" and item.created_by != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")

    from app.services.cascade_delete import cascade_delete_post
    cascade_delete_post(db, post_id)
    return None


# --- post:resource relationship endpoints ---

@router.get("/posts/{post_id}/resources", response_model=list[schemas.PostResourceResponse], tags=["posts"])
def list_post_resources(
    post_id: int,
    db: Session = Depends(get_db),
):
    item = crud.posts.get(db, id=post_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.post_resources.get_multi_by_post(db, post_id=post_id)


@router.post("/posts/{post_id}/resources", response_model=schemas.PostResourceResponse, status_code=status.HTTP_201_CREATED, tags=["posts"])
def add_post_resource(
    post_id: int,
    body: schemas.PostResourceAdd,
    db: Session = Depends(get_db),
):
    post = crud.posts.get(db, id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    resource = crud.resources.get(db, id=body.resource_id)
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    # Check duplicate
    existing = crud.post_resources.get_by_post_and_resource(db, post_id=post_id, resource_id=body.resource_id)
    if existing:
        raise HTTPException(status_code=409, detail="Resource already attached to this post")
    return crud.post_resources.create(
        db, post_id=post_id, resource_id=body.resource_id,
        display_type=body.display_type or "attachment", position=body.position,
    )


@router.patch("/posts/{post_id}/resources/{relation_id}", response_model=schemas.PostResourceResponse, tags=["posts"])
def update_post_resource(
    post_id: int,
    relation_id: int,
    body: schemas.PostResourceAdd,
    db: Session = Depends(get_db),
):
    post = crud.posts.get(db, id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    rel = crud.post_resources.get(db, id=relation_id)
    if rel is None or rel.post_id != post_id:
        raise HTTPException(status_code=404, detail="Post-resource relation not found")
    return crud.post_resources.update(db, db_obj=rel, display_type=body.display_type, position=body.position)


@router.delete("/posts/{post_id}/resources/{relation_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["posts"])
def remove_post_resource(
    post_id: int,
    relation_id: int,
    db: Session = Depends(get_db),
):
    post = crud.posts.get(db, id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    rel = crud.post_resources.get(db, id=relation_id)
    if rel is None or rel.post_id != post_id:
        raise HTTPException(status_code=404, detail="Post-resource relation not found")
    crud.post_resources.remove(db, id=relation_id)
    return None


# --- post:post relationship endpoints ---

@router.get("/posts/{post_id}/related", response_model=list[schemas.PostPostResponse], tags=["posts"])
def list_post_related(
    post_id: int,
    relation_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    item = crud.posts.get(db, id=post_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.post_posts.get_multi_by_source(db, source_post_id=post_id, relation_type=relation_type)


@router.post("/posts/{post_id}/related", response_model=schemas.PostPostResponse, status_code=status.HTTP_201_CREATED, tags=["posts"])
def add_post_related(
    post_id: int,
    body: schemas.PostRelationAdd,
    db: Session = Depends(get_db),
):
    post = crud.posts.get(db, id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    target = crud.posts.get(db, id=body.target_post_id)
    if target is None:
        raise HTTPException(status_code=404, detail="Target post not found")
    return crud.post_posts.create(
        db, source_post_id=post_id, target_post_id=body.target_post_id,
        relation_type=body.relation_type or "reference", position=body.position,
    )


@router.patch("/posts/{post_id}/related/{relation_id}", response_model=schemas.PostPostResponse, tags=["posts"])
def update_post_related(
    post_id: int,
    relation_id: int,
    body: schemas.PostRelationAdd,
    db: Session = Depends(get_db),
):
    post = crud.posts.get(db, id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    rel = crud.post_posts.get(db, id=relation_id)
    if rel is None or rel.source_post_id != post_id:
        raise HTTPException(status_code=404, detail="Post relation not found")
    return crud.post_posts.update(db, db_obj=rel, relation_type=body.relation_type, position=body.position)


@router.delete("/posts/{post_id}/related/{relation_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["posts"])
def remove_post_related(
    post_id: int,
    relation_id: int,
    db: Session = Depends(get_db),
):
    post = crud.posts.get(db, id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    rel = crud.post_posts.get(db, id=relation_id)
    if rel is None or rel.source_post_id != post_id:
        raise HTTPException(status_code=404, detail="Post relation not found")
    crud.post_posts.remove(db, id=relation_id)
    return None
