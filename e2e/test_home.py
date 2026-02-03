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

        title = page.locator("h1")
        expect(title).to_contain_text("创意在这里起飞")

    def test_home_page_shows_subtitle(self, page: Page):
        """E2E-HOME-003: Home page shows the subtitle."""
        wait_for_app_load(page, FRONTEND_URL)

        subtitle = page.locator("text=发现最激动人心的 Hackathon")
        expect(subtitle).to_be_visible()

    def test_home_page_dark_theme(self, page: Page):
        """E2E-HOME-006: Home page uses dark theme (Neon Forge)."""
        wait_for_app_load(page, FRONTEND_URL)

        root = page.locator(".bg-nf-dark")
        expect(root.first).to_be_visible()

        # The lime green accent should be visible
        lime_element = page.locator(".text-nf-lime, [class*='text-nf-lime']")
        expect(lime_element.first).to_be_visible()
