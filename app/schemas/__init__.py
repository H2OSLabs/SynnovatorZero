"""Schemas package"""
from app.schemas.user import User, UserCreate, UserUpdate
from app.schemas.resource import Resource, ResourceCreate, ResourceUpdate
from app.schemas.category import Category, CategoryCreate, CategoryUpdate
from app.schemas.post import Post, PostCreate, PostUpdate
from app.schemas.rule import Rule, RuleCreate, RuleUpdate
from app.schemas.group import Group, GroupCreate, GroupUpdate
from app.schemas.interaction import Interaction, InteractionCreate, InteractionUpdate
from app.schemas.comment import Comment, CommentCreate, CommentUpdate
from app.schemas.rating import Rating, RatingCreate, RatingUpdate
from app.schemas.member import Member, MemberCreate, MemberUpdate
from app.schemas.memberadd import MemberAdd
from app.schemas.categoryruleadd import CategoryRuleAdd
from app.schemas.categorypostadd import CategoryPostAdd
from app.schemas.categorygroupadd import CategoryGroupAdd
from app.schemas.postresourceadd import PostResourceAdd
from app.schemas.postrelationadd import PostRelationAdd
from app.schemas.paginateduserlist import PaginatedUserList
from app.schemas.paginatedcategorylist import PaginatedCategoryList
from app.schemas.paginatedpostlist import PaginatedPostList
from app.schemas.paginatedresourcelist import PaginatedResourceList
from app.schemas.paginatedrulelist import PaginatedRuleList
from app.schemas.paginatedgrouplist import PaginatedGroupList
from app.schemas.paginatedcommentlist import PaginatedCommentList
from app.schemas.paginatedratinglist import PaginatedRatingList
from app.schemas.paginatedmemberlist import PaginatedMemberList
from app.schemas.batchids import BatchIds
from app.schemas.batchstatusupdate import BatchStatusUpdate
from app.schemas.batchroleupdate import BatchRoleUpdate
from app.schemas.batchresult import BatchResult
from app.schemas.user_user import UserUserCreate, UserUserResponse
from app.schemas.post_resource import PostResourceResponse
from app.schemas.post_post import PostPostResponse
from app.schemas.category_rule import CategoryRuleResponse
from app.schemas.category_post import CategoryPostResponse
from app.schemas.category_group import CategoryGroupResponse
from app.schemas.target_interaction import TargetInteractionCreate, TargetInteractionResponse
from app.schemas.paginatedinteractionlist import PaginatedInteractionList
from app.schemas.category_category import CategoryCategoryAdd, CategoryCategoryResponse
from app.schemas.notification import (
    Notification, NotificationCreate, NotificationUpdate,
    NotificationType, PaginatedNotificationList
)
