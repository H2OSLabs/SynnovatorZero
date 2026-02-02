"""Resource API tests — covers TC-RES-001 through TC-RES-903 (Layer 0 scope)"""


def _create_user(client, username="testuser", email="test@example.com"):
    """Helper: create a user and return the user id."""
    resp = client.post("/api/users", json={
        "username": username,
        "email": email,
        "role": "participant",
    })
    return resp.json()["id"]


# ---------- TC-RES-001: 最小字段创建资源 ----------
def test_create_resource_minimal(client):
    user_id = _create_user(client)
    resp = client.post(
        "/api/resources",
        json={"filename": "test-file.txt"},
        headers={"X-User-Id": str(user_id)},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["filename"] == "test-file.txt"
    assert data["created_by"] == user_id
    assert "id" in data
    assert "created_at" in data


# ---------- TC-RES-002: 带完整元信息创建资源 ----------
def test_create_resource_full(client):
    user_id = _create_user(client)
    resp = client.post(
        "/api/resources",
        json={
            "filename": "demo.mp4",
            "display_name": "Demo Video",
            "description": "Project demonstration",
            "mime_type": "video/mp4",
        },
        headers={"X-User-Id": str(user_id)},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["filename"] == "demo.mp4"
    assert data["display_name"] == "Demo Video"
    assert data["description"] == "Project demonstration"
    assert data["mime_type"] == "video/mp4"


# ---------- TC-RES-030: 更新资源元信息 ----------
def test_update_resource_metadata(client):
    user_id = _create_user(client)
    create_resp = client.post(
        "/api/resources",
        json={"filename": "doc.pdf"},
        headers={"X-User-Id": str(user_id)},
    )
    resource_id = create_resp.json()["id"]

    resp = client.patch(f"/api/resources/{resource_id}", json={
        "display_name": "Updated Name",
        "description": "Updated description",
    }, headers={"X-User-Id": str(user_id)})
    assert resp.status_code == 200
    data = resp.json()
    assert data["display_name"] == "Updated Name"
    assert data["description"] == "Updated description"


# ---------- TC-RES-031: 删除资源 (soft delete) ----------
def test_delete_resource(client):
    user_id = _create_user(client)
    create_resp = client.post(
        "/api/resources",
        json={"filename": "to-delete.txt"},
        headers={"X-User-Id": str(user_id)},
    )
    resource_id = create_resp.json()["id"]

    del_resp = client.delete(f"/api/resources/{resource_id}", headers={"X-User-Id": str(user_id)})
    assert del_resp.status_code == 204

    # Resource should no longer be accessible
    get_resp = client.get(f"/api/resources/{resource_id}")
    assert get_resp.status_code == 404

    # Resource should not appear in list
    list_resp = client.get("/api/resources")
    filenames = [r["filename"] for r in list_resp.json()["items"]]
    assert "to-delete.txt" not in filenames


# ---------- TC-RES-900: 缺少 filename 被拒绝 ----------
def test_missing_filename_rejected(client):
    user_id = _create_user(client)
    resp = client.post(
        "/api/resources",
        json={},
        headers={"X-User-Id": str(user_id)},
    )
    assert resp.status_code == 422


# ---------- TC-RES-901: 未登录用户创建资源被拒绝 ----------
def test_unauthenticated_create_rejected(client):
    """Creating resource with invalid user returns 401.

    Note: In mock mode, requests without X-User-Id header auto-create a mock user.
    This test verifies auth failure by providing an invalid (non-existent) user ID.
    """
    resp = client.post("/api/resources", json={"filename": "test.txt"}, headers={"X-User-Id": "99999"})
    assert resp.status_code == 401


# ---------- Additional: list resources ----------
def test_list_resources(client):
    user_id = _create_user(client)
    headers = {"X-User-Id": str(user_id)}
    client.post("/api/resources", json={"filename": "f1.txt"}, headers=headers)
    client.post("/api/resources", json={"filename": "f2.txt"}, headers=headers)
    resp = client.get("/api/resources")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


# ---------- Additional: get nonexistent resource ----------
def test_get_nonexistent_resource(client):
    resp = client.get("/api/resources/9999")
    assert resp.status_code == 404


# ---------- Additional: read created resource back ----------
def test_read_resource(client):
    user_id = _create_user(client)
    create_resp = client.post(
        "/api/resources",
        json={"filename": "readable.txt"},
        headers={"X-User-Id": str(user_id)},
    )
    resource_id = create_resp.json()["id"]
    get_resp = client.get(f"/api/resources/{resource_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["filename"] == "readable.txt"
