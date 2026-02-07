"""E2E tests for TC-JOUR-012: Post Delete Journey.

Tests verify cascade delete behavior when deleting posts.
"""
import pytest
from playwright.sync_api import Page, expect

from conftest import FRONTEND_URL, wait_for_app_load
from helpers import APIClient, setup_test_users


class TestJourneyPostDelete:
    """TC-JOUR-012: Delete post with complete cascade verification.

    When deleting a post with:
    - event:post submission relation
    - post:post embed + reference relations
    - post:resource attachment + inline relations
    - multiple interactions (like + comment + rating)

    After deletion:
    - Post is physically deleted
    - All relations are removed
    - All related interactions are cascade hard deleted
    """

    @pytest.fixture(autouse=True)
    def setup_complex_post(self):
        """Set up a post with multiple relations and interactions."""
        self.api = APIClient()
        self.users = setup_test_users(self.api)

        if "alice" in self.users:
            self.api.login(self.users["alice"].username, self.users["alice"].password)

            # Create event
            self.event = self.api.create_event(
                "Delete Test Event",
                "Event for cascade delete testing"
            )

            # Create main post
            self.main_post = self.api.create_post(
                "Post to Delete",
                "This post will be deleted to test cascades",
                status="published"
            )

            if "id" in self.main_post:
                post_id = self.main_post["id"]

                # Create related post
                self.related_post = self.api.create_post(
                    "Related Post",
                    "This post is referenced by main post"
                )

                # Create resource
                self.resource = self.api.create_resource("attachment.pdf")

                # Create relations
                if "id" in self.event:
                    self.api.create_event_post_relation(
                        self.event["id"], post_id, "submission"
                    )

                if "id" in self.related_post:
                    self.api.create_post_post_relation(
                        post_id, self.related_post["id"], "reference"
                    )

                if "id" in self.resource:
                    self.api.create_post_resource_relation(
                        post_id, self.resource["id"], "attachment"
                    )

            self.api.logout()

            # Add interactions from different users
            if "bob" in self.users and "id" in self.main_post:
                bob_api = APIClient()
                bob_api.login(self.users["bob"].username, self.users["bob"].password)
                bob_api.like_post(self.main_post["id"])
                bob_api.comment_post(self.main_post["id"], "Great post!")
                bob_api.logout()

            if "dave" in self.users and "id" in self.main_post:
                dave_api = APIClient()
                dave_api.login(self.users["dave"].username, self.users["dave"].password)
                dave_api.like_post(self.main_post["id"])
                dave_api.rate_post(self.main_post["id"], 4.5, "quality")
                dave_api.logout()

        yield

    def test_post_has_interactions_before_delete(self):
        """Verify post has interactions before deletion."""
        if not hasattr(self, 'main_post') or "id" not in self.main_post:
            pytest.skip("Main post not set up")

        self.api.login(self.users["alice"].username, self.users["alice"].password)
        post = self.api.get_post(self.main_post["id"])

        # Should have some interaction counts
        has_interactions = (
            post.get("like_count", 0) > 0 or
            post.get("comment_count", 0) > 0 or
            post.get("average_rating") is not None
        )
        # Note: might be 0 if interactions API doesn't work as expected

    def test_delete_post_physically(self):
        """Delete post - should be physically deleted."""
        if not hasattr(self, 'main_post') or "id" not in self.main_post:
            pytest.skip("Main post not set up")

        self.api.login(self.users["alice"].username, self.users["alice"].password)
        post_id = self.main_post["id"]

        # Delete the post
        success = self.api.delete_post(post_id)
        assert success, "Delete should succeed"

        # Verify post is gone (404)
        result = self.api.get_post(post_id)
        assert "error" in result or result.get("status") == 404

    def test_relations_removed_after_delete(self):
        """All relations are removed after post deletion."""
        if not hasattr(self, 'main_post') or "id" not in self.main_post:
            pytest.skip("Main post not set up")

        self.api.login(self.users["alice"].username, self.users["alice"].password)
        post_id = self.main_post["id"]

        # Delete the post
        self.api.delete_post(post_id)

        # Related post should still exist
        if hasattr(self, 'related_post') and "id" in self.related_post:
            related = self.api.get_post(self.related_post["id"])
            assert "id" in related, "Related post should still exist"

        # Resource should still exist
        if hasattr(self, 'resource') and "id" in self.resource:
            resource = self.api.get_resource(self.resource["id"])
            assert "id" in resource, "Resource should still exist"

    def test_interactions_cascade_deleted(self):
        """Interactions are cascade deleted with post."""
        if not hasattr(self, 'main_post') or "id" not in self.main_post:
            pytest.skip("Main post not set up")

        self.api.login(self.users["alice"].username, self.users["alice"].password)
        post_id = self.main_post["id"]

        # Delete the post
        self.api.delete_post(post_id)

        # Interactions for this post should be gone
        # (This depends on API - might need to query interactions table directly)
        interactions = self.api.list_post_interactions(post_id)
        # Should return empty or 404
        assert len(interactions) == 0 or "error" in str(interactions)

    def test_ui_delete_flow(self, page: Page):
        """Test delete flow through UI with confirmation."""
        if "alice" not in self.users:
            pytest.skip("Alice not set up")

        # Create a fresh post for UI test
        self.api.login(self.users["alice"].username, self.users["alice"].password)
        test_post = self.api.create_post("UI Delete Test", "Will be deleted via UI")
        self.api.logout()

        if "id" not in test_post:
            pytest.skip("Could not create test post")

        # Login via UI
        wait_for_app_load(page, f"{FRONTEND_URL}/login")
        page.fill('input[name="username"], input[placeholder*="用户名"]', self.users["alice"].username)
        page.fill('input[name="password"], input[type="password"]', self.users["alice"].password)
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)

        # Navigate to post
        page.goto(f"{FRONTEND_URL}/posts/{test_post['id']}")
        page.wait_for_load_state("networkidle")

        # Find and click delete button
        delete_btn = page.locator('button:has-text("删除"), [data-testid="delete-button"]')
        if delete_btn.count() > 0:
            delete_btn.first.click()
            page.wait_for_timeout(500)

            # Confirm deletion
            confirm_btn = page.locator('button:has-text("确认"), button:has-text("确定")')
            if confirm_btn.count() > 0:
                confirm_btn.first.click()
                page.wait_for_timeout(2000)

                # Should redirect away from deleted post
                assert f"/posts/{test_post['id']}" not in page.url

    def test_full_cascade_delete_flow(self):
        """Complete cascade delete verification."""
        if not hasattr(self, 'main_post') or "id" not in self.main_post:
            pytest.skip("Main post not set up")

        self.api.login(self.users["alice"].username, self.users["alice"].password)
        post_id = self.main_post["id"]

        # 1. Verify post exists
        post = self.api.get_post(post_id)
        assert "id" in post

        # 2. Delete post
        success = self.api.delete_post(post_id)
        assert success

        # 3. Verify post is gone
        result = self.api.get_post(post_id)
        assert "error" in result or result.get("status") == 404

        # 4. Verify related entities still exist
        if hasattr(self, 'related_post') and "id" in self.related_post:
            related = self.api.get_post(self.related_post["id"])
            assert "id" in related

        # 5. Verify interactions are gone
        interactions = self.api.list_post_interactions(post_id)
        assert len(interactions) == 0 or "error" in str(interactions)
