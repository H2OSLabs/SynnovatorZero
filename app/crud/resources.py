"""Resource CRUD operations"""
from app.crud.base import CRUDBase
from app.models.resource import Resource
from app.schemas.resource import ResourceCreate, ResourceUpdate


class CRUDResource(CRUDBase[Resource, ResourceCreate, ResourceUpdate]):
    pass


resources = CRUDResource(Resource)
