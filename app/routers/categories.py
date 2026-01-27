"""categories API 路由"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Any, List, Optional

from app import crud, schemas
from app.database import get_db

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
):
    return crud.categories.create(db, obj_in=category_in)


@router.get("/categories/{category_id}", response_model=schemas.Category, tags=["categories"])
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    item = crud.categories.get(db, id=category_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return item


@router.patch("/categories/{category_id}", response_model=schemas.Category, tags=["categories"])
def update_category(
    category_id: int,
    category_in: schemas.CategoryUpdate,
    db: Session = Depends(get_db),
):
    item = crud.categories.get(db, id=category_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.categories.update(db, db_obj=item, obj_in=category_in)


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["categories"])
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    item = crud.categories.get(db, id=category_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Category not found")
    crud.categories.remove(db, id=category_id)
    return None


@router.get("/categories/{category_id}/rules", tags=["categories"])
def list_category_rules(
    category_id: int,
    db: Session = Depends(get_db),
):
    # TODO: Implement with relationship table
    item = crud.categories.get(db, id=category_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return []


@router.post("/categories/{category_id}/rules", status_code=status.HTTP_201_CREATED, tags=["categories"])
def add_category_rule(
    category_id: int,
    body: schemas.CategoryRuleAdd,
    db: Session = Depends(get_db),
):
    # TODO: Implement with relationship table
    item = crud.categories.get(db, id=category_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"category_id": category_id, "rule_id": body.rule_id}


@router.delete("/categories/{category_id}/rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["categories"])
def remove_category_rule(
    category_id: int,
    rule_id: int,
    db: Session = Depends(get_db),
):
    # TODO: Implement with relationship table
    return None


@router.get("/categories/{category_id}/posts", response_model=schemas.PaginatedPostList, tags=["categories"])
def list_category_posts(
    category_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    relation_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    # TODO: Implement with relationship table
    item = crud.categories.get(db, id=category_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"items": [], "total": 0, "skip": skip, "limit": limit}


@router.post("/categories/{category_id}/posts", status_code=status.HTTP_201_CREATED, tags=["categories"])
def add_category_post(
    category_id: int,
    body: schemas.CategoryPostAdd,
    db: Session = Depends(get_db),
):
    # TODO: Implement with relationship table
    item = crud.categories.get(db, id=category_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"category_id": category_id, "post_id": body.post_id}


@router.get("/categories/{category_id}/groups", tags=["categories"])
def list_category_groups(
    category_id: int,
    db: Session = Depends(get_db),
):
    # TODO: Implement with relationship table
    item = crud.categories.get(db, id=category_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return []


@router.post("/categories/{category_id}/groups", status_code=status.HTTP_201_CREATED, tags=["categories"])
def add_category_group(
    category_id: int,
    body: schemas.CategoryGroupAdd,
    db: Session = Depends(get_db),
):
    # TODO: Implement with relationship table
    item = crud.categories.get(db, id=category_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"category_id": category_id, "group_id": body.group_id}
