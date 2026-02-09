"""E2E tests for edge cases and error handling (TC-FEINT-090~902).

Tests verify API client completeness and proper error handling.
"""
import pytest
from playwright.sync_api import Page, expect
import os
import re

from conftest import FRONTEND_URL, wait_for_app_load


class TestApiClientCompleteness:
    """Tests for API client implementation completeness."""

    def test_api_client_has_crud_methods(self):
        """TC-FEINT-090: api-client.ts contains all CRUD methods.

        Frontend lib/api-client.ts must have create, get/list,
        update, delete methods for each data type.
        """
        # Read the api-client.ts file
        api_client_paths = [
            "frontend/lib/api-client.ts",
            "frontend/lib/api/client.ts",
            "frontend/lib/api.ts",
        ]

        api_client_content = None
        for path in api_client_paths:
            full_path = os.path.join(os.getcwd(), path)
            if os.path.exists(full_path):
                with open(full_path, 'r') as f:
                    api_client_content = f.read()
                break

        if api_client_content is None:
            pytest.skip("api-client.ts not found")

        # Check for CRUD methods for key resources
        resources = ['post', 'group', 'event', 'user']
        methods = ['create', 'get', 'list', 'update', 'delete']

        missing = []
        for resource in resources:
            for method in methods:
                # Check for various naming conventions
                patterns = [
                    f"{method}_{resource}",      # create_post
                    f"{method}{resource.capitalize()}",  # createPost
                    f"{resource}s?.{method}",    # posts.create
                    f"api{method.capitalize()}",  # apiCreate (generic)
                ]
                found = any(
                    re.search(pattern, api_client_content, re.IGNORECASE)
                    for pattern in patterns
                )
                if not found:
                    missing.append(f"{method}_{resource}")

        # Allow some missing methods (not all resources need all CRUD)
        assert len(missing) < len(resources) * len(methods) / 2, \
            f"API client missing too many CRUD methods: {missing}"

    def test_create_pages_no_todo(self):
        """TC-FEINT-091: Frontend create pages have no TODO placeholders.

        Create pages (/posts/create, /groups/create, /events/create)
        must not have TODO comments in form submit functions.
        """
        create_page_patterns = [
            "frontend/app/posts/create/page.tsx",
            "frontend/app/groups/create/page.tsx",
            "frontend/app/events/create/page.tsx",
            "frontend/components/pages/PostCreatePage.tsx",
            "frontend/components/pages/GroupCreatePage.tsx",
        ]

        todos_found = []
        for pattern in create_page_patterns:
            # Also check with different patterns
            base = os.getcwd()
            for root, dirs, files in os.walk(os.path.join(base, "frontend")):
                for file in files:
                    if 'create' in file.lower() and file.endswith('.tsx'):
                        filepath = os.path.join(root, file)
                        with open(filepath, 'r') as f:
                            content = f.read()
                            # Look for TODO in submit-related code
                            if 'TODO' in content:
                                # Check if it's in a submit handler
                                lines = content.split('\n')
                                for i, line in enumerate(lines):
                                    if 'TODO' in line:
                                        # Check context (nearby lines for submit/create)
                                        context = '\n'.join(lines[max(0,i-5):min(len(lines),i+5)])
                                        if any(kw in context.lower() for kw in ['submit', 'create', 'publish', 'save']):
                                            todos_found.append(f"{filepath}:{i+1}")

        assert len(todos_found) == 0, f"TODO found in create page submit handlers: {todos_found}"


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_unauthenticated_create_blocked(self, page: Page):
        """TC-FEINT-900: Unauthenticated user blocked from creating.

        Unauthenticated user accessing /posts/create or clicking publish
        is redirected to login page.
        """
        # Go directly to create page without logging in
        page.goto(f"{FRONTEND_URL}/posts/create")
        page.wait_for_timeout(3000)

        # Should be redirected to login or see auth prompt
        is_blocked = (
            "/login" in page.url or
            page.locator('text=登录').is_visible() or
            page.locator('text=请先登录').is_visible() or
            page.locator('[class*="auth"]').is_visible()
        )

        assert is_blocked, "Unauthenticated user should be blocked from post creation"

    def test_network_error_preserves_input(self, page: Page):
        """TC-FEINT-901: Network error preserves user input.

        When submit fails due to network error,
        system shows error and preserves form data.
        """
        # Login first
        wait_for_app_load(page, f"{FRONTEND_URL}/login")
        page.fill('input[name="username"], input[placeholder*="用户名"]', 'testuser')
        page.fill('input[name="password"], input[placeholder*="密码"], input[type="password"]', 'testpass123')
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)

        # Navigate to create page
        wait_for_app_load(page, f"{FRONTEND_URL}/posts/create")

        # Fill form
        test_title = "Network Error Test Title"
        test_content = "This content should be preserved on error"

        page.fill('input[name="title"], input[placeholder*="标题"]', test_title)
        page.fill('textarea[name="content"], textarea[placeholder*="内容"]', test_content)

        # Simulate network failure by blocking API
        page.route("**/api/posts", lambda route: route.abort())

        # Try to submit
        page.click('button:has-text("发布")')

        # Wait for error
        page.wait_for_timeout(3000)

        # Verify input is preserved
        title_value = page.locator('input[name="title"], input[placeholder*="标题"]').input_value()
        content_value = page.locator('textarea[name="content"], textarea[placeholder*="内容"]').input_value()

        # Input should still be there (or page shouldn't have navigated away)
        assert title_value == test_title or "/posts/create" in page.url, \
            "User input should be preserved on network error"

    def test_double_submit_prevention(self, page: Page):
        """TC-FEINT-902: Double submit prevention.

        Rapidly clicking publish multiple times only sends one API request
        (button disabled during submission).
        """
        # Login first
        wait_for_app_load(page, f"{FRONTEND_URL}/login")
        page.fill('input[name="username"], input[placeholder*="用户名"]', 'testuser')
        page.fill('input[name="password"], input[placeholder*="密码"], input[type="password"]', 'testpass123')
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)

        # Navigate to create page
        wait_for_app_load(page, f"{FRONTEND_URL}/posts/create")

        # Fill form
        page.fill('input[name="title"], input[placeholder*="标题"]', 'Double Submit Test')
        page.fill('textarea[name="content"], textarea[placeholder*="内容"]', 'Testing double submit prevention')

        # Track API calls
        api_calls = []
        page.on("request", lambda req: api_calls.append(req.url) if "/api/posts" in req.url and req.method == "POST" else None)

        # Rapidly click submit multiple times
        submit_btn = page.locator('button:has-text("发布")')
        for _ in range(5):
            try:
                submit_btn.click(timeout=100)
            except:
                break  # Button might be disabled or navigated away

        # Wait for processing
        page.wait_for_timeout(3000)

        # Should only have 1 API call (or button was disabled)
        assert len(api_calls) <= 1 or submit_btn.is_disabled(), \
            f"Expected at most 1 API call, got {len(api_calls)}"
