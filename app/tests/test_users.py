"""User API tests — covers TC-USER-001 through TC-USER-903"""


# ---------- TC-USER-001: 创建 participant 用户 ----------
def test_create_participant_user(client):
    resp = client.post("/api/users", json={
        "username": "alice",
        "email": "alice@example.com",
        "display_name": "Alice",
        "role": "participant",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "alice"
    assert data["email"] == "alice@example.com"
    assert data["display_name"] == "Alice"
    assert data["role"] == "participant"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


# ---------- TC-USER-002: 创建 organizer 用户 ----------
def test_create_organizer_user(client):
    resp = client.post("/api/users", json={
        "username": "judge",
        "email": "judge@example.com",
        "role": "organizer",
    })
    assert resp.status_code == 201
    assert resp.json()["role"] == "organizer"


# ---------- TC-USER-003: 创建 admin 用户 ----------
def test_create_admin_user(client):
    resp = client.post("/api/users", json={
        "username": "admin1",
        "email": "admin1@example.com",
        "role": "admin",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["role"] == "admin"
    # Verify by reading back
    get_resp = client.get(f"/api/users/{data['id']}")
    assert get_resp.status_code == 200
    assert get_resp.json()["role"] == "admin"


# ---------- TC-USER-004: 读取已创建的用户 ----------
def test_read_user(client):
    create_resp = client.post("/api/users", json={
        "username": "bob",
        "email": "bob@example.com",
        "display_name": "Bob Builder",
        "role": "participant",
    })
    user_id = create_resp.json()["id"]

    resp = client.get(f"/api/users/{user_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == "bob"
    assert data["email"] == "bob@example.com"
    assert data["display_name"] == "Bob Builder"
    assert data["role"] == "participant"


# ---------- TC-USER-010: 用户修改自己的个人信息 ----------
def test_update_user_profile(client, auth_headers):
    create_resp = client.post("/api/users", json={
        "username": "bob",
        "email": "bob@example.com",
        "role": "participant",
    })
    user_id = create_resp.json()["id"]

    resp = client.patch(f"/api/users/{user_id}", json={
        "display_name": "Bob Updated",
        "bio": "I build things",
    }, headers=auth_headers(user_id))
    assert resp.status_code == 200
    data = resp.json()
    assert data["display_name"] == "Bob Updated"
    assert data["bio"] == "I build things"


# ---------- TC-USER-011: Admin 修改其他用户的角色 ----------
def test_admin_change_user_role(client, admin_user, auth_headers):
    create_resp = client.post("/api/users", json={
        "username": "charlie",
        "email": "charlie@example.com",
        "role": "participant",
    })
    user_id = create_resp.json()["id"]

    resp = client.patch(f"/api/users/{user_id}", json={
        "role": "organizer",
    }, headers=auth_headers(admin_user["id"]))
    assert resp.status_code == 200
    assert resp.json()["role"] == "organizer"


# ---------- TC-USER-020: 删除用户 (soft delete) ----------
def test_delete_user(client, admin_user, auth_headers):
    create_resp = client.post("/api/users", json={
        "username": "charlie",
        "email": "charlie@example.com",
        "role": "participant",
    })
    user_id = create_resp.json()["id"]

    # Delete (using admin)
    del_resp = client.delete(f"/api/users/{user_id}", headers=auth_headers(admin_user["id"]))
    assert del_resp.status_code == 204

    # User should no longer be accessible
    get_resp = client.get(f"/api/users/{user_id}")
    assert get_resp.status_code == 404

    # User should not appear in list
    list_resp = client.get("/api/users")
    assert list_resp.status_code == 200
    usernames = [u["username"] for u in list_resp.json()["items"]]
    assert "charlie" not in usernames


# ---------- TC-USER-900: 重复 username 被拒绝 ----------
def test_duplicate_username_rejected(client):
    client.post("/api/users", json={
        "username": "alice",
        "email": "alice@example.com",
        "role": "participant",
    })
    resp = client.post("/api/users", json={
        "username": "alice",
        "email": "alice2@example.com",
        "role": "participant",
    })
    assert resp.status_code == 409
    assert "Username already exists" in resp.json()["detail"]


# ---------- TC-USER-901: 重复 email 被拒绝 ----------
def test_duplicate_email_rejected(client):
    client.post("/api/users", json={
        "username": "alice",
        "email": "alice@example.com",
        "role": "participant",
    })
    resp = client.post("/api/users", json={
        "username": "alice2",
        "email": "alice@example.com",
        "role": "participant",
    })
    assert resp.status_code == 409
    assert "Email already exists" in resp.json()["detail"]


# ---------- TC-USER-903: 缺少必填字段 email ----------
def test_missing_required_email(client):
    resp = client.post("/api/users", json={
        "username": "nomail",
    })
    assert resp.status_code == 422


# ---------- Additional: default role ----------
def test_default_role_is_participant(client):
    resp = client.post("/api/users", json={
        "username": "defaultrole",
        "email": "default@example.com",
    })
    assert resp.status_code == 201
    assert resp.json()["role"] == "participant"


# ---------- Additional: invalid role rejected ----------
def test_invalid_role_rejected(client):
    resp = client.post("/api/users", json={
        "username": "badrole",
        "email": "badrole@example.com",
        "role": "superadmin",
    })
    assert resp.status_code == 422


# ---------- Additional: list users ----------
def test_list_users(client):
    client.post("/api/users", json={"username": "u1", "email": "u1@example.com"})
    client.post("/api/users", json={"username": "u2", "email": "u2@example.com"})
    resp = client.get("/api/users")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


# ---------- Additional: get nonexistent user ----------
def test_get_nonexistent_user(client):
    resp = client.get("/api/users/9999")
    assert resp.status_code == 404


# ---------- Additional: update uniqueness check on username ----------
def test_update_duplicate_username_rejected(client, auth_headers):
    client.post("/api/users", json={"username": "u1", "email": "u1@example.com"})
    resp2 = client.post("/api/users", json={"username": "u2", "email": "u2@example.com"})
    user2_id = resp2.json()["id"]
    resp = client.patch(f"/api/users/{user2_id}", json={"username": "u1"}, headers=auth_headers(user2_id))
    assert resp.status_code == 409


# ---------- Additional: update uniqueness check on email ----------
def test_update_duplicate_email_rejected(client, auth_headers):
    client.post("/api/users", json={"username": "u1", "email": "u1@example.com"})
    resp2 = client.post("/api/users", json={"username": "u2", "email": "u2@example.com"})
    user2_id = resp2.json()["id"]
    resp = client.patch(f"/api/users/{user2_id}", json={"email": "u1@example.com"}, headers=auth_headers(user2_id))
    assert resp.status_code == 409
