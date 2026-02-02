"""Notification event system tests — covers event triggers and notification creation."""
from app.crud.notifications import notifications as notification_crud
from app.services.notification_events import parse_mentions, notify_mentions


def _create_user(client, username, role="participant"):
    """Helper to create a user for testing."""
    resp = client.post("/api/users", json={
        "username": username,
        "email": f"{username}@example.com",
        "role": role,
    })
    return resp.json()


def _create_post(client, user_id, title="Test Post"):
    """Helper to create a post for testing."""
    resp = client.post("/api/posts", json={
        "title": title,
        "content": "Test content",
    }, headers={"X-User-Id": str(user_id)})
    return resp.json()


# ---------- Follow Notification Tests ----------

def test_follow_creates_notification(client, db_session):
    """TC-NOTIF-EVENT-001: Following a user creates a notification."""
    follower = _create_user(client, "follower_notif")
    followed = _create_user(client, "followed_notif")

    # Follow the user
    resp = client.post(
        f"/api/users/{followed['id']}/follow",
        headers={"X-User-Id": str(follower["id"])}
    )
    assert resp.status_code == 201

    # Check notification was created for the followed user
    notifications = notification_crud.get_multi_by_user(db_session, user_id=followed["id"])
    assert len(notifications) == 1
    notif = notifications[0]
    assert notif.type == "follow"
    assert notif.user_id == followed["id"]
    assert notif.actor_id == follower["id"]
    assert follower["username"] in notif.content
    assert notif.is_read is False


def test_follow_notification_has_related_url(client, db_session):
    """TC-NOTIF-EVENT-002: Follow notification includes profile URL."""
    follower = _create_user(client, "follower_url")
    followed = _create_user(client, "followed_url")

    client.post(
        f"/api/users/{followed['id']}/follow",
        headers={"X-User-Id": str(follower["id"])}
    )

    notifications = notification_crud.get_multi_by_user(db_session, user_id=followed["id"])
    assert len(notifications) == 1
    assert f"/users/{follower['id']}" in notifications[0].related_url


def test_unfollow_does_not_create_notification(client, db_session):
    """TC-NOTIF-EVENT-003: Unfollowing does not create notification."""
    follower = _create_user(client, "follower_unf")
    followed = _create_user(client, "followed_unf")

    # Follow then unfollow
    client.post(
        f"/api/users/{followed['id']}/follow",
        headers={"X-User-Id": str(follower["id"])}
    )
    initial_count = len(notification_crud.get_multi_by_user(db_session, user_id=followed["id"]))

    client.delete(
        f"/api/users/{followed['id']}/follow",
        headers={"X-User-Id": str(follower["id"])}
    )

    # No new notification from unfollow
    final_count = len(notification_crud.get_multi_by_user(db_session, user_id=followed["id"]))
    assert final_count == initial_count


# ---------- Comment Notification Tests ----------

def test_comment_creates_notification(client, db_session):
    """TC-NOTIF-EVENT-010: Commenting on a post creates notification for author."""
    author = _create_user(client, "post_author_notif")
    commenter = _create_user(client, "commenter_notif")
    post = _create_post(client, author["id"], "Test Post for Comment")

    # Add a comment
    resp = client.post(
        f"/api/posts/{post['id']}/comments",
        json={"type": "comment", "value": "Great post!"},
        headers={"X-User-Id": str(commenter["id"])}
    )
    assert resp.status_code == 201

    # Check notification was created for the post author
    notifications = notification_crud.get_multi_by_user(db_session, user_id=author["id"])
    comment_notifs = [n for n in notifications if n.type == "comment"]
    assert len(comment_notifs) == 1
    notif = comment_notifs[0]
    assert notif.user_id == author["id"]
    assert notif.actor_id == commenter["id"]
    assert commenter["username"] in notif.content
    assert post["title"] in notif.content


def test_comment_on_own_post_no_notification(client, db_session):
    """TC-NOTIF-EVENT-011: Commenting on own post does not create notification."""
    author = _create_user(client, "self_commenter")
    post = _create_post(client, author["id"], "My Own Post")

    # Comment on own post
    client.post(
        f"/api/posts/{post['id']}/comments",
        json={"type": "comment", "value": "Commenting on my own post"},
        headers={"X-User-Id": str(author["id"])}
    )

    # Should not have any comment notifications
    notifications = notification_crud.get_multi_by_user(db_session, user_id=author["id"])
    comment_notifs = [n for n in notifications if n.type == "comment"]
    assert len(comment_notifs) == 0


def test_comment_notification_has_related_url(client, db_session):
    """TC-NOTIF-EVENT-012: Comment notification includes post URL."""
    author = _create_user(client, "author_url")
    commenter = _create_user(client, "commenter_url")
    post = _create_post(client, author["id"])

    client.post(
        f"/api/posts/{post['id']}/comments",
        json={"type": "comment", "value": "Nice!"},
        headers={"X-User-Id": str(commenter["id"])}
    )

    notifications = notification_crud.get_multi_by_user(db_session, user_id=author["id"])
    comment_notifs = [n for n in notifications if n.type == "comment"]
    assert len(comment_notifs) == 1
    assert f"/posts/{post['id']}" in comment_notifs[0].related_url


# ---------- Mention Parsing Tests ----------

def test_parse_simple_mention():
    """TC-NOTIF-EVENT-020: Parse single @mention."""
    mentions = parse_mentions("Hello @john_doe how are you?")
    assert mentions == ["john_doe"]


def test_parse_multiple_mentions():
    """TC-NOTIF-EVENT-021: Parse multiple @mentions."""
    mentions = parse_mentions("@alice and @bob should see this @charlie")
    assert set(mentions) == {"alice", "bob", "charlie"}


def test_parse_duplicate_mentions():
    """TC-NOTIF-EVENT-022: Duplicate mentions are deduplicated."""
    mentions = parse_mentions("@user1 hello @user1 again")
    assert mentions == ["user1"]


def test_parse_no_mentions():
    """TC-NOTIF-EVENT-023: No mentions returns empty list."""
    mentions = parse_mentions("Hello world, no mentions here")
    assert mentions == []


def test_parse_mention_with_underscore_hyphen():
    """TC-NOTIF-EVENT-024: Mentions with underscore and hyphen work."""
    mentions = parse_mentions("@user_name and @user-name")
    assert set(mentions) == {"user_name", "user-name"}


def test_parse_mention_at_start_and_end():
    """TC-NOTIF-EVENT-025: Mentions at start and end of string."""
    mentions = parse_mentions("@start middle @end")
    assert set(mentions) == {"start", "end"}


def test_parse_mention_with_punctuation():
    """TC-NOTIF-EVENT-026: Mention followed by punctuation."""
    mentions = parse_mentions("Thanks @user! And @other, great job.")
    assert set(mentions) == {"user", "other"}


# ---------- Mention Notification Tests ----------

def test_mention_creates_notification(client, db_session):
    """TC-NOTIF-EVENT-030: @mention in comment creates notification."""
    author = _create_user(client, "author_mention")
    commenter = _create_user(client, "commenter_mention")
    mentioned = _create_user(client, "mentioned_user")
    post = _create_post(client, author["id"])

    # Comment with @mention
    client.post(
        f"/api/posts/{post['id']}/comments",
        json={"type": "comment", "value": f"Hey @{mentioned['username']} check this out!"},
        headers={"X-User-Id": str(commenter["id"])}
    )

    # Check notification was created for mentioned user
    notifications = notification_crud.get_multi_by_user(db_session, user_id=mentioned["id"])
    mention_notifs = [n for n in notifications if n.type == "mention"]
    assert len(mention_notifs) == 1
    notif = mention_notifs[0]
    assert notif.user_id == mentioned["id"]
    assert notif.actor_id == commenter["id"]
    assert commenter["username"] in notif.content


def test_mention_nonexistent_user_no_notification(client, db_session):
    """TC-NOTIF-EVENT-031: @mention of non-existent user creates no notification."""
    author = _create_user(client, "author_nonexist")
    commenter = _create_user(client, "commenter_nonexist")
    post = _create_post(client, author["id"])

    # Comment with @mention of non-existent user
    client.post(
        f"/api/posts/{post['id']}/comments",
        json={"type": "comment", "value": "@nonexistent_user_xyz check this!"},
        headers={"X-User-Id": str(commenter["id"])}
    )

    # The only notification should be for the post author (comment notification)
    # No mention notification should be created for non-existent user
    all_notifs = notification_crud.get_multi_by_user(db_session, user_id=author["id"])
    mention_notifs = [n for n in all_notifs if n.type == "mention"]
    assert len(mention_notifs) == 0


def test_self_mention_no_notification(client, db_session):
    """TC-NOTIF-EVENT-032: Self @mention does not create notification."""
    author = _create_user(client, "author_selfmention")
    commenter = _create_user(client, "commenter_selfmention")
    post = _create_post(client, author["id"])

    # Comment mentioning self
    client.post(
        f"/api/posts/{post['id']}/comments",
        json={"type": "comment", "value": f"I @{commenter['username']} wrote this"},
        headers={"X-User-Id": str(commenter["id"])}
    )

    # Commenter should not receive mention notification for self-mention
    commenter_notifs = notification_crud.get_multi_by_user(db_session, user_id=commenter["id"])
    mention_notifs = [n for n in commenter_notifs if n.type == "mention"]
    assert len(mention_notifs) == 0


def test_multiple_mentions_create_multiple_notifications(client, db_session):
    """TC-NOTIF-EVENT-033: Multiple @mentions create multiple notifications."""
    author = _create_user(client, "author_multi")
    commenter = _create_user(client, "commenter_multi")
    mentioned1 = _create_user(client, "mentioned_one")
    mentioned2 = _create_user(client, "mentioned_two")
    post = _create_post(client, author["id"])

    # Comment with multiple @mentions
    client.post(
        f"/api/posts/{post['id']}/comments",
        json={"type": "comment", "value": f"@{mentioned1['username']} and @{mentioned2['username']} check this!"},
        headers={"X-User-Id": str(commenter["id"])}
    )

    # Check both mentioned users got notifications
    notifs1 = notification_crud.get_multi_by_user(db_session, user_id=mentioned1["id"])
    notifs2 = notification_crud.get_multi_by_user(db_session, user_id=mentioned2["id"])
    mention_notifs1 = [n for n in notifs1 if n.type == "mention"]
    mention_notifs2 = [n for n in notifs2 if n.type == "mention"]
    assert len(mention_notifs1) == 1
    assert len(mention_notifs2) == 1


# ---------- Integration Tests ----------

def test_comment_with_mention_creates_both_notifications(client, db_session):
    """TC-NOTIF-EVENT-040: Comment with @mention creates both comment and mention notifications."""
    author = _create_user(client, "author_both")
    commenter = _create_user(client, "commenter_both")
    mentioned = _create_user(client, "mentioned_both")
    post = _create_post(client, author["id"])

    # Comment with @mention (author is different from mentioned)
    client.post(
        f"/api/posts/{post['id']}/comments",
        json={"type": "comment", "value": f"@{mentioned['username']} check this post!"},
        headers={"X-User-Id": str(commenter["id"])}
    )

    # Author gets comment notification
    author_notifs = notification_crud.get_multi_by_user(db_session, user_id=author["id"])
    assert any(n.type == "comment" for n in author_notifs)

    # Mentioned user gets mention notification
    mentioned_notifs = notification_crud.get_multi_by_user(db_session, user_id=mentioned["id"])
    assert any(n.type == "mention" for n in mentioned_notifs)


def test_comment_mentioning_author_creates_both_notifications(client, db_session):
    """TC-NOTIF-EVENT-041: Mentioning post author creates both comment and mention notifications."""
    author = _create_user(client, "author_mentioned")
    commenter = _create_user(client, "commenter_author")
    post = _create_post(client, author["id"])

    # Comment mentioning the post author
    client.post(
        f"/api/posts/{post['id']}/comments",
        json={"type": "comment", "value": f"@{author['username']} your post is great!"},
        headers={"X-User-Id": str(commenter["id"])}
    )

    # Author gets both comment and mention notifications
    author_notifs = notification_crud.get_multi_by_user(db_session, user_id=author["id"])
    types = [n.type for n in author_notifs]
    assert "comment" in types
    assert "mention" in types


def test_notification_unread_count_increases(client, db_session):
    """TC-NOTIF-EVENT-050: Notifications increase unread count."""
    follower = _create_user(client, "follower_count")
    followed = _create_user(client, "followed_count")

    # Initial unread count
    initial_count = notification_crud.count_unread(db_session, user_id=followed["id"])

    # Follow to trigger notification
    client.post(
        f"/api/users/{followed['id']}/follow",
        headers={"X-User-Id": str(follower["id"])}
    )

    # Unread count should increase
    final_count = notification_crud.count_unread(db_session, user_id=followed["id"])
    assert final_count == initial_count + 1
