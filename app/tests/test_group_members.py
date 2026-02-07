"""Group member (group:user) tests — covers TC-REL-GU-001, TC-REL-GU-900, TC-REL-GU-901
TC-REL-GU-902 deferred to Phase 6 (requires event_group + rule enforcement).
"""


def _create_user(client, username="alice"):
    resp = client.post("/api/users", json={
        "username": username,
        "email": f"{username}@example.com",
    })
    return resp.json()["id"]


def _create_group(client, uid, name="Test Team", require_approval=True):
    resp = client.post("/api/groups", json={
        "name": name,
        "require_approval": require_approval,
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201
    return resp.json()


# ---------- TC-REL-GU: Add member ----------
def test_add_member_to_group_with_approval(client):
    """Add member to group with require_approval=true → status=pending."""
    owner_id = _create_user(client, "owner")
    member_id = _create_user(client, "member1")
    group = _create_group(client, owner_id, require_approval=True)

    resp = client.post(f"/api/groups/{group['id']}/members", json={
        "user_id": member_id,
        "role": "member",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["user_id"] == member_id
    assert data["group_id"] == group["id"]
    assert data["role"] == "member"
    assert data["status"] == "pending"


def test_add_member_to_group_without_approval(client):
    """Add member to group with require_approval=false → status=accepted."""
    owner_id = _create_user(client, "owner2")
    member_id = _create_user(client, "member2")
    group = _create_group(client, owner_id, require_approval=False)

    resp = client.post(f"/api/groups/{group['id']}/members", json={
        "user_id": member_id,
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["status"] == "accepted"
    assert data["joined_at"] is not None


def test_add_owner_member(client):
    """Add owner role member."""
    uid = _create_user(client, "creator")
    group = _create_group(client, uid)

    resp = client.post(f"/api/groups/{group['id']}/members", json={
        "user_id": uid,
        "role": "owner",
    })
    assert resp.status_code == 201
    assert resp.json()["role"] == "owner"


# ---------- TC-REL-GU-900: Duplicate member rejected ----------
def test_duplicate_member_rejected(client):
    """TC-REL-GU-900: Already a member, re-adding rejected."""
    owner_id = _create_user(client, "dup_owner")
    member_id = _create_user(client, "dup_member")
    group = _create_group(client, owner_id)

    client.post(f"/api/groups/{group['id']}/members", json={"user_id": member_id})
    resp = client.post(f"/api/groups/{group['id']}/members", json={"user_id": member_id})
    assert resp.status_code == 409


# ---------- TC-REL-GU-901: Invalid role enum rejected ----------
def test_invalid_role_rejected(client):
    """TC-REL-GU-901: Invalid role 'superadmin' rejected."""
    owner_id = _create_user(client, "role_owner")
    member_id = _create_user(client, "role_member")
    group = _create_group(client, owner_id)

    resp = client.post(f"/api/groups/{group['id']}/members", json={
        "user_id": member_id,
        "role": "superadmin",
    })
    assert resp.status_code == 422


# ---------- TC-REL-GU-001: Remove member ----------
def test_remove_member(client):
    """TC-REL-GU-001: Remove accepted member from group."""
    owner_id = _create_user(client, "rm_owner")
    member_id = _create_user(client, "rm_member")
    group = _create_group(client, owner_id, require_approval=False)

    client.post(f"/api/groups/{group['id']}/members", json={"user_id": member_id})

    del_resp = client.delete(f"/api/groups/{group['id']}/members/{member_id}")
    assert del_resp.status_code == 204

    # Verify removed
    list_resp = client.get(f"/api/groups/{group['id']}/members")
    assert list_resp.json()["total"] == 0


# ---------- List members ----------
def test_list_members(client):
    """List all members of a group."""
    owner_id = _create_user(client, "list_owner")
    m1 = _create_user(client, "list_m1")
    m2 = _create_user(client, "list_m2")
    group = _create_group(client, owner_id, require_approval=False)

    client.post(f"/api/groups/{group['id']}/members", json={"user_id": m1})
    client.post(f"/api/groups/{group['id']}/members", json={"user_id": m2})

    resp = client.get(f"/api/groups/{group['id']}/members")
    assert resp.status_code == 200
    assert resp.json()["total"] == 2


def test_list_members_by_status(client):
    """List members filtered by status."""
    owner_id = _create_user(client, "fs_owner")
    m1 = _create_user(client, "fs_m1")
    m2 = _create_user(client, "fs_m2")
    group = _create_group(client, owner_id, require_approval=True)

    # m1 pending
    client.post(f"/api/groups/{group['id']}/members", json={"user_id": m1})
    # m2 pending then accepted
    client.post(f"/api/groups/{group['id']}/members", json={"user_id": m2})
    client.patch(f"/api/groups/{group['id']}/members/{m2}", json={"status": "accepted"})

    resp_pending = client.get(f"/api/groups/{group['id']}/members?status=pending")
    assert resp_pending.json()["total"] == 1

    resp_accepted = client.get(f"/api/groups/{group['id']}/members?status=accepted")
    assert resp_accepted.json()["total"] == 1


# ---------- Approve/reject member ----------
def test_approve_member(client):
    """Approve pending member → accepted, joined_at set."""
    owner_id = _create_user(client, "app_owner")
    member_id = _create_user(client, "app_member")
    group = _create_group(client, owner_id, require_approval=True)

    client.post(f"/api/groups/{group['id']}/members", json={"user_id": member_id})

    resp = client.patch(f"/api/groups/{group['id']}/members/{member_id}", json={
        "status": "accepted",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "accepted"
    assert data["joined_at"] is not None


def test_reject_member(client):
    """Reject pending member → rejected."""
    owner_id = _create_user(client, "rej_owner")
    member_id = _create_user(client, "rej_member")
    group = _create_group(client, owner_id, require_approval=True)

    client.post(f"/api/groups/{group['id']}/members", json={"user_id": member_id})

    resp = client.patch(f"/api/groups/{group['id']}/members/{member_id}", json={
        "status": "rejected",
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "rejected"


# ---------- Member not found ----------
def test_remove_nonexistent_member(client):
    """Remove member that doesn't exist returns 404."""
    owner_id = _create_user(client, "ne_owner")
    group = _create_group(client, owner_id)
    resp = client.delete(f"/api/groups/{group['id']}/members/9999")
    assert resp.status_code == 404


def test_add_member_to_nonexistent_group(client):
    """Add member to nonexistent group returns 404."""
    member_id = _create_user(client, "nogrp_member")
    resp = client.post("/api/groups/9999/members", json={"user_id": member_id})
    assert resp.status_code == 404
