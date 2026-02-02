"""categories API 路由"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app import crud, schemas
from app.database import get_db
from app.deps import get_current_user_id, require_current_user_id, require_role
from app.schemas.category import VALID_STATUS_TRANSITIONS

router = APIRouter()


@router.get("/categories", response_model=schemas.PaginatedCategoryList, tags=["categories"])
def list_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    items = crud.categories.get_multi(db, skip=skip, limit=limit)
    total = len(items)
    return {"items": items, "total": total, "skip": skip, "limit": limit}


@router.post("/categories", response_model=schemas.Category, status_code=status.HTTP_201_CREATED, tags=["categories"])
def create_category(
    category_in: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_role("organizer", "admin")),
):
    obj_data = category_in.model_dump()
    obj_data["created_by"] = user_id
    from app.models.category import Category as CategoryModel
    db_obj = CategoryModel(**obj_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/categories/{category_id}", response_model=schemas.Category, tags=["categories"])
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user_id: Optional[int] = Depends(get_current_user_id),
):
    item = crud.categories.get(db, id=category_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Category not found")
    # Draft categories only visible to creator
    if item.status == "draft" and item.created_by != current_user_id:
        raise HTTPException(status_code=404, detail="Category not found")
    return item


@router.patch("/categories/{category_id}", response_model=schemas.Category, tags=["categories"])
def update_category(
    category_id: int,
    category_in: schemas.CategoryUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_role("organizer", "admin")),
):
    item = crud.categories.get(db, id=category_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Category not found")
    # Ownership check: only creator or admin can update
    from app import crud as _crud
    current_user = _crud.users.get(db, id=user_id)
    if current_user and current_user.role != "admin" and item.created_by != user_id:
        raise HTTPException(status_code=403, detail="Not the category owner")

    # Validate status transition (draft → published → closed, strictly one-way)
    status_changed = False
    if category_in.status is not None and category_in.status != item.status:
        status_changed = True
        current_status = item.status
        new_status = category_in.status
        allowed = VALID_STATUS_TRANSITIONS.get(current_status, ())
        if new_status not in allowed:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid status transition: {current_status} → {new_status}. "
                       f"Allowed transitions: {current_status} → {', '.join(allowed) if allowed else '(none, terminal state)'}",
            )

    # Rule engine: pre-checks for category status change
    if status_changed:
        from app.services.rule_engine import run_pre_checks, RuleCheckError
        try:
            run_pre_checks(
                db,
                trigger="update_content(category.status)",
                category_id=category_id,
                context={"user_id": user_id, "new_status": new_status},
            )
        except RuleCheckError as e:
            raise HTTPException(status_code=422, detail=e.message)

    result = crud.categories.update(db, db_obj=item, obj_in=category_in)
    # Rule engine: post-hooks for category status change
    if status_changed:
        from app.services.rule_engine import run_post_hooks
        run_post_hooks(
            db,
            trigger="update_content(category.status)",
            category_id=category_id,
            context={"user_id": user_id},
        )
    return result


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["categories"])
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_current_user_id),
):
    item = crud.categories.get(db, id=category_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Category not found")

    # Permission check: creator or admin
    user = crud.users.get(db, id=user_id)
    if user.role != "admin" and item.created_by != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this category")

    from app.services.cascade_delete import cascade_delete_category
    cascade_delete_category(db, category_id)
    return None


# --- category:rule relationship endpoints ---

@router.get("/categories/{category_id}/rules", response_model=list[schemas.CategoryRuleResponse], tags=["categories"])
def list_category_rules(
    category_id: int,
    db: Session = Depends(get_db),
):
    item = crud.categories.get(db, id=category_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.category_rules.get_multi_by_category(db, category_id=category_id)


@router.post("/categories/{category_id}/rules", response_model=schemas.CategoryRuleResponse, status_code=status.HTTP_201_CREATED, tags=["categories"])
def add_category_rule(
    category_id: int,
    body: schemas.CategoryRuleAdd,
    db: Session = Depends(get_db),
):
    category = crud.categories.get(db, id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    rule = crud.rules.get(db, id=body.rule_id)
    if rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    # Check duplicate
    existing = crud.category_rules.get_by_category_and_rule(db, category_id=category_id, rule_id=body.rule_id)
    if existing:
        raise HTTPException(status_code=409, detail="Rule already associated with this category")
    return crud.category_rules.create(db, category_id=category_id, rule_id=body.rule_id, priority=body.priority or 0)


@router.patch("/categories/{category_id}/rules/{rule_id}", response_model=schemas.CategoryRuleResponse, tags=["categories"])
def update_category_rule_priority(
    category_id: int,
    rule_id: int,
    body: schemas.CategoryRuleAdd,
    db: Session = Depends(get_db),
):
    rel = crud.category_rules.get_by_category_and_rule(db, category_id=category_id, rule_id=rule_id)
    if rel is None:
        raise HTTPException(status_code=404, detail="Category-rule relation not found")
    if body.priority is not None:
        rel = crud.category_rules.update_priority(db, db_obj=rel, priority=body.priority)
    return rel


@router.delete("/categories/{category_id}/rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["categories"])
def remove_category_rule(
    category_id: int,
    rule_id: int,
    db: Session = Depends(get_db),
):
    rel = crud.category_rules.get_by_category_and_rule(db, category_id=category_id, rule_id=rule_id)
    if rel is None:
        raise HTTPException(status_code=404, detail="Category-rule relation not found")
    crud.category_rules.remove_by_category_and_rule(db, category_id=category_id, rule_id=rule_id)
    return None


# --- category:post relationship endpoints ---

@router.get("/categories/{category_id}/posts", response_model=list[schemas.CategoryPostResponse], tags=["categories"])
def list_category_posts(
    category_id: int,
    relation_type: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user_id: Optional[int] = Depends(get_current_user_id),
):
    item = crud.categories.get(db, id=category_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Category not found")
    rels = crud.category_posts.get_multi_by_category(
        db, category_id=category_id, relation_type=relation_type, skip=skip, limit=limit,
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


@router.post("/categories/{category_id}/posts", response_model=schemas.CategoryPostResponse, status_code=status.HTTP_201_CREATED, tags=["categories"])
def add_category_post(
    category_id: int,
    body: schemas.CategoryPostAdd,
    db: Session = Depends(get_db),
):
    category = crud.categories.get(db, id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    post = crud.posts.get(db, id=body.post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    # Check duplicate
    existing = crud.category_posts.get_by_category_and_post(db, category_id=category_id, post_id=body.post_id)
    if existing:
        raise HTTPException(status_code=409, detail="Post already associated with this category")
    # Rule engine: pre-checks for create_relation(category_post)
    relation_type = body.relation_type or "submission"
    if relation_type == "submission":
        from app.services.rule_engine import run_pre_checks, RuleCheckError
        try:
            run_pre_checks(
                db,
                trigger="create_relation(category_post)",
                category_id=category_id,
                context={"user_id": post.created_by, "post_id": body.post_id},
            )
        except RuleCheckError as e:
            raise HTTPException(status_code=422, detail=e.message)
    result = crud.category_posts.create(db, category_id=category_id, post_id=body.post_id, relation_type=relation_type)
    # Rule engine: post-hooks
    if relation_type == "submission":
        from app.services.rule_engine import run_post_hooks
        run_post_hooks(
            db,
            trigger="create_relation(category_post)",
            category_id=category_id,
            context={"user_id": post.created_by, "post_id": body.post_id},
        )
    return result


@router.delete("/categories/{category_id}/posts/{relation_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["categories"])
def remove_category_post(
    category_id: int,
    relation_id: int,
    db: Session = Depends(get_db),
):
    rel = crud.category_posts.get(db, id=relation_id)
    if rel is None or rel.category_id != category_id:
        raise HTTPException(status_code=404, detail="Category-post relation not found")
    crud.category_posts.remove(db, id=relation_id)
    return None


# --- category:group relationship endpoints (team registration) ---

@router.get("/categories/{category_id}/groups", response_model=list[schemas.CategoryGroupResponse], tags=["categories"])
def list_category_groups(
    category_id: int,
    db: Session = Depends(get_db),
):
    item = crud.categories.get(db, id=category_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.category_groups.get_multi_by_category(db, category_id=category_id)


@router.post("/categories/{category_id}/groups", response_model=schemas.CategoryGroupResponse, status_code=status.HTTP_201_CREATED, tags=["categories"])
def add_category_group(
    category_id: int,
    body: schemas.CategoryGroupAdd,
    db: Session = Depends(get_db),
):
    category = crud.categories.get(db, id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    group = crud.groups.get(db, id=body.group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    # Check duplicate registration
    existing = crud.category_groups.get_by_category_and_group(db, category_id=category_id, group_id=body.group_id)
    if existing:
        raise HTTPException(status_code=409, detail="Group already registered for this category")
    # Rule engine: pre-checks for create_relation(category_group)
    from app.services.rule_engine import run_pre_checks, RuleCheckError
    try:
        # Find group creator to use as user_id context
        ctx_user_id = group.created_by if group.created_by else None
        run_pre_checks(
            db,
            trigger="create_relation(category_group)",
            category_id=category_id,
            context={"user_id": ctx_user_id, "group_id": body.group_id},
        )
    except RuleCheckError as e:
        raise HTTPException(status_code=422, detail=e.message)
    return crud.category_groups.create(db, category_id=category_id, group_id=body.group_id)


@router.delete("/categories/{category_id}/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["categories"])
def remove_category_group(
    category_id: int,
    group_id: int,
    db: Session = Depends(get_db),
):
    rel = crud.category_groups.get_by_category_and_group(db, category_id=category_id, group_id=group_id)
    if rel is None:
        raise HTTPException(status_code=404, detail="Category-group relation not found")
    crud.category_groups.remove_by_category_and_group(db, category_id=category_id, group_id=group_id)
    return None


# --- category:category relationship endpoints (stage/track/prerequisite) ---

@router.get("/categories/{category_id}/associations", response_model=list[schemas.CategoryCategoryResponse], tags=["categories"])
def list_category_associations(
    category_id: int,
    relation_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    item = crud.categories.get(db, id=category_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.category_categories.get_multi_by_source(db, source_category_id=category_id, relation_type=relation_type)


@router.post("/categories/{category_id}/associations", response_model=schemas.CategoryCategoryResponse, status_code=status.HTTP_201_CREATED, tags=["categories"])
def add_category_association(
    category_id: int,
    body: schemas.CategoryCategoryAdd,
    db: Session = Depends(get_db),
):
    source = crud.categories.get(db, id=category_id)
    if source is None:
        raise HTTPException(status_code=404, detail="Source category not found")
    target = crud.categories.get(db, id=body.target_category_id)
    if target is None:
        raise HTTPException(status_code=404, detail="Target category not found")
    # Self-reference check
    if category_id == body.target_category_id:
        raise HTTPException(status_code=422, detail="Cannot reference self")
    # Duplicate check
    existing = crud.category_categories.get_by_source_and_target(
        db, source_category_id=category_id, target_category_id=body.target_category_id,
    )
    if existing:
        raise HTTPException(status_code=409, detail="Association already exists")
    # Cycle detection for stage/prerequisite
    if body.relation_type in ("stage", "prerequisite"):
        if crud.category_categories.has_cycle(
            db, source_id=category_id, target_id=body.target_category_id,
            relation_type=body.relation_type,
        ):
            raise HTTPException(status_code=422, detail="Circular dependency detected")
    return crud.category_categories.create(
        db, source_category_id=category_id, target_category_id=body.target_category_id,
        relation_type=body.relation_type, stage_order=body.stage_order,
    )


@router.delete("/categories/{category_id}/associations/{target_category_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["categories"])
def remove_category_association(
    category_id: int,
    target_category_id: int,
    db: Session = Depends(get_db),
):
    rel = crud.category_categories.get_by_source_and_target(
        db, source_category_id=category_id, target_category_id=target_category_id,
    )
    if rel is None:
        raise HTTPException(status_code=404, detail="Category association not found")
    crud.category_categories.remove_by_source_and_target(
        db, source_category_id=category_id, target_category_id=target_category_id,
    )
    return None
