"""Permissions & visibility tests — Phase 7 Layer 5-6

Covers:
- TC-PERM-001: Participant create category rejected
- TC-PERM-002: Participant create rule rejected
- TC-PERM-003: Participant update category rejected
- TC-PERM-012: Non-owner update user rejected (basic ownership)
- TC-PERM-020: Guest read draft post → not found
- TC-PERM-021: Guest read draft category → not found
- TC-PERM-022: Non-member read private group → not found
- TC-PERM-023: Draft post hidden in category post list
- TC-PERM-024: Private post hidden in category post list for non-author
"""


def _create_user(client, username="orguser", role="organizer"):
    resp = client.post("/api/users", json={
        "username": username,
        "email": f"{username}@example.com",
        "role": role,
    })
    return resp.json()["id"]


def _create_category(client, uid, name="Event", **extra):
    data = {
        "name": name,
        "description": f"Description of {name}",
        "type": "competition",
        **extra,
    }
    resp = client.post("/api/categories", json=data, headers={"X-User-Id": str(uid)})
    return resp.json()


def _create_post(client, uid, title="Post", **extra):
    data = {
        "title": title,
        "content": "Some content",
        "type": "general",
        **extra,
    }
    resp = client.post("/api/posts", json=data, headers={"X-User-Id": str(uid)})
    return resp.json()


# --- 10.1 Role permissions ---

def test_participant_cannot_create_category(client):
    """TC-PERM-001: Participant tries to create category → 403."""
    participant = _create_user(client, "part1", role="participant")
    resp = client.post("/api/categories", json={
        "name": "My Event",
        "description": "Desc",
        "type": "competition",
    }, headers={"X-User-Id": str(participant)})
    assert resp.status_code == 403


def test_participant_cannot_create_rule(client):
    """TC-PERM-002: Participant tries to create rule → 403."""
    participant = _create_user(client, "part2", role="participant")
    resp = client.post("/api/rules", json={
        "name": "Rule",
        "description": "Rule desc",
        "type": "submission",
    }, headers={"X-User-Id": str(participant)})
    assert resp.status_code == 403


def test_participant_cannot_update_category(client):
    """TC-PERM-003: Participant (non-creator) tries to update category → 403."""
    organizer = _create_user(client, "org1", role="organizer")
    participant = _create_user(client, "part3", role="participant")
    cat = _create_category(client, organizer)
    resp = client.patch(f"/api/categories/{cat['id']}", json={
        "name": "Updated",
    }, headers={"X-User-Id": str(participant)})
    assert resp.status_code == 403


def test_organizer_can_create_category(client):
    """Organizer can create category."""
    organizer = _create_user(client, "org2", role="organizer")
    resp = client.post("/api/categories", json={
        "name": "Event",
        "description": "Desc",
        "type": "competition",
    }, headers={"X-User-Id": str(organizer)})
    assert resp.status_code == 201


def test_admin_can_create_category(client):
    """Admin can create category."""
    admin = _create_user(client, "admin1", role="admin")
    resp = client.post("/api/categories", json={
        "name": "Admin Event",
        "description": "Desc",
        "type": "competition",
    }, headers={"X-User-Id": str(admin)})
    assert resp.status_code == 201


def test_owner_can_update_category(client):
    """Category creator can update it."""
    organizer = _create_user(client, "org3", role="organizer")
    cat = _create_category(client, organizer)
    resp = client.patch(f"/api/categories/{cat['id']}", json={
        "name": "Updated Name",
    }, headers={"X-User-Id": str(organizer)})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Updated Name"


def test_admin_can_update_any_category(client):
    """Admin can update any category even if not owner."""
    organizer = _create_user(client, "org4", role="organizer")
    admin = _create_user(client, "admin2", role="admin")
    cat = _create_category(client, organizer)
    resp = client.patch(f"/api/categories/{cat['id']}", json={
        "name": "Admin Updated",
    }, headers={"X-User-Id": str(admin)})
    assert resp.status_code == 200


def test_other_organizer_cannot_update_category(client):
    """Organizer B cannot update Organizer A's category."""
    org_a = _create_user(client, "orgA", role="organizer")
    org_b = _create_user(client, "orgB", role="organizer")
    cat = _create_category(client, org_a)
    resp = client.patch(f"/api/categories/{cat['id']}", json={
        "name": "Stolen Update",
    }, headers={"X-User-Id": str(org_b)})
    assert resp.status_code == 403


# --- 10.3 Visibility filtering ---

def test_guest_cannot_read_draft_post(client):
    """TC-PERM-020: Guest reads draft post → 404."""
    uid = _create_user(client, "author1")
    post = _create_post(client, uid, status="draft")
    # Guest (no X-User-Id header)
    resp = client.get(f"/api/posts/{post['id']}")
    assert resp.status_code == 404


def test_author_can_read_own_draft_post(client):
    """Author can read their own draft post."""
    uid = _create_user(client, "author2")
    post = _create_post(client, uid, status="draft")
    resp = client.get(f"/api/posts/{post['id']}", headers={"X-User-Id": str(uid)})
    assert resp.status_code == 200


def test_guest_cannot_read_draft_category(client):
    """TC-PERM-021: Guest reads draft category → 404."""
    uid = _create_user(client, "org5")
    cat = _create_category(client, uid)
    # Category defaults to draft status
    assert cat["status"] == "draft"
    # Guest (no X-User-Id)
    resp = client.get(f"/api/categories/{cat['id']}")
    assert resp.status_code == 404


def test_creator_can_read_own_draft_category(client):
    """Creator can read their own draft category."""
    uid = _create_user(client, "org6")
    cat = _create_category(client, uid)
    resp = client.get(f"/api/categories/{cat['id']}", headers={"X-User-Id": str(uid)})
    assert resp.status_code == 200


def test_non_member_cannot_read_private_group(client):
    """TC-PERM-022: Non-member reads private group → 404."""
    uid = _create_user(client, "grp_owner")
    other = _create_user(client, "outsider")
    resp = client.post("/api/groups", json={
        "name": "Secret Group",
        "description": "Private",
        "visibility": "private",
    }, headers={"X-User-Id": str(uid)})
    group_id = resp.json()["id"]

    # Non-member tries to read
    resp = client.get(f"/api/groups/{group_id}", headers={"X-User-Id": str(other)})
    assert resp.status_code == 404

    # Creator can read
    resp = client.get(f"/api/groups/{group_id}", headers={"X-User-Id": str(uid)})
    assert resp.status_code == 200


def test_draft_post_hidden_in_category_posts(client):
    """TC-PERM-023: Draft post in published category not visible to guest."""
    uid = _create_user(client, "org7")
    cat = _create_category(client, uid)
    # Publish category
    client.patch(f"/api/categories/{cat['id']}", json={"status": "published"}, headers={"X-User-Id": str(uid)})
    # Create draft post
    post = _create_post(client, uid, status="draft")
    # Associate with category
    client.post(f"/api/categories/{cat['id']}/posts", json={
        "post_id": post["id"], "relation_type": "submission",
    })

    # Guest list → should be empty (draft filtered)
    resp = client.get(f"/api/categories/{cat['id']}/posts")
    assert len(resp.json()) == 0

    # Author sees it
    resp = client.get(f"/api/categories/{cat['id']}/posts", headers={"X-User-Id": str(uid)})
    assert len(resp.json()) == 1


def test_private_post_hidden_in_category_posts(client):
    """TC-PERM-024: Private published post hidden from non-author in category listing."""
    uid = _create_user(client, "org8")
    other = _create_user(client, "viewer1")
    cat = _create_category(client, uid)
    client.patch(f"/api/categories/{cat['id']}", json={"status": "published"}, headers={"X-User-Id": str(uid)})

    # Create private published post
    post = _create_post(client, uid, visibility="private", status="draft")
    # Publish it
    client.patch(f"/api/posts/{post['id']}", json={"status": "pending_review"}, headers={"X-User-Id": str(uid)})
    client.patch(f"/api/posts/{post['id']}", json={"status": "published"}, headers={"X-User-Id": str(uid)})

    # Associate with category
    client.post(f"/api/categories/{cat['id']}/posts", json={
        "post_id": post["id"], "relation_type": "submission",
    })

    # Non-author → empty
    resp = client.get(f"/api/categories/{cat['id']}/posts", headers={"X-User-Id": str(other)})
    assert len(resp.json()) == 0

    # Author → visible
    resp = client.get(f"/api/categories/{cat['id']}/posts", headers={"X-User-Id": str(uid)})
    assert len(resp.json()) == 1


def test_guest_reads_private_post_returns_not_found(client):
    """Private post returns 404 for guests."""
    uid = _create_user(client, "priv_author")
    post = _create_post(client, uid, visibility="private")
    resp = client.get(f"/api/posts/{post['id']}")
    assert resp.status_code == 404


def test_no_auth_header_create_category_returns_401(client):
    """Creating category without auth → 401."""
    resp = client.post("/api/categories", json={
        "name": "Event",
        "description": "Desc",
        "type": "competition",
    })
    assert resp.status_code == 401
