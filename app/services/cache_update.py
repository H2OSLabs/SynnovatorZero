"""Cache update functions for denormalized counts"""
from sqlalchemy.orm import Session

from app import crud
from app.models.user import User
from app.models.event import Event


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


def update_event_participant_cache(db: Session, event_id: int) -> None:
    """Update event's participant_count cache field.

    Should be called after group registration/unregistration to maintain cache consistency.
    """
    event = db.query(Event).filter(Event.id == event_id).first()
    if event is None:
        return

    # Count registered groups/teams
    event.participant_count = crud.event_groups.count_by_category(db, event_id=event_id)

    db.add(event)
    db.commit()
