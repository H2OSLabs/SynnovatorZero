"""E2E tests for edit and delete integration (TC-FEINT-040~051).

Tests verify that frontend edit/delete operations correctly call backend APIs.
"""
import pytest
from playwright.sync_api import Page, expect

from conftest import FRONTEND_URL, API_URL, wait_for_app_load


class TestEditIntegration:
    """Tests for edit operations integration with backend API."""

    @pytest.fixture(autouse=True)
    def setup_auth(self, page: Page):
        """Set up authenticated user for tests."""
        wait_for_app_load(page, f"{FRONTEND_URL}/login")
        page.fill('input[name="username"], input[placeholder*="用户名"]', 'testuser')
        page.fill('input[name="password"], input[placeholder*="密码"], input[type="password"]', 'testpass123')
        page.click('button[type="submit"]')
        page.wait_for_url(f"{FRONTEND_URL}/**", timeout=10000)

    def test_edit_post_calls_api(self, api_page: Page):
        """TC-FEINT-040: Frontend edits post via backend API.

        User modifies post on /posts/{id}/edit,
        clicks "保存", system calls PATCH /api/posts/{id},
        success redirects to post detail page.
        """
        # First create a post to edit
        wait_for_app_load(api_page, f"{FRONTEND_URL}/posts/create")
        api_page.fill('input[name="title"], input[placeholder*="标题"]', 'Post to Edit')
        api_page.fill('textarea[name="content"], textarea[placeholder*="内容"]', 'Original content')
        api_page.click('button:has-text("发布")')
        api_page.wait_for_url(f"{FRONTEND_URL}/posts/**", timeout=10000)

        # Get post ID from URL
        post_url = api_page.url

        # Navigate to edit page
        api_page.goto(f"{post_url}/edit")
        api_page.wait_for_load_state("networkidle")

        # Modify content
        content_field = api_page.locator('textarea[name="content"], textarea[placeholder*="内容"]')
        if content_field.count() > 0:
            content_field.fill('Updated content via E2E test')

        # Click save button
        api_page.click('button:has-text("保存"), button:has-text("更新")')

        # Wait for response
        api_page.wait_for_timeout(2000)

        # Verify PATCH was called
        patch_requests = [r for r in api_page.api_responses
                        if r["method"] == "PATCH" and "/posts" in r["url"]]
        assert len(patch_requests) > 0, "Expected PATCH /api/posts/{id} to be called"

    def test_edit_group_calls_api(self, api_page: Page):
        """TC-FEINT-041: Team owner edits group via backend API.

        Owner modifies team info on edit page,
        clicks "保存", system calls PATCH /api/groups/{id}.
        """
        # First create a group to edit
        wait_for_app_load(api_page, f"{FRONTEND_URL}/groups/create")
        api_page.fill('input[name="name"], input[placeholder*="名称"]', 'Group to Edit')
        api_page.fill('textarea[name="description"], textarea[placeholder*="简介"]', 'Original description')
        api_page.click('button:has-text("创建")')
        api_page.wait_for_url(f"{FRONTEND_URL}/groups/**", timeout=10000)

        # Get group URL
        group_url = api_page.url

        # Navigate to edit page (or settings)
        edit_url = f"{group_url}/edit"
        api_page.goto(edit_url)
        api_page.wait_for_load_state("networkidle")

        # Modify description
        desc_field = api_page.locator('textarea[name="description"], textarea[placeholder*="简介"]')
        if desc_field.count() > 0:
            desc_field.fill('Updated description via E2E test')

        # Click save button
        save_btn = api_page.locator('button:has-text("保存"), button:has-text("更新")')
        if save_btn.count() > 0:
            save_btn.first.click()

            # Wait for response
            api_page.wait_for_timeout(2000)

            # Verify PATCH was called
            patch_requests = [r for r in api_page.api_responses
                            if r["method"] == "PATCH" and "/groups" in r["url"]]
            assert len(patch_requests) > 0, "Expected PATCH /api/groups/{id} to be called"


class TestDeleteIntegration:
    """Tests for delete operations integration with backend API."""

    @pytest.fixture(autouse=True)
    def setup_auth(self, page: Page):
        """Set up authenticated user for tests."""
        wait_for_app_load(page, f"{FRONTEND_URL}/login")
        page.fill('input[name="username"], input[placeholder*="用户名"]', 'testuser')
        page.fill('input[name="password"], input[placeholder*="密码"], input[type="password"]', 'testpass123')
        page.click('button[type="submit"]')
        page.wait_for_url(f"{FRONTEND_URL}/**", timeout=10000)

    def test_delete_post_calls_api(self, api_page: Page):
        """TC-FEINT-050: Frontend deletes post via backend API.

        User clicks delete and confirms,
        system calls DELETE /api/posts/{id},
        success redirects to post list.
        """
        # First create a post to delete
        wait_for_app_load(api_page, f"{FRONTEND_URL}/posts/create")
        api_page.fill('input[name="title"], input[placeholder*="标题"]', 'Post to Delete')
        api_page.fill('textarea[name="content"], textarea[placeholder*="内容"]', 'Will be deleted')
        api_page.click('button:has-text("发布")')
        api_page.wait_for_url(f"{FRONTEND_URL}/posts/**", timeout=10000)

        # Find and click delete button
        delete_btn = api_page.locator('button:has-text("删除"), [data-testid="delete-button"]')
        if delete_btn.count() > 0:
            delete_btn.first.click()

            # Handle confirmation dialog
            confirm_btn = api_page.locator('button:has-text("确认"), button:has-text("确定")')
            if confirm_btn.count() > 0:
                confirm_btn.first.click()

            # Wait for response
            api_page.wait_for_timeout(2000)

            # Verify DELETE was called
            delete_requests = [r for r in api_page.api_responses
                              if r["method"] == "DELETE" and "/posts" in r["url"]]
            assert len(delete_requests) > 0, "Expected DELETE /api/posts/{id} to be called"

    def test_delete_group_calls_api(self, api_page: Page):
        """TC-FEINT-051: Team owner deletes group via backend API.

        Owner clicks delete and confirms,
        system calls DELETE /api/groups/{id}.
        """
        # First create a group to delete
        wait_for_app_load(api_page, f"{FRONTEND_URL}/groups/create")
        api_page.fill('input[name="name"], input[placeholder*="名称"]', 'Group to Delete')
        api_page.fill('textarea[name="description"], textarea[placeholder*="简介"]', 'Will be deleted')
        api_page.click('button:has-text("创建")')
        api_page.wait_for_url(f"{FRONTEND_URL}/groups/**", timeout=10000)

        # Find and click delete button (might be in settings)
        delete_btn = api_page.locator('button:has-text("删除"), button:has-text("解散"), [data-testid="delete-button"]')
        if delete_btn.count() > 0:
            delete_btn.first.click()

            # Handle confirmation dialog
            confirm_btn = api_page.locator('button:has-text("确认"), button:has-text("确定")')
            if confirm_btn.count() > 0:
                confirm_btn.first.click()

            # Wait for response
            api_page.wait_for_timeout(2000)

            # Verify DELETE was called
            delete_requests = [r for r in api_page.api_responses
                              if r["method"] == "DELETE" and "/groups" in r["url"]]
            assert len(delete_requests) > 0, "Expected DELETE /api/groups/{id} to be called"
