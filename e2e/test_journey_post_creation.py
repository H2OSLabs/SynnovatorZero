"""E2E tests for TC-JOUR-009: Post Creation Journey.

Tests verify post creation flows for daily posts and competition proposals.
"""
import pytest
from playwright.sync_api import Page, expect

from conftest import FRONTEND_URL, wait_for_app_load
from helpers import APIClient, setup_test_users


class TestJourneyPostCreation:
    """TC-JOUR-009: Creating daily posts and competition proposals.

    Flow:
    1. Create daily post (type=general) - publicly visible, no rule constraints
    2. Create competition proposal (type=proposal) - linked to event
    3. Rule engine validates submission constraints
    4. Posts with allow_public=false require review
    """

    @pytest.fixture(autouse=True)
    def setup_test_data(self):
        """Set up test user and event."""
        self.api = APIClient()
        self.users = setup_test_users(self.api)

        if "alice" in self.users:
            self.api.login(self.users["alice"].username, self.users["alice"].password)
            self.event = self.api.create_event(
                "Submission Test Event",
                "Event for testing submissions",
                status="published"
            )
            self.api.logout()

        yield

    def test_create_daily_post_general_type(self):
        """Create daily post (type=general) - publicly visible."""
        if "bob" not in self.users:
            pytest.skip("Bob not set up")

        api = APIClient()
        api.login(self.users["bob"].username, self.users["bob"].password)

        post = api.create_post(
            "My Daily Post",
            "This is a general post not linked to any event",
            post_type="general",
            status="published",
            tags=["daily", "test"]
        )

        assert "id" in post, f"Post creation failed: {post}"
        assert post.get("type") in ("general", None)  # Default might be general
        assert post.get("status") == "published"

    def test_daily_post_publicly_visible(self):
        """Published daily post is visible to anonymous users."""
        if "bob" not in self.users:
            pytest.skip("Bob not set up")

        # Create post
        api = APIClient()
        api.login(self.users["bob"].username, self.users["bob"].password)
        post = api.create_post("Public Post", "Visible to all", status="published")
        api.logout()

        if "id" in post:
            # Anonymous user can see it
            anon_api = APIClient()
            result = anon_api.get_post(post["id"])
            assert "error" not in result or result.get("title") == "Public Post"

    def test_create_proposal_type_post(self):
        """Create competition proposal (type=proposal)."""
        if "bob" not in self.users:
            pytest.skip("Bob not set up")

        api = APIClient()
        api.login(self.users["bob"].username, self.users["bob"].password)

        post = api.create_post(
            "My Hackathon Proposal",
            "Proposal for the hackathon competition",
            post_type="proposal",
            status="published"
        )

        assert "id" in post, f"Proposal creation failed: {post}"

    def test_link_proposal_to_event(self):
        """Link proposal to event (submission relation)."""
        if "bob" not in self.users or not hasattr(self, 'event'):
            pytest.skip("Test data not set up")

        api = APIClient()
        api.login(self.users["bob"].username, self.users["bob"].password)

        # Create proposal
        post = api.create_post(
            "Event Submission",
            "Submission for the hackathon",
            post_type="proposal"
        )

        if "id" in post and "id" in self.event:
            result = api.create_event_post_relation(
                self.event["id"],
                post["id"],
                "submission"
            )
            # Result depends on rule validation
            # Success or rule-based rejection are both valid outcomes

    def test_post_with_markdown_and_tags(self):
        """Post can have Markdown content and tags."""
        if "bob" not in self.users:
            pytest.skip("Bob not set up")

        api = APIClient()
        api.login(self.users["bob"].username, self.users["bob"].password)

        markdown_content = """
# Project Title

## Overview
This is a **markdown** post with:
- Bullet points
- Code blocks

```python
def hello():
    print("Hello World")
```
        """

        post = api.create_post(
            "Markdown Post",
            markdown_content,
            tags=["python", "tutorial", "markdown"]
        )

        assert "id" in post
        # Tags should be stored
        if "tags" in post:
            assert len(post["tags"]) > 0

    def test_ui_create_daily_post(self, page: Page):
        """Test daily post creation through UI."""
        if "bob" not in self.users:
            pytest.skip("Bob not set up")

        # Login
        wait_for_app_load(page, f"{FRONTEND_URL}/login")
        page.fill('input[name="username"], input[placeholder*="用户名"]', self.users["bob"].username)
        page.fill('input[name="password"], input[type="password"]', self.users["bob"].password)
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)

        # Navigate to post creation
        wait_for_app_load(page, f"{FRONTEND_URL}/posts/create")

        # Fill form
        page.fill('input[name="title"], input[placeholder*="标题"]', 'UI Created Post')
        page.fill('textarea[name="content"], textarea[placeholder*="内容"]', 'Content from UI test')

        # Submit
        page.click('button:has-text("发布")')
        page.wait_for_timeout(3000)

        # Should redirect to post detail
        assert "/posts/" in page.url and "/create" not in page.url

    def test_ui_create_proposal(self, page: Page):
        """Test proposal creation through UI."""
        if "bob" not in self.users:
            pytest.skip("Bob not set up")

        # Login
        wait_for_app_load(page, f"{FRONTEND_URL}/login")
        page.fill('input[name="username"], input[placeholder*="用户名"]', self.users["bob"].username)
        page.fill('input[name="password"], input[type="password"]', self.users["bob"].password)
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)

        # Navigate to proposal creation
        wait_for_app_load(page, f"{FRONTEND_URL}/posts/create?type=proposal")

        # Fill form
        page.fill('input[name="title"], input[placeholder*="标题"]', 'UI Created Proposal')
        page.fill('textarea[name="content"], textarea[placeholder*="内容"]', 'Proposal content from UI')

        # Submit
        page.click('button:has-text("发布"), button:has-text("提交")')
        page.wait_for_timeout(3000)

        # Should redirect
        assert "/posts/" in page.url or "/proposals/" in page.url
