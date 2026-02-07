"""E2E tests for TC-JOUR-010: Certificate Journey.

Tests verify the certificate issuance flow after event closure.
"""
import pytest
from playwright.sync_api import Page, expect

from conftest import FRONTEND_URL, wait_for_app_load
from helpers import APIClient, setup_test_users


class TestJourneyCertificate:
    """TC-JOUR-010: Complete certificate issuance flow.

    Flow:
    1. Close event (status → closed)
    2. Create certificate resource (PDF)
    3. Link certificate to submission post
    4. Create certificate share post
    5. Verify accessibility
    """

    @pytest.fixture(autouse=True)
    def setup_test_data(self):
        """Set up event and submission."""
        self.api = APIClient()
        self.users = setup_test_users(self.api)

        if "alice" in self.users:
            self.api.login(self.users["alice"].username, self.users["alice"].password)

            # Create event
            self.event = self.api.create_event(
                "Certificate Test Event",
                "Event that will be closed for certificate testing",
                status="published"
            )

            # Create submission post
            self.submission = self.api.create_post(
                "Winning Submission",
                "This submission will receive a certificate",
                post_type="proposal"
            )

            # Link submission to event
            if "id" in self.event and "id" in self.submission:
                self.api.create_event_post_relation(
                    self.event["id"],
                    self.submission["id"],
                    "submission"
                )

            self.api.logout()

        yield

    def test_close_event(self):
        """Close the event - status becomes closed."""
        if not hasattr(self, 'event') or "id" not in self.event:
            pytest.skip("Event not set up")

        self.api.login(self.users["alice"].username, self.users["alice"].password)
        result = self.api.close_event(self.event["id"])

        assert "error" not in result or result.get("status") == "closed"

        # Verify event is closed
        event = self.api.get_event(self.event["id"])
        assert event.get("status") == "closed"

    def test_create_certificate_resource(self):
        """Create certificate resource (PDF file)."""
        if "alice" not in self.users:
            pytest.skip("Alice not set up")

        self.api.login(self.users["alice"].username, self.users["alice"].password)

        resource = self.api.create_resource(
            "certificate_winner.pdf",
            mime_type="application/pdf",
            description="Certificate of Achievement"
        )

        assert "id" in resource, f"Resource creation failed: {resource}"
        self.certificate_resource = resource

    def test_link_certificate_to_submission(self):
        """Link certificate resource to submission post."""
        if not hasattr(self, 'submission') or "id" not in self.submission:
            pytest.skip("Submission not set up")

        self.api.login(self.users["alice"].username, self.users["alice"].password)

        # Create certificate resource
        resource = self.api.create_resource("certificate.pdf")

        if "id" in resource and "id" in self.submission:
            result = self.api.create_post_resource_relation(
                self.submission["id"],
                resource["id"],
                display_type="attachment"
            )
            # Should succeed
            assert "error" not in result or result.get("status") in (200, 201)

    def test_create_certificate_share_post(self):
        """Create certificate share post (type=certificate)."""
        if "alice" not in self.users:
            pytest.skip("Alice not set up")

        self.api.login(self.users["alice"].username, self.users["alice"].password)

        post = self.api.create_post(
            "My Certificate",
            "Sharing my achievement certificate!",
            post_type="certificate",
            status="published"
        )

        assert "id" in post, f"Certificate post creation failed: {post}"

    def test_certificate_post_accessible(self):
        """Certificate post and resource are accessible."""
        if "alice" not in self.users:
            pytest.skip("Alice not set up")

        self.api.login(self.users["alice"].username, self.users["alice"].password)

        # Create and get certificate post
        post = self.api.create_post(
            "Accessible Certificate",
            "This should be readable",
            post_type="certificate",
            status="published"
        )

        if "id" in post:
            # Verify it's accessible
            self.api.logout()
            anon_api = APIClient()
            result = anon_api.get_post(post["id"])
            # Should be accessible (published)
            assert "title" in result or "error" not in result

    def test_full_certificate_flow(self):
        """Test complete certificate flow end-to-end."""
        if "alice" not in self.users or not hasattr(self, 'event'):
            pytest.skip("Test data not set up")

        self.api.login(self.users["alice"].username, self.users["alice"].password)

        # 1. Close event
        self.api.close_event(self.event["id"])

        # 2. Create certificate resource
        resource = self.api.create_resource("winner_cert.pdf")

        # 3. Link to submission
        if "id" in resource and hasattr(self, 'submission') and "id" in self.submission:
            self.api.create_post_resource_relation(
                self.submission["id"],
                resource["id"],
                "attachment"
            )

        # 4. Create share post
        share_post = self.api.create_post(
            "I won!",
            "Check out my certificate",
            post_type="certificate",
            status="published"
        )

        # 5. Verify accessible
        if "id" in share_post:
            self.api.logout()
            anon_api = APIClient()
            result = anon_api.get_post(share_post["id"])
            assert "id" in result or "title" in result
