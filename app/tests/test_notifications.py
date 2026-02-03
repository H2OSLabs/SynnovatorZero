"""Notification API tests — covers notification CRUD and status management."""
from app.crud.notifications import notifications as notification_crud


def _create_user(client, username):
    """Helper to create a user for testing."""
    resp = client.post("/api/users", json={
        "username": username,
        "email": f"{username}@example.com",
    })
    return resp.json()["id"]


def _create_notification(db_session, user_id, type="system", content="Test notification", title=None):
    """Helper to create a notification directly in DB."""
    return notification_crud.create(
        db_session,
        user_id=user_id,
        type=type,
        content=content,
        title=title,
    )


# ---------- List Notifications Tests ----------

def test_list_notifications_empty(client):
    """TC-NOTIF-001: List notifications for user with none returns empty list."""
    user_id = _create_user(client, "notif_empty")

    resp = client.get("/api/notifications", headers={"X-User-Id": str(user_id)})
    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []
    assert data["total"] == 0


def test_list_notifications_with_items(client, db_session):
    """TC-NOTIF-002: List notifications returns user's notifications."""
    user_id = _create_user(client, "notif_user")

    # Create notifications directly in DB
    _create_notification(db_session, user_id, content="Notification 1")
    _create_notification(db_session, user_id, content="Notification 2")
    _create_notification(db_session, user_id, content="Notification 3")

    resp = client.get("/api/notifications", headers={"X-User-Id": str(user_id)})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 3
    assert len(data["items"]) == 3


def test_list_notifications_filter_unread(client, db_session):
    """TC-NOTIF-003: Filter notifications by unread status."""
    user_id = _create_user(client, "notif_filter")

    # Create notifications
    n1 = _create_notification(db_session, user_id, content="Unread 1")
    n2 = _create_notification(db_session, user_id, content="Unread 2")
    n3 = _create_notification(db_session, user_id, content="Read 1")

    # Mark one as read
    notification_crud.mark_as_read(db_session, db_obj=n3)

    # Filter by is_read=false
    resp = client.get("/api/notifications?is_read=false", headers={"X-User-Id": str(user_id)})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2

    # Filter by is_read=true
    resp = client.get("/api/notifications?is_read=true", headers={"X-User-Id": str(user_id)})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1


def test_list_notifications_pagination(client, db_session):
    """TC-NOTIF-004: Pagination works correctly."""
    user_id = _create_user(client, "notif_page")

    # Create 5 notifications
    for i in range(5):
        _create_notification(db_session, user_id, content=f"Notification {i}")

    # Get first 2
    resp = client.get("/api/notifications?skip=0&limit=2", headers={"X-User-Id": str(user_id)})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["items"]) == 2
    assert data["total"] == 5
    assert data["skip"] == 0
    assert data["limit"] == 2

    # Get next 2
    resp = client.get("/api/notifications?skip=2&limit=2", headers={"X-User-Id": str(user_id)})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["items"]) == 2


def test_list_notifications_other_user_isolated(client, db_session):
    """TC-NOTIF-005: Users can only see their own notifications."""
    user1 = _create_user(client, "notif_user1")
    user2 = _create_user(client, "notif_user2")

    # Create notifications for user1
    _create_notification(db_session, user1, content="User1's notification")

    # User2 should see no notifications
    resp = client.get("/api/notifications", headers={"X-User-Id": str(user2)})
    assert resp.status_code == 200
    assert resp.json()["total"] == 0


# ---------- Get Notification Tests ----------

def test_get_notification(client, db_session):
    """TC-NOTIF-010: Get a specific notification by ID."""
    user_id = _create_user(client, "notif_get")
    notif = _create_notification(db_session, user_id, content="Test content", title="Test Title")

    resp = client.get(f"/api/notifications/{notif.id}", headers={"X-User-Id": str(user_id)})
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == notif.id
    assert data["content"] == "Test content"
    assert data["title"] == "Test Title"
    assert data["is_read"] is False


def test_get_notification_not_found(client):
    """TC-NOTIF-011: Get non-existent notification returns 404."""
    user_id = _create_user(client, "notif_nf")

    resp = client.get("/api/notifications/99999", headers={"X-User-Id": str(user_id)})
    assert resp.status_code == 404


def test_get_notification_other_user(client, db_session):
    """TC-NOTIF-012: Cannot get another user's notification."""
    user1 = _create_user(client, "notif_own1")
    user2 = _create_user(client, "notif_own2")
    notif = _create_notification(db_session, user1, content="User1's private notification")

    # User2 tries to access User1's notification
    resp = client.get(f"/api/notifications/{notif.id}", headers={"X-User-Id": str(user2)})
    assert resp.status_code == 404  # Returns 404 to not leak existence


# ---------- Mark as Read Tests ----------

def test_mark_notification_as_read(client, db_session):
    """TC-NOTIF-020: Mark notification as read."""
    user_id = _create_user(client, "notif_mark")
    notif = _create_notification(db_session, user_id, content="To be read")

    resp = client.patch(
        f"/api/notifications/{notif.id}",
        json={"is_read": True},
        headers={"X-User-Id": str(user_id)},
    )
    assert resp.status_code == 200
    assert resp.json()["is_read"] is True


def test_mark_notification_already_read(client, db_session):
    """TC-NOTIF-021: Mark already-read notification doesn't error."""
    user_id = _create_user(client, "notif_already")
    notif = _create_notification(db_session, user_id, content="Already read")
    notification_crud.mark_as_read(db_session, db_obj=notif)

    resp = client.patch(
        f"/api/notifications/{notif.id}",
        json={"is_read": True},
        headers={"X-User-Id": str(user_id)},
    )
    assert resp.status_code == 200


def test_mark_notification_other_user(client, db_session):
    """TC-NOTIF-022: Cannot mark another user's notification as read."""
    user1 = _create_user(client, "notif_mark1")
    user2 = _create_user(client, "notif_mark2")
    notif = _create_notification(db_session, user1, content="User1's notification")

    resp = client.patch(
        f"/api/notifications/{notif.id}",
        json={"is_read": True},
        headers={"X-User-Id": str(user2)},
    )
    assert resp.status_code == 404


# ---------- Unread Count Tests ----------

def test_unread_count_zero(client):
    """TC-NOTIF-030: Unread count is 0 for user with no notifications."""
    user_id = _create_user(client, "notif_count0")

    resp = client.get("/api/notifications/unread-count", headers={"X-User-Id": str(user_id)})
    assert resp.status_code == 200
    assert resp.json()["unread_count"] == 0


def test_unread_count_with_notifications(client, db_session):
    """TC-NOTIF-031: Unread count reflects unread notifications."""
    user_id = _create_user(client, "notif_count")

    # Create 3 unread notifications
    _create_notification(db_session, user_id, content="Unread 1")
    _create_notification(db_session, user_id, content="Unread 2")
    n3 = _create_notification(db_session, user_id, content="Unread 3")

    resp = client.get("/api/notifications/unread-count", headers={"X-User-Id": str(user_id)})
    assert resp.status_code == 200
    assert resp.json()["unread_count"] == 3

    # Mark one as read
    notification_crud.mark_as_read(db_session, db_obj=n3)

    resp = client.get("/api/notifications/unread-count", headers={"X-User-Id": str(user_id)})
    assert resp.json()["unread_count"] == 2


# ---------- Mark All as Read Tests ----------

def test_mark_all_as_read(client, db_session):
    """TC-NOTIF-040: Mark all notifications as read."""
    user_id = _create_user(client, "notif_all")

    # Create 3 unread notifications
    _create_notification(db_session, user_id, content="Unread 1")
    _create_notification(db_session, user_id, content="Unread 2")
    _create_notification(db_session, user_id, content="Unread 3")

    resp = client.post("/api/notifications/read-all", headers={"X-User-Id": str(user_id)})
    assert resp.status_code == 200
    assert resp.json()["marked_count"] == 3

    # Verify all are read
    resp = client.get("/api/notifications/unread-count", headers={"X-User-Id": str(user_id)})
    assert resp.json()["unread_count"] == 0


def test_mark_all_as_read_empty(client):
    """TC-NOTIF-041: Mark all as read with no notifications returns 0."""
    user_id = _create_user(client, "notif_all_empty")

    resp = client.post("/api/notifications/read-all", headers={"X-User-Id": str(user_id)})
    assert resp.status_code == 200
    assert resp.json()["marked_count"] == 0


def test_mark_all_as_read_already_read(client, db_session):
    """TC-NOTIF-042: Mark all as read when all already read returns 0."""
    user_id = _create_user(client, "notif_all_read")

    # Create and mark as read
    n1 = _create_notification(db_session, user_id, content="Read 1")
    n2 = _create_notification(db_session, user_id, content="Read 2")
    notification_crud.mark_as_read(db_session, db_obj=n1)
    notification_crud.mark_as_read(db_session, db_obj=n2)

    resp = client.post("/api/notifications/read-all", headers={"X-User-Id": str(user_id)})
    assert resp.status_code == 200
    assert resp.json()["marked_count"] == 0


# ---------- Notification Types Tests ----------

def test_notification_types(client, db_session):
    """TC-NOTIF-050: Different notification types are handled correctly."""
    user_id = _create_user(client, "notif_types")

    # Valid types per NotificationType enum: award, comment, team_request, follow, mention, system
    types = ["follow", "comment", "mention", "team_request", "award", "system"]
    for t in types:
        _create_notification(db_session, user_id, type=t, content=f"{t} notification")

    resp = client.get("/api/notifications", headers={"X-User-Id": str(user_id)})
    assert resp.status_code == 200
    assert resp.json()["total"] == len(types)


# ---------- Auth Required Tests ----------
# Note: In mock mode, requests without X-User-Id header auto-create a mock user.
# These tests verify auth failure by providing an invalid (non-existent) user ID.

def test_list_notifications_no_auth(client):
    """TC-NOTIF-060: List notifications with invalid user returns 401."""
    resp = client.get("/api/notifications", headers={"X-User-Id": "99999"})
    assert resp.status_code == 401


def test_get_notification_no_auth(client, db_session):
    """TC-NOTIF-061: Get notification with invalid user returns 401."""
    user_id = _create_user(client, "notif_noauth")
    notif = _create_notification(db_session, user_id, content="Test")

    resp = client.get(f"/api/notifications/{notif.id}", headers={"X-User-Id": "99999"})
    assert resp.status_code == 401


def test_mark_notification_no_auth(client, db_session):
    """TC-NOTIF-062: Mark notification with invalid user returns 401."""
    user_id = _create_user(client, "notif_noauth2")
    notif = _create_notification(db_session, user_id, content="Test")

    resp = client.patch(f"/api/notifications/{notif.id}", json={"is_read": True}, headers={"X-User-Id": "99999"})
    assert resp.status_code == 401


def test_unread_count_no_auth(client):
    """TC-NOTIF-063: Unread count with invalid user returns 401."""
    resp = client.get("/api/notifications/unread-count", headers={"X-User-Id": "99999"})
    assert resp.status_code == 401


def test_mark_all_no_auth(client):
    """TC-NOTIF-064: Mark all as read with invalid user returns 401."""
    resp = client.post("/api/notifications/read-all", headers={"X-User-Id": "99999"})
    assert resp.status_code == 401
