"""Models package - import all models so Base.metadata knows about them"""
from app.models.user import User
from app.models.resource import Resource
from app.models.category import Category
from app.models.post import Post
from app.models.rule import Rule
from app.models.group import Group
from app.models.comment import Comment
from app.models.rating import Rating
from app.models.member import Member
