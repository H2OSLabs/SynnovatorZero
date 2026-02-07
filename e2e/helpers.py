"""E2E test helpers for user journey tests.

Provides API client functions and test data management utilities.
"""
import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


# Server URLs
BACKEND_URL = "http://localhost:8000"
API_URL = f"{BACKEND_URL}/api"


@dataclass
class TestUser:
    """Represents a test user."""
    id: str
    username: str
    email: str
    role: str
    password: str = "testpass123"


class APIClient:
    """API client for E2E tests."""

    def __init__(self, base_url: str = API_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.current_user: Optional[TestUser] = None

    # ==================== Auth ====================

    def register(self, username: str, email: str, password: str, role: str = "participant") -> Dict:
        """Register a new user."""
        resp = self.session.post(f"{self.base_url}/auth/register", json={
            "username": username,
            "email": email,
            "password": password,
            "role": role,
        })
        return resp.json() if resp.status_code in (200, 201) else {"error": resp.text, "status": resp.status_code}

    def login(self, username: str, password: str) -> Dict:
        """Login a user."""
        resp = self.session.post(f"{self.base_url}/auth/login", json={
            "username": username,
            "password": password,
        })
        if resp.status_code == 200:
            data = resp.json()
            self.current_user = TestUser(
                id=data.get("user_id", data.get("id", "")),
                username=username,
                email=data.get("email", ""),
                role=data.get("role", "participant"),
                password=password,
            )
            # Store auth header if token is returned
            if "token" in data:
                self.session.headers["Authorization"] = f"Bearer {data['token']}"
            return data
        return {"error": resp.text, "status": resp.status_code}

    def logout(self):
        """Logout current user."""
        self.current_user = None
        self.session.headers.pop("Authorization", None)

    # ==================== Users ====================

    def create_user(self, username: str, email: str = None, role: str = "participant", password: str = "testpass123") -> Dict:
        """Create a test user via API."""
        email = email or f"{username}@test.example.com"
        resp = self.session.post(f"{self.base_url}/users", json={
            "username": username,
            "email": email,
            "role": role,
            "password": password,
        })
        return resp.json() if resp.status_code == 201 else {"error": resp.text, "status": resp.status_code}

    def get_user(self, user_id: str) -> Dict:
        """Get user by ID."""
        resp = self.session.get(f"{self.base_url}/users/{user_id}")
        return resp.json() if resp.status_code == 200 else {"error": resp.text, "status": resp.status_code}

    def list_users(self, **params) -> List[Dict]:
        """List users with optional filters."""
        resp = self.session.get(f"{self.base_url}/users", params=params)
        return resp.json() if resp.status_code == 200 else []

    # ==================== Events ====================

    def create_event(self, title: str, description: str = "", **kwargs) -> Dict:
        """Create an event."""
        data = {
            "title": title,
            "description": description,
            "status": kwargs.get("status", "published"),
            **kwargs,
        }
        resp = self.session.post(f"{self.base_url}/events", json=data)
        return resp.json() if resp.status_code == 201 else {"error": resp.text, "status": resp.status_code}

    def get_event(self, event_id: str) -> Dict:
        """Get event by ID."""
        resp = self.session.get(f"{self.base_url}/events/{event_id}")
        return resp.json() if resp.status_code == 200 else {"error": resp.text, "status": resp.status_code}

    def list_events(self, **params) -> List[Dict]:
        """List events with optional filters."""
        resp = self.session.get(f"{self.base_url}/events", params=params)
        return resp.json() if resp.status_code == 200 else []

    def close_event(self, event_id: str) -> Dict:
        """Close an event."""
        resp = self.session.patch(f"{self.base_url}/events/{event_id}", json={"status": "closed"})
        return resp.json() if resp.status_code == 200 else {"error": resp.text, "status": resp.status_code}

    # ==================== Posts ====================

    def create_post(self, title: str, content: str = "", post_type: str = "general", **kwargs) -> Dict:
        """Create a post."""
        data = {
            "title": title,
            "content": content,
            "type": post_type,
            "status": kwargs.get("status", "published"),
            **kwargs,
        }
        resp = self.session.post(f"{self.base_url}/posts", json=data)
        return resp.json() if resp.status_code == 201 else {"error": resp.text, "status": resp.status_code}

    def get_post(self, post_id: str) -> Dict:
        """Get post by ID."""
        resp = self.session.get(f"{self.base_url}/posts/{post_id}")
        return resp.json() if resp.status_code == 200 else {"error": resp.text, "status": resp.status_code}

    def list_posts(self, **params) -> List[Dict]:
        """List posts with optional filters."""
        resp = self.session.get(f"{self.base_url}/posts", params=params)
        return resp.json() if resp.status_code == 200 else []

    def update_post(self, post_id: str, **data) -> Dict:
        """Update a post."""
        resp = self.session.patch(f"{self.base_url}/posts/{post_id}", json=data)
        return resp.json() if resp.status_code == 200 else {"error": resp.text, "status": resp.status_code}

    def delete_post(self, post_id: str) -> bool:
        """Delete a post."""
        resp = self.session.delete(f"{self.base_url}/posts/{post_id}")
        return resp.status_code in (200, 204)

    # ==================== Groups ====================

    def create_group(self, name: str, description: str = "", **kwargs) -> Dict:
        """Create a group/team."""
        data = {
            "name": name,
            "description": description,
            "require_approval": kwargs.get("require_approval", False),
            **kwargs,
        }
        resp = self.session.post(f"{self.base_url}/groups", json=data)
        return resp.json() if resp.status_code == 201 else {"error": resp.text, "status": resp.status_code}

    def get_group(self, group_id: str) -> Dict:
        """Get group by ID."""
        resp = self.session.get(f"{self.base_url}/groups/{group_id}")
        return resp.json() if resp.status_code == 200 else {"error": resp.text, "status": resp.status_code}

    def list_groups(self, **params) -> List[Dict]:
        """List groups."""
        resp = self.session.get(f"{self.base_url}/groups", params=params)
        return resp.json() if resp.status_code == 200 else []

    def delete_group(self, group_id: str) -> bool:
        """Delete a group."""
        resp = self.session.delete(f"{self.base_url}/groups/{group_id}")
        return resp.status_code in (200, 204)

    # ==================== Group Membership ====================

    def join_group(self, group_id: str, user_id: str = None) -> Dict:
        """Apply to join a group."""
        user_id = user_id or (self.current_user.id if self.current_user else None)
        resp = self.session.post(f"{self.base_url}/groups/{group_id}/members", json={"user_id": user_id})
        return resp.json() if resp.status_code in (200, 201) else {"error": resp.text, "status": resp.status_code}

    def approve_member(self, group_id: str, user_id: str) -> Dict:
        """Approve a membership request."""
        resp = self.session.patch(f"{self.base_url}/groups/{group_id}/members/{user_id}", json={"status": "accepted"})
        return resp.json() if resp.status_code == 200 else {"error": resp.text, "status": resp.status_code}

    def reject_member(self, group_id: str, user_id: str) -> Dict:
        """Reject a membership request."""
        resp = self.session.patch(f"{self.base_url}/groups/{group_id}/members/{user_id}", json={"status": "rejected"})
        return resp.json() if resp.status_code == 200 else {"error": resp.text, "status": resp.status_code}

    def list_group_members(self, group_id: str) -> List[Dict]:
        """List group members."""
        resp = self.session.get(f"{self.base_url}/groups/{group_id}/members")
        return resp.json() if resp.status_code == 200 else []

    # ==================== Interactions ====================

    def like_post(self, post_id: str) -> Dict:
        """Like a post."""
        resp = self.session.post(f"{self.base_url}/posts/{post_id}/like")
        return resp.json() if resp.status_code in (200, 201) else {"error": resp.text, "status": resp.status_code}

    def comment_post(self, post_id: str, content: str) -> Dict:
        """Comment on a post."""
        resp = self.session.post(f"{self.base_url}/posts/{post_id}/comments", json={"content": content})
        return resp.json() if resp.status_code in (200, 201) else {"error": resp.text, "status": resp.status_code}

    def rate_post(self, post_id: str, score: float, dimension: str = "overall") -> Dict:
        """Rate a post."""
        resp = self.session.post(f"{self.base_url}/posts/{post_id}/ratings", json={
            "score": score,
            "dimension": dimension,
        })
        return resp.json() if resp.status_code in (200, 201) else {"error": resp.text, "status": resp.status_code}

    def list_post_interactions(self, post_id: str) -> List[Dict]:
        """List interactions on a post."""
        resp = self.session.get(f"{self.base_url}/posts/{post_id}/interactions")
        return resp.json() if resp.status_code == 200 else []

    # ==================== Resources ====================

    def create_resource(self, filename: str, **kwargs) -> Dict:
        """Create a resource."""
        data = {
            "filename": filename,
            **kwargs,
        }
        resp = self.session.post(f"{self.base_url}/resources", json=data)
        return resp.json() if resp.status_code == 201 else {"error": resp.text, "status": resp.status_code}

    def get_resource(self, resource_id: str) -> Dict:
        """Get resource by ID."""
        resp = self.session.get(f"{self.base_url}/resources/{resource_id}")
        return resp.json() if resp.status_code == 200 else {"error": resp.text, "status": resp.status_code}

    # ==================== Relations ====================

    def create_event_group_relation(self, event_id: str, group_id: str, relation_type: str = "registration") -> Dict:
        """Create event-group relation (team registration)."""
        resp = self.session.post(f"{self.base_url}/events/{event_id}/groups", json={
            "group_id": group_id,
            "relation_type": relation_type,
        })
        return resp.json() if resp.status_code in (200, 201) else {"error": resp.text, "status": resp.status_code}

    def create_event_post_relation(self, event_id: str, post_id: str, relation_type: str = "submission") -> Dict:
        """Create event-post relation (submission)."""
        resp = self.session.post(f"{self.base_url}/events/{event_id}/posts", json={
            "post_id": post_id,
            "relation_type": relation_type,
        })
        return resp.json() if resp.status_code in (200, 201) else {"error": resp.text, "status": resp.status_code}

    def create_post_resource_relation(self, post_id: str, resource_id: str, display_type: str = "attachment") -> Dict:
        """Create post-resource relation."""
        resp = self.session.post(f"{self.base_url}/posts/{post_id}/resources", json={
            "resource_id": resource_id,
            "display_type": display_type,
        })
        return resp.json() if resp.status_code in (200, 201) else {"error": resp.text, "status": resp.status_code}

    def create_post_post_relation(self, post_id: str, related_post_id: str, relation_type: str = "reference") -> Dict:
        """Create post-post relation (version, reference, embed)."""
        resp = self.session.post(f"{self.base_url}/posts/{post_id}/related", json={
            "related_post_id": related_post_id,
            "relation_type": relation_type,
        })
        return resp.json() if resp.status_code in (200, 201) else {"error": resp.text, "status": resp.status_code}


# ==================== Test Data Management ====================

def setup_test_users(api: APIClient) -> Dict[str, TestUser]:
    """Create standard test users."""
    users = {}

    # Alice - Team owner / Organizer
    alice = api.create_user("alice_test", "alice@test.example.com", "organizer", "alicepass123")
    if "id" in alice:
        users["alice"] = TestUser(alice["id"], "alice_test", "alice@test.example.com", "organizer", "alicepass123")

    # Bob - Team member / Participant
    bob = api.create_user("bob_test", "bob@test.example.com", "participant", "bobpass123")
    if "id" in bob:
        users["bob"] = TestUser(bob["id"], "bob_test", "bob@test.example.com", "participant", "bobpass123")

    # Carol - Applicant
    carol = api.create_user("carol_test", "carol@test.example.com", "participant", "carolpass123")
    if "id" in carol:
        users["carol"] = TestUser(carol["id"], "carol_test", "carol@test.example.com", "participant", "carolpass123")

    # Dave - Community member
    dave = api.create_user("dave_test", "dave@test.example.com", "participant", "davepass123")
    if "id" in dave:
        users["dave"] = TestUser(dave["id"], "dave_test", "dave@test.example.com", "participant", "davepass123")

    return users


def cleanup_test_data(api: APIClient, users: Dict[str, TestUser] = None):
    """Clean up test data after tests."""
    # This is a placeholder - actual cleanup depends on API capabilities
    pass
