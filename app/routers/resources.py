"""resources API 路由"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Any, List, Optional

from app import crud, schemas
from app.database import get_db

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
):
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


@router.delete("/resources/{resource_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["resources"])
def delete_resource(
    resource_id: int,
    db: Session = Depends(get_db),
):
    item = crud.resources.get(db, id=resource_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    crud.resources.remove(db, id=resource_id)
    return None
