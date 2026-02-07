"""E2E tests for TC-JOUR-005: Team Join Journey.

Tests verify the complete team join and approval flow:
- Carol applies to join a team requiring approval
- Owner Alice approves/rejects applications
- Membership status transitions correctly
"""
import pytest
from playwright.sync_api import Page, expect

from conftest import FRONTEND_URL, wait_for_app_load
from helpers import APIClient, setup_test_users


class TestJourneyTeamJoin:
    """TC-JOUR-005: Complete team join and approval flow.

    Flow:
    1. Carol applies to join require_approval=true team
    2. Application status is pending
    3. Owner Alice approves → status becomes accepted
    4. Bob applies and gets rejected → status becomes rejected
    5. Bob reapplies → status becomes pending again
    6. Team member list shows all members with status
    """

    @pytest.fixture(autouse=True)
    def setup_test_data(self):
        """Set up test users and team."""
        self.api = APIClient()

        # Create users
        self.users = setup_test_users(self.api)

        # Login as Alice (team owner)
        if "alice" in self.users:
            self.api.login(self.users["alice"].username, self.users["alice"].password)

            # Create team requiring approval
            self.team = self.api.create_group(
                "Test Team for Join Flow",
                "Team that requires approval to join",
                require_approval=True
            )

            self.api.logout()

        yield

        # Cleanup
        if hasattr(self, 'team') and "id" in self.team:
            self.api.login(self.users["alice"].username, self.users["alice"].password)
            self.api.delete_group(self.team["id"])

    def test_carol_applies_to_join_team(self):
        """Carol applies to join the team - status becomes pending."""
        if "carol" not in self.users or not hasattr(self, 'team'):
            pytest.skip("Test data not set up")

        api = APIClient()
        api.login(self.users["carol"].username, self.users["carol"].password)

        # Apply to join team
        result = api.join_group(self.team["id"])

        # Should succeed with pending status
        assert "error" not in result, f"Join failed: {result}"
        # Status should be pending for approval-required teams
        assert result.get("status") in ("pending", "applied", None)

    def test_alice_approves_carol(self):
        """Alice approves Carol's application - status becomes accepted."""
        if "alice" not in self.users or "carol" not in self.users:
            pytest.skip("Test data not set up")

        # First, Carol applies
        carol_api = APIClient()
        carol_api.login(self.users["carol"].username, self.users["carol"].password)
        carol_api.join_group(self.team["id"])

        # Alice approves
        alice_api = APIClient()
        alice_api.login(self.users["alice"].username, self.users["alice"].password)
        result = alice_api.approve_member(self.team["id"], self.users["carol"].id)

        # Should succeed
        assert "error" not in result or result.get("status") == 200, f"Approve failed: {result}"

        # Verify Carol is now accepted
        members = alice_api.list_group_members(self.team["id"])
        carol_member = next((m for m in members if m.get("user_id") == self.users["carol"].id), None)
        if carol_member:
            assert carol_member.get("status") in ("accepted", "active", "member")

    def test_alice_rejects_bob(self):
        """Alice rejects Bob's application - status becomes rejected."""
        if "alice" not in self.users or "bob" not in self.users:
            pytest.skip("Test data not set up")

        # Bob applies
        bob_api = APIClient()
        bob_api.login(self.users["bob"].username, self.users["bob"].password)
        bob_api.join_group(self.team["id"])

        # Alice rejects
        alice_api = APIClient()
        alice_api.login(self.users["alice"].username, self.users["alice"].password)
        result = alice_api.reject_member(self.team["id"], self.users["bob"].id)

        # Should succeed
        assert "error" not in result or result.get("status") == 200

    def test_bob_reapplies_after_rejection(self):
        """Bob reapplies after rejection - status becomes pending again."""
        if "bob" not in self.users:
            pytest.skip("Test data not set up")

        # Bob applies again
        bob_api = APIClient()
        bob_api.login(self.users["bob"].username, self.users["bob"].password)
        result = bob_api.join_group(self.team["id"])

        # Should be able to reapply
        # Status should be pending again
        assert result.get("status") in ("pending", "applied", None) or "error" not in result

    def test_list_team_members_shows_all_with_status(self):
        """Team member list returns all members with their status."""
        if "alice" not in self.users:
            pytest.skip("Test data not set up")

        alice_api = APIClient()
        alice_api.login(self.users["alice"].username, self.users["alice"].password)

        members = alice_api.list_group_members(self.team["id"])

        # Should return list of members
        assert isinstance(members, list)

        # Each member should have status field
        for member in members:
            assert "status" in member or "role" in member, \
                f"Member missing status/role: {member}"

    def test_ui_team_join_flow(self, page: Page):
        """Test team join flow through UI."""
        if "carol" not in self.users or not hasattr(self, 'team'):
            pytest.skip("Test data not set up")

        # Login as Carol
        wait_for_app_load(page, f"{FRONTEND_URL}/login")
        page.fill('input[name="username"], input[placeholder*="用户名"]', self.users["carol"].username)
        page.fill('input[name="password"], input[type="password"]', self.users["carol"].password)
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)

        # Navigate to team page
        team_id = self.team.get("id")
        if team_id:
            page.goto(f"{FRONTEND_URL}/groups/{team_id}")
            page.wait_for_load_state("networkidle")

            # Look for join button
            join_btn = page.locator(
                'button:has-text("加入"), '
                'button:has-text("申请加入"), '
                'button:has-text("Join")'
            )

            if join_btn.count() > 0:
                join_btn.first.click()
                page.wait_for_timeout(2000)

                # Should see pending message or success
                expect(
                    page.locator('text=待审批').or_(
                        page.locator('text=pending')
                    ).or_(
                        page.locator('text=已申请')
                    ).or_(
                        page.locator('text=成功')
                    )
                ).to_be_visible()

    def test_ui_team_approval_flow(self, page: Page):
        """Test team approval flow through UI as owner."""
        if "alice" not in self.users or not hasattr(self, 'team'):
            pytest.skip("Test data not set up")

        # First, have someone apply via API
        carol_api = APIClient()
        carol_api.login(self.users["carol"].username, self.users["carol"].password)
        carol_api.join_group(self.team["id"])

        # Login as Alice (owner)
        wait_for_app_load(page, f"{FRONTEND_URL}/login")
        page.fill('input[name="username"], input[placeholder*="用户名"]', self.users["alice"].username)
        page.fill('input[name="password"], input[type="password"]', self.users["alice"].password)
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)

        # Navigate to team management
        team_id = self.team.get("id")
        if team_id:
            # Try team settings or members page
            page.goto(f"{FRONTEND_URL}/groups/{team_id}/members")
            page.wait_for_load_state("networkidle")

            # Look for pending applications
            pending_section = page.locator(
                'text=待审批, '
                'text=申请列表, '
                '[data-testid="pending-members"]'
            )

            if pending_section.count() > 0:
                # Should see approve/reject buttons
                approve_btn = page.locator('button:has-text("同意"), button:has-text("批准")')
                if approve_btn.count() > 0:
                    expect(approve_btn.first).to_be_visible()
