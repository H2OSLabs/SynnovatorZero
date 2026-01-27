"""Rule CRUD operations"""
from app.crud.base import CRUDBase
from app.models.rule import Rule
from app.schemas.rule import RuleCreate, RuleUpdate


class CRUDRule(CRUDBase[Rule, RuleCreate, RuleUpdate]):
    pass


rules = CRUDRule(Rule)
