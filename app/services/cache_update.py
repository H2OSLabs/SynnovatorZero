"""Cache update functions for denormalized counts"""
from sqlalchemy.orm import Session

from app import crud
from app.models.user import User
from app.models.category import Category


def update_user_follow_cache(db: Session, user_id: int) -> None:
    """Update user's follower_count and following_count cache fields.

    Should be called after follow/unfollow operations to maintain cache consistency.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return

    # Count followers (users who follow this user)
    user.follower_count = crud.user_users.count_followers(db, user_id=user_id)

    # Count following (users this user follows)
    user.following_count = crud.user_users.count_following(db, user_id=user_id)

    db.add(user)
    db.commit()


def update_category_participant_cache(db: Session, category_id: int) -> None:
    """Update category's participant_count cache field.

    Should be called after group registration/unregistration to maintain cache consistency.
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        return

    # Count registered groups/teams
    category.participant_count = crud.category_groups.count_by_category(db, category_id=category_id)

    db.add(category)
    db.commit()
