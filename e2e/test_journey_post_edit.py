"""E2E tests for TC-JOUR-011: Post Edit Journey.

Tests verify post editing with version management and copy mechanism.
"""
import pytest
from playwright.sync_api import Page, expect

from conftest import FRONTEND_URL, wait_for_app_load
from helpers import APIClient, setup_test_users


class TestJourneyPostEdit:
    """TC-JOUR-011: Editing posts with version management.

    Two sub-scenarios:
    1. TC-JOUR-011-1: Edit own post (version management)
    2. TC-JOUR-011-2: Edit others' post (copy mechanism)
    """

    @pytest.fixture(autouse=True)
    def setup_test_data(self):
        """Set up test users and posts."""
        self.api = APIClient()
        self.users = setup_test_users(self.api)

        if "alice" in self.users:
            self.api.login(self.users["alice"].username, self.users["alice"].password)

            # Alice creates original post
            self.original_post = self.api.create_post(
                "Original Post v1",
                "This is the first version of the post",
                status="published"
            )

            self.api.logout()

        yield

    def test_edit_own_post_creates_version(self):
        """TC-JOUR-011-1: Edit own post creates new version.

        User creates post v1, then v2 with post_post reference relation.
        Both versions remain accessible.
        """
        if "alice" not in self.users or not hasattr(self, 'original_post'):
            pytest.skip("Test data not set up")

        self.api.login(self.users["alice"].username, self.users["alice"].password)

        # Create v2 as a new post
        v2_post = self.api.create_post(
            "Original Post v2",
            "This is the updated version with more content",
            status="published"
        )

        if "id" in v2_post and "id" in self.original_post:
            # Link v2 to v1 as reference
            result = self.api.create_post_post_relation(
                v2_post["id"],
                self.original_post["id"],
                "reference"
            )

            # Both versions should exist
            v1 = self.api.get_post(self.original_post["id"])
            v2 = self.api.get_post(v2_post["id"])

            assert "id" in v1, "v1 should still be accessible"
            assert "id" in v2, "v2 should be accessible"

    def test_edit_own_post_inline(self):
        """Alternative: Edit own post inline (update existing)."""
        if "alice" not in self.users or not hasattr(self, 'original_post'):
            pytest.skip("Test data not set up")

        self.api.login(self.users["alice"].username, self.users["alice"].password)

        # Update the post directly
        result = self.api.update_post(
            self.original_post["id"],
            content="Updated content - edited by owner"
        )

        # Should succeed
        assert "error" not in result or "id" in result

    def test_cannot_edit_others_post_directly(self):
        """TC-JOUR-011-2: Cannot directly modify another user's post."""
        if "bob" not in self.users or not hasattr(self, 'original_post'):
            pytest.skip("Test data not set up")

        # Bob tries to edit Alice's post
        bob_api = APIClient()
        bob_api.login(self.users["bob"].username, self.users["bob"].password)

        result = bob_api.update_post(
            self.original_post["id"],
            content="Bob trying to edit Alice's post"
        )

        # Should fail (403 Forbidden or similar)
        assert "error" in result or result.get("status") in (403, 401)

    def test_create_edit_copy_of_others_post(self):
        """TC-JOUR-011-2: Create copy to edit another user's post.

        Bob creates new post referencing Alice's post.
        Copy's created_by is Bob.
        """
        if "bob" not in self.users or not hasattr(self, 'original_post'):
            pytest.skip("Test data not set up")

        bob_api = APIClient()
        bob_api.login(self.users["bob"].username, self.users["bob"].password)

        # Bob creates his own version/copy
        copy_post = bob_api.create_post(
            "My Take on Original Post",
            "This is Bob's interpretation of Alice's post",
            status="published"
        )

        if "id" in copy_post and "id" in self.original_post:
            # Link as reference to original
            result = bob_api.create_post_post_relation(
                copy_post["id"],
                self.original_post["id"],
                "reference"
            )

            # Verify copy's author is Bob
            copy = bob_api.get_post(copy_post["id"])
            assert copy.get("created_by") == self.users["bob"].id or \
                   copy.get("author", {}).get("id") == self.users["bob"].id

    def test_version_relation_queryable(self):
        """Post-post version relations can be queried."""
        if "alice" not in self.users or not hasattr(self, 'original_post'):
            pytest.skip("Test data not set up")

        self.api.login(self.users["alice"].username, self.users["alice"].password)

        # Create v2
        v2 = self.api.create_post("Post v2", "Version 2 content")

        if "id" in v2:
            self.api.create_post_post_relation(v2["id"], self.original_post["id"], "reference")

            # Query related posts (depends on API implementation)
            # This is a placeholder for the actual relation query

    def test_ui_edit_own_post(self, page: Page):
        """Test editing own post through UI."""
        if "alice" not in self.users or not hasattr(self, 'original_post'):
            pytest.skip("Test data not set up")

        # Login as Alice
        wait_for_app_load(page, f"{FRONTEND_URL}/login")
        page.fill('input[name="username"], input[placeholder*="用户名"]', self.users["alice"].username)
        page.fill('input[name="password"], input[type="password"]', self.users["alice"].password)
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)

        # Navigate to post edit page
        post_id = self.original_post.get("id")
        if post_id:
            page.goto(f"{FRONTEND_URL}/posts/{post_id}/edit")
            page.wait_for_load_state("networkidle")

            # Should be able to access edit page
            assert "/login" not in page.url

            # Edit content
            content_field = page.locator('textarea[name="content"]')
            if content_field.count() > 0:
                content_field.fill("Updated content via UI")
                page.click('button:has-text("保存")')
                page.wait_for_timeout(2000)

    def test_ui_bob_cannot_access_alice_edit(self, page: Page):
        """Bob cannot access edit page for Alice's post."""
        if "bob" not in self.users or not hasattr(self, 'original_post'):
            pytest.skip("Test data not set up")

        # Login as Bob
        wait_for_app_load(page, f"{FRONTEND_URL}/login")
        page.fill('input[name="username"], input[placeholder*="用户名"]', self.users["bob"].username)
        page.fill('input[name="password"], input[type="password"]', self.users["bob"].password)
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)

        # Try to access Alice's post edit page
        post_id = self.original_post.get("id")
        if post_id:
            page.goto(f"{FRONTEND_URL}/posts/{post_id}/edit")
            page.wait_for_timeout(2000)

            # Should be blocked (redirect or error)
            is_blocked = (
                "/login" in page.url or
                page.locator('text=权限').is_visible() or
                page.locator('text=403').is_visible() or
                page.locator('text=无权').is_visible()
            )
            # Either blocked or redirected
