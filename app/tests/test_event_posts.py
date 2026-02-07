"""Event:Post relation tests — Phase 6 Layer 4

Covers:
- TC-REL-CP-001: Associate post as submission
- TC-REL-CP-002: Associate post as reference
- TC-REL-CP-003: Filter by relation_type=submission
- TC-REL-CP-004: List all without filter
- TC-REL-CP-900: (deferred — deadline enforcement, Phase 7)
- TC-REL-CP-901: (deferred — format check, Phase 7)
- TC-REL-CP-902: Max submissions enforcement
"""


def _create_user(client, username="author"):
    resp = client.post("/api/users", json={
        "username": username,
        "email": f"{username}@example.com",
        "role": "organizer",
    })
    return resp.json()["id"]


def _create_event(client, uid, name="Contest"):
    resp = client.post("/api/events", json={
        "name": name,
        "description": "A test contest",
        "type": "competition",
    }, headers={"X-User-Id": str(uid)})
    return resp.json()["id"]


def _create_post(client, uid, title="My Submission"):
    resp = client.post("/api/posts", json={
        "title": title,
    }, headers={"X-User-Id": str(uid)})
    return resp.json()["id"]


def _create_rule(client, uid, max_submissions=None):
    body = {"name": "Rule", "description": "A test rule"}
    if max_submissions is not None:
        body["max_submissions"] = max_submissions
    resp = client.post("/api/rules", json=body, headers={"X-User-Id": str(uid)})
    return resp.json()["id"]


def test_associate_post_as_submission(client):
    """TC-REL-CP-001: Associate post as submission."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    post_id = _create_post(client, uid)
    resp = client.post(f"/api/events/{cat_id}/posts", json={
        "post_id": post_id,
        "relation_type": "submission",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["event_id"] == cat_id
    assert data["post_id"] == post_id
    assert data["relation_type"] == "submission"


def test_associate_post_as_reference(client):
    """TC-REL-CP-002: Associate post as reference."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    post_id = _create_post(client, uid)
    resp = client.post(f"/api/events/{cat_id}/posts", json={
        "post_id": post_id,
        "relation_type": "reference",
    })
    assert resp.status_code == 201
    assert resp.json()["relation_type"] == "reference"


def test_filter_by_relation_type(client):
    """TC-REL-CP-003: Filter by relation_type=submission."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    p1 = _create_post(client, uid, "Submission Post")
    p2 = _create_post(client, uid, "Reference Post")
    client.post(f"/api/events/{cat_id}/posts", json={"post_id": p1, "relation_type": "submission"})
    client.post(f"/api/events/{cat_id}/posts", json={"post_id": p2, "relation_type": "reference"})
    h = {"X-User-Id": str(uid)}
    resp = client.get(f"/api/events/{cat_id}/posts", params={"relation_type": "submission"}, headers=h)
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 1
    assert items[0]["post_id"] == p1


def test_list_all_category_posts(client):
    """TC-REL-CP-004: List all without filter."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    p1 = _create_post(client, uid, "Post A")
    p2 = _create_post(client, uid, "Post B")
    client.post(f"/api/events/{cat_id}/posts", json={"post_id": p1, "relation_type": "submission"})
    client.post(f"/api/events/{cat_id}/posts", json={"post_id": p2, "relation_type": "reference"})
    resp = client.get(f"/api/events/{cat_id}/posts", headers={"X-User-Id": str(uid)})
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_max_submissions_enforced(client):
    """TC-REL-CP-902: Max submissions reached rejects new submission."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    rule_id = _create_rule(client, uid, max_submissions=1)
    # Associate rule to event
    client.post(f"/api/events/{cat_id}/rules", json={"rule_id": rule_id, "priority": 0})
    # First submission succeeds
    p1 = _create_post(client, uid, "First Submission")
    resp1 = client.post(f"/api/events/{cat_id}/posts", json={"post_id": p1, "relation_type": "submission"})
    assert resp1.status_code == 201
    # Second submission by same user fails
    p2 = _create_post(client, uid, "Second Submission")
    resp2 = client.post(f"/api/events/{cat_id}/posts", json={"post_id": p2, "relation_type": "submission"})
    assert resp2.status_code == 422
    assert "Max submissions" in resp2.json()["detail"]


def test_reference_not_limited_by_max_submissions(client):
    """Reference type not limited by max_submissions rule."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    rule_id = _create_rule(client, uid, max_submissions=1)
    client.post(f"/api/events/{cat_id}/rules", json={"rule_id": rule_id, "priority": 0})
    # First submission
    p1 = _create_post(client, uid, "Submission")
    client.post(f"/api/events/{cat_id}/posts", json={"post_id": p1, "relation_type": "submission"})
    # Reference still allowed even after max submissions
    p2 = _create_post(client, uid, "Reference")
    resp = client.post(f"/api/events/{cat_id}/posts", json={"post_id": p2, "relation_type": "reference"})
    assert resp.status_code == 201


def test_duplicate_category_post_rejected(client):
    """Duplicate event:post association rejected (409)."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    post_id = _create_post(client, uid)
    resp1 = client.post(f"/api/events/{cat_id}/posts", json={"post_id": post_id, "relation_type": "submission"})
    assert resp1.status_code == 201
    resp2 = client.post(f"/api/events/{cat_id}/posts", json={"post_id": post_id, "relation_type": "submission"})
    assert resp2.status_code == 409


def test_remove_category_post(client):
    """Remove event:post relation."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    post_id = _create_post(client, uid)
    resp = client.post(f"/api/events/{cat_id}/posts", json={"post_id": post_id, "relation_type": "submission"})
    relation_id = resp.json()["id"]
    del_resp = client.delete(f"/api/events/{cat_id}/posts/{relation_id}")
    assert del_resp.status_code == 204
    # List should be empty
    list_resp = client.get(f"/api/events/{cat_id}/posts", headers={"X-User-Id": str(uid)})
    assert len(list_resp.json()) == 0


def test_nonexistent_category_rejected(client):
    """Associate post to nonexistent event returns 404."""
    uid = _create_user(client)
    post_id = _create_post(client, uid)
    resp = client.post("/api/events/9999/posts", json={"post_id": post_id, "relation_type": "submission"})
    assert resp.status_code == 404


def test_nonexistent_post_rejected(client):
    """Associate nonexistent post to event returns 404."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    resp = client.post(f"/api/events/{cat_id}/posts", json={"post_id": 9999, "relation_type": "submission"})
    assert resp.status_code == 404
