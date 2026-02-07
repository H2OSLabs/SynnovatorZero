"""E2E tests for event creation integration (TC-FEINT-020~021).

Tests verify that frontend event forms correctly call backend APIs
and enforce role-based access.
"""
import pytest
from playwright.sync_api import Page, expect

from conftest import FRONTEND_URL, API_URL, wait_for_app_load


class TestEventCreationIntegration:
    """Tests for event creation integration with backend API."""

    @pytest.fixture
    def organizer_auth(self, page: Page):
        """Set up organizer user for tests."""
        wait_for_app_load(page, f"{FRONTEND_URL}/login")
        # Login as organizer
        page.fill('input[name="username"], input[placeholder*="用户名"]', 'organizer')
        page.fill('input[name="password"], input[placeholder*="密码"], input[type="password"]', 'orgpass123')
        page.click('button[type="submit"]')
        page.wait_for_url(f"{FRONTEND_URL}/**", timeout=10000)
        return page

    @pytest.fixture
    def participant_auth(self, page: Page):
        """Set up participant user for tests."""
        wait_for_app_load(page, f"{FRONTEND_URL}/login")
        # Login as participant
        page.fill('input[name="username"], input[placeholder*="用户名"]', 'participant')
        page.fill('input[name="password"], input[placeholder*="密码"], input[type="password"]', 'partpass123')
        page.click('button[type="submit"]')
        page.wait_for_url(f"{FRONTEND_URL}/**", timeout=10000)
        return page

    def test_create_event_calls_api(self, api_page: Page):
        """TC-FEINT-020: Organizer creates event via backend API.

        Organizer fills event info on /events/create,
        clicks "创建", system calls POST /api/events,
        success redirects to event detail page.
        """
        # Login as organizer first
        wait_for_app_load(api_page, f"{FRONTEND_URL}/login")
        api_page.fill('input[name="username"], input[placeholder*="用户名"]', 'organizer')
        api_page.fill('input[name="password"], input[placeholder*="密码"], input[type="password"]', 'orgpass123')
        api_page.click('button[type="submit"]')
        api_page.wait_for_timeout(2000)

        # Navigate to event create page
        wait_for_app_load(api_page, f"{FRONTEND_URL}/events/create")

        # Fill event form
        api_page.fill('input[name="title"], input[name="name"], input[placeholder*="名称"]', 'E2E Test Event')
        api_page.fill('textarea[name="description"], textarea[placeholder*="描述"]', 'Event description')

        # Fill dates if present
        start_date = api_page.locator('input[name="start_date"], input[type="date"]')
        if start_date.count() > 0:
            start_date.first.fill('2026-03-01')

        end_date = api_page.locator('input[name="end_date"], input[type="date"]:nth-of-type(2)')
        if end_date.count() > 0:
            end_date.first.fill('2026-03-15')

        # Click create button
        api_page.click('button:has-text("创建"), button:has-text("发布")')

        # Wait for navigation
        api_page.wait_for_timeout(3000)

        # Verify API was called
        event_requests = [r for r in api_page.api_responses
                        if r["method"] == "POST" and "/events" in r["url"]]
        assert len(event_requests) > 0, "Expected POST /api/events to be called"

    def test_non_organizer_cannot_access_create(self, page: Page):
        """TC-FEINT-021: Non-organizer cannot access event creation.

        Participant accesses /events/create,
        system redirects or shows permission denied.
        """
        # Login as participant
        wait_for_app_load(page, f"{FRONTEND_URL}/login")
        page.fill('input[name="username"], input[placeholder*="用户名"]', 'participant')
        page.fill('input[name="password"], input[placeholder*="密码"], input[type="password"]', 'partpass123')
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)

        # Try to access event create page
        page.goto(f"{FRONTEND_URL}/events/create")
        page.wait_for_timeout(2000)

        # Should be redirected or see permission error
        is_blocked = (
            "/events/create" not in page.url or  # Redirected away
            page.locator('text=权限').is_visible() or
            page.locator('text=forbidden').is_visible() or
            page.locator('text=无权').is_visible() or
            page.locator('[class*="error"]').is_visible()
        )

        # Either redirected or error shown
        assert is_blocked or "/events/create" not in page.url, \
            "Non-organizer should be blocked from event creation"
