"""resources API 路由"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app import crud, schemas
from app.database import get_db
from app.deps import get_current_user_id, require_current_user_id

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
    current_user_id: int = Depends(require_current_user_id),
):
    resource_in.created_by = current_user_id
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


@router.patch("/resources/{resource_id}", response_model=schemas.Resource, tags=["resources"])
def update_resource(
    resource_id: int,
    resource_in: schemas.ResourceUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_current_user_id),
):
    item = crud.resources.get(db, id=resource_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    # Permission check: creator or admin
    user = crud.users.get(db, id=user_id)
    if user.role != "admin" and item.created_by != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this resource")

    return crud.resources.update(db, db_obj=item, obj_in=resource_in)


@router.delete("/resources/{resource_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["resources"])
def delete_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_current_user_id),
):
    item = crud.resources.get(db, id=resource_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    # Permission check: creator or admin
    user = crud.users.get(db, id=user_id)
    if user.role != "admin" and item.created_by != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this resource")

    crud.resources.remove(db, id=resource_id)
    return None


@router.post("/resources/{resource_id}/copy-request", status_code=status.HTTP_202_ACCEPTED, tags=["resources"])
def request_copy_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(require_current_user_id),
):
    resource = crud.resources.get(db, id=resource_id)
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
        
    if resource.created_by == user_id:
        raise HTTPException(status_code=400, detail="Cannot copy your own resource (just use it)")
        
    from app.services.notification_events import notify_asset_copy_request
    notify_asset_copy_request(db, requester_id=user_id, resource_id=resource_id)
    
    return {"message": "Copy request sent"}


@router.post("/resources/{resource_id}/copy-approve", response_model=schemas.Resource, status_code=status.HTTP_201_CREATED, tags=["resources"])
def approve_copy_resource(
    resource_id: int,
    requester_id: int = Query(..., description="User ID of the requester"),
    db: Session = Depends(get_db),
    user_id: int = Depends(require_current_user_id),
):
    resource = crud.resources.get(db, id=resource_id)
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
        
    # Only owner can approve
    if resource.created_by != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to approve copy of this resource")
        
    # Check if requester exists
    requester = crud.users.get(db, id=requester_id)
    if not requester:
        raise HTTPException(status_code=404, detail="Requester not found")
        
    # Perform copy
    # We create a new resource with same data but new owner
    new_resource_in = schemas.ResourceCreate(
        name=f"{resource.name} (Copy)",
        type=resource.type,
        url=resource.url,
        description=resource.description,
        meta_info=resource.meta_info
    )
    new_resource_in.created_by = requester_id
    new_resource = crud.resources.create(db, obj_in=new_resource_in)
    
    # Notify requester
    from app.services.notification_events import notify_asset_copy_result
    notify_asset_copy_result(db, requester_id=requester_id, resource_id=resource_id, result="accepted")
    
    return new_resource


@router.post("/resources/{resource_id}/copy-reject", status_code=status.HTTP_204_NO_CONTENT, tags=["resources"])
def reject_copy_resource(
    resource_id: int,
    requester_id: int = Query(..., description="User ID of the requester"),
    db: Session = Depends(get_db),
    user_id: int = Depends(require_current_user_id),
):
    resource = crud.resources.get(db, id=resource_id)
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
        
    if resource.created_by != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    from app.services.notification_events import notify_asset_copy_result
    notify_asset_copy_result(db, requester_id=requester_id, resource_id=resource_id, result="rejected")
    
    return None
