"""Auth API tests — covers login, logout, and token refresh endpoints."""


def _create_user(client, username, role="participant"):
    """Helper to create a user for testing."""
    resp = client.post("/api/users", json={
        "username": username,
        "email": f"{username}@example.com",
        "role": role,
    })
    return resp.json()


# ---------- Login Tests ----------

def test_login_success(client):
    """TC-AUTH-001: Successful login returns user info."""
    user = _create_user(client, "auth_user")

    resp = client.post("/api/auth/login", json={
        "username": "auth_user",
        "password": "any_password",  # Password not verified in current implementation
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["user_id"] == user["id"]
    assert data["username"] == "auth_user"
    assert data["role"] == "participant"


def test_login_admin_user(client):
    """TC-AUTH-002: Admin user login returns admin role."""
    user = _create_user(client, "admin_auth", role="admin")

    resp = client.post("/api/auth/login", json={
        "username": "admin_auth",
        "password": "any_password",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["role"] == "admin"


def test_login_organizer_user(client):
    """TC-AUTH-003: Organizer user login returns organizer role."""
    user = _create_user(client, "organizer_auth", role="organizer")

    resp = client.post("/api/auth/login", json={
        "username": "organizer_auth",
        "password": "any_password",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["role"] == "organizer"


def test_login_invalid_username(client):
    """TC-AUTH-004: Login with non-existent username returns 401."""
    resp = client.post("/api/auth/login", json={
        "username": "nonexistent_user",
        "password": "any_password",
    })
    assert resp.status_code == 401
    assert "Invalid username or password" in resp.json()["detail"]


def test_login_empty_username(client):
    """TC-AUTH-005: Login with empty username returns 401 (user not found)."""
    resp = client.post("/api/auth/login", json={
        "username": "",
        "password": "any_password",
    })
    # Empty username is valid but no user exists with empty username
    assert resp.status_code == 401


def test_login_missing_password(client):
    """TC-AUTH-006: Login without password field returns 422."""
    _create_user(client, "no_pwd_user")

    resp = client.post("/api/auth/login", json={
        "username": "no_pwd_user",
    })
    assert resp.status_code == 422


# ---------- Logout Tests ----------

def test_logout_success(client):
    """TC-AUTH-010: Successful logout returns 204."""
    user = _create_user(client, "logout_user")

    resp = client.post("/api/auth/logout", headers={"X-User-Id": str(user["id"])})
    assert resp.status_code == 204


def test_logout_without_auth(client):
    """TC-AUTH-011: Logout with invalid user ID returns 401.

    Note: In mock mode, requests without X-User-Id header auto-create a mock user.
    This test verifies auth failure by providing an invalid (non-existent) user ID.
    """
    resp = client.post("/api/auth/logout", headers={"X-User-Id": "99999"})
    assert resp.status_code == 401


def test_logout_invalid_user_id(client):
    """TC-AUTH-012: Logout with non-existent user returns 401 (user validation is enforced)."""
    # User ID validation is enforced - logout requires a valid user
    resp = client.post("/api/auth/logout", headers={"X-User-Id": "99999"})
    assert resp.status_code == 401


# ---------- Token Refresh Tests ----------

def test_refresh_not_implemented(client):
    """TC-AUTH-020: Token refresh returns 501 (not implemented)."""
    resp = client.post("/api/auth/refresh", json={
        "refresh_token": "any_token",
    })
    assert resp.status_code == 501
    assert "not implemented" in resp.json()["detail"].lower()


# ---------- Integration Tests ----------

def test_login_then_use_session(client):
    """TC-AUTH-030: Login then use returned user_id for authenticated requests."""
    _create_user(client, "session_user")

    # Login
    login_resp = client.post("/api/auth/login", json={
        "username": "session_user",
        "password": "password",
    })
    assert login_resp.status_code == 200
    user_id = login_resp.json()["user_id"]

    # Use the user_id for an authenticated request
    # Update user profile
    update_resp = client.patch(
        f"/api/users/{user_id}",
        json={"bio": "Updated bio"},
        headers={"X-User-Id": str(user_id)},
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["bio"] == "Updated bio"


def test_login_multiple_users(client):
    """TC-AUTH-031: Multiple users can login independently."""
    user1 = _create_user(client, "multi_user1")
    user2 = _create_user(client, "multi_user2")

    # Login user1
    resp1 = client.post("/api/auth/login", json={
        "username": "multi_user1",
        "password": "password",
    })
    assert resp1.status_code == 200
    assert resp1.json()["user_id"] == user1["id"]

    # Login user2
    resp2 = client.post("/api/auth/login", json={
        "username": "multi_user2",
        "password": "password",
    })
    assert resp2.status_code == 200
    assert resp2.json()["user_id"] == user2["id"]
