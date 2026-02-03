"""Group API tests — covers TC-GRP-001 through TC-GRP-901"""


def _create_user(client, username="owner", role="organizer"):
    """Helper: create a user and return their ID."""
    resp = client.post("/api/users", json={
        "username": username,
        "email": f"{username}@example.com",
        "role": role,
    })
    return resp.json()["id"]


# ---------- TC-GRP-001: 创建公开团队（需审批）----------
def test_create_public_group_with_approval(client):
    uid = _create_user(client)
    resp = client.post("/api/groups", json={
        "name": "Team Alpha",
        "description": "A public team requiring approval",
        "visibility": "public",
        "require_approval": True,
        "max_members": 5,
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Team Alpha"
    assert data["visibility"] == "public"
    assert data["require_approval"] is True
    assert data["max_members"] == 5
    assert data["created_by"] == uid
    assert "id" in data
    assert "created_at" in data


# ---------- TC-GRP-002: 创建私有团队（无需审批）----------
def test_create_private_group_without_approval(client):
    uid = _create_user(client)
    resp = client.post("/api/groups", json={
        "name": "Team Beta",
        "description": "A private team without approval",
        "visibility": "private",
        "require_approval": False,
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201
    data = resp.json()
    assert data["visibility"] == "private"
    assert data["require_approval"] is False


# ---------- TC-GRP-010: Owner 更新团队描述和 max_members ----------
def test_update_group_description_and_max_members(client):
    uid = _create_user(client)
    create_resp = client.post("/api/groups", json={
        "name": "Team Gamma",
        "visibility": "public",
        "max_members": 5,
    }, headers={"X-User-Id": str(uid)})
    group_id = create_resp.json()["id"]

    resp = client.patch(f"/api/groups/{group_id}", json={
        "description": "Updated description",
        "max_members": 10,
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 200
    data = resp.json()
    assert data["description"] == "Updated description"
    assert data["max_members"] == 10


# ---------- TC-GRP-011: 修改 require_approval (true → false) ----------
def test_update_require_approval(client):
    uid = _create_user(client)
    create_resp = client.post("/api/groups", json={
        "name": "Team Delta",
        "visibility": "public",
        "require_approval": True,
    }, headers={"X-User-Id": str(uid)})
    group_id = create_resp.json()["id"]

    resp = client.patch(f"/api/groups/{group_id}", json={
        "require_approval": False,
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 200
    assert resp.json()["require_approval"] is False


# ---------- TC-GRP-012: 修改 visibility (public → private) ----------
def test_update_visibility(client):
    uid = _create_user(client)
    create_resp = client.post("/api/groups", json={
        "name": "Team Epsilon",
        "visibility": "public",
    }, headers={"X-User-Id": str(uid)})
    group_id = create_resp.json()["id"]

    resp = client.patch(f"/api/groups/{group_id}", json={
        "visibility": "private",
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 200
    assert resp.json()["visibility"] == "private"


# ---------- TC-GRP-020: 删除团队 (soft delete) ----------
def test_delete_group(client):
    uid = _create_user(client)
    create_resp = client.post("/api/groups", json={
        "name": "Team Delete Me",
        "visibility": "public",
    }, headers={"X-User-Id": str(uid)})
    group_id = create_resp.json()["id"]

    del_resp = client.delete(f"/api/groups/{group_id}", headers={"X-User-Id": str(uid)})
    assert del_resp.status_code == 204

    # Group should no longer be accessible
    get_resp = client.get(f"/api/groups/{group_id}")
    assert get_resp.status_code == 404

    # Group should not appear in list
    list_resp = client.get("/api/groups")
    assert list_resp.status_code == 200
    names = [g["name"] for g in list_resp.json()["items"]]
    assert "Team Delete Me" not in names


# ---------- TC-GRP-900: 无效 visibility 枚举被拒绝 ----------
def test_invalid_visibility_rejected(client):
    uid = _create_user(client)
    resp = client.post("/api/groups", json={
        "name": "Bad Visibility",
        "visibility": "restricted",
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 422


# ---------- TC-GRP-901: 未认证用户无法创建团队 ----------
def test_unauthenticated_cannot_create_group(client):
    """Creating group with invalid user returns 401.

    Note: In mock mode, requests without X-User-Id header auto-create a mock user.
    This test verifies auth failure by providing an invalid (non-existent) user ID.
    """
    resp = client.post("/api/groups", json={
        "name": "No Auth Group",
        "visibility": "public",
    }, headers={"X-User-Id": "99999"})
    assert resp.status_code == 401


# ---------- Additional: list groups ----------
def test_list_groups(client):
    uid = _create_user(client)
    client.post("/api/groups", json={"name": "G1", "visibility": "public"}, headers={"X-User-Id": str(uid)})
    client.post("/api/groups", json={"name": "G2", "visibility": "private"}, headers={"X-User-Id": str(uid)})
    resp = client.get("/api/groups")
    assert resp.status_code == 200
    assert resp.json()["total"] == 2


def test_list_groups_filter_by_visibility(client):
    uid = _create_user(client)
    client.post("/api/groups", json={"name": "G1", "visibility": "public"}, headers={"X-User-Id": str(uid)})
    client.post("/api/groups", json={"name": "G2", "visibility": "private"}, headers={"X-User-Id": str(uid)})
    resp = client.get("/api/groups?visibility=private")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["visibility"] == "private"


def test_list_groups_filter_invalid_visibility_rejected(client):
    uid = _create_user(client)
    client.post("/api/groups", json={"name": "G1", "visibility": "public"}, headers={"X-User-Id": str(uid)})
    resp = client.get("/api/groups?visibility=secret")
    assert resp.status_code == 422


# ---------- Additional: get nonexistent group ----------
def test_get_nonexistent_group(client):
    resp = client.get("/api/groups/9999")
    assert resp.status_code == 404


# ---------- Additional: default visibility is public ----------
def test_default_visibility_is_public(client):
    uid = _create_user(client)
    resp = client.post("/api/groups", json={
        "name": "Default Vis",
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201
    assert resp.json()["visibility"] == "public"


# ---------- Additional: default require_approval is false ----------
def test_default_require_approval_is_false(client):
    uid = _create_user(client)
    resp = client.post("/api/groups", json={
        "name": "Default Approval",
        "visibility": "public",
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201
    assert resp.json()["require_approval"] is False
