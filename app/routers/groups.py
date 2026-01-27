"""groups API 路由"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app import crud, schemas
from app.database import get_db
from app.deps import get_current_user_id, require_current_user_id

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
    user_id: int = Depends(require_current_user_id),
):
    obj_data = group_in.model_dump()
    obj_data["created_by"] = user_id
    from app.models.group import Group as GroupModel
    db_obj = GroupModel(**obj_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/groups/{group_id}", response_model=schemas.Group, tags=["groups"])
def get_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user_id: Optional[int] = Depends(get_current_user_id),
):
    item = crud.groups.get(db, id=group_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Group not found")
    # Private groups only visible to members or creator
    if item.visibility == "private":
        if current_user_id is None:
            raise HTTPException(status_code=404, detail="Group not found")
        if item.created_by != current_user_id:
            member = crud.members.get_by_group_and_user(db, group_id=group_id, user_id=current_user_id)
            if member is None:
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
    from app.services.cascade_delete import cascade_delete_group
    cascade_delete_group(db, group_id)
    return None


# --- Group member endpoints (group:user relationship) ---

@router.get("/groups/{group_id}/members", response_model=schemas.PaginatedMemberList, tags=["groups"])
def list_group_members(
    group_id: int,
    member_status: Optional[str] = Query(None, alias="status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    item = crud.groups.get(db, id=group_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Group not found")
    items = crud.members.get_multi_by_group(db, group_id=group_id, status=member_status, skip=skip, limit=limit)
    total = crud.members.count_by_group(db, group_id=group_id, status=member_status)
    return {"items": items, "total": total, "skip": skip, "limit": limit}


@router.post("/groups/{group_id}/members", response_model=schemas.Member, status_code=status.HTTP_201_CREATED, tags=["groups"])
def add_group_member(
    group_id: int,
    body: schemas.MemberAdd,
    db: Session = Depends(get_db),
):
    group = crud.groups.get(db, id=group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    # Check duplicate membership
    existing = crud.members.get_by_group_and_user(db, group_id=group_id, user_id=body.user_id)
    if existing:
        raise HTTPException(status_code=409, detail="User is already a member of this group")
    # Rule engine: pre-checks for create_relation(group_user)
    # Find categories this group is registered to and run checks
    cat_groups = crud.category_groups.get_multi_by_group(db, group_id=group_id)
    for cg in cat_groups:
        from app.services.rule_engine import run_pre_checks, RuleCheckError
        try:
            run_pre_checks(
                db,
                trigger="create_relation(group_user)",
                category_id=cg.category_id,
                context={"user_id": body.user_id, "group_id": group_id},
            )
        except RuleCheckError as e:
            raise HTTPException(status_code=422, detail=e.message)

    # Determine initial status based on group's require_approval setting
    initial_status = "pending" if getattr(group, "require_approval", True) else "accepted"
    return crud.members.create(
        db, group_id=group_id, user_id=body.user_id,
        role=body.role or "member", status=initial_status,
    )


@router.patch("/groups/{group_id}/members/{user_id}", response_model=schemas.Member, tags=["groups"])
def update_group_member(
    group_id: int,
    user_id: int,
    body: schemas.MemberUpdate,
    db: Session = Depends(get_db),
):
    group = crud.groups.get(db, id=group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    member = crud.members.get_by_group_and_user(db, group_id=group_id, user_id=user_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    if body.status is not None:
        member = crud.members.update_status(db, db_obj=member, new_status=body.status)
    if body.role is not None:
        member = crud.members.update_role(db, db_obj=member, new_role=body.role)
    return member


@router.delete("/groups/{group_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["groups"])
def remove_group_member(
    group_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    group = crud.groups.get(db, id=group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    member = crud.members.get_by_group_and_user(db, group_id=group_id, user_id=user_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    crud.members.remove_by_group_and_user(db, group_id=group_id, user_id=user_id)
    return None
