"""E2E test configuration and fixtures.

This module provides pytest fixtures for E2E testing with Playwright.
Tests assume both backend (port 8000) and frontend (port 3000) servers are running.

Usage:
    # Run with servers managed by with_server.py:
    python3 scripts/with_server.py \
        --server "uv run uvicorn app.main:app --port 8000" --port 8000 \
        --server "cd frontend && npm run dev -- -p 3000" --port 3000 \
        --timeout 60 \
        -- uv run pytest e2e/ -v
"""
import pytest
from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext


# Server URLs
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"
API_URL = f"{BACKEND_URL}/api"


@pytest.fixture(scope="session")
def browser():
    """Create a browser instance for the test session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser):
    """Create a new browser context for each test."""
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        locale="zh-CN",
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """Create a new page for each test."""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def api_page(context: BrowserContext):
    """Create a page with API request interceptor for testing."""
    page = context.new_page()

    # Store API responses for verification
    page.api_responses = []

    def handle_response(response):
        if API_URL in response.url:
            page.api_responses.append({
                "url": response.url,
                "status": response.status,
                "method": response.request.method,
            })

    page.on("response", handle_response)
    yield page
    page.close()


# Helper functions for tests
def create_test_user(page: Page, username: str, email: str = None, role: str = "participant"):
    """Create a test user via API."""
    import requests
    email = email or f"{username}@test.example.com"
    resp = requests.post(f"{API_URL}/users", json={
        "username": username,
        "email": email,
        "role": role,
    })
    return resp.json() if resp.status_code == 201 else None


def wait_for_app_load(page: Page, url: str, timeout: int = 30000):
    """Navigate to URL and wait for app to be fully loaded."""
    page.goto(url)
    page.wait_for_load_state("networkidle", timeout=timeout)


def take_screenshot(page: Page, name: str):
    """Take a screenshot for debugging."""
    page.screenshot(path=f"/tmp/e2e_{name}.png", full_page=True)
