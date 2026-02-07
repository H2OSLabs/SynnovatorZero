"""CRUD 操作模块"""
from app.crud.base import CRUDBase
from app.crud.users import users
from app.crud.resources import resources
from app.crud.events import events
from app.crud.posts import posts
from app.crud.rules import rules
from app.crud.groups import groups
from app.crud.interactions import interactions, comments, ratings
from app.crud.members import members
from app.crud.user_users import user_users
from app.crud.post_resources import post_resources
from app.crud.post_posts import post_posts
from app.crud.event_rules import event_rules
from app.crud.event_posts import event_posts
from app.crud.event_groups import event_groups
from app.crud.target_interactions import target_interactions
from app.crud.event_events import event_events
from app.crud.notifications import notifications
