"""Interaction CRUD operations (comments, ratings)"""
from app.crud.base import CRUDBase
from app.models.comment import Comment
from app.models.rating import Rating
from app.schemas.comment import CommentCreate, CommentUpdate
from app.schemas.rating import RatingCreate, RatingUpdate


class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):
    pass


class CRUDRating(CRUDBase[Rating, RatingCreate, RatingUpdate]):
    pass


comments = CRUDComment(Comment)
ratings = CRUDRating(Rating)
