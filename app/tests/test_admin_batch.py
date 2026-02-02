"""Tests for admin batch operations (Phase 13)"""
import pytest
from app.tests.conftest import make_auth_headers


class TestBatchDeletePosts:
    """Tests for POST /admin/posts/batch-delete"""

    def test_batch_delete_posts_success(self, client, admin_user, auth_headers):
        """Admin can batch delete multiple posts"""
        # Create posts
        h = auth_headers(admin_user["id"])
        posts = []
        for i in range(3):
            resp = client.post("/api/posts", json={
                "title": f"Post {i}",
                "type": "general",
            }, headers=h)
            assert resp.status_code == 201
            posts.append(resp.json())

        # Batch delete
        resp = client.post("/api/admin/posts/batch-delete", json={
            "ids": [p["id"] for p in posts]
        }, headers=h)
        assert resp.status_code == 200
        data = resp.json()
        assert data["success_count"] == 3
        assert data["failed_count"] == 0

        # Verify posts are deleted (soft delete)
        for p in posts:
            resp = client.get(f"/api/posts/{p['id']}")
            assert resp.status_code == 404

    def test_batch_delete_posts_partial_failure(self, client, admin_user, auth_headers):
        """Batch delete with some invalid IDs"""
        h = auth_headers(admin_user["id"])

        # Create one post
        resp = client.post("/api/posts", json={
            "title": "Valid Post",
            "type": "general",
        }, headers=h)
        assert resp.status_code == 201
        valid_post = resp.json()

        # Try to delete valid post + non-existent IDs
        resp = client.post("/api/admin/posts/batch-delete", json={
            "ids": [valid_post["id"], 9999, 9998]
        }, headers=h)
        assert resp.status_code == 200
        data = resp.json()
        assert data["success_count"] == 1
        assert data["failed_count"] == 2
        assert 9999 in data["failed_ids"]
        assert 9998 in data["failed_ids"]

    def test_batch_delete_posts_non_admin_forbidden(self, client, participant_user, auth_headers):
        """Non-admin users cannot batch delete"""
        h = auth_headers(participant_user["id"])
        resp = client.post("/api/admin/posts/batch-delete", json={
            "ids": [1, 2, 3]
        }, headers=h)
        assert resp.status_code == 403


class TestBatchUpdatePostStatus:
    """Tests for POST /admin/posts/batch-update-status"""

    def test_batch_update_status_success(self, client, admin_user, auth_headers):
        """Admin can batch update post statuses"""
        h = auth_headers(admin_user["id"])

        # Create posts (default status is draft)
        posts = []
        for i in range(3):
            resp = client.post("/api/posts", json={
                "title": f"Post {i}",
                "type": "general",
            }, headers=h)
            assert resp.status_code == 201
            posts.append(resp.json())

        # Batch update to published
        resp = client.post("/api/admin/posts/batch-update-status", json={
            "ids": [p["id"] for p in posts],
            "status": "published"
        }, headers=h)
        assert resp.status_code == 200
        data = resp.json()
        assert data["success_count"] == 3
        assert data["failed_count"] == 0

        # Verify statuses are updated
        for p in posts:
            resp = client.get(f"/api/posts/{p['id']}")
            assert resp.status_code == 200
            assert resp.json()["status"] == "published"

    def test_batch_update_status_invalid_status(self, client, admin_user, auth_headers):
        """Invalid status is rejected"""
        h = auth_headers(admin_user["id"])
        resp = client.post("/api/admin/posts/batch-update-status", json={
            "ids": [1],
            "status": "invalid_status"
        }, headers=h)
        assert resp.status_code == 422

    def test_batch_update_status_partial_failure(self, client, admin_user, auth_headers):
        """Batch update with some invalid IDs"""
        h = auth_headers(admin_user["id"])

        # Create one post
        resp = client.post("/api/posts", json={
            "title": "Valid Post",
            "type": "general",
        }, headers=h)
        assert resp.status_code == 201
        valid_post = resp.json()

        # Try to update valid post + non-existent ID
        resp = client.post("/api/admin/posts/batch-update-status", json={
            "ids": [valid_post["id"], 9999],
            "status": "published"
        }, headers=h)
        assert resp.status_code == 200
        data = resp.json()
        assert data["success_count"] == 1
        assert data["failed_count"] == 1
        assert 9999 in data["failed_ids"]

    def test_batch_update_status_non_admin_forbidden(self, client, participant_user, auth_headers):
        """Non-admin users cannot batch update statuses"""
        h = auth_headers(participant_user["id"])
        resp = client.post("/api/admin/posts/batch-update-status", json={
            "ids": [1],
            "status": "published"
        }, headers=h)
        assert resp.status_code == 403


class TestBatchUpdateUserRoles:
    """Tests for POST /admin/users/batch-update-roles"""

    def test_batch_update_roles_success(self, client, admin_user, auth_headers):
        """Admin can batch update user roles"""
        h = auth_headers(admin_user["id"])

        # Create users
        users = []
        for i in range(3):
            resp = client.post("/api/users", json={
                "username": f"user_{i}",
                "email": f"user_{i}@example.com",
                "role": "participant"
            })
            assert resp.status_code == 201
            users.append(resp.json())

        # Batch update to organizer
        resp = client.post("/api/admin/users/batch-update-roles", json={
            "ids": [u["id"] for u in users],
            "role": "organizer"
        }, headers=h)
        assert resp.status_code == 200
        data = resp.json()
        assert data["success_count"] == 3
        assert data["failed_count"] == 0

        # Verify roles are updated
        for u in users:
            resp = client.get(f"/api/users/{u['id']}")
            assert resp.status_code == 200
            assert resp.json()["role"] == "organizer"

    def test_batch_update_roles_invalid_role(self, client, admin_user, auth_headers):
        """Invalid role is rejected"""
        h = auth_headers(admin_user["id"])
        resp = client.post("/api/admin/users/batch-update-roles", json={
            "ids": [1],
            "role": "superadmin"
        }, headers=h)
        assert resp.status_code == 422

    def test_batch_update_roles_partial_failure(self, client, admin_user, auth_headers):
        """Batch update with some invalid IDs"""
        h = auth_headers(admin_user["id"])

        # Create one user
        resp = client.post("/api/users", json={
            "username": "valid_user",
            "email": "valid@example.com",
            "role": "participant"
        })
        assert resp.status_code == 201
        valid_user = resp.json()

        # Try to update valid user + non-existent ID
        resp = client.post("/api/admin/users/batch-update-roles", json={
            "ids": [valid_user["id"], 9999],
            "role": "organizer"
        }, headers=h)
        assert resp.status_code == 200
        data = resp.json()
        assert data["success_count"] == 1
        assert data["failed_count"] == 1
        assert 9999 in data["failed_ids"]

    def test_batch_update_roles_non_admin_forbidden(self, client, participant_user, auth_headers):
        """Non-admin users cannot batch update roles"""
        h = auth_headers(participant_user["id"])
        resp = client.post("/api/admin/users/batch-update-roles", json={
            "ids": [1],
            "role": "organizer"
        }, headers=h)
        assert resp.status_code == 403

    def test_batch_update_roles_to_admin(self, client, admin_user, auth_headers):
        """Admin can promote users to admin"""
        h = auth_headers(admin_user["id"])

        # Create a participant
        resp = client.post("/api/users", json={
            "username": "promote_me",
            "email": "promote@example.com",
            "role": "participant"
        })
        assert resp.status_code == 201
        user = resp.json()

        # Promote to admin
        resp = client.post("/api/admin/users/batch-update-roles", json={
            "ids": [user["id"]],
            "role": "admin"
        }, headers=h)
        assert resp.status_code == 200
        assert resp.json()["success_count"] == 1

        # Verify role is updated
        resp = client.get(f"/api/users/{user['id']}")
        assert resp.json()["role"] == "admin"
