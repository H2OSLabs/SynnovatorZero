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


def notify_friend(db: Session, *, user_a_id: int, user_b_id: int) -> None:
    """Create notifications when two users become friends (mutual follow).
    
    Args:
        db: Database session
        user_a_id: User A
        user_b_id: User B
    """
    user_a = crud.users.get(db, id=user_a_id)
    user_b = crud.users.get(db, id=user_b_id)
    
    if not user_a or not user_b:
        return

    # Notify User A
    notification_crud.create(
        db,
        user_id=user_a_id,
        type="friend",
        title="新好友",
        content=f"你和 {user_b.username} 互相关注，成为好友啦！",
        related_url=f"/users/{user_b_id}",
        actor_id=user_b_id,
    )

    # Notify User B
    notification_crud.create(
        db,
        user_id=user_b_id,
        type="friend",
        title="新好友",
        content=f"你和 {user_a.username} 互相关注，成为好友啦！",
        related_url=f"/users/{user_a_id}",
        actor_id=user_a_id,
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


def notify_like(
    db: Session,
    *,
    liker_id: int,
    post_id: int,
) -> None:
    """Create a notification when someone likes a post."""
    post = crud.posts.get(db, id=post_id)
    if not post:
        return

    # Don't notify self-likes
    if post.created_by == liker_id:
        return

    liker = crud.users.get(db, id=liker_id)
    if not liker:
        return

    notification_crud.create(
        db,
        user_id=post.created_by,
        type="like",  # Front-end maps this to 'award' icon or generic, we should map to 'award' or add 'like'
        title="收到赞",
        content=f"{liker.username} 赞了你的作品「{post.title}」",
        related_url=f"/posts/{post_id}",
        actor_id=liker_id,
    )


def notify_bookmark(
    db: Session,
    *,
    user_id: int,
    post_id: int,
) -> None:
    """Create a notification when someone bookmarks a post."""
    post = crud.posts.get(db, id=post_id)
    if not post:
        return

    if post.created_by == user_id:
        return

    actor = crud.users.get(db, id=user_id)
    if not actor:
        return

    notification_crud.create(
        db,
        user_id=post.created_by,
        type="bookmark", # We'll need to add icon for this
        title="收到收藏",
        content=f"{actor.username} 收藏了你的作品「{post.title}」",
        related_url=f"/posts/{post_id}",
        actor_id=user_id,
    )


def notify_team_invite(
    db: Session,
    *,
    inviter_id: int,
    invitee_id: int,
    group_id: int,
) -> None:
    """Create a notification when a user is invited to a team."""
    group = crud.groups.get(db, id=group_id)
    inviter = crud.users.get(db, id=inviter_id)
    
    if not group or not inviter:
        return

    notification_crud.create(
        db,
        user_id=invitee_id,
        type="team_invite",
        title="团队邀请",
        content=f"{inviter.username} 邀请你加入团队 {group.name}",
        related_url=f"/groups/{group_id}?invite_id={group_id}", # Or specialized invite page? User can go to group page and accept.
        actor_id=inviter_id,
    )


def notify_team_invite_result(
    db: Session,
    *,
    inviter_id: int,
    invitee_id: int,
    group_id: int,
    result: str, # accepted / rejected
) -> None:
    group = crud.groups.get(db, id=group_id)
    invitee = crud.users.get(db, id=invitee_id)
    
    status_text = "接受" if result == "accepted" else "拒绝"
    
    notification_crud.create(
        db,
        user_id=inviter_id,
        type="team_invite_result",
        title=f"邀请被{status_text}",
        content=f"{invitee.username} 已{status_text}加入团队 {group.name} 的邀请",
        related_url=f"/groups/{group_id}",
        actor_id=invitee_id,
    )


def notify_asset_copy_request(
    db: Session,
    *,
    requester_id: int,
    resource_id: int,
) -> None:
    resource = crud.resources.get(db, id=resource_id)
    requester = crud.users.get(db, id=requester_id)
    
    if not resource or not requester:
        return
        
    notification_crud.create(
        db,
        user_id=resource.created_by,
        type="asset_copy_req",
        title="资产复制申请",
        content=f"{requester.username} 申请复制你的资产「{resource.name}」",
        related_url=f"/assets/{resource_id}?requester_id={requester_id}",
        actor_id=requester_id,
    )


def notify_asset_copy_result(
    db: Session,
    *,
    requester_id: int,
    resource_id: int,
    result: str, # accepted / rejected
) -> None:
    resource = crud.resources.get(db, id=resource_id)
    status_text = "同意" if result == "accepted" else "拒绝"
    
    notification_crud.create(
        db,
        user_id=requester_id,
        type="asset_copy_result",
        title=f"复制申请被{status_text}",
        content=f"你复制资产「{resource.name}」的申请已被{status_text}",
        related_url=f"/assets/{resource_id}",
        actor_id=resource.created_by,
    )


def notify_asset_link_request(
    db: Session,
    *,
    requester_id: int, # Resource owner requesting to link
    resource_id: int,
    post_id: int,
) -> None:
    resource = crud.resources.get(db, id=resource_id)
    post = crud.posts.get(db, id=post_id)
    requester = crud.users.get(db, id=requester_id)
    
    if not resource or not post or not requester:
        return
        
    notification_crud.create(
        db,
        user_id=post.created_by,
        type="asset_link_req",
        title="资产关联申请",
        content=f"{requester.username} 申请将资产「{resource.name}」关联到你的提案「{post.title}」",
        related_url=f"/posts/{post_id}?link_resource_id={resource_id}",
        actor_id=requester_id,
    )


def notify_asset_link_result(
    db: Session,
    *,
    requester_id: int,
    resource_id: int,
    post_id: int,
    result: str,
) -> None:
    resource = crud.resources.get(db, id=resource_id)
    post = crud.posts.get(db, id=post_id)
    status_text = "同意" if result == "accepted" else "拒绝"
    
    notification_crud.create(
        db,
        user_id=requester_id,
        type="asset_link_result",
        title=f"关联申请被{status_text}",
        content=f"你将资产「{resource.name}」关联到提案「{post.title}」的申请已被{status_text}",
        related_url=f"/posts/{post_id}",
        actor_id=post.created_by,
    )


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
