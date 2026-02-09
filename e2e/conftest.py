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

Tracing:
    # Run with tracing enabled (saves trace on failure):
    uv run pytest e2e/ -v --e2e-trace

    # View trace file:
    playwright show-trace /tmp/e2e_traces/<test_name>.zip

    # Run with tracing for all tests (including passed):
    uv run pytest e2e/ -v --e2e-trace-all
"""
import socket
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext, Error as PlaywrightError


# Trace output directory
TRACE_DIR = Path("/tmp/e2e_traces")
TRACE_DIR.mkdir(exist_ok=True)


# Server URLs
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"
API_URL = f"{BACKEND_URL}/api"


def _is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    """Check if a port is open."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


# Cache frontend availability for session
_frontend_available = None


def is_frontend_available() -> bool:
    """Check if frontend server is available (cached for session)."""
    global _frontend_available
    if _frontend_available is None:
        _frontend_available = _is_port_open("localhost", 3000)
    return _frontend_available


def skip_if_no_frontend():
    """Skip test if frontend is not available."""
    if not is_frontend_available():
        pytest.skip("Frontend server not running (port 3000)")


# ==================== Pytest Hooks ====================

def pytest_addoption(parser):
    """Add custom command line options for tracing."""
    parser.addoption(
        "--e2e-trace",
        action="store_true",
        default=False,
        help="Enable Playwright tracing (saves trace on test failure)",
    )
    parser.addoption(
        "--e2e-trace-all",
        action="store_true",
        default=False,
        help="Enable Playwright tracing for all tests (including passed)",
    )


@pytest.fixture(scope="session")
def trace_enabled(request) -> bool:
    """Check if tracing is enabled."""
    return request.config.getoption("--e2e-trace") or request.config.getoption("--e2e-trace-all")


@pytest.fixture(scope="session")
def trace_all(request) -> bool:
    """Check if tracing should be saved for all tests."""
    return request.config.getoption("--e2e-trace-all")


# ==================== Browser Fixtures ====================

@pytest.fixture(scope="session")
def browser():
    """Create a browser instance for the test session."""
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
        except PlaywrightError:
            browser = p.chromium.launch(channel="chrome", headless=True)
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


# ==================== Traced Fixtures ====================

@pytest.fixture(scope="function")
def traced_context(browser: Browser, request, trace_enabled: bool, trace_all: bool):
    """Create a browser context with tracing enabled.

    Trace is saved to /tmp/e2e_traces/<test_name>.zip on failure,
    or for all tests if --trace-all is used.

    Usage:
        def test_something(traced_context):
            page = traced_context.new_page()
            # ... test code ...
    """
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        locale="zh-CN",
    )

    if trace_enabled:
        context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True,
        )

    yield context

    # Save trace based on test outcome
    if trace_enabled:
        test_name = request.node.name.replace("/", "_").replace("::", "_")
        trace_path = TRACE_DIR / f"{test_name}.zip"

        # Check if test failed
        if hasattr(request.node, "rep_call"):
            test_failed = request.node.rep_call.failed
        else:
            test_failed = False

        # Save trace if test failed or --trace-all is set
        if test_failed or trace_all:
            context.tracing.stop(path=str(trace_path))
            print(f"\n📦 Trace saved: {trace_path}")
            print(f"   View with: playwright show-trace {trace_path}")
        else:
            context.tracing.stop()

    context.close()


@pytest.fixture(scope="function")
def traced_page(traced_context: BrowserContext):
    """Create a page with tracing from traced_context.

    Also captures console logs and network errors.

    Usage:
        def test_something(traced_page):
            traced_page.goto("http://localhost:3000")
            # Access logs: traced_page.console_logs
            # Access errors: traced_page.console_errors
    """
    page = traced_context.new_page()

    # Store console messages
    page.console_logs = []
    page.console_errors = []
    page.network_errors = []

    def handle_console(msg):
        entry = {
            "type": msg.type,
            "text": msg.text,
            "location": msg.location,
        }
        if msg.type == "error":
            page.console_errors.append(entry)
        page.console_logs.append(entry)

    def handle_page_error(error):
        page.console_errors.append({
            "type": "page_error",
            "text": str(error),
        })

    def handle_request_failed(request):
        page.network_errors.append({
            "url": request.url,
            "method": request.method,
            "failure": request.failure,
        })

    page.on("console", handle_console)
    page.on("pageerror", handle_page_error)
    page.on("requestfailed", handle_request_failed)

    yield page
    page.close()


# Pytest hook to record test outcome for traced_context
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Record test outcome for use in fixtures."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


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
    """Navigate to URL and wait for app to be fully loaded.

    Skips test if frontend server is not running.
    """
    if FRONTEND_URL in url:
        skip_if_no_frontend()
    page.goto(url)
    page.wait_for_load_state("networkidle", timeout=timeout)


def take_screenshot(page: Page, name: str):
    """Take a screenshot for debugging."""
    page.screenshot(path=f"/tmp/e2e_{name}.png", full_page=True)


def print_console_logs(page: Page):
    """Print captured console logs from a traced_page.

    Usage:
        def test_something(traced_page):
            traced_page.goto(url)
            # ... test fails ...
            print_console_logs(traced_page)  # See what went wrong
    """
    if hasattr(page, "console_logs"):
        print("\n=== Console Logs ===")
        for log in page.console_logs:
            prefix = "❌" if log["type"] == "error" else "📝"
            print(f"{prefix} [{log['type']}] {log['text']}")

    if hasattr(page, "network_errors") and page.network_errors:
        print("\n=== Network Errors ===")
        for err in page.network_errors:
            print(f"❌ {err['method']} {err['url']}: {err['failure']}")


def assert_no_console_errors(page: Page):
    """Assert that no console errors were captured.

    Usage:
        def test_page_loads_cleanly(traced_page):
            traced_page.goto(url)
            assert_no_console_errors(traced_page)
    """
    if hasattr(page, "console_errors") and page.console_errors:
        errors = [e["text"] for e in page.console_errors]
        raise AssertionError(f"Console errors detected: {errors}")
