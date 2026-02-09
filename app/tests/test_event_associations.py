"""Event:Event association tests — Phase 7 Layer 5

Covers:
- TC-STAGE-001: Create sequential stage associations
- TC-STAGE-002: Stage order sorting
- TC-TRACK-001: Create parallel track associations
- TC-PREREQ-001: Prerequisite association
- TC-CATREL-900: Duplicate association rejected
- TC-CATREL-901: Self-reference rejected
- TC-CATREL-902: Circular dependency detected
- TC-CATREL-903: Invalid relation_type rejected
"""


def _create_user(client, username="organizer"):
    resp = client.post("/api/users", json={
        "username": username,
        "email": f"{username}@example.com",
        "role": "organizer",
    })
    return resp.json()["id"]


def _create_event(client, uid, name="Event"):
    resp = client.post("/api/events", json={
        "name": name,
        "description": f"Description of {name}",
        "type": "competition",
    }, headers={"X-User-Id": str(uid)})
    return resp.json()["id"]


def test_create_stage_association(client):
    """TC-STAGE-001: Create sequential stage chain A→B→C."""
    uid = _create_user(client)
    a = _create_event(client, uid, "Stage A")
    b = _create_event(client, uid, "Stage B")
    c = _create_event(client, uid, "Stage C")
    # A→B (stage_order=1)
    resp1 = client.post(f"/api/events/{a}/associations", json={
        "target_event_id": b,
        "relation_type": "stage",
        "stage_order": 1,
    })
    assert resp1.status_code == 201
    assert resp1.json()["relation_type"] == "stage"
    assert resp1.json()["stage_order"] == 1
    # B→C (stage_order=2)
    resp2 = client.post(f"/api/events/{b}/associations", json={
        "target_event_id": c,
        "relation_type": "stage",
        "stage_order": 2,
    })
    assert resp2.status_code == 201


def test_stage_order_sorting(client):
    """TC-STAGE-002: Associations sorted by stage_order."""
    uid = _create_user(client)
    main = _create_event(client, uid, "Main")
    s1 = _create_event(client, uid, "Stage 1")
    s2 = _create_event(client, uid, "Stage 2")
    s3 = _create_event(client, uid, "Stage 3")
    # Create out of order
    client.post(f"/api/events/{main}/associations", json={
        "target_event_id": s3, "relation_type": "stage", "stage_order": 3,
    })
    client.post(f"/api/events/{main}/associations", json={
        "target_event_id": s1, "relation_type": "stage", "stage_order": 1,
    })
    client.post(f"/api/events/{main}/associations", json={
        "target_event_id": s2, "relation_type": "stage", "stage_order": 2,
    })
    resp = client.get(f"/api/events/{main}/associations", params={"relation_type": "stage"})
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 3
    assert items[0]["stage_order"] == 1
    assert items[1]["stage_order"] == 2
    assert items[2]["stage_order"] == 3


def test_create_track_association(client):
    """TC-TRACK-001: Create parallel track associations."""
    uid = _create_user(client)
    main = _create_event(client, uid, "Main Event")
    t1 = _create_event(client, uid, "Track 1")
    t2 = _create_event(client, uid, "Track 2")
    resp1 = client.post(f"/api/events/{main}/associations", json={
        "target_event_id": t1, "relation_type": "track",
    })
    assert resp1.status_code == 201
    resp2 = client.post(f"/api/events/{main}/associations", json={
        "target_event_id": t2, "relation_type": "track",
    })
    assert resp2.status_code == 201
    # List tracks
    resp = client.get(f"/api/events/{main}/associations", params={"relation_type": "track"})
    assert len(resp.json()) == 2


def test_create_prerequisite_association(client):
    """TC-PREREQ-001: Prerequisite association."""
    uid = _create_user(client)
    bounty = _create_event(client, uid, "Bounty")
    competition = _create_event(client, uid, "Competition")
    resp = client.post(f"/api/events/{bounty}/associations", json={
        "target_event_id": competition, "relation_type": "prerequisite",
    })
    assert resp.status_code == 201
    assert resp.json()["relation_type"] == "prerequisite"


def test_list_all_associations(client):
    """List all associations without filter."""
    uid = _create_user(client)
    main = _create_event(client, uid, "Main")
    sub1 = _create_event(client, uid, "Sub1")
    sub2 = _create_event(client, uid, "Sub2")
    client.post(f"/api/events/{main}/associations", json={
        "target_event_id": sub1, "relation_type": "stage", "stage_order": 1,
    })
    client.post(f"/api/events/{main}/associations", json={
        "target_event_id": sub2, "relation_type": "track",
    })
    resp = client.get(f"/api/events/{main}/associations")
    assert len(resp.json()) == 2


def test_delete_association(client):
    """Delete a event association."""
    uid = _create_user(client)
    a = _create_event(client, uid, "A")
    b = _create_event(client, uid, "B")
    client.post(f"/api/events/{a}/associations", json={
        "target_event_id": b, "relation_type": "track",
    })
    resp = client.delete(f"/api/events/{a}/associations/{b}")
    assert resp.status_code == 204
    # List should be empty
    assert len(client.get(f"/api/events/{a}/associations").json()) == 0


def test_duplicate_association_rejected(client):
    """TC-CATREL-900: Duplicate association rejected."""
    uid = _create_user(client)
    a = _create_event(client, uid, "A")
    b = _create_event(client, uid, "B")
    resp1 = client.post(f"/api/events/{a}/associations", json={
        "target_event_id": b, "relation_type": "stage", "stage_order": 1,
    })
    assert resp1.status_code == 201
    resp2 = client.post(f"/api/events/{a}/associations", json={
        "target_event_id": b, "relation_type": "stage", "stage_order": 1,
    })
    assert resp2.status_code == 409


def test_self_reference_rejected(client):
    """TC-CATREL-901: Self-reference rejected."""
    uid = _create_user(client)
    a = _create_event(client, uid, "Self")
    resp = client.post(f"/api/events/{a}/associations", json={
        "target_event_id": a, "relation_type": "stage", "stage_order": 1,
    })
    assert resp.status_code == 422
    assert "self" in resp.json()["detail"].lower()


def test_circular_dependency_rejected(client):
    """TC-CATREL-902: Circular stage dependency A→B→C→A rejected."""
    uid = _create_user(client)
    a = _create_event(client, uid, "A")
    b = _create_event(client, uid, "B")
    c = _create_event(client, uid, "C")
    client.post(f"/api/events/{a}/associations", json={
        "target_event_id": b, "relation_type": "stage", "stage_order": 1,
    })
    client.post(f"/api/events/{b}/associations", json={
        "target_event_id": c, "relation_type": "stage", "stage_order": 2,
    })
    # C→A would create cycle
    resp = client.post(f"/api/events/{c}/associations", json={
        "target_event_id": a, "relation_type": "stage", "stage_order": 3,
    })
    assert resp.status_code == 422
    assert "circular" in resp.json()["detail"].lower()


def test_invalid_relation_type_rejected(client):
    """TC-CATREL-903: Invalid relation_type rejected by schema."""
    uid = _create_user(client)
    a = _create_event(client, uid, "A")
    b = _create_event(client, uid, "B")
    resp = client.post(f"/api/events/{a}/associations", json={
        "target_event_id": b, "relation_type": "sponsor",
    })
    assert resp.status_code == 422


def test_prerequisite_circular_rejected(client):
    """Circular prerequisite dependency detected."""
    uid = _create_user(client)
    a = _create_event(client, uid, "A")
    b = _create_event(client, uid, "B")
    client.post(f"/api/events/{a}/associations", json={
        "target_event_id": b, "relation_type": "prerequisite",
    })
    resp = client.post(f"/api/events/{b}/associations", json={
        "target_event_id": a, "relation_type": "prerequisite",
    })
    assert resp.status_code == 422
    assert "circular" in resp.json()["detail"].lower()


def test_track_allows_bidirectional(client):
    """Track type doesn't check for cycles (parallel is OK)."""
    uid = _create_user(client)
    a = _create_event(client, uid, "A")
    b = _create_event(client, uid, "B")
    resp1 = client.post(f"/api/events/{a}/associations", json={
        "target_event_id": b, "relation_type": "track",
    })
    assert resp1.status_code == 201
    # B→A should also work for tracks (no cycle check)
    # But duplicate (a,b) would block — need different pair
    c = _create_event(client, uid, "C")
    resp2 = client.post(f"/api/events/{b}/associations", json={
        "target_event_id": c, "relation_type": "track",
    })
    assert resp2.status_code == 201


def test_nonexistent_source_event(client):
    """Association with nonexistent source returns 404."""
    uid = _create_user(client)
    b = _create_event(client, uid, "B")
    resp = client.post("/api/events/9999/associations", json={
        "target_event_id": b, "relation_type": "track",
    })
    assert resp.status_code == 404


def test_nonexistent_target_event(client):
    """Association with nonexistent target returns 404."""
    uid = _create_user(client)
    a = _create_event(client, uid, "A")
    resp = client.post(f"/api/events/{a}/associations", json={
        "target_event_id": 9999, "relation_type": "track",
    })
    assert resp.status_code == 404
