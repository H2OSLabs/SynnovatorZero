"""Interaction model tests — basic CRUD for the unified Interaction model.
Full interaction behavior tests (likes/comments/ratings with cache updates,
target binding, etc.) are deferred to Phase 6 (Layer 4) when target:interaction
relationship table is implemented.

This phase covers:
- TC-IACT-900: Invalid interaction type rejected
- Basic CRUD on the Interaction model
"""
from app.models.interaction import Interaction


def _create_user(client, username="author"):
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


# ---------- Interaction model via DB session ----------
def test_create_like_interaction(db_session):
    """Create a like interaction directly in DB."""
    interaction = Interaction(type="like", created_by=1)
    db_session.add(interaction)
    db_session.commit()
    db_session.refresh(interaction)
    assert interaction.id is not None
    assert interaction.type == "like"
    assert interaction.value is None
    assert interaction.created_by == 1


def test_create_comment_interaction(db_session):
    """Create a comment interaction directly in DB."""
    interaction = Interaction(type="comment", value="Great work!", created_by=1)
    db_session.add(interaction)
    db_session.commit()
    db_session.refresh(interaction)
    assert interaction.type == "comment"
    assert interaction.value == "Great work!"


def test_create_rating_interaction(db_session):
    """Create a rating interaction directly in DB."""
    scores = {"Innovation": 87, "Technical": 82, "Practical": 78, "Demo": 91}
    interaction = Interaction(type="rating", value=scores, created_by=1)
    db_session.add(interaction)
    db_session.commit()
    db_session.refresh(interaction)
    assert interaction.type == "rating"
    assert interaction.value["Innovation"] == 87


def test_nested_comment_interaction(db_session):
    """Create nested comment using parent_id."""
    parent = Interaction(type="comment", value="Top-level comment", created_by=1)
    db_session.add(parent)
    db_session.commit()
    db_session.refresh(parent)

    reply = Interaction(type="comment", value="Reply to comment", parent_id=parent.id, created_by=2)
    db_session.add(reply)
    db_session.commit()
    db_session.refresh(reply)
    assert reply.parent_id == parent.id


def test_soft_delete_interaction(db_session):
    """Soft delete an interaction."""
    from datetime import datetime, timezone
    interaction = Interaction(type="like", created_by=1)
    db_session.add(interaction)
    db_session.commit()

    interaction.deleted_at = datetime.now(timezone.utc)
    db_session.commit()
    db_session.refresh(interaction)
    assert interaction.deleted_at is not None


# ---------- Interaction schema validation ----------
def test_invalid_interaction_type_rejected():
    """TC-IACT-900: Invalid type rejected by schema."""
    from pydantic import ValidationError
    from app.schemas.interaction import InteractionCreate
    try:
        InteractionCreate(type="bookmark")
        assert False, "Should have raised ValidationError"
    except ValidationError:
        pass


def test_valid_interaction_types():
    """Verify all valid types are accepted."""
    from app.schemas.interaction import InteractionCreate
    for t in ("like", "comment", "rating"):
        obj = InteractionCreate(type=t)
        assert obj.type == t


# ---------- Existing interaction router stubs ----------
def test_like_post_endpoint(client):
    """Basic like endpoint returns success."""
    uid = _create_user(client)
    post = _create_post(client, uid)
    resp = client.post(f"/api/posts/{post['id']}/like", headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201
    assert resp.json()["liked"] is True


def test_like_nonexistent_post(client):
    """Like nonexistent post returns 404."""
    uid = _create_user(client)
    resp = client.post("/api/posts/9999/like", headers={"X-User-Id": str(uid)})
    assert resp.status_code == 404


def test_list_post_comments_empty(client):
    """List comments on post with no comments."""
    uid = _create_user(client)
    post = _create_post(client, uid)
    resp = client.get(f"/api/posts/{post['id']}/comments")
    assert resp.status_code == 200
    assert resp.json()["total"] == 0


def test_list_post_ratings_empty(client):
    """List ratings on post with no ratings."""
    uid = _create_user(client)
    post = _create_post(client, uid)
    resp = client.get(f"/api/posts/{post['id']}/ratings")
    assert resp.status_code == 200
    assert resp.json()["total"] == 0
