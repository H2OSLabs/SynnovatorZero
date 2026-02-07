"""Event:Rule relation tests — Phase 6 Layer 4

Covers:
- TC-REL-CR-001: Associate rule to event with priority
- TC-REL-CR-002: Update event:rule priority
- TC-REL-CR-003: Delete event:rule (rule itself preserved)
- TC-REL-CR-900: Duplicate association rejected
"""


def _create_user(client, username="organizer"):
    resp = client.post("/api/users", json={
        "username": username,
        "email": f"{username}@example.com",
        "role": "organizer",
    })
    return resp.json()["id"]


def _create_event(client, uid, name="Test Event"):
    resp = client.post("/api/events", json={
        "name": name,
        "description": "A test event",
        "type": "competition",
    }, headers={"X-User-Id": str(uid)})
    return resp.json()["id"]


def _create_rule(client, uid, name="Test Rule"):
    resp = client.post("/api/rules", json={
        "name": name,
        "description": "A test rule",
        "max_submissions": 5,
    }, headers={"X-User-Id": str(uid)})
    return resp.json()["id"]


def test_associate_rule_to_category(client):
    """TC-REL-CR-001: Associate rule to event with priority."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    rule_id = _create_rule(client, uid)
    resp = client.post(f"/api/events/{cat_id}/rules", json={
        "rule_id": rule_id,
        "priority": 1,
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["event_id"] == cat_id
    assert data["rule_id"] == rule_id
    assert data["priority"] == 1


def test_list_category_rules(client):
    """List rules associated with a event, ordered by priority."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    r1 = _create_rule(client, uid, "Rule A")
    r2 = _create_rule(client, uid, "Rule B")
    client.post(f"/api/events/{cat_id}/rules", json={"rule_id": r1, "priority": 2})
    client.post(f"/api/events/{cat_id}/rules", json={"rule_id": r2, "priority": 1})
    resp = client.get(f"/api/events/{cat_id}/rules")
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 2
    # Priority-ordered: r2 (1) before r1 (2)
    assert items[0]["rule_id"] == r2
    assert items[1]["rule_id"] == r1


def test_update_category_rule_priority(client):
    """TC-REL-CR-002: Update priority from 1 to 10."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    rule_id = _create_rule(client, uid)
    client.post(f"/api/events/{cat_id}/rules", json={"rule_id": rule_id, "priority": 1})
    resp = client.patch(f"/api/events/{cat_id}/rules/{rule_id}", json={
        "rule_id": rule_id,
        "priority": 10,
    })
    assert resp.status_code == 200
    assert resp.json()["priority"] == 10


def test_delete_event_rule_preserves_rule(client):
    """TC-REL-CR-003: Delete relation, rule itself preserved."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    rule_id = _create_rule(client, uid)
    client.post(f"/api/events/{cat_id}/rules", json={"rule_id": rule_id, "priority": 0})
    resp = client.delete(f"/api/events/{cat_id}/rules/{rule_id}")
    assert resp.status_code == 204
    # Relation gone
    rules = client.get(f"/api/events/{cat_id}/rules")
    assert len(rules.json()) == 0
    # Rule still exists
    rule_resp = client.get(f"/api/rules/{rule_id}")
    assert rule_resp.status_code == 200


def test_duplicate_association_rejected(client):
    """TC-REL-CR-900: Same rule twice on same event rejected."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    rule_id = _create_rule(client, uid)
    resp1 = client.post(f"/api/events/{cat_id}/rules", json={"rule_id": rule_id, "priority": 0})
    assert resp1.status_code == 201
    resp2 = client.post(f"/api/events/{cat_id}/rules", json={"rule_id": rule_id, "priority": 0})
    assert resp2.status_code == 409


def test_associate_rule_to_nonexistent_category(client):
    """Associate rule to nonexistent event returns 404."""
    uid = _create_user(client)
    rule_id = _create_rule(client, uid)
    resp = client.post("/api/events/9999/rules", json={"rule_id": rule_id, "priority": 0})
    assert resp.status_code == 404


def test_associate_nonexistent_rule_to_category(client):
    """Associate nonexistent rule to event returns 404."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    resp = client.post(f"/api/events/{cat_id}/rules", json={"rule_id": 9999, "priority": 0})
    assert resp.status_code == 404
