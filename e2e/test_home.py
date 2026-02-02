"""E2E tests for the home page."""
import pytest
from playwright.sync_api import Page, expect

from conftest import FRONTEND_URL, wait_for_app_load, take_screenshot


class TestHomePage:
    """Tests for the home page (/)."""

    def test_home_page_loads(self, page: Page):
        """E2E-HOME-001: Home page loads successfully."""
        wait_for_app_load(page, FRONTEND_URL)

        # Verify page title or main content
        expect(page.locator("h1")).to_be_visible()

    def test_home_page_shows_title(self, page: Page):
        """E2E-HOME-002: Home page shows the platform title."""
        wait_for_app_load(page, FRONTEND_URL)

        # Check for the Chinese title "协创者"
        title = page.locator("h1")
        expect(title).to_contain_text("协创者")

    def test_home_page_shows_subtitle(self, page: Page):
        """E2E-HOME-003: Home page shows the English subtitle."""
        wait_for_app_load(page, FRONTEND_URL)

        # Check for subtitle
        subtitle = page.locator("text=Creative Collaboration Platform")
        expect(subtitle).to_be_visible()

    def test_demo_link_exists(self, page: Page):
        """E2E-HOME-004: Home page has a link to the demo page."""
        wait_for_app_load(page, FRONTEND_URL)

        # Find demo link
        demo_link = page.locator("text=查看组件演示")
        expect(demo_link).to_be_visible()

    def test_demo_link_navigates(self, page: Page):
        """E2E-HOME-005: Clicking demo link navigates to /demo."""
        wait_for_app_load(page, FRONTEND_URL)

        # Click demo link
        page.click("text=查看组件演示")
        page.wait_for_load_state("networkidle")

        # Verify URL changed
        assert "/demo" in page.url

    def test_home_page_dark_theme(self, page: Page):
        """E2E-HOME-006: Home page uses dark theme (Neon Forge)."""
        wait_for_app_load(page, FRONTEND_URL)

        # Check for dark background on main element
        main = page.locator("main")
        expect(main).to_be_visible()

        # The lime green accent should be visible
        lime_element = page.locator(".text-nf-lime, [class*='text-nf-lime']")
        expect(lime_element.first).to_be_visible()
