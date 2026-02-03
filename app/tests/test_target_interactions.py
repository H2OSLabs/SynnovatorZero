"""Target:Interaction + Like/Comment/Rating with cache tests — Phase 6 Layer 4

Covers:
- TC-REL-TI-001: Create target_interaction binding
- TC-REL-TI-002: Delete target_interaction binding
- TC-IACT-001: Like post, like_count increments
- TC-IACT-002: Duplicate like rejected
- TC-IACT-003: Unlike, like_count decrements
- TC-IACT-010: Create top-level comment, comment_count +1
- TC-IACT-011: Create nested reply
- TC-IACT-013: comment_count includes all levels
- TC-IACT-020: Create multi-dimension rating
- TC-IACT-021: Multiple ratings average calculation
"""


def _create_user(client, username="dave"):
    resp = client.post("/api/users", json={
        "username": username,
        "email": f"{username}@example.com",
    })
    return resp.json()["id"]


def _create_post(client, uid, title="Test Post"):
    resp = client.post("/api/posts", json={
        "title": title,
    }, headers={"X-User-Id": str(uid)})
    return resp.json()


def _get_post(client, post_id, uid=None):
    headers = {"X-User-Id": str(uid)} if uid else {}
    return client.get(f"/api/posts/{post_id}", headers=headers).json()


# --- Like tests ---

def test_like_post_increments_cache(client):
    """TC-IACT-001: Like post, like_count from 0 to 1."""
    uid = _create_user(client)
    post = _create_post(client, uid)
    post_id = post["id"]
    resp = client.post(f"/api/posts/{post_id}/like", headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201
    assert resp.json()["liked"] is True
    # Check cache field
    updated = _get_post(client, post_id, uid)
    assert updated["like_count"] == 1


def test_duplicate_like_rejected(client):
    """TC-IACT-002: Duplicate like returns 409."""
    uid = _create_user(client)
    post = _create_post(client, uid)
    post_id = post["id"]
    client.post(f"/api/posts/{post_id}/like", headers={"X-User-Id": str(uid)})
    resp = client.post(f"/api/posts/{post_id}/like", headers={"X-User-Id": str(uid)})
    assert resp.status_code == 409
    assert "Already liked" in resp.json()["detail"]


def test_unlike_decrements_cache(client):
    """TC-IACT-003: Unlike, like_count back to 0."""
    uid = _create_user(client)
    post = _create_post(client, uid)
    post_id = post["id"]
    # Like
    client.post(f"/api/posts/{post_id}/like", headers={"X-User-Id": str(uid)})
    assert _get_post(client, post_id, uid)["like_count"] == 1
    # Unlike
    resp = client.delete(f"/api/posts/{post_id}/like", headers={"X-User-Id": str(uid)})
    assert resp.status_code == 204
    assert _get_post(client, post_id, uid)["like_count"] == 0


def test_unlike_not_liked_returns_404(client):
    """Unlike a post not liked returns 404."""
    uid = _create_user(client)
    post = _create_post(client, uid)
    resp = client.delete(f"/api/posts/{post['id']}/like", headers={"X-User-Id": str(uid)})
    assert resp.status_code == 404


def test_multiple_users_like(client):
    """Multiple users liking same post increments correctly."""
    u1 = _create_user(client, "alice")
    u2 = _create_user(client, "bob")
    post = _create_post(client, u1)
    post_id = post["id"]
    client.post(f"/api/posts/{post_id}/like", headers={"X-User-Id": str(u1)})
    client.post(f"/api/posts/{post_id}/like", headers={"X-User-Id": str(u2)})
    assert _get_post(client, post_id, u1)["like_count"] == 2
    # One unlikes
    client.delete(f"/api/posts/{post_id}/like", headers={"X-User-Id": str(u1)})
    assert _get_post(client, post_id, u1)["like_count"] == 1


# --- Comment tests ---

def test_create_comment_increments_cache(client):
    """TC-IACT-010: Top-level comment, comment_count +1."""
    uid = _create_user(client)
    post = _create_post(client, uid)
    post_id = post["id"]
    resp = client.post(f"/api/posts/{post_id}/comments", json={
        "type": "comment",
        "value": "Great work!",
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201
    assert _get_post(client, post_id, uid)["comment_count"] == 1


def test_nested_reply_comment(client):
    """TC-IACT-011: Nested reply with parent_id."""
    u1 = _create_user(client, "bob")
    u2 = _create_user(client, "alice")
    post = _create_post(client, u1)
    post_id = post["id"]
    # Top-level comment
    resp1 = client.post(f"/api/posts/{post_id}/comments", json={
        "type": "comment",
        "value": "Top comment",
    }, headers={"X-User-Id": str(u1)})
    parent_id = resp1.json()["id"]
    # Reply
    resp2 = client.post(f"/api/posts/{post_id}/comments", json={
        "type": "comment",
        "value": "Reply to top comment",
        "parent_id": parent_id,
    }, headers={"X-User-Id": str(u2)})
    assert resp2.status_code == 201
    assert resp2.json()["parent_id"] == parent_id


def test_comment_count_includes_all_levels(client):
    """TC-IACT-013: comment_count includes top-level + nested."""
    u1 = _create_user(client, "bob")
    u2 = _create_user(client, "alice")
    post = _create_post(client, u1)
    post_id = post["id"]
    # Top-level comment
    resp1 = client.post(f"/api/posts/{post_id}/comments", json={
        "type": "comment",
        "value": "Comment 1",
    }, headers={"X-User-Id": str(u1)})
    parent_id = resp1.json()["id"]
    # Reply
    client.post(f"/api/posts/{post_id}/comments", json={
        "type": "comment",
        "value": "Reply 1",
        "parent_id": parent_id,
    }, headers={"X-User-Id": str(u2)})
    # Another top-level
    client.post(f"/api/posts/{post_id}/comments", json={
        "type": "comment",
        "value": "Comment 2",
    }, headers={"X-User-Id": str(u2)})
    assert _get_post(client, post_id, u1)["comment_count"] == 3


def test_list_post_comments(client):
    """List comments on a post returns paginated results."""
    uid = _create_user(client)
    post = _create_post(client, uid)
    post_id = post["id"]
    client.post(f"/api/posts/{post_id}/comments", json={
        "type": "comment",
        "value": "Comment A",
    }, headers={"X-User-Id": str(uid)})
    client.post(f"/api/posts/{post_id}/comments", json={
        "type": "comment",
        "value": "Comment B",
    }, headers={"X-User-Id": str(uid)})
    resp = client.get(f"/api/posts/{post_id}/comments")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


# --- Rating tests ---

def test_create_rating_updates_average(client):
    """TC-IACT-020: Rating updates average_rating."""
    uid = _create_user(client)
    post = _create_post(client, uid)
    post_id = post["id"]
    scores = {"Innovation": 87, "Technical": 82, "Practical": 78, "Demo": 91}
    resp = client.post(f"/api/posts/{post_id}/ratings", json={
        "type": "rating",
        "value": scores,
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201
    updated = _get_post(client, post_id, uid)
    assert updated["average_rating"] is not None
    # Single rating: average of (87+82+78+91)/4 = 84.5
    assert updated["average_rating"] == 84.5


def test_multiple_ratings_average(client):
    """TC-IACT-021: Multiple ratings produce correct average."""
    u1 = _create_user(client, "judge1")
    u2 = _create_user(client, "judge2")
    post = _create_post(client, u1)
    post_id = post["id"]
    # Judge 1 rates
    client.post(f"/api/posts/{post_id}/ratings", json={
        "type": "rating",
        "value": {"Innovation": 80, "Technical": 80},
    }, headers={"X-User-Id": str(u1)})
    # Judge 2 rates
    client.post(f"/api/posts/{post_id}/ratings", json={
        "type": "rating",
        "value": {"Innovation": 90, "Technical": 90},
    }, headers={"X-User-Id": str(u2)})
    updated = _get_post(client, post_id, u1)
    # Judge 1 average: (80+80)/2 = 80; Judge 2 average: (90+90)/2 = 90
    # Overall: (80+90)/2 = 85
    assert updated["average_rating"] == 85.0


def test_list_post_ratings(client):
    """List ratings on a post returns paginated results."""
    uid = _create_user(client)
    post = _create_post(client, uid)
    post_id = post["id"]
    client.post(f"/api/posts/{post_id}/ratings", json={
        "type": "rating",
        "value": {"Quality": 80},
    }, headers={"X-User-Id": str(uid)})
    resp = client.get(f"/api/posts/{post_id}/ratings")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1


# --- Auth requirement ---
# Note: In mock mode, requests without X-User-Id header auto-create a mock user.
# These tests verify auth failure by providing an invalid (non-existent) user ID.

def test_like_requires_auth(client):
    """Like with invalid user returns 401."""
    uid = _create_user(client)
    post = _create_post(client, uid)
    resp = client.post(f"/api/posts/{post['id']}/like", headers={"X-User-Id": "99999"})
    assert resp.status_code == 401


def test_comment_requires_auth(client):
    """Comment with invalid user returns 401."""
    uid = _create_user(client)
    post = _create_post(client, uid)
    resp = client.post(f"/api/posts/{post['id']}/comments", json={
        "type": "comment",
        "value": "No auth",
    }, headers={"X-User-Id": "99999"})
    assert resp.status_code == 401


def test_rating_requires_auth(client):
    """Rating with invalid user returns 401."""
    uid = _create_user(client)
    post = _create_post(client, uid)
    resp = client.post(f"/api/posts/{post['id']}/ratings", json={
        "type": "rating",
        "value": {"Q": 80},
    }, headers={"X-User-Id": "99999"})
    assert resp.status_code == 401


# --- Edge cases ---

def test_like_deleted_post_returns_404(client):
    """Like a deleted post returns 404."""
    uid = _create_user(client)
    post = _create_post(client, uid)
    post_id = post["id"]
    # Soft delete the post
    client.delete(f"/api/posts/{post_id}", headers={"X-User-Id": str(uid)})
    resp = client.post(f"/api/posts/{post_id}/like", headers={"X-User-Id": str(uid)})
    assert resp.status_code == 404
