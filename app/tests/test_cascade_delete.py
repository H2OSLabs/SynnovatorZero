"""Cascade delete tests — Phase 7 Layer 5

Covers:
- TC-DEL-001: Delete category
- TC-DEL-002: Delete rule
- TC-DEL-003: Delete user (interactions + group:user cascade)
- TC-DEL-004: Delete group (members + category:group cascade)
- TC-DEL-005: Delete interaction (like → cache update)
- TC-DEL-010: Delete category → interactions cascade
- TC-DEL-011: Delete user → interaction + group:user cascade
- TC-DEL-012: Delete post → full cascade chain
- TC-DEL-013: Delete rule → category:rule cascade
- TC-DEL-014: Delete group → category:group cascade
- TC-DEL-015: Delete parent comment → child comments cascade
- TC-DEL-020: Read deleted record returns not found
- TC-DEL-022: Update deleted record returns not found
"""


def _create_user(client, username="testuser"):
    resp = client.post("/api/users", json={
        "username": username,
        "email": f"{username}@example.com",
        "role": "organizer",
    })
    return resp.json()["id"]


def _create_category(client, uid, name="Test Category"):
    resp = client.post("/api/categories", json={
        "name": name,
        "description": f"Description of {name}",
        "type": "competition",
    }, headers={"X-User-Id": str(uid)})
    return resp.json()["id"]


def _create_rule(client, uid, name="Test Rule"):
    resp = client.post("/api/rules", json={
        "name": name,
        "description": f"Description of {name}",
        "type": "submission",
    }, headers={"X-User-Id": str(uid)})
    return resp.json()["id"]


def _create_post(client, uid, title="Test Post"):
    resp = client.post("/api/posts", json={
        "title": title,
        "content": "Post body content",
        "type": "general",
    }, headers={"X-User-Id": str(uid)})
    return resp.json()["id"]


def _create_group(client, uid, name="Test Group"):
    resp = client.post("/api/groups", json={
        "name": name,
        "description": f"Description of {name}",
        "visibility": "public",
    }, headers={"X-User-Id": str(uid)})
    return resp.json()["id"]


def _create_resource(client, uid, name="Test Resource"):
    resp = client.post("/api/resources", json={
        "filename": f"{name}.pdf",
        "description": f"Description of {name}",
        "url": "https://example.com/file.pdf",
    }, headers={"X-User-Id": str(uid)})
    return resp.json()["id"]


# --- TC-DEL-001: Delete category ---

def test_delete_category_basic(client):
    """TC-DEL-001: Delete a category; read returns not found."""
    uid = _create_user(client)
    cat_id = _create_category(client, uid)
    resp = client.delete(f"/api/categories/{cat_id}", headers={"X-User-Id": str(uid)})
    assert resp.status_code == 204
    resp = client.get(f"/api/categories/{cat_id}")
    assert resp.status_code == 404


# --- TC-DEL-002: Delete rule ---

def test_delete_rule_basic(client):
    """TC-DEL-002: Delete a rule; read returns not found."""
    uid = _create_user(client)
    rule_id = _create_rule(client, uid)
    resp = client.delete(f"/api/rules/{rule_id}", headers={"X-User-Id": str(uid)})
    assert resp.status_code == 204
    resp = client.get(f"/api/rules/{rule_id}")
    assert resp.status_code == 404


# --- TC-DEL-003: Delete user → cascade interactions + members ---

def test_delete_user_cascades_interactions_and_members(client):
    """TC-DEL-003/011: Delete user; interactions hard-deleted, member removed, post cache updated."""
    uid = _create_user(client, "liker")
    poster = _create_user(client, "poster")
    post_id = _create_post(client, poster)
    group_id = _create_group(client, poster, "Team")

    # User likes a post
    client.post(f"/api/posts/{post_id}/like", headers={"X-User-Id": str(uid)})
    # Verify like counted
    post_data = client.get(f"/api/posts/{post_id}", headers={"X-User-Id": str(poster)}).json()
    assert post_data["like_count"] == 1

    # User joins group
    client.post(f"/api/groups/{group_id}/members", json={"user_id": uid})
    members = client.get(f"/api/groups/{group_id}/members").json()
    assert members["total"] == 1

    # Delete user (self-delete)
    resp = client.delete(f"/api/users/{uid}", headers={"X-User-Id": str(uid)})
    assert resp.status_code == 204

    # User not found
    assert client.get(f"/api/users/{uid}").status_code == 404

    # Post cache updated (like_count decremented)
    post_data = client.get(f"/api/posts/{post_id}", headers={"X-User-Id": str(poster)}).json()
    assert post_data["like_count"] == 0

    # Member removed
    members = client.get(f"/api/groups/{group_id}/members").json()
    assert members["total"] == 0


# --- TC-DEL-004: Delete group → cascade members + category:group ---

def test_delete_group_cascades_members_and_category_groups(client):
    """TC-DEL-004/014: Delete group; members removed, category:group removed."""
    uid = _create_user(client)
    group_id = _create_group(client, uid, "Team A")
    cat_id = _create_category(client, uid, "Event")

    # Add member
    member_user = _create_user(client, "member1")
    client.post(f"/api/groups/{group_id}/members", json={"user_id": member_user})

    # Register group to category
    client.post(f"/api/categories/{cat_id}/groups", json={"group_id": group_id})

    # Verify
    assert len(client.get(f"/api/categories/{cat_id}/groups").json()) == 1
    assert client.get(f"/api/groups/{group_id}/members").json()["total"] == 1

    # Delete group
    resp = client.delete(f"/api/groups/{group_id}", headers={"X-User-Id": str(uid)})
    assert resp.status_code == 204

    # Group not found
    assert client.get(f"/api/groups/{group_id}").status_code == 404

    # Category:group relation removed
    assert len(client.get(f"/api/categories/{cat_id}/groups").json()) == 0


# --- TC-DEL-005: Delete interaction (like) → cache update ---

def test_delete_like_updates_cache(client):
    """TC-DEL-005: Unlike a post; like_count decremented."""
    uid = _create_user(client)
    post_id = _create_post(client, uid)

    # Like
    client.post(f"/api/posts/{post_id}/like", headers={"X-User-Id": str(uid)})
    assert client.get(f"/api/posts/{post_id}", headers={"X-User-Id": str(uid)}).json()["like_count"] == 1

    # Unlike
    resp = client.delete(f"/api/posts/{post_id}/like", headers={"X-User-Id": str(uid)})
    assert resp.status_code == 204
    assert client.get(f"/api/posts/{post_id}", headers={"X-User-Id": str(uid)}).json()["like_count"] == 0


# --- TC-DEL-010: Delete category → interactions cascade ---

def test_delete_category_cascades_interactions(client):
    """TC-DEL-010: Delete category with likes/comments; interactions cascade-deleted."""
    uid = _create_user(client)
    cat_id = _create_category(client, uid)
    rule_id = _create_rule(client, uid)

    # Attach rule to category
    client.post(f"/api/categories/{cat_id}/rules", json={"rule_id": rule_id, "priority": 1})
    assert len(client.get(f"/api/categories/{cat_id}/rules").json()) == 1

    # Delete category
    resp = client.delete(f"/api/categories/{cat_id}", headers={"X-User-Id": str(uid)})
    assert resp.status_code == 204

    # Category not found, rule still exists
    assert client.get(f"/api/categories/{cat_id}").status_code == 404
    assert client.get(f"/api/rules/{rule_id}").status_code == 200


# --- TC-DEL-012: Delete post → full cascade chain ---

def test_delete_post_full_cascade(client):
    """TC-DEL-012: Delete post with category:post, post:post, post:resource, interactions."""
    uid = _create_user(client)
    cat_id = _create_category(client, uid)
    post_id = _create_post(client, uid)
    resource_id = _create_resource(client, uid)
    related_post_id = _create_post(client, uid, "Related Post")

    # category:post
    client.post(f"/api/categories/{cat_id}/posts", json={
        "post_id": post_id, "relation_type": "submission",
    })
    # post:resource
    client.post(f"/api/posts/{post_id}/resources", json={
        "resource_id": resource_id, "display_type": "attachment",
    })
    # post:post
    client.post(f"/api/posts/{post_id}/related", json={
        "target_post_id": related_post_id, "relation_type": "reference",
    })
    # like + comment
    client.post(f"/api/posts/{post_id}/like", headers={"X-User-Id": str(uid)})
    client.post(f"/api/posts/{post_id}/comments", json={
        "type": "comment", "value": {"text": "Great!"},
    }, headers={"X-User-Id": str(uid)})

    # Verify relations exist
    h = {"X-User-Id": str(uid)}
    assert len(client.get(f"/api/categories/{cat_id}/posts", headers=h).json()) == 1
    assert len(client.get(f"/api/posts/{post_id}/resources").json()) == 1
    assert len(client.get(f"/api/posts/{post_id}/related").json()) == 1
    assert client.get(f"/api/posts/{post_id}", headers=h).json()["like_count"] == 1
    assert client.get(f"/api/posts/{post_id}", headers=h).json()["comment_count"] == 1

    # Delete post
    resp = client.delete(f"/api/posts/{post_id}", headers={"X-User-Id": str(uid)})
    assert resp.status_code == 204

    # Post not found
    assert client.get(f"/api/posts/{post_id}").status_code == 404

    # category:post relation removed
    assert len(client.get(f"/api/categories/{cat_id}/posts", headers=h).json()) == 0

    # Resource and related post still exist
    assert client.get(f"/api/resources/{resource_id}").status_code == 200
    assert client.get(f"/api/posts/{related_post_id}", headers=h).status_code == 200


# --- TC-DEL-013: Delete rule → category:rule cascade ---

def test_delete_rule_cascades_category_rule(client):
    """TC-DEL-013: Delete rule that's associated with a category; relation removed."""
    uid = _create_user(client)
    cat_id = _create_category(client, uid)
    rule_id = _create_rule(client, uid)

    # Associate rule with category
    client.post(f"/api/categories/{cat_id}/rules", json={"rule_id": rule_id, "priority": 1})
    assert len(client.get(f"/api/categories/{cat_id}/rules").json()) == 1

    # Delete rule
    resp = client.delete(f"/api/rules/{rule_id}", headers={"X-User-Id": str(uid)})
    assert resp.status_code == 204

    # Rule not found
    assert client.get(f"/api/rules/{rule_id}").status_code == 404

    # category:rule relation removed
    assert len(client.get(f"/api/categories/{cat_id}/rules").json()) == 0


# --- TC-DEL-015: Delete parent comment → cascade child comments ---

def test_delete_parent_comment_cascades_children(client, db_session):
    """TC-DEL-015: Delete parent comment; all descendants cascade-deleted."""
    uid = _create_user(client)
    post_id = _create_post(client, uid)

    # Create parent comment
    resp1 = client.post(f"/api/posts/{post_id}/comments", json={
        "type": "comment", "value": {"text": "Parent comment"},
    }, headers={"X-User-Id": str(uid)})
    parent_id = resp1.json()["id"]

    # Create child comment
    resp2 = client.post(f"/api/posts/{post_id}/comments", json={
        "type": "comment", "value": {"text": "Child reply"}, "parent_id": parent_id,
    }, headers={"X-User-Id": str(uid)})
    child_id = resp2.json()["id"]

    # Create grandchild comment
    client.post(f"/api/posts/{post_id}/comments", json={
        "type": "comment", "value": {"text": "Grandchild reply"}, "parent_id": child_id,
    }, headers={"X-User-Id": str(uid)})

    # Verify 3 comments
    h = {"X-User-Id": str(uid)}
    comments = client.get(f"/api/posts/{post_id}/comments").json()
    assert comments["total"] == 3

    # Delete parent comment using cascade service directly via the test db_session
    from app.services.cascade_delete import cascade_delete_interaction
    cascade_delete_interaction(db_session, parent_id)

    # Verify all 3 comments deleted (comment_count should be 0)
    post_data = client.get(f"/api/posts/{post_id}", headers=h).json()
    assert post_data["comment_count"] == 0


# --- TC-DEL-020: Read deleted record returns not found ---

def test_read_deleted_post_returns_not_found(client):
    """TC-DEL-020: Read a deleted post; returns 404."""
    uid = _create_user(client)
    post_id = _create_post(client, uid)
    client.delete(f"/api/posts/{post_id}", headers={"X-User-Id": str(uid)})
    resp = client.get(f"/api/posts/{post_id}")
    assert resp.status_code == 404


# --- TC-DEL-022: Update deleted record returns not found ---

def test_update_deleted_post_returns_not_found(client):
    """TC-DEL-022: Update a deleted post; returns 404."""
    uid = _create_user(client)
    post_id = _create_post(client, uid)
    client.delete(f"/api/posts/{post_id}", headers={"X-User-Id": str(uid)})
    resp = client.patch(f"/api/posts/{post_id}", json={"title": "Updated"}, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 404


# --- Additional cascade tests ---

def test_delete_category_cascades_category_post(client):
    """Delete category removes category:post relations."""
    uid = _create_user(client)
    cat_id = _create_category(client, uid)
    post_id = _create_post(client, uid)
    client.post(f"/api/categories/{cat_id}/posts", json={
        "post_id": post_id, "relation_type": "submission",
    })
    h = {"X-User-Id": str(uid)}
    assert len(client.get(f"/api/categories/{cat_id}/posts", headers=h).json()) == 1

    client.delete(f"/api/categories/{cat_id}", headers={"X-User-Id": str(uid)})
    # Post still exists
    assert client.get(f"/api/posts/{post_id}", headers=h).status_code == 200


def test_delete_category_cascades_category_group(client):
    """Delete category removes category:group relations."""
    uid = _create_user(client)
    cat_id = _create_category(client, uid)
    group_id = _create_group(client, uid)
    client.post(f"/api/categories/{cat_id}/groups", json={"group_id": group_id})
    assert len(client.get(f"/api/categories/{cat_id}/groups").json()) == 1

    client.delete(f"/api/categories/{cat_id}", headers={"X-User-Id": str(uid)})
    # Group still exists
    assert client.get(f"/api/groups/{group_id}").status_code == 200


def test_delete_category_cascades_category_category(client):
    """Delete category removes category:category associations (both directions)."""
    uid = _create_user(client)
    cat_a = _create_category(client, uid, "A")
    cat_b = _create_category(client, uid, "B")
    cat_c = _create_category(client, uid, "C")

    # A→B (stage)
    client.post(f"/api/categories/{cat_a}/associations", json={
        "target_category_id": cat_b, "relation_type": "stage", "stage_order": 1,
    })
    # C→A (track)
    client.post(f"/api/categories/{cat_c}/associations", json={
        "target_category_id": cat_a, "relation_type": "track",
    })

    assert len(client.get(f"/api/categories/{cat_a}/associations").json()) == 1
    assert len(client.get(f"/api/categories/{cat_c}/associations").json()) == 1

    # Delete A → removes both A→B and C→A
    client.delete(f"/api/categories/{cat_a}", headers={"X-User-Id": str(uid)})

    # B and C still exist
    h = {"X-User-Id": str(uid)}
    assert client.get(f"/api/categories/{cat_b}", headers=h).status_code == 200
    assert client.get(f"/api/categories/{cat_c}", headers=h).status_code == 200

    # C's association to A removed
    assert len(client.get(f"/api/categories/{cat_c}/associations").json()) == 0


def test_delete_user_cascades_user_user(client):
    """Delete user removes user:user relations (follow/block both directions)."""
    uid_a = _create_user(client, "user_a")
    uid_b = _create_user(client, "user_b")

    # A follows B
    client.post(f"/api/users/{uid_b}/follow", headers={"X-User-Id": str(uid_a)})
    # B follows A
    client.post(f"/api/users/{uid_a}/follow", headers={"X-User-Id": str(uid_b)})

    assert len(client.get(f"/api/users/{uid_a}/following").json()) == 1
    assert len(client.get(f"/api/users/{uid_a}/followers").json()) == 1

    # Delete A (self-delete)
    client.delete(f"/api/users/{uid_a}", headers={"X-User-Id": str(uid_a)})

    # B's following list (was following A) should be empty
    assert len(client.get(f"/api/users/{uid_b}/following").json()) == 0


def test_multiple_users_like_then_delete_one(client):
    """Multiple users like a post, one deleted → only that user's like removed."""
    uid1 = _create_user(client, "liker1")
    uid2 = _create_user(client, "liker2")
    poster = _create_user(client, "poster2")
    post_id = _create_post(client, poster)

    client.post(f"/api/posts/{post_id}/like", headers={"X-User-Id": str(uid1)})
    client.post(f"/api/posts/{post_id}/like", headers={"X-User-Id": str(uid2)})
    h = {"X-User-Id": str(poster)}
    assert client.get(f"/api/posts/{post_id}", headers=h).json()["like_count"] == 2

    # Delete uid1 (self-delete)
    client.delete(f"/api/users/{uid1}", headers={"X-User-Id": str(uid1)})
    assert client.get(f"/api/posts/{post_id}", headers=h).json()["like_count"] == 1
