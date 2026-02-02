"""resources API 路由"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app import crud, schemas
from app.database import get_db
from app.deps import get_current_user_id, require_current_user_id

router = APIRouter()


@router.get("/resources", response_model=schemas.PaginatedResourceList, tags=["resources"])
def list_resources(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    items = crud.resources.get_multi(db, skip=skip, limit=limit)
    total = len(items)
    return {"items": items, "total": total, "skip": skip, "limit": limit}


@router.post("/resources", response_model=schemas.Resource, status_code=status.HTTP_201_CREATED, tags=["resources"])
def create_resource(
    resource_in: schemas.ResourceCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(require_current_user_id),
):
    resource_in.created_by = current_user_id
    return crud.resources.create(db, obj_in=resource_in)


@router.get("/resources/{resource_id}", response_model=schemas.Resource, tags=["resources"])
def get_resource(
    resource_id: int,
    db: Session = Depends(get_db),
):
    item = crud.resources.get(db, id=resource_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return item


@router.patch("/resources/{resource_id}", response_model=schemas.Resource, tags=["resources"])
def update_resource(
    resource_id: int,
    resource_in: schemas.ResourceUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_current_user_id),
):
    item = crud.resources.get(db, id=resource_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    # Permission check: creator or admin
    user = crud.users.get(db, id=user_id)
    if user.role != "admin" and item.created_by != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this resource")

    return crud.resources.update(db, db_obj=item, obj_in=resource_in)


@router.delete("/resources/{resource_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["resources"])
def delete_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_current_user_id),
):
    item = crud.resources.get(db, id=resource_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    # Permission check: creator or admin
    user = crud.users.get(db, id=user_id)
    if user.role != "admin" and item.created_by != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this resource")

    crud.resources.remove(db, id=resource_id)
    return None
