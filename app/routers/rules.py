"""rules API 路由"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app import crud, schemas
from app.database import get_db
from app.deps import get_current_user_id, require_current_user_id, require_role

router = APIRouter()


@router.get("/rules", response_model=schemas.PaginatedRuleList, tags=["rules"])
def list_rules(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    items = crud.rules.get_multi(db, skip=skip, limit=limit)
    total = len(items)
    return {"items": items, "total": total, "skip": skip, "limit": limit}


@router.post("/rules", response_model=schemas.Rule, status_code=status.HTTP_201_CREATED, tags=["rules"])
def create_rule(
    rule_in: schemas.RuleCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_role("organizer", "admin")),
):
    obj_data = rule_in.model_dump()
    obj_data["created_by"] = user_id
    from app.models.rule import Rule as RuleModel
    db_obj = RuleModel(**obj_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/rules/{rule_id}", response_model=schemas.Rule, tags=["rules"])
def get_rule(
    rule_id: int,
    db: Session = Depends(get_db),
):
    item = crud.rules.get(db, id=rule_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return item


@router.patch("/rules/{rule_id}", response_model=schemas.Rule, tags=["rules"])
def update_rule(
    rule_id: int,
    rule_in: schemas.RuleUpdate,
    db: Session = Depends(get_db),
):
    item = crud.rules.get(db, id=rule_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return crud.rules.update(db, db_obj=item, obj_in=rule_in)


@router.delete("/rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["rules"])
def delete_rule(
    rule_id: int,
    db: Session = Depends(get_db),
):
    item = crud.rules.get(db, id=rule_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    from app.services.cascade_delete import cascade_delete_rule
    cascade_delete_rule(db, rule_id)
    return None
