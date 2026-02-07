"""Category:Group relation tests — Phase 6 Layer 4

Covers:
- TC-REL-CG-001: Team registers for category
- TC-REL-CG-002: List registered teams
- TC-REL-CG-003: Team unregisters (DELETE)
- TC-REL-CG-900: Duplicate registration rejected
- TC-REL-CG-901: (deferred — same user in multiple groups check requires member data)
"""


def _create_user(client, username="organizer"):
    resp = client.post("/api/users", json={
        "username": username,
        "email": f"{username}@example.com",
        "role": "organizer",
    })
    return resp.json()["id"]


def _create_category(client, uid, name="Competition"):
    resp = client.post("/api/categories", json={
        "name": name,
        "description": "A test competition",
        "type": "competition",
    }, headers={"X-User-Id": str(uid)})
    return resp.json()["id"]


def _create_group(client, uid, name="Team Alpha"):
    resp = client.post("/api/groups", json={
        "name": name,
    }, headers={"X-User-Id": str(uid)})
    return resp.json()["id"]


def test_register_team_proposal(client):
    """TC-REL-CG-001: Team registers for category."""
    uid = _create_user(client)
    cat_id = _create_category(client, uid)
    group_id = _create_group(client, uid)
    resp = client.post(f"/api/categories/{cat_id}/groups", json={
        "group_id": group_id,
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["category_id"] == cat_id
    assert data["group_id"] == group_id


def test_list_registered_teams(client):
    """TC-REL-CG-002: List registered teams."""
    uid = _create_user(client)
    cat_id = _create_category(client, uid)
    g1 = _create_group(client, uid, "Team Alpha")
    g2 = _create_group(client, uid, "Team Beta")
    client.post(f"/api/categories/{cat_id}/groups", json={"group_id": g1})
    client.post(f"/api/categories/{cat_id}/groups", json={"group_id": g2})
    resp = client.get(f"/api/categories/{cat_id}/groups")
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 2
    group_ids = {item["group_id"] for item in items}
    assert g1 in group_ids
    assert g2 in group_ids


def test_unregister_team(client):
    """TC-REL-CG-003: Team unregisters from category."""
    uid = _create_user(client)
    cat_id = _create_category(client, uid)
    group_id = _create_group(client, uid)
    client.post(f"/api/categories/{cat_id}/groups", json={"group_id": group_id})
    resp = client.delete(f"/api/categories/{cat_id}/groups/{group_id}")
    assert resp.status_code == 204
    # List should be empty
    list_resp = client.get(f"/api/categories/{cat_id}/groups")
    assert len(list_resp.json()) == 0


def test_duplicate_registration_rejected(client):
    """TC-REL-CG-900: Same team registers twice rejected."""
    uid = _create_user(client)
    cat_id = _create_category(client, uid)
    group_id = _create_group(client, uid)
    resp1 = client.post(f"/api/categories/{cat_id}/groups", json={"group_id": group_id})
    assert resp1.status_code == 201
    resp2 = client.post(f"/api/categories/{cat_id}/groups", json={"group_id": group_id})
    assert resp2.status_code == 409


def test_register_nonexistent_category(client):
    """Register team to nonexistent category returns 404."""
    uid = _create_user(client)
    group_id = _create_group(client, uid)
    resp = client.post("/api/categories/9999/groups", json={"group_id": group_id})
    assert resp.status_code == 404


def test_register_nonexistent_group(client):
    """Register nonexistent group to category returns 404."""
    uid = _create_user(client)
    cat_id = _create_category(client, uid)
    resp = client.post(f"/api/categories/{cat_id}/groups", json={"group_id": 9999})
    assert resp.status_code == 404


def test_unregister_nonexistent_relation(client):
    """Unregister non-registered group returns 404."""
    uid = _create_user(client)
    cat_id = _create_category(client, uid)
    group_id = _create_group(client, uid)
    resp = client.delete(f"/api/categories/{cat_id}/groups/{group_id}")
    assert resp.status_code == 404
