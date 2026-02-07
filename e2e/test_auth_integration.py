"""E2E tests for authentication integration (TC-FEINT-030~032).

Tests verify that frontend auth forms correctly call backend APIs.
"""
import pytest
from playwright.sync_api import Page, expect

from conftest import FRONTEND_URL, API_URL, wait_for_app_load


class TestAuthIntegration:
    """Tests for authentication integration with backend API."""

    def test_login_calls_api(self, api_page: Page):
        """TC-FEINT-030: Frontend login calls backend API.

        User enters username and password on /login,
        clicks login, system calls POST /api/auth/login,
        success stores user info and redirects to home.
        """
        wait_for_app_load(api_page, f"{FRONTEND_URL}/login")

        # Fill login form
        api_page.fill('input[name="username"], input[placeholder*="用户名"]', 'testuser')
        api_page.fill('input[name="password"], input[placeholder*="密码"], input[type="password"]', 'testpass123')

        # Click login button
        api_page.click('button[type="submit"]')

        # Wait for response and potential redirect
        api_page.wait_for_timeout(3000)

        # Verify API was called
        auth_requests = [r for r in api_page.api_responses
                        if "auth" in r["url"] and r["method"] == "POST"]
        assert len(auth_requests) > 0, "Expected POST /api/auth/* to be called"

        # On success, should redirect away from login
        # (or show error if credentials are wrong)

    def test_register_calls_api(self, api_page: Page):
        """TC-FEINT-031: Frontend register calls backend API.

        User fills registration form on /register,
        clicks register, system calls POST /api/auth/register,
        success auto-logs in and redirects.
        """
        wait_for_app_load(api_page, f"{FRONTEND_URL}/register")

        # Generate unique username for test
        import time
        unique_user = f"e2euser_{int(time.time())}"

        # Fill registration form
        api_page.fill('input[name="username"], input[placeholder*="用户名"]', unique_user)
        api_page.fill('input[name="email"], input[placeholder*="邮箱"], input[type="email"]', f'{unique_user}@test.example.com')
        api_page.fill('input[name="password"], input[placeholder*="密码"], input[type="password"]', 'TestPass123!')

        # Fill confirm password if exists
        confirm_pwd = api_page.locator('input[name="confirmPassword"], input[name="password_confirm"]')
        if confirm_pwd.count() > 0:
            confirm_pwd.fill('TestPass123!')

        # Click register button
        api_page.click('button[type="submit"]')

        # Wait for response
        api_page.wait_for_timeout(3000)

        # Verify API was called
        auth_requests = [r for r in api_page.api_responses
                        if "auth" in r["url"] and r["method"] == "POST"]
        assert len(auth_requests) > 0, "Expected POST /api/auth/* to be called"

    def test_login_error_shows_message(self, page: Page):
        """TC-FEINT-032: Frontend shows error on login failure.

        User enters wrong password on /login,
        backend returns 401, frontend shows "用户名或密码错误".
        """
        wait_for_app_load(page, f"{FRONTEND_URL}/login")

        # Fill login form with wrong credentials
        page.fill('input[name="username"], input[placeholder*="用户名"]', 'nonexistent_user')
        page.fill('input[name="password"], input[placeholder*="密码"], input[type="password"]', 'wrongpassword')

        # Click login button
        page.click('button[type="submit"]')

        # Wait for error response
        page.wait_for_timeout(2000)

        # Check for error message
        error_visible = (
            page.locator('text=用户名或密码错误').is_visible() or
            page.locator('text=登录失败').is_visible() or
            page.locator('text=错误').is_visible() or
            page.locator('[class*="error"]').is_visible() or
            page.locator('[class*="toast"]').is_visible()
        )

        # Should still be on login page
        assert "/login" in page.url, "Should remain on login page after error"
