"""Mock authentication tests — covers mock auth mode switching and auto user creation."""
import pytest
from unittest.mock import patch

from app.core.config import Settings


def _create_user(client, username, role="participant"):
    """Helper to create a user for testing."""
    resp = client.post("/api/users", json={
        "username": username,
        "email": f"{username}@example.com",
        "role": role,
    })
    return resp.json()


# ---------- Mock Mode Tests ----------

def test_mock_auth_enabled_by_default():
    """TC-MOCK-001: Mock auth is enabled by default."""
    from app.core.config import settings
    # In test environment, mock_auth should be True
    assert settings.mock_auth is True


def test_require_user_with_valid_header(client):
    """TC-MOCK-002: With valid X-User-Id header, returns that user's ID."""
    user = _create_user(client, "mock_valid")

    # Access an endpoint that requires auth
    resp = client.get("/api/notifications", headers={"X-User-Id": str(user["id"])})
    assert resp.status_code == 200


def test_require_user_with_invalid_header(client):
    """TC-MOCK-003: With invalid X-User-Id (non-existent), returns 401."""
    resp = client.get("/api/notifications", headers={"X-User-Id": "99999"})
    assert resp.status_code == 401
    assert "User not found" in resp.json()["detail"]


def test_require_user_without_header_creates_mock_user(client):
    """TC-MOCK-004: Without X-User-Id header, auto-creates and uses mock user."""
    # This test depends on the mock_auth behavior
    # When no header is provided, it should create a mock user
    resp = client.get("/api/notifications")  # No auth header

    # In mock mode with auto-create, this should succeed
    # The endpoint will use the auto-created mock user
    assert resp.status_code == 200


def test_mock_user_auto_creation_idempotent(client):
    """TC-MOCK-005: Multiple requests without header use same mock user."""
    # First request - creates mock user
    resp1 = client.get("/api/notifications")
    assert resp1.status_code == 200

    # Second request - reuses mock user
    resp2 = client.get("/api/notifications")
    assert resp2.status_code == 200


# ---------- Role Check Tests in Mock Mode ----------

def test_role_check_with_valid_role(client):
    """TC-MOCK-010: Role check passes for user with allowed role."""
    admin = _create_user(client, "mock_admin", role="admin")

    # Access admin endpoint (POST /admin/posts/batch-update-status requires admin role)
    resp = client.post(
        "/api/admin/posts/batch-update-status",
        json={"ids": [], "status": "published"},
        headers={"X-User-Id": str(admin["id"])}
    )
    # Should not fail with 403 (might be 200 for empty batch)
    assert resp.status_code != 403


def test_role_check_with_invalid_role(client):
    """TC-MOCK-011: Role check fails for user with wrong role."""
    participant = _create_user(client, "mock_participant", role="participant")

    # Try to access admin endpoint
    resp = client.post(
        "/api/admin/posts/batch-update-status",
        json={"ids": [], "status": "published"},
        headers={"X-User-Id": str(participant["id"])}
    )
    assert resp.status_code == 403
    assert "not allowed" in resp.json()["detail"].lower()


# ---------- Config Tests ----------

def test_settings_from_env():
    """TC-MOCK-020: Settings can be loaded from environment."""
    with patch.dict("os.environ", {
        "MOCK_AUTH": "false",
        "MOCK_USER_ID": "42",
        "MOCK_USER_ROLE": "admin",
    }):
        # Create new settings instance to pick up env vars
        new_settings = Settings()
        assert new_settings.mock_auth is False
        assert new_settings.mock_user_id == 42
        assert new_settings.mock_user_role == "admin"


def test_settings_default_values():
    """TC-MOCK-021: Settings have sensible defaults."""
    from app.core.config import settings

    # Default values
    assert settings.mock_auth is True
    assert settings.mock_user_id == 1
    assert settings.mock_user_role == "participant"
    assert settings.api_prefix == "/api"


# ---------- Helper Function Tests ----------

def test_is_mock_auth_enabled(client):
    """TC-MOCK-030: is_mock_auth_enabled returns correct value."""
    from app.deps import is_mock_auth_enabled

    # Should return True in test environment
    assert is_mock_auth_enabled() is True


# ---------- Integration Tests ----------

def test_login_works_in_mock_mode(client):
    """TC-MOCK-040: Login endpoint works in mock mode."""
    user = _create_user(client, "mock_login_user")

    resp = client.post("/api/auth/login", json={
        "username": "mock_login_user",
        "password": "any_password",
    })
    assert resp.status_code == 200
    assert resp.json()["user_id"] == user["id"]


def test_logout_works_in_mock_mode(client):
    """TC-MOCK-041: Logout endpoint works in mock mode."""
    user = _create_user(client, "mock_logout_user")

    resp = client.post("/api/auth/logout", headers={"X-User-Id": str(user["id"])})
    assert resp.status_code == 204


def test_follow_works_in_mock_mode(client):
    """TC-MOCK-042: Follow endpoint works in mock mode."""
    user1 = _create_user(client, "mock_follower")
    user2 = _create_user(client, "mock_followee")

    resp = client.post(
        f"/api/users/{user2['id']}/follow",
        headers={"X-User-Id": str(user1["id"])}
    )
    assert resp.status_code == 201


def test_notification_crud_works_in_mock_mode(client, db_session):
    """TC-MOCK-043: Notification CRUD works in mock mode."""
    user = _create_user(client, "mock_notif_user")

    # Create notification via direct DB access (simulating system event)
    from app.crud.notifications import notifications as notif_crud
    notif_crud.create(
        db_session,
        user_id=user["id"],
        type="system",
        content="Test notification in mock mode"
    )

    # Read via API
    resp = client.get("/api/notifications", headers={"X-User-Id": str(user["id"])})
    assert resp.status_code == 200
    assert resp.json()["total"] == 1
