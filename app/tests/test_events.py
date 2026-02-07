"""Event API tests — covers TC-CAT-001 through TC-CAT-902"""


def _create_user(client, username="organizer", role="organizer"):
    """Helper: create a user and return their ID."""
    resp = client.post("/api/users", json={
        "username": username,
        "email": f"{username}@example.com",
        "role": role,
    })
    return resp.json()["id"]


def _create_event(client, uid, **overrides):
    """Helper: create a event and return the response data."""
    payload = {
        "name": "Test Event",
        "description": "A test event",
        "type": "competition",
    }
    payload.update(overrides)
    resp = client.post("/api/events", json=payload, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201
    return resp.json()


# ---------- TC-CAT-001: 创建 competition 类型活动 ----------
def test_create_competition_event(client):
    uid = _create_user(client)
    resp = client.post("/api/events", json={
        "name": "2025 AI Hackathon",
        "description": "AI innovation competition",
        "type": "competition",
        "content": "# Welcome\n\nJoin us!",
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "2025 AI Hackathon"
    assert data["type"] == "competition"
    assert data["status"] == "draft"
    assert data["content"] == "# Welcome\n\nJoin us!"
    assert data["created_by"] == uid
    assert "id" in data
    assert "created_at" in data


# ---------- TC-CAT-002: 创建 operation 类型活动 ----------
def test_create_operation_event(client):
    uid = _create_user(client)
    resp = client.post("/api/events", json={
        "name": "Weekly Workshop",
        "description": "Regular workshop series",
        "type": "operation",
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201
    data = resp.json()
    assert data["type"] == "operation"
    assert data["status"] == "draft"


# ---------- TC-CAT-003: 读取已创建的活动 ----------
def test_read_event(client):
    uid = _create_user(client)
    cat = _create_event(client, uid, name="Read Me", description="Read test")

    resp = client.get(f"/api/events/{cat['id']}", headers={"X-User-Id": str(uid)})
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Read Me"
    assert data["description"] == "Read test"
    assert data["type"] == "competition"
    assert data["status"] == "draft"
    assert data["created_by"] == uid


# ---------- TC-CAT-010: 状态流: draft → published → closed ----------
def test_status_transition_draft_published_closed(client):
    uid = _create_user(client)
    cat = _create_event(client, uid)
    h = {"X-User-Id": str(uid)}

    # draft → published
    resp1 = client.patch(f"/api/events/{cat['id']}", json={"status": "published"}, headers=h)
    assert resp1.status_code == 200
    assert resp1.json()["status"] == "published"

    # published → closed
    resp2 = client.patch(f"/api/events/{cat['id']}", json={"status": "closed"}, headers=h)
    assert resp2.status_code == 200
    assert resp2.json()["status"] == "closed"


# ---------- TC-CAT-010 (reverse): invalid backwards transition ----------
def test_status_transition_cannot_go_backwards(client):
    uid = _create_user(client)
    cat = _create_event(client, uid)
    h = {"X-User-Id": str(uid)}

    # draft → published
    client.patch(f"/api/events/{cat['id']}", json={"status": "published"}, headers=h)

    # published → draft (invalid)
    resp = client.patch(f"/api/events/{cat['id']}", json={"status": "draft"}, headers=h)
    assert resp.status_code == 422
    assert "Invalid status transition" in resp.json()["detail"]


# ---------- TC-CAT-010: closed is terminal ----------
def test_closed_is_terminal_state(client):
    uid = _create_user(client)
    cat = _create_event(client, uid)
    h = {"X-User-Id": str(uid)}
    client.patch(f"/api/events/{cat['id']}", json={"status": "published"}, headers=h)
    client.patch(f"/api/events/{cat['id']}", json={"status": "closed"}, headers=h)

    # closed → published (invalid)
    resp = client.patch(f"/api/events/{cat['id']}", json={"status": "published"}, headers=h)
    assert resp.status_code == 422

    # closed → draft (invalid)
    resp2 = client.patch(f"/api/events/{cat['id']}", json={"status": "draft"}, headers=h)
    assert resp2.status_code == 422


# ---------- TC-CAT-010: draft cannot skip to closed ----------
def test_draft_cannot_skip_to_closed(client):
    uid = _create_user(client)
    cat = _create_event(client, uid)

    # draft → closed (invalid, must go through published)
    resp = client.patch(f"/api/events/{cat['id']}", json={"status": "closed"}, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 422


# ---------- TC-CAT-011: 修改名称和描述 ----------
def test_update_name_and_description(client):
    uid = _create_user(client)
    cat = _create_event(client, uid)

    resp = client.patch(f"/api/events/{cat['id']}", json={
        "name": "Updated Name",
        "description": "Updated description",
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Updated Name"
    assert data["description"] == "Updated description"


# ---------- TC-CAT-020: 删除活动 (soft delete) ----------
def test_delete_event(client):
    uid = _create_user(client)
    cat = _create_event(client, uid, name="Delete Me")

    del_resp = client.delete(f"/api/events/{cat['id']}", headers={"X-User-Id": str(uid)})
    assert del_resp.status_code == 204

    # Event should no longer be accessible
    get_resp = client.get(f"/api/events/{cat['id']}")
    assert get_resp.status_code == 404

    # Event should not appear in list
    list_resp = client.get("/api/events")
    assert list_resp.status_code == 200
    names = [c["name"] for c in list_resp.json()["items"]]
    assert "Delete Me" not in names


# ---------- TC-CAT-900: 无效 type 枚举被拒绝 ----------
def test_invalid_type_rejected(client):
    uid = _create_user(client)
    resp = client.post("/api/events", json={
        "name": "Bad Type",
        "description": "Invalid type",
        "type": "workshop",
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 422


# ---------- TC-CAT-901: 无效 status 枚举被拒绝 ----------
def test_invalid_status_rejected(client):
    uid = _create_user(client)
    resp = client.post("/api/events", json={
        "name": "Bad Status",
        "description": "Invalid status",
        "type": "competition",
        "status": "archived",
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 422


# ---------- TC-CAT-902: 未认证用户无法创建活动 ----------
def test_unauthenticated_cannot_create_event(client):
    """Creating event with invalid user returns 401.

    Note: In mock mode, requests without X-User-Id header auto-create a mock user.
    This test verifies auth failure by providing an invalid (non-existent) user ID.
    """
    resp = client.post("/api/events", json={
        "name": "No Auth",
        "description": "Should fail",
        "type": "competition",
    }, headers={"X-User-Id": "99999"})
    assert resp.status_code == 401


# ---------- Additional: list events ----------
def test_list_categories(client):
    uid = _create_user(client)
    _create_event(client, uid, name="C1")
    _create_event(client, uid, name="C2")
    resp = client.get("/api/events")
    assert resp.status_code == 200
    assert resp.json()["total"] == 2


def test_list_categories_filter_by_status(client):
    uid = _create_user(client)
    _create_event(client, uid, name="Draft1", status="draft")
    _create_event(client, uid, name="Published1", status="published")
    _create_event(client, uid, name="Closed1", status="closed")

    resp = client.get("/api/events?status=published")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["status"] == "published"


def test_list_categories_filter_by_type(client):
    uid = _create_user(client)
    _create_event(client, uid, name="Comp1", type="competition")
    _create_event(client, uid, name="Op1", type="operation")

    resp = client.get("/api/events?type=operation")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["type"] == "operation"


def test_list_categories_filter_invalid_value_rejected(client):
    uid = _create_user(client)
    _create_event(client, uid, name="C1")

    resp = client.get("/api/events?status=archived")
    assert resp.status_code == 422

    resp2 = client.get("/api/events?type=workshop")
    assert resp2.status_code == 422


# ---------- Additional: get nonexistent event ----------
def test_get_nonexistent_category(client):
    resp = client.get("/api/events/9999")
    assert resp.status_code == 404


# ---------- Additional: default status is draft ----------
def test_default_status_is_draft(client):
    uid = _create_user(client)
    cat = _create_event(client, uid)
    assert cat["status"] == "draft"


# ---------- Additional: same status transition is allowed (no-op) ----------
def test_same_status_transition_is_noop(client):
    uid = _create_user(client)
    cat = _create_event(client, uid)

    # draft → draft should be fine (no change)
    resp = client.patch(f"/api/events/{cat['id']}", json={"status": "draft"}, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 200
    assert resp.json()["status"] == "draft"
