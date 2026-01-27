"""posts API 路由"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Any, List, Optional

from app import crud, schemas
from app.database import get_db

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
):
    return crud.posts.create(db, obj_in=post_in)


@router.get("/posts/{post_id}", response_model=schemas.Post, tags=["posts"])
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    item = crud.posts.get(db, id=post_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return item


@router.patch("/posts/{post_id}", response_model=schemas.Post, tags=["posts"])
def update_post(
    post_id: int,
    post_in: schemas.PostUpdate,
    db: Session = Depends(get_db),
):
    item = crud.posts.get(db, id=post_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.posts.update(db, db_obj=item, obj_in=post_in)


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["posts"])
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    item = crud.posts.get(db, id=post_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Post not found")
    crud.posts.remove(db, id=post_id)
    return None


@router.get("/posts/{post_id}/resources", tags=["posts"])
def list_post_resources(
    post_id: int,
    db: Session = Depends(get_db),
):
    # TODO: Implement with relationship table
    item = crud.posts.get(db, id=post_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return []


@router.post("/posts/{post_id}/resources", status_code=status.HTTP_201_CREATED, tags=["posts"])
def add_post_resource(
    post_id: int,
    body: schemas.PostResourceAdd,
    db: Session = Depends(get_db),
):
    # TODO: Implement with relationship table
    item = crud.posts.get(db, id=post_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post_id": post_id, "resource_id": body.resource_id}


@router.get("/posts/{post_id}/related", tags=["posts"])
def list_post_related(
    post_id: int,
    relation_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    # TODO: Implement with relationship table
    item = crud.posts.get(db, id=post_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return []


@router.post("/posts/{post_id}/related", status_code=status.HTTP_201_CREATED, tags=["posts"])
def add_post_related(
    post_id: int,
    body: schemas.PostRelationAdd,
    db: Session = Depends(get_db),
):
    # TODO: Implement with relationship table
    item = crud.posts.get(db, id=post_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post_id": post_id, "target_post_id": body.target_post_id}
