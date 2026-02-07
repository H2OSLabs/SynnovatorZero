"""events API 路由"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app import crud, schemas
from app.database import get_db
from app.deps import get_current_user_id, require_current_user_id, require_role
from app.schemas.event import CATEGORY_STATUSES, CATEGORY_TYPES, VALID_STATUS_TRANSITIONS

router = APIRouter()


@router.get("/events", response_model=schemas.PaginatedEventList, tags=["events"])
def list_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(crud.events.model).filter(
        crud.events.model.deleted_at.is_(None),
    )
    if status is not None:
        if status not in CATEGORY_STATUSES:
            raise HTTPException(status_code=422, detail=f"Invalid status: {status}")
        query = query.filter(crud.events.model.status == status)
    if type is not None:
        if type not in CATEGORY_TYPES:
            raise HTTPException(status_code=422, detail=f"Invalid type: {type}")
        query = query.filter(crud.events.model.type == type)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return {"items": items, "total": total, "skip": skip, "limit": limit}


@router.post("/events", response_model=schemas.Event, status_code=status.HTTP_201_CREATED, tags=["events"])
def create_category(
    event_in: schemas.EventCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_role("organizer", "admin")),
):
    obj_data = event_in.model_dump()
    obj_data["created_by"] = user_id
    from app.models.event import Event as CategoryModel
    db_obj = CategoryModel(**obj_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/events/{event_id}", response_model=schemas.Event, tags=["events"])
def get_category(
    event_id: int,
    db: Session = Depends(get_db),
    current_user_id: Optional[int] = Depends(get_current_user_id),
):
    item = crud.events.get(db, id=event_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Event not found")
    # Draft events only visible to creator
    if item.status == "draft" and item.created_by != current_user_id:
        raise HTTPException(status_code=404, detail="Event not found")
    return item


@router.patch("/events/{event_id}", response_model=schemas.Event, tags=["events"])
def update_category(
    event_id: int,
    event_in: schemas.EventUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_role("organizer", "admin")),
):
    item = crud.events.get(db, id=event_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Event not found")
    # Ownership check: only creator or admin can update
    from app import crud as _crud
    current_user = _crud.users.get(db, id=user_id)
    if current_user and current_user.role != "admin" and item.created_by != user_id:
        raise HTTPException(status_code=403, detail="Not the event owner")

    # Validate status transition (draft → published → closed, strictly one-way)
    status_changed = False
    if event_in.status is not None and event_in.status != item.status:
        status_changed = True
        current_status = item.status
        new_status = event_in.status
        allowed = VALID_STATUS_TRANSITIONS.get(current_status, ())
        if new_status not in allowed:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid status transition: {current_status} → {new_status}. "
                       f"Allowed transitions: {current_status} → {', '.join(allowed) if allowed else '(none, terminal state)'}",
            )

    # Rule engine: pre-checks for event status change
    if status_changed:
        from app.services.rule_engine import run_pre_checks, RuleCheckError
        try:
            run_pre_checks(
                db,
                trigger="update_content(event.status)",
                event_id=event_id,
                context={"user_id": user_id, "new_status": new_status},
            )
        except RuleCheckError as e:
            raise HTTPException(status_code=422, detail=e.message)

    result = crud.events.update(db, db_obj=item, obj_in=event_in)
    # Rule engine: post-hooks for event status change
    if status_changed:
        from app.services.rule_engine import run_post_hooks
        run_post_hooks(
            db,
            trigger="update_content(event.status)",
            event_id=event_id,
            context={"user_id": user_id},
        )
    return result


@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["events"])
def delete_category(
    event_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_current_user_id),
):
    item = crud.events.get(db, id=event_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Event not found")

    # Permission check: creator or admin
    user = crud.users.get(db, id=user_id)
    if user.role != "admin" and item.created_by != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this event")

    from app.services.cascade_delete import cascade_delete_event
    cascade_delete_event(db, event_id)
    return None


# --- event:rule relationship endpoints ---

@router.get("/events/{event_id}/rules", response_model=list[schemas.EventRuleResponse], tags=["events"])
def list_category_rules(
    event_id: int,
    db: Session = Depends(get_db),
):
    item = crud.events.get(db, id=event_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return crud.event_rules.get_multi_by_category(db, event_id=event_id)


@router.post("/events/{event_id}/rules", response_model=schemas.EventRuleResponse, status_code=status.HTTP_201_CREATED, tags=["events"])
def add_category_rule(
    event_id: int,
    body: schemas.EventRuleAdd,
    db: Session = Depends(get_db),
):
    event = crud.events.get(db, id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    rule = crud.rules.get(db, id=body.rule_id)
    if rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    # Check duplicate
    existing = crud.event_rules.get_by_category_and_rule(db, event_id=event_id, rule_id=body.rule_id)
    if existing:
        raise HTTPException(status_code=409, detail="Rule already associated with this event")
    return crud.event_rules.create(db, event_id=event_id, rule_id=body.rule_id, priority=body.priority or 0)


@router.patch("/events/{event_id}/rules/{rule_id}", response_model=schemas.EventRuleResponse, tags=["events"])
def update_category_rule_priority(
    event_id: int,
    rule_id: int,
    body: schemas.EventRuleAdd,
    db: Session = Depends(get_db),
):
    rel = crud.event_rules.get_by_category_and_rule(db, event_id=event_id, rule_id=rule_id)
    if rel is None:
        raise HTTPException(status_code=404, detail="Event-rule relation not found")
    if body.priority is not None:
        rel = crud.event_rules.update_priority(db, db_obj=rel, priority=body.priority)
    return rel


@router.delete("/events/{event_id}/rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["events"])
def remove_category_rule(
    event_id: int,
    rule_id: int,
    db: Session = Depends(get_db),
):
    rel = crud.event_rules.get_by_category_and_rule(db, event_id=event_id, rule_id=rule_id)
    if rel is None:
        raise HTTPException(status_code=404, detail="Event-rule relation not found")
    crud.event_rules.remove_by_category_and_rule(db, event_id=event_id, rule_id=rule_id)
    return None


# --- event:post relationship endpoints ---

@router.get("/events/{event_id}/posts", response_model=list[schemas.EventPostResponse], tags=["events"])
def list_category_posts(
    event_id: int,
    relation_type: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user_id: Optional[int] = Depends(get_current_user_id),
):
    item = crud.events.get(db, id=event_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Event not found")
    rels = crud.event_posts.get_multi_by_category(
        db, event_id=event_id, relation_type=relation_type, skip=skip, limit=limit,
    )
    # Filter out draft and private posts for non-owners
    filtered = []
    for rel in rels:
        post = crud.posts.get(db, id=rel.post_id)
        if post is None:
            continue  # soft-deleted post
        if post.status == "draft" and post.created_by != current_user_id:
            continue
        if post.visibility == "private" and post.created_by != current_user_id:
            continue
        filtered.append(rel)
    return filtered


@router.post("/events/{event_id}/posts", response_model=schemas.EventPostResponse, status_code=status.HTTP_201_CREATED, tags=["events"])
def add_category_post(
    event_id: int,
    body: schemas.EventPostAdd,
    db: Session = Depends(get_db),
):
    event = crud.events.get(db, id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    post = crud.posts.get(db, id=body.post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    # Check duplicate
    existing = crud.event_posts.get_by_category_and_post(db, event_id=event_id, post_id=body.post_id)
    if existing:
        raise HTTPException(status_code=409, detail="Post already associated with this event")
    # Rule engine: pre-checks for create_relation(event_post)
    relation_type = body.relation_type or "submission"
    if relation_type == "submission":
        from app.services.rule_engine import run_pre_checks, RuleCheckError
        try:
            run_pre_checks(
                db,
                trigger="create_relation(event_post)",
                event_id=event_id,
                context={"user_id": post.created_by, "post_id": body.post_id},
            )
        except RuleCheckError as e:
            raise HTTPException(status_code=422, detail=e.message)
    result = crud.event_posts.create(db, event_id=event_id, post_id=body.post_id, relation_type=relation_type)
    # Rule engine: post-hooks
    if relation_type == "submission":
        from app.services.rule_engine import run_post_hooks
        run_post_hooks(
            db,
            trigger="create_relation(event_post)",
            event_id=event_id,
            context={"user_id": post.created_by, "post_id": body.post_id},
        )
    return result


@router.delete("/events/{event_id}/posts/{relation_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["events"])
def remove_category_post(
    event_id: int,
    relation_id: int,
    db: Session = Depends(get_db),
):
    rel = crud.event_posts.get(db, id=relation_id)
    if rel is None or rel.event_id != event_id:
        raise HTTPException(status_code=404, detail="Event-post relation not found")
    crud.event_posts.remove(db, id=relation_id)
    return None


# --- event:group relationship endpoints (team registration) ---

@router.get("/events/{event_id}/groups", response_model=list[schemas.EventGroupResponse], tags=["events"])
def list_category_groups(
    event_id: int,
    db: Session = Depends(get_db),
):
    item = crud.events.get(db, id=event_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return crud.event_groups.get_multi_by_category(db, event_id=event_id)


@router.post("/events/{event_id}/groups", response_model=schemas.EventGroupResponse, status_code=status.HTTP_201_CREATED, tags=["events"])
def add_category_group(
    event_id: int,
    body: schemas.EventGroupAdd,
    db: Session = Depends(get_db),
):
    event = crud.events.get(db, id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    group = crud.groups.get(db, id=body.group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    # Check duplicate registration
    existing = crud.event_groups.get_by_category_and_group(db, event_id=event_id, group_id=body.group_id)
    if existing:
        raise HTTPException(status_code=409, detail="Group already registered for this event")
    # Rule engine: pre-checks for create_relation(event_group)
    from app.services.rule_engine import run_pre_checks, RuleCheckError
    try:
        # Find group creator to use as user_id context
        ctx_user_id = group.created_by if group.created_by else None
        run_pre_checks(
            db,
            trigger="create_relation(event_group)",
            event_id=event_id,
            context={"user_id": ctx_user_id, "group_id": body.group_id},
        )
    except RuleCheckError as e:
        raise HTTPException(status_code=422, detail=e.message)
    return crud.event_groups.create(db, event_id=event_id, group_id=body.group_id)


@router.delete("/events/{event_id}/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["events"])
def remove_category_group(
    event_id: int,
    group_id: int,
    db: Session = Depends(get_db),
):
    rel = crud.event_groups.get_by_category_and_group(db, event_id=event_id, group_id=group_id)
    if rel is None:
        raise HTTPException(status_code=404, detail="Event-group relation not found")
    crud.event_groups.remove_by_category_and_group(db, event_id=event_id, group_id=group_id)
    return None


# --- event:event relationship endpoints (stage/track/prerequisite) ---

@router.get("/events/{event_id}/associations", response_model=list[schemas.EventEventResponse], tags=["events"])
def list_category_associations(
    event_id: int,
    relation_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    item = crud.events.get(db, id=event_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return crud.event_events.get_multi_by_source(db, source_event_id=event_id, relation_type=relation_type)


@router.post("/events/{event_id}/associations", response_model=schemas.EventEventResponse, status_code=status.HTTP_201_CREATED, tags=["events"])
def add_category_association(
    event_id: int,
    body: schemas.EventEventAdd,
    db: Session = Depends(get_db),
):
    source = crud.events.get(db, id=event_id)
    if source is None:
        raise HTTPException(status_code=404, detail="Source event not found")
    target = crud.events.get(db, id=body.target_event_id)
    if target is None:
        raise HTTPException(status_code=404, detail="Target event not found")
    # Self-reference check
    if event_id == body.target_event_id:
        raise HTTPException(status_code=422, detail="Cannot reference self")
    # Duplicate check
    existing = crud.event_events.get_by_source_and_target(
        db, source_event_id=event_id, target_event_id=body.target_event_id,
    )
    if existing:
        raise HTTPException(status_code=409, detail="Association already exists")
    # Cycle detection for stage/prerequisite
    if body.relation_type in ("stage", "prerequisite"):
        if crud.event_events.has_cycle(
            db, source_id=event_id, target_id=body.target_event_id,
            relation_type=body.relation_type,
        ):
            raise HTTPException(status_code=422, detail="Circular dependency detected")
    return crud.event_events.create(
        db, source_event_id=event_id, target_event_id=body.target_event_id,
        relation_type=body.relation_type, stage_order=body.stage_order,
    )


@router.delete("/events/{event_id}/associations/{target_event_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["events"])
def remove_category_association(
    event_id: int,
    target_event_id: int,
    db: Session = Depends(get_db),
):
    rel = crud.event_events.get_by_source_and_target(
        db, source_event_id=event_id, target_event_id=target_event_id,
    )
    if rel is None:
        raise HTTPException(status_code=404, detail="Event association not found")
    crud.event_events.remove_by_source_and_target(
        db, source_event_id=event_id, target_event_id=target_event_id,
    )
    return None
