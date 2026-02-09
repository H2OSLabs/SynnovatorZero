"""Demo test for Playwright tracing functionality.

Run with:
    uv run pytest e2e/test_trace_demo.py -v --e2e-trace-all

View trace:
    playwright show-trace /tmp/e2e_traces/test_explore_with_tracing.zip
"""
import pytest
from conftest import FRONTEND_URL, wait_for_app_load, print_console_logs, assert_no_console_errors


class TestTraceDemo:
    """Demonstrate tracing and console log capture."""

    def test_explore_with_tracing(self, traced_page):
        """Test explore page with full tracing enabled.

        This test captures:
        - Screenshots at each step
        - Network requests
        - Console logs
        - DOM snapshots

        View the trace with:
            playwright show-trace /tmp/e2e_traces/test_explore_with_tracing.zip
        """
        # Navigate to explore page
        traced_page.goto(f"{FRONTEND_URL}/explore")
        traced_page.wait_for_load_state("networkidle")
        traced_page.wait_for_timeout(2000)

        # Check page loaded
        page_text = traced_page.inner_text("body")
        assert "探索" in page_text, "Should see explore page header"

        # Print any console logs for debugging
        print_console_logs(traced_page)

        # Verify no JS errors
        # Note: Some Next.js dev warnings are expected
        js_errors = [e for e in traced_page.console_errors
                     if "error" in e.get("type", "").lower()
                     and "warning" not in e.get("text", "").lower()]

        if js_errors:
            print(f"JS Errors found: {js_errors}")

    def test_login_flow_with_tracing(self, traced_page):
        """Test login flow with tracing to debug form issues."""
        traced_page.goto(f"{FRONTEND_URL}/login")
        traced_page.wait_for_load_state("networkidle")

        # Check form fields exist
        username_input = traced_page.locator('input[placeholder*="用户名"]')
        password_input = traced_page.locator('input[type="password"]')

        assert username_input.count() > 0, "Username input should exist"
        assert password_input.count() > 0, "Password input should exist"

        # Fill form
        username_input.fill("test_user")
        password_input.fill("test_password")

        # Print console logs
        print_console_logs(traced_page)

    @pytest.mark.skip(reason="Intentional failure to demo trace on failure")
    def test_intentional_failure_for_trace(self, traced_page):
        """This test intentionally fails to demonstrate trace capture on failure."""
        traced_page.goto(f"{FRONTEND_URL}/nonexistent-page")
        traced_page.wait_for_timeout(2000)

        # This will fail
        assert "This text does not exist" in traced_page.inner_text("body")
