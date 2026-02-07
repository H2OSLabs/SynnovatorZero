"""Notification event service — triggers notifications on user actions.

This module provides functions to create notifications when specific events occur:
- follow: When user A follows user B
- comment: When user A comments on user B's post
- mention: When user A mentions user B in a comment (via @username)
- team_request: When user A requests to join user B's team
- award: When user receives an award/certificate

Usage:
    from app.services.notification_events import notify_follow, notify_comment

    # In follow endpoint:
    notify_follow(db, follower_id=1, followed_id=2)

    # In comment endpoint:
    notify_comment(db, commenter_id=1, post_id=123, comment_content="Nice work!")
"""
import re
from typing import Optional, List

from sqlalchemy.orm import Session

from app import crud
from app.crud.notifications import notifications as notification_crud


def notify_follow(db: Session, *, follower_id: int, followed_id: int) -> None:
    """Create a notification when a user is followed.

    Args:
        db: Database session
        follower_id: The user who is following
        followed_id: The user being followed
    """
    follower = crud.users.get(db, id=follower_id)
    if not follower:
        return

    notification_crud.create(
        db,
        user_id=followed_id,
        type="follow",
        title="新粉丝",
        content=f"{follower.username} 关注了你",
        related_url=f"/users/{follower_id}",
        actor_id=follower_id,
    )


def notify_comment(
    db: Session,
    *,
    commenter_id: int,
    post_id: int,
    comment_content: Optional[str] = None,
) -> None:
    """Create a notification when someone comments on a post.

    Args:
        db: Database session
        commenter_id: The user who posted the comment
        post_id: The post being commented on
        comment_content: The comment text (for @mention parsing)
    """
    # Get the post to find the author
    post = crud.posts.get(db, id=post_id)
    if not post:
        return

    # Don't notify if user comments on their own post
    if post.created_by == commenter_id:
        return

    commenter = crud.users.get(db, id=commenter_id)
    if not commenter:
        return

    notification_crud.create(
        db,
        user_id=post.created_by,
        type="comment",
        title="新评论",
        content=f"{commenter.username} 评论了你的作品「{post.title}」",
        related_url=f"/posts/{post_id}",
        actor_id=commenter_id,
    )

    # Parse @mentions and create mention notifications
    if comment_content:
        notify_mentions(db, mentioner_id=commenter_id, content=comment_content, related_url=f"/posts/{post_id}")


def parse_mentions(content: str) -> List[str]:
    """Parse @username mentions from content.

    Args:
        content: The text content to parse

    Returns:
        List of mentioned usernames (without @ prefix)
    """
    # Match @username pattern - allows alphanumeric, underscore, hyphen
    # Stops at whitespace, punctuation, or end of string
    pattern = r"@([a-zA-Z0-9_-]+)"
    matches = re.findall(pattern, content)
    return list(set(matches))  # Remove duplicates


def notify_mentions(
    db: Session,
    *,
    mentioner_id: int,
    content: str,
    related_url: Optional[str] = None,
) -> List[int]:
    """Parse @mentions from content and create notifications.

    Args:
        db: Database session
        mentioner_id: The user who wrote the content with mentions
        content: The text content containing @mentions
        related_url: Optional URL related to the mention context

    Returns:
        List of user IDs that were notified
    """
    usernames = parse_mentions(content)
    if not usernames:
        return []

    mentioner = crud.users.get(db, id=mentioner_id)
    if not mentioner:
        return []

    notified_ids = []
    for username in usernames:
        mentioned_user = crud.users.get_by_username(db, username=username)
        if not mentioned_user:
            continue

        # Don't notify if user mentions themselves
        if mentioned_user.id == mentioner_id:
            continue

        notification_crud.create(
            db,
            user_id=mentioned_user.id,
            type="mention",
            title="有人提到了你",
            content=f"{mentioner.username} 在评论中提到了你",
            related_url=related_url,
            actor_id=mentioner_id,
        )
        notified_ids.append(mentioned_user.id)

    return notified_ids


def notify_team_request(
    db: Session,
    *,
    requester_id: int,
    team_owner_id: int,
    team_name: str,
    team_id: int,
) -> None:
    """Create a notification when someone requests to join a team.

    Args:
        db: Database session
        requester_id: The user requesting to join
        team_owner_id: The team owner who needs to approve
        team_name: The name of the team
        team_id: The ID of the team
    """
    requester = crud.users.get(db, id=requester_id)
    if not requester:
        return

    notification_crud.create(
        db,
        user_id=team_owner_id,
        type="team_request",
        title="入队申请",
        content=f"{requester.username} 申请加入团队「{team_name}」",
        related_url=f"/groups/{team_id}",
        actor_id=requester_id,
    )


def notify_award(
    db: Session,
    *,
    user_id: int,
    award_name: str,
    category_name: Optional[str] = None,
    event_id: Optional[int] = None,
) -> None:
    """Create a notification when a user receives an award.

    Args:
        db: Database session
        user_id: The user receiving the award
        award_name: The name of the award
        category_name: Optional event/event name
        event_id: Optional event/event ID for the URL
    """
    content = f"恭喜！你获得了「{award_name}」"
    if category_name:
        content += f" (来自活动「{category_name}」)"

    related_url = f"/events/{event_id}" if event_id else None

    notification_crud.create(
        db,
        user_id=user_id,
        type="award",
        title="获奖通知",
        content=content,
        related_url=related_url,
    )


def notify_system(
    db: Session,
    *,
    user_id: int,
    title: str,
    content: str,
    related_url: Optional[str] = None,
) -> None:
    """Create a system notification for a user.

    Args:
        db: Database session
        user_id: The user to notify
        title: Notification title
        content: Notification content
        related_url: Optional related URL
    """
    notification_crud.create(
        db,
        user_id=user_id,
        type="system",
        title=title,
        content=content,
        related_url=related_url,
    )
