"""interactions API routes — like/comment/rating with target:interaction binding + cache update"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app import crud, schemas
from app.database import get_db
from app.deps import require_current_user_id
from app.models.interaction import Interaction
from app.models.post import Post

router = APIRouter()


def _get_target(db: Session, target_type: str, target_id: int):
    """Validate target exists and is not deleted."""
    if target_type == "post":
        return crud.posts.get(db, id=target_id)
    elif target_type == "event":
        return crud.events.get(db, id=target_id)
    elif target_type == "resource":
        return crud.resources.get(db, id=target_id)
    return None


def _update_post_cache(db: Session, post_id: int):
    """Recalculate and update post cache fields (like_count, comment_count, average_rating)."""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return
    post.like_count = crud.target_interactions.count_by_target_and_type(
        db, target_type="post", target_id=post_id, interaction_type="like",
    )
    post.comment_count = crud.target_interactions.count_by_target_and_type(
        db, target_type="post", target_id=post_id, interaction_type="comment",
    )
    # Calculate average_rating from all rating interactions bound to this post
    rating_tis = crud.target_interactions.get_multi_by_target(
        db, target_type="post", target_id=post_id, interaction_type="rating",
    )
    if rating_tis:
        total = 0.0
        count = 0
        for ti in rating_tis:
            interaction = crud.interactions.get(db, id=ti.interaction_id)
            if interaction and interaction.value and isinstance(interaction.value, dict):
                scores = list(interaction.value.values())
                if scores:
                    total += sum(scores) / len(scores)
                    count += 1
        post.average_rating = round(total / count, 2) if count > 0 else None
    else:
        post.average_rating = None
    db.commit()
    db.refresh(post)


# --- Like endpoints ---

@router.get("/posts/{post_id}/like", tags=["interactions"])
def check_post_like_status(
    post_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_current_user_id),
):
    """Check if the current user has liked the post."""
    post = crud.posts.get(db, id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    liked = crud.target_interactions.has_like_by_user(db, target_type="post", target_id=post_id, user_id=user_id)
    return {"post_id": post_id, "liked": liked}


@router.post("/posts/{post_id}/like", status_code=status.HTTP_201_CREATED, tags=["interactions"])
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_current_user_id),
):
    post = crud.posts.get(db, id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    # Dedup check
    if crud.target_interactions.has_like_by_user(db, target_type="post", target_id=post_id, user_id=user_id):
        raise HTTPException(status_code=409, detail="Already liked this post")
    # Create interaction + binding
    interaction = Interaction(type="like", created_by=user_id)
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    crud.target_interactions.create(db, target_type="post", target_id=post_id, interaction_id=interaction.id)
    _update_post_cache(db, post_id)
    return {"post_id": post_id, "liked": True}


@router.delete("/posts/{post_id}/like", status_code=status.HTTP_204_NO_CONTENT, tags=["interactions"])
def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_current_user_id),
):
    post = crud.posts.get(db, id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    ti = crud.target_interactions.get_like_by_user(db, target_type="post", target_id=post_id, user_id=user_id)
    if ti is None:
        raise HTTPException(status_code=404, detail="Not liked")
    # Remove interaction + binding
    interaction_id = ti.interaction_id
    crud.target_interactions.remove(db, id=ti.id)
    interaction = crud.interactions.get(db, id=interaction_id)
    if interaction:
        db.delete(interaction)
        db.commit()
    _update_post_cache(db, post_id)
    return None


# --- Comment endpoints ---

@router.get("/posts/{post_id}/comments", response_model=schemas.PaginatedInteractionList, tags=["interactions"])
def list_post_comments(
    post_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    post = crud.posts.get(db, id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    # Get comments via target_interaction binding
    tis = crud.target_interactions.get_multi_by_target(
        db, target_type="post", target_id=post_id, interaction_type="comment",
    )
    # Build comment objects from the legacy Comment model for backward compatibility
    items = []
    for ti in tis:
        interaction = crud.interactions.get(db, id=ti.interaction_id)
        if interaction:
            items.append(interaction)
    total = len(items)
    return {"items": items[skip:skip+limit], "total": total, "skip": skip, "limit": limit}


@router.post("/posts/{post_id}/comments", response_model=schemas.Interaction, status_code=status.HTTP_201_CREATED, tags=["interactions"])
def add_post_comment(
    post_id: int,
    body: schemas.InteractionCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_current_user_id),
):
    post = crud.posts.get(db, id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    # Create comment interaction
    interaction = Interaction(type="comment", value=body.value, parent_id=body.parent_id, created_by=user_id)
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    crud.target_interactions.create(db, target_type="post", target_id=post_id, interaction_id=interaction.id)
    _update_post_cache(db, post_id)
    # Create notification for post author (and @mentions)
    from app.services.notification_events import notify_comment
    comment_text = body.value if isinstance(body.value, str) else None
    notify_comment(db, commenter_id=user_id, post_id=post_id, comment_content=comment_text)
    return interaction


# --- Rating endpoints ---

@router.get("/posts/{post_id}/ratings", response_model=schemas.PaginatedInteractionList, tags=["interactions"])
def list_post_ratings(
    post_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    post = crud.posts.get(db, id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    tis = crud.target_interactions.get_multi_by_target(
        db, target_type="post", target_id=post_id, interaction_type="rating",
    )
    items = []
    for ti in tis:
        interaction = crud.interactions.get(db, id=ti.interaction_id)
        if interaction:
            items.append(interaction)
    total = len(items)
    return {"items": items[skip:skip+limit], "total": total, "skip": skip, "limit": limit}


@router.post("/posts/{post_id}/ratings", response_model=schemas.Interaction, status_code=status.HTTP_201_CREATED, tags=["interactions"])
def submit_post_rating(
    post_id: int,
    body: schemas.InteractionCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_current_user_id),
):
    post = crud.posts.get(db, id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    # Create rating interaction
    interaction = Interaction(type="rating", value=body.value, created_by=user_id)
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    crud.target_interactions.create(db, target_type="post", target_id=post_id, interaction_id=interaction.id)
    _update_post_cache(db, post_id)
    return interaction
