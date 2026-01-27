"""users API 路由"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Literal, Optional

from app import crud, schemas
from app.database import get_db
from app.deps import require_current_user_id

router = APIRouter()


@router.get("/users", response_model=schemas.PaginatedUserList, tags=["users"])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    role: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    items = crud.users.get_multi(db, skip=skip, limit=limit)
    if role:
        items = [u for u in items if u.role == role]
    total = len(items)
    return {"items": items, "total": total, "skip": skip, "limit": limit}


@router.post("/users", response_model=schemas.User, status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    existing = crud.users.get_by_username(db, username=user_in.username)
    if existing:
        raise HTTPException(status_code=409, detail="Username already exists")
    existing = crud.users.get_by_email(db, email=user_in.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")
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
    # Check uniqueness if username is being changed
    if user_in.username and user_in.username != item.username:
        existing = crud.users.get_by_username(db, username=user_in.username)
        if existing:
            raise HTTPException(status_code=409, detail="Username already exists")
    # Check uniqueness if email is being changed
    if user_in.email and user_in.email != item.email:
        existing = crud.users.get_by_email(db, email=user_in.email)
        if existing:
            raise HTTPException(status_code=409, detail="Email already exists")
    return crud.users.update(db, db_obj=item, obj_in=user_in)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    item = crud.users.get(db, id=user_id)
    if item is None:
        raise HTTPException(status_code=404, detail="User not found")
    from app.services.cascade_delete import cascade_delete_user
    cascade_delete_user(db, user_id)
    return None


# --- user:user relationship endpoints (follow/block) ---

@router.post("/users/{user_id}/follow", response_model=schemas.UserUserResponse, status_code=status.HTTP_201_CREATED, tags=["users"])
def follow_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(require_current_user_id),
):
    """Current user follows target user_id."""
    if current_user_id == user_id:
        raise HTTPException(status_code=422, detail="Cannot follow self")
    target = crud.users.get(db, id=user_id)
    if target is None:
        raise HTTPException(status_code=404, detail="User not found")
    # Check if target has blocked current user
    if crud.user_users.has_block(db, blocker_id=user_id, blocked_id=current_user_id):
        raise HTTPException(status_code=403, detail="Blocked by target user")
    # Check duplicate
    existing = crud.user_users.get_relation(
        db, source_user_id=current_user_id, target_user_id=user_id, relation_type="follow",
    )
    if existing:
        raise HTTPException(status_code=409, detail="Already following this user")
    return crud.user_users.create(db, source_user_id=current_user_id, target_user_id=user_id, relation_type="follow")


@router.delete("/users/{user_id}/follow", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def unfollow_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(require_current_user_id),
):
    """Current user unfollows target user_id."""
    rel = crud.user_users.get_relation(
        db, source_user_id=current_user_id, target_user_id=user_id, relation_type="follow",
    )
    if rel is None:
        raise HTTPException(status_code=404, detail="Not following this user")
    crud.user_users.remove(db, source_user_id=current_user_id, target_user_id=user_id, relation_type="follow")
    return None


@router.post("/users/{user_id}/block", response_model=schemas.UserUserResponse, status_code=status.HTTP_201_CREATED, tags=["users"])
def block_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(require_current_user_id),
):
    """Current user blocks target user_id."""
    if current_user_id == user_id:
        raise HTTPException(status_code=422, detail="Cannot block self")
    target = crud.users.get(db, id=user_id)
    if target is None:
        raise HTTPException(status_code=404, detail="User not found")
    existing = crud.user_users.get_relation(
        db, source_user_id=current_user_id, target_user_id=user_id, relation_type="block",
    )
    if existing:
        raise HTTPException(status_code=409, detail="Already blocked this user")
    return crud.user_users.create(db, source_user_id=current_user_id, target_user_id=user_id, relation_type="block")


@router.delete("/users/{user_id}/block", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def unblock_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(require_current_user_id),
):
    """Current user unblocks target user_id."""
    rel = crud.user_users.get_relation(
        db, source_user_id=current_user_id, target_user_id=user_id, relation_type="block",
    )
    if rel is None:
        raise HTTPException(status_code=404, detail="Not blocking this user")
    crud.user_users.remove(db, source_user_id=current_user_id, target_user_id=user_id, relation_type="block")
    return None


@router.get("/users/{user_id}/following", response_model=list[schemas.UserUserResponse], tags=["users"])
def list_following(
    user_id: int,
    db: Session = Depends(get_db),
):
    """List users that user_id is following."""
    user = crud.users.get(db, id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.user_users.get_following(db, user_id=user_id)


@router.get("/users/{user_id}/followers", response_model=list[schemas.UserUserResponse], tags=["users"])
def list_followers(
    user_id: int,
    db: Session = Depends(get_db),
):
    """List users who follow user_id."""
    user = crud.users.get(db, id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.user_users.get_followers(db, user_id=user_id)


@router.get("/users/{user_id}/is-friend/{other_id}", tags=["users"])
def check_friendship(
    user_id: int,
    other_id: int,
    db: Session = Depends(get_db),
):
    """Check if two users are mutual friends."""
    return {"is_friend": crud.user_users.is_mutual_follow(db, user_a=user_id, user_b=other_id)}
