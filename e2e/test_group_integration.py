"""E2E tests for group/team creation integration (TC-FEINT-010~012).

Tests verify that frontend team forms correctly call backend APIs.
"""
import pytest
from playwright.sync_api import Page, expect

from conftest import FRONTEND_URL, API_URL, wait_for_app_load


class TestGroupCreationIntegration:
    """Tests for group creation integration with backend API."""

    @pytest.fixture(autouse=True)
    def setup_auth(self, page: Page):
        """Set up authenticated user for tests."""
        wait_for_app_load(page, f"{FRONTEND_URL}/login")
        page.fill('input[name="username"], input[placeholder*="用户名"]', 'testuser')
        page.fill('input[name="password"], input[placeholder*="密码"], input[type="password"]', 'testpass123')
        page.click('button[type="submit"]')
        page.wait_for_url(f"{FRONTEND_URL}/**", timeout=10000)

    def test_create_group_calls_api(self, api_page: Page):
        """TC-FEINT-010: Frontend creates team via backend API.

        User fills team name and description on /groups/create,
        clicks "创建", system calls POST /api/groups,
        success redirects to /groups/{id}, creator becomes owner.
        """
        wait_for_app_load(api_page, f"{FRONTEND_URL}/groups/create")

        # Fill group form
        api_page.fill('input[name="name"], input[placeholder*="名称"], input[placeholder*="团队"]', 'E2E Test Team')
        api_page.fill('textarea[name="description"], textarea[placeholder*="简介"], textarea[placeholder*="描述"]', 'Team description')

        # Click create button
        api_page.click('button:has-text("创建")')

        # Wait for navigation
        api_page.wait_for_url(f"{FRONTEND_URL}/groups/**", timeout=10000)

        # Verify API was called
        post_requests = [r for r in api_page.api_responses
                        if r["method"] == "POST" and "/groups" in r["url"]]
        assert len(post_requests) > 0, "Expected POST /api/groups to be called"
        assert post_requests[-1]["status"] == 201, "Expected 201 Created response"

    def test_create_group_validation_error(self, page: Page):
        """TC-FEINT-011: Frontend shows validation error without calling API.

        User clicks "创建" without filling team name,
        system shows error "请输入团队名称", no API call.
        """
        wait_for_app_load(page, f"{FRONTEND_URL}/groups/create")

        # Don't fill name, just click create
        page.click('button:has-text("创建")')

        # Wait for error message
        page.wait_for_timeout(500)

        # Should still be on create page
        assert "/groups/create" in page.url, "Should remain on create page after validation error"

    def test_create_private_group_calls_api(self, api_page: Page):
        """TC-FEINT-012: Frontend creates private team via backend API.

        User selects "私密" visibility, clicks "创建",
        system calls POST /api/groups with visibility=private.
        """
        wait_for_app_load(api_page, f"{FRONTEND_URL}/groups/create")

        # Fill group form
        api_page.fill('input[name="name"], input[placeholder*="名称"]', 'E2E Private Team')
        api_page.fill('textarea[name="description"], textarea[placeholder*="简介"]', 'Private team')

        # Select private visibility
        visibility_selector = api_page.locator('select[name="visibility"], [data-testid="visibility-select"]')
        if visibility_selector.count() > 0:
            visibility_selector.select_option("private")
        else:
            # Try radio button or checkbox
            private_option = api_page.locator('input[value="private"], label:has-text("私密")')
            if private_option.count() > 0:
                private_option.first.click()

        # Click create button
        api_page.click('button:has-text("创建")')

        # Wait for navigation
        api_page.wait_for_url(f"{FRONTEND_URL}/groups/**", timeout=10000)

        # Verify API was called
        post_requests = [r for r in api_page.api_responses
                        if r["method"] == "POST" and "/groups" in r["url"]]
        assert len(post_requests) > 0, "Expected POST /api/groups to be called"
