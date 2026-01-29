"""User follow/block (user:user) tests — covers TC-FRIEND-001 through TC-FRIEND-007,
TC-FRIEND-900, TC-FRIEND-901, TC-FRIEND-902.
"""


def _create_user(client, username):
    resp = client.post("/api/users", json={
        "username": username,
        "email": f"{username}@example.com",
    })
    return resp.json()["id"]


# ---------- TC-FRIEND-001: Follow ----------
def test_follow_user(client):
    """TC-FRIEND-001: User A follows user B."""
    a = _create_user(client, "alice_f")
    b = _create_user(client, "bob_f")

    resp = client.post(f"/api/users/{b}/follow", headers={"X-User-Id": str(a)})
    assert resp.status_code == 201
    data = resp.json()
    assert data["source_user_id"] == a
    assert data["target_user_id"] == b
    assert data["relation_type"] == "follow"

    # Check following list
    following = client.get(f"/api/users/{a}/following")
    assert len(following.json()) == 1
    assert following.json()[0]["target_user_id"] == b


# ---------- TC-FRIEND-002: Mutual follow = friends ----------
def test_mutual_follow_is_friend(client):
    """TC-FRIEND-002: A follows B, B follows A → friends."""
    a = _create_user(client, "mutual_a")
    b = _create_user(client, "mutual_b")

    client.post(f"/api/users/{b}/follow", headers={"X-User-Id": str(a)})
    client.post(f"/api/users/{a}/follow", headers={"X-User-Id": str(b)})

    resp = client.get(f"/api/users/{a}/is-friend/{b}")
    assert resp.json()["is_friend"] is True


# ---------- TC-FRIEND-003: One-way follow is not friend ----------
def test_one_way_follow_not_friend(client):
    """TC-FRIEND-003: Only A→B follow, not friends."""
    a = _create_user(client, "oneway_a")
    b = _create_user(client, "oneway_b")

    client.post(f"/api/users/{b}/follow", headers={"X-User-Id": str(a)})

    resp = client.get(f"/api/users/{a}/is-friend/{b}")
    assert resp.json()["is_friend"] is False


# ---------- TC-FRIEND-004: Unfollow ----------
def test_unfollow_user(client):
    """TC-FRIEND-004: Unfollow removes from list, breaks friendship."""
    a = _create_user(client, "unf_a")
    b = _create_user(client, "unf_b")

    client.post(f"/api/users/{b}/follow", headers={"X-User-Id": str(a)})
    client.post(f"/api/users/{a}/follow", headers={"X-User-Id": str(b)})

    # Unfollow
    del_resp = client.delete(f"/api/users/{b}/follow", headers={"X-User-Id": str(a)})
    assert del_resp.status_code == 204

    # No longer in following list
    following = client.get(f"/api/users/{a}/following")
    assert len(following.json()) == 0

    # No longer friends
    resp = client.get(f"/api/users/{a}/is-friend/{b}")
    assert resp.json()["is_friend"] is False


# ---------- TC-FRIEND-005: Block overrides friendship ----------
def test_block_overrides_friendship(client):
    """TC-FRIEND-005: A blocks B → not friends even with mutual follow."""
    a = _create_user(client, "block_a")
    b = _create_user(client, "block_b")

    # Mutual follow
    client.post(f"/api/users/{b}/follow", headers={"X-User-Id": str(a)})
    client.post(f"/api/users/{a}/follow", headers={"X-User-Id": str(b)})

    # A blocks B
    resp = client.post(f"/api/users/{b}/block", headers={"X-User-Id": str(a)})
    assert resp.status_code == 201

    # Not friends anymore
    resp = client.get(f"/api/users/{a}/is-friend/{b}")
    assert resp.json()["is_friend"] is False


# ---------- TC-FRIEND-006: Blocked user cannot follow ----------
def test_blocked_user_cannot_follow(client):
    """TC-FRIEND-006: A blocks B, B cannot follow A."""
    a = _create_user(client, "blkf_a")
    b = _create_user(client, "blkf_b")

    client.post(f"/api/users/{b}/block", headers={"X-User-Id": str(a)})

    resp = client.post(f"/api/users/{a}/follow", headers={"X-User-Id": str(b)})
    assert resp.status_code == 403
    assert "blocked" in resp.json()["detail"].lower()


# ---------- TC-FRIEND-007: Delete user cascades user:user (deferred to Phase 7) ----------
# TC-FRIEND-007 requires soft delete cascade, tested separately in Phase 7


# ---------- TC-FRIEND-900: Cannot follow self ----------
def test_cannot_follow_self(client):
    """TC-FRIEND-900: Self-follow rejected."""
    a = _create_user(client, "self_follow")

    resp = client.post(f"/api/users/{a}/follow", headers={"X-User-Id": str(a)})
    assert resp.status_code == 422
    assert "self" in resp.json()["detail"].lower()


# ---------- TC-FRIEND-901: Duplicate follow rejected ----------
def test_duplicate_follow_rejected(client):
    """TC-FRIEND-901: Already following, second follow rejected."""
    a = _create_user(client, "dup_fa")
    b = _create_user(client, "dup_fb")

    client.post(f"/api/users/{b}/follow", headers={"X-User-Id": str(a)})
    resp = client.post(f"/api/users/{b}/follow", headers={"X-User-Id": str(a)})
    assert resp.status_code == 409


# ---------- TC-FRIEND-902: Invalid relation_type rejected ----------
def test_invalid_relation_type_rejected(client):
    """TC-FRIEND-902: Only follow/block are valid. 'mute' rejected via schema."""
    from pydantic import ValidationError
    from app.schemas.user_user import UserUserCreate
    try:
        UserUserCreate(source_user_id=1, target_user_id=2, relation_type="mute")
        assert False, "Should have raised ValidationError"
    except ValidationError:
        pass


# ---------- Additional: Followers list ----------
def test_followers_list(client):
    """List followers of a user."""
    a = _create_user(client, "flw_a")
    b = _create_user(client, "flw_b")
    c = _create_user(client, "flw_c")

    client.post(f"/api/users/{a}/follow", headers={"X-User-Id": str(b)})
    client.post(f"/api/users/{a}/follow", headers={"X-User-Id": str(c)})

    resp = client.get(f"/api/users/{a}/followers")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


# ---------- Additional: Follow nonexistent user ----------
def test_follow_nonexistent_user(client):
    """Follow nonexistent user returns 404."""
    a = _create_user(client, "fne_a")
    resp = client.post("/api/users/9999/follow", headers={"X-User-Id": str(a)})
    assert resp.status_code == 404


# ---------- Additional: Unfollow when not following ----------
def test_unfollow_not_following(client):
    """Unfollow when not following returns 404."""
    a = _create_user(client, "unfne_a")
    b = _create_user(client, "unfne_b")
    resp = client.delete(f"/api/users/{b}/follow", headers={"X-User-Id": str(a)})
    assert resp.status_code == 404


# ---------- Additional: Unblock when not blocking ----------
def test_unblock_not_blocking(client):
    """Unblock when not blocking returns 404."""
    a = _create_user(client, "unbne_a")
    b = _create_user(client, "unbne_b")
    resp = client.delete(f"/api/users/{b}/block", headers={"X-User-Id": str(a)})
    assert resp.status_code == 404


# ---------- Additional: Cannot block self ----------
def test_cannot_block_self(client):
    """Self-block rejected."""
    a = _create_user(client, "self_block")
    resp = client.post(f"/api/users/{a}/block", headers={"X-User-Id": str(a)})
    assert resp.status_code == 422
