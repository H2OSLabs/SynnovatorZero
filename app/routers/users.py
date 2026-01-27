"""users API 路由"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Any, List, Optional

from app import crud, schemas
from app.database import get_db

router = APIRouter()


@router.get("/users", response_model=schemas.PaginatedUserList, tags=["users"])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    role: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    items = crud.users.get_multi(db, skip=skip, limit=limit)
    total = len(items)
    return {"items": items, "total": total, "skip": skip, "limit": limit}


@router.post("/users", response_model=schemas.User, status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    return crud.users.create(db, obj_in=user_in)


@router.get("/users/{user_id}", response_model=schemas.User, tags=["users"])
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    item = crud.users.get(db, id=user_id)
    if item is None:
        raise HTTPException(status_code=404, detail="User not found")
    return item


@router.patch("/users/{user_id}", response_model=schemas.User, tags=["users"])
def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    db: Session = Depends(get_db),
):
    item = crud.users.get(db, id=user_id)
    if item is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.users.update(db, db_obj=item, obj_in=user_in)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    item = crud.users.get(db, id=user_id)
    if item is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.users.remove(db, id=user_id)
    return None
