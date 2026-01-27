"""groups API 路由"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Any, List, Optional

from app import crud, schemas
from app.database import get_db

router = APIRouter()


@router.get("/groups", response_model=schemas.PaginatedGroupList, tags=["groups"])
def list_groups(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    visibility: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    items = crud.groups.get_multi(db, skip=skip, limit=limit)
    total = len(items)
    return {"items": items, "total": total, "skip": skip, "limit": limit}


@router.post("/groups", response_model=schemas.Group, status_code=status.HTTP_201_CREATED, tags=["groups"])
def create_group(
    group_in: schemas.GroupCreate,
    db: Session = Depends(get_db),
):
    return crud.groups.create(db, obj_in=group_in)


@router.get("/groups/{group_id}", response_model=schemas.Group, tags=["groups"])
def get_group(
    group_id: int,
    db: Session = Depends(get_db),
):
    item = crud.groups.get(db, id=group_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return item


@router.patch("/groups/{group_id}", response_model=schemas.Group, tags=["groups"])
def update_group(
    group_id: int,
    group_in: schemas.GroupUpdate,
    db: Session = Depends(get_db),
):
    item = crud.groups.get(db, id=group_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return crud.groups.update(db, db_obj=item, obj_in=group_in)


@router.delete("/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["groups"])
def delete_group(
    group_id: int,
    db: Session = Depends(get_db),
):
    item = crud.groups.get(db, id=group_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Group not found")
    crud.groups.remove(db, id=group_id)
    return None


@router.get("/groups/{group_id}/members", response_model=schemas.PaginatedMemberList, tags=["groups"])
def list_group_members(
    group_id: int,
    member_status: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
):
    # TODO: Implement with member query
    item = crud.groups.get(db, id=group_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return {"items": [], "total": 0, "skip": 0, "limit": 100}


@router.post("/groups/{group_id}/members", status_code=status.HTTP_201_CREATED, tags=["groups"])
def add_group_member(
    group_id: int,
    body: schemas.MemberAdd,
    db: Session = Depends(get_db),
):
    # TODO: Implement with member creation
    item = crud.groups.get(db, id=group_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return {"group_id": group_id, "user_id": body.user_id}


@router.patch("/groups/{group_id}/members/{user_id}", response_model=schemas.Member, tags=["groups"])
def update_group_member(
    group_id: int,
    user_id: int,
    body: schemas.MemberUpdate,
    db: Session = Depends(get_db),
):
    # TODO: Implement with member query
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/groups/{group_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["groups"])
def remove_group_member(
    group_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    # TODO: Implement with member deletion
    return None
