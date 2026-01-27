"""interactions API 路由"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Any, List, Optional

from app import crud, schemas
from app.database import get_db

router = APIRouter()


@router.post("/posts/{post_id}/like", status_code=status.HTTP_201_CREATED, tags=["interactions"])
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    # TODO: Implement like with current user
    item = crud.posts.get(db, id=post_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post_id": post_id, "liked": True}


@router.delete("/posts/{post_id}/like", status_code=status.HTTP_204_NO_CONTENT, tags=["interactions"])
def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    # TODO: Implement unlike with current user
    return None


@router.get("/posts/{post_id}/comments", response_model=schemas.PaginatedCommentList, tags=["interactions"])
def list_post_comments(
    post_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    # TODO: Filter comments by post_id
    item = crud.posts.get(db, id=post_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"items": [], "total": 0, "skip": skip, "limit": limit}


@router.post("/posts/{post_id}/comments", response_model=schemas.Comment, status_code=status.HTTP_201_CREATED, tags=["interactions"])
def add_post_comment(
    post_id: int,
    body: schemas.CommentCreate,
    db: Session = Depends(get_db),
):
    item = crud.posts.get(db, id=post_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.comments.create(db, obj_in=body)


@router.patch("/posts/{post_id}/comments/{comment_id}", response_model=schemas.Comment, tags=["interactions"])
def update_post_comment(
    post_id: int,
    comment_id: int,
    body: schemas.CommentUpdate,
    db: Session = Depends(get_db),
):
    item = crud.comments.get(db, id=comment_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return crud.comments.update(db, db_obj=item, obj_in=body)


@router.delete("/posts/{post_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["interactions"])
def delete_post_comment(
    post_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
):
    item = crud.comments.get(db, id=comment_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    crud.comments.remove(db, id=comment_id)
    return None


@router.get("/posts/{post_id}/ratings", response_model=schemas.PaginatedRatingList, tags=["interactions"])
def list_post_ratings(
    post_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    # TODO: Filter ratings by post_id
    item = crud.posts.get(db, id=post_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"items": [], "total": 0, "skip": skip, "limit": limit}


@router.post("/posts/{post_id}/ratings", response_model=schemas.Rating, status_code=status.HTTP_201_CREATED, tags=["interactions"])
def submit_post_rating(
    post_id: int,
    body: schemas.RatingCreate,
    db: Session = Depends(get_db),
):
    item = crud.posts.get(db, id=post_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.ratings.create(db, obj_in=body)
