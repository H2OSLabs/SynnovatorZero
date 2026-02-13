"""groups API 路由"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app import crud, schemas
from app.database import get_db
from app.deps import get_current_user_id, require_current_user_id
from app.schemas.group import VISIBILITY_VALUES

router = APIRouter()


@router.get("/groups", response_model=schemas.PaginatedGroupList, tags=["groups"])
def list_groups(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    visibility: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    from sqlalchemy import or_, func
    query = db.query(crud.groups.model).filter(
        crud.groups.model.deleted_at.is_(None),
    )
    
    if q is not None and q.strip():
        q_norm = q.strip().lower()
        like = f"%{q_norm}%"
        query = query.filter(
            or_(
                func.lower(crud.groups.model.name).like(like),
                func.lower(crud.groups.model.description).like(like),
            )
        )
        
    if visibility is not None:
        if visibility not in VISIBILITY_VALUES:
            raise HTTPException(status_code=422, detail=f"Invalid visibility: {visibility}")
        query = query.filter(crud.groups.model.visibility == visibility)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
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

    # Auto-add creator as owner member
    crud.members.create(
        db, group_id=db_obj.id, user_id=user_id,
        role="owner", status="accepted",
    )

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
    user_id: int = Depends(require_current_user_id),
):
    item = crud.groups.get(db, id=group_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Group not found")

    # Permission check: owner, admin member, or platform admin
    user = crud.users.get(db, id=user_id)
    if user.role != "admin":
        if item.created_by != user_id:
            member = crud.members.get_by_group_and_user(db, group_id=group_id, user_id=user_id)
            if member is None or member.role != "admin":
                raise HTTPException(status_code=403, detail="Not authorized to update this group")

    return crud.groups.update(db, db_obj=item, obj_in=group_in)


@router.delete("/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["groups"])
def delete_group(
    group_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_current_user_id),
):
    item = crud.groups.get(db, id=group_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Group not found")

    # Permission check: owner or platform admin
    user = crud.users.get(db, id=user_id)
    if user.role != "admin" and item.created_by != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this group")

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
    current_user_id: int = Depends(require_current_user_id),
):
    group = crud.groups.get(db, id=group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
        
    # Check duplicate membership
    existing = crud.members.get_by_group_and_user(db, group_id=group_id, user_id=body.user_id)
    if existing:
        raise HTTPException(status_code=409, detail="User is already a member of this group")

    # Determine mode: Application or Invitation
    is_application = (body.user_id == current_user_id)
    
    if not is_application:
        # Invitation: Only owner/admin can invite others
        # Check permissions
        is_authorized = False
        if group.created_by == current_user_id:
            is_authorized = True
        else:
            admin_member = crud.members.get_by_group_and_user(db, group_id=group_id, user_id=current_user_id)
            if admin_member and admin_member.role == "admin":
                is_authorized = True
        
        if not is_authorized:
            raise HTTPException(status_code=403, detail="Only group admins can invite members")
            
    # Rule engine: pre-checks for create_relation(group_user)
    cat_groups = crud.event_groups.get_multi_by_group(db, group_id=group_id)
    for cg in cat_groups:
        from app.services.rule_engine import run_pre_checks, RuleCheckError
        try:
            run_pre_checks(
                db,
                trigger="create_relation(group_user)",
                event_id=cg.event_id,
                context={"user_id": body.user_id, "group_id": group_id},
            )
        except RuleCheckError as e:
            raise HTTPException(status_code=422, detail=e.message)

    if is_application:
        # User applying to join
        initial_status = "pending" if getattr(group, "require_approval", True) else "accepted"
        member = crud.members.create(
            db, group_id=group_id, user_id=body.user_id,
            role=body.role or "member", status=initial_status,
        )
        
        # Send notification if pending
        if initial_status == "pending":
            applicant = crud.users.get(db, id=body.user_id)
            applicant_name = applicant.username if applicant else "Someone"
            
            if group.created_by:
                crud.notifications.create(
                    db,
                    user_id=group.created_by,
                    type="team_apply",
                    title="团队加入申请",
                    content=f"用户 {applicant_name} 申请加入团队 {group.name}",
                    related_url=f"/users/{body.user_id}?apply_group_id={group_id}",
                    actor_id=body.user_id,
                )
    else:
        # Invitation
        initial_status = "invited"
        member = crud.members.create(
            db, group_id=group_id, user_id=body.user_id,
            role=body.role or "member", status=initial_status,
        )
        
        # Send notification to invitee
        from app.services.notification_events import notify_team_invite
        notify_team_invite(
            db,
            inviter_id=current_user_id,
            invitee_id=body.user_id,
            group_id=group_id
        )
            
    return member


@router.patch("/groups/{group_id}/members/{user_id}", response_model=schemas.Member, tags=["groups"])
def update_group_member(
    group_id: int,
    user_id: int,
    body: schemas.MemberUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(require_current_user_id),
):
    group = crud.groups.get(db, id=group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
        
    member = crud.members.get_by_group_and_user(db, group_id=group_id, user_id=user_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")

    # Permission check:
    # 1. Group Owner/Admin can update any member status (e.g. approve pending, kick member)
    # 2. User themselves can update status if invited (accept/reject)
    
    is_admin = False
    if group.created_by == current_user_id:
        is_admin = True
    else:
        admin_member = crud.members.get_by_group_and_user(db, group_id=group_id, user_id=current_user_id)
        if admin_member and admin_member.role == "admin":
            is_admin = True
        else:
             # Also allow platform admin
            user = crud.users.get(db, id=current_user_id)
            if user.role == "admin":
                is_admin = True

    is_self = (user_id == current_user_id)
    
    if not is_admin:
        # If not admin, check if self-update for invitation
        if is_self and member.status == "invited" and body.status in ["accepted", "rejected"]:
            pass # Allowed
        else:
            raise HTTPException(status_code=403, detail="Not authorized to update member status")

    if body.status is not None:
        # If admin changing pending -> accepted/rejected (Reviewing application)
        if is_admin and member.status == "pending" and body.status in ["accepted", "rejected"]:
            member = crud.members.update_status(db, db_obj=member, new_status=body.status)
            
            # Send notification to applicant
            status_text = "通过" if body.status == "accepted" else "拒绝"
            crud.notifications.create(
                db,
                user_id=user_id,
                type="team_apply_result",
                title=f"申请被{status_text}",
                content=f"您申请加入团队 {group.name} 的请求已被{status_text}",
                related_url=f"/groups/{group_id}",
                actor_id=current_user_id,
            )
            
        # If user changing invited -> accepted/rejected (Responding to invitation)
        elif is_self and member.status == "invited" and body.status in ["accepted", "rejected"]:
             member = crud.members.update_status(db, db_obj=member, new_status=body.status)
             
             # Notify inviter (we don't track inviter in Member model easily unless we add a column, 
             # but we can notify group owner/admins)
             # Let's assume notify group owner for now as simplified "inviter"
             from app.services.notification_events import notify_team_invite_result
             if group.created_by:
                 notify_team_invite_result(
                     db,
                     inviter_id=group.created_by, # Should ideally be the actual inviter, but we lack that data in Member.
                     invitee_id=user_id,
                     group_id=group_id,
                     result=body.status
                 )

        # Admin force updating other statuses (e.g. banning) - general case
        elif is_admin:
             member = crud.members.update_status(db, db_obj=member, new_status=body.status)
             
        else:
             raise HTTPException(status_code=403, detail="Invalid status transition")
            
    if body.role is not None:
        if not is_admin:
             raise HTTPException(status_code=403, detail="Only admins can change roles")
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


@router.get("/my/groups", response_model=schemas.PaginatedGroupList, tags=["groups"])
def list_my_groups(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None, description="Filter by membership status"),
    db: Session = Depends(get_db),
    user_id: int = Depends(require_current_user_id),
):
    """List groups the current user is a member of."""
    memberships = crud.members.get_multi_by_user(db, user_id=user_id, status=status, skip=skip, limit=limit)
    total = crud.members.count_by_user(db, user_id=user_id, status=status)

    # Fetch the actual group objects
    groups = []
    for m in memberships:
        group = crud.groups.get(db, id=m.group_id)
        if group:
            groups.append(group)

    return {"items": groups, "total": total, "skip": skip, "limit": limit}
