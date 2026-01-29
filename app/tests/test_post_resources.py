"""Post:resource relationship tests — covers TC-REL-PR-001 through TC-REL-PR-005"""


def _create_user(client, username="author"):
    resp = client.post("/api/users", json={
        "username": username,
        "email": f"{username}@example.com",
    })
    return resp.json()["id"]


def _create_post(client, uid, title="Test Post"):
    resp = client.post("/api/posts", json={
        "title": title,
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201
    return resp.json()


def _create_resource(client, uid, filename="test.pdf"):
    resp = client.post("/api/resources", json={
        "filename": filename,
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201
    return resp.json()


# ---------- TC-REL-PR-001: Attach resource as attachment ----------
def test_attach_resource_as_attachment(client):
    """TC-REL-PR-001: Attach resource with display_type=attachment."""
    uid = _create_user(client, "pr_author1")
    post = _create_post(client, uid)
    resource = _create_resource(client, uid)

    resp = client.post(f"/api/posts/{post['id']}/resources", json={
        "resource_id": resource["id"],
        "display_type": "attachment",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["post_id"] == post["id"]
    assert data["resource_id"] == resource["id"]
    assert data["display_type"] == "attachment"


# ---------- TC-REL-PR-002: Attach resource as inline ----------
def test_attach_resource_as_inline(client):
    """TC-REL-PR-002: Attach resource with display_type=inline."""
    uid = _create_user(client, "pr_author2")
    post = _create_post(client, uid)
    resource = _create_resource(client, uid)

    resp = client.post(f"/api/posts/{post['id']}/resources", json={
        "resource_id": resource["id"],
        "display_type": "inline",
    })
    assert resp.status_code == 201
    assert resp.json()["display_type"] == "inline"


# ---------- TC-REL-PR-003: Multiple resources with position ----------
def test_multiple_resources_with_position(client):
    """TC-REL-PR-003: Same post, multiple resources with position sorting."""
    uid = _create_user(client, "pr_author3")
    post = _create_post(client, uid)
    r1 = _create_resource(client, uid, "file1.pdf")
    r2 = _create_resource(client, uid, "file2.pdf")

    client.post(f"/api/posts/{post['id']}/resources", json={
        "resource_id": r1["id"],
        "position": 0,
    })
    client.post(f"/api/posts/{post['id']}/resources", json={
        "resource_id": r2["id"],
        "position": 1,
    })

    resp = client.get(f"/api/posts/{post['id']}/resources")
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 2
    assert items[0]["position"] == 0
    assert items[1]["position"] == 1


# ---------- TC-REL-PR-004: Update display_type ----------
def test_update_post_resource_display_type(client):
    """TC-REL-PR-004: Change display_type from attachment to inline."""
    uid = _create_user(client, "pr_author4")
    post = _create_post(client, uid)
    resource = _create_resource(client, uid)

    create_resp = client.post(f"/api/posts/{post['id']}/resources", json={
        "resource_id": resource["id"],
        "display_type": "attachment",
    })
    rel_id = create_resp.json()["id"]

    update_resp = client.patch(f"/api/posts/{post['id']}/resources/{rel_id}", json={
        "resource_id": resource["id"],
        "display_type": "inline",
    })
    assert update_resp.status_code == 200
    assert update_resp.json()["display_type"] == "inline"


# ---------- TC-REL-PR-005: Remove post:resource (resource still exists) ----------
def test_remove_post_resource(client):
    """TC-REL-PR-005: Remove relation, resource entity still accessible."""
    uid = _create_user(client, "pr_author5")
    post = _create_post(client, uid)
    resource = _create_resource(client, uid)

    create_resp = client.post(f"/api/posts/{post['id']}/resources", json={
        "resource_id": resource["id"],
    })
    rel_id = create_resp.json()["id"]

    del_resp = client.delete(f"/api/posts/{post['id']}/resources/{rel_id}")
    assert del_resp.status_code == 204

    # Resource still accessible
    res_resp = client.get(f"/api/resources/{resource['id']}")
    assert res_resp.status_code == 200

    # Relation list empty
    list_resp = client.get(f"/api/posts/{post['id']}/resources")
    assert len(list_resp.json()) == 0


# ---------- Additional: Duplicate resource attachment rejected ----------
def test_duplicate_resource_rejected(client):
    """Attaching same resource to same post twice rejected."""
    uid = _create_user(client, "pr_dup")
    post = _create_post(client, uid)
    resource = _create_resource(client, uid)

    client.post(f"/api/posts/{post['id']}/resources", json={
        "resource_id": resource["id"],
    })
    resp = client.post(f"/api/posts/{post['id']}/resources", json={
        "resource_id": resource["id"],
    })
    assert resp.status_code == 409


# ---------- Additional: Attach to nonexistent post ----------
def test_attach_to_nonexistent_post(client):
    """Attach resource to nonexistent post returns 404."""
    uid = _create_user(client, "pr_nopost")
    resource = _create_resource(client, uid)
    resp = client.post("/api/posts/9999/resources", json={
        "resource_id": resource["id"],
    })
    assert resp.status_code == 404


# ---------- Additional: Attach nonexistent resource ----------
def test_attach_nonexistent_resource(client):
    """Attach nonexistent resource to post returns 404."""
    uid = _create_user(client, "pr_nores")
    post = _create_post(client, uid)
    resp = client.post(f"/api/posts/{post['id']}/resources", json={
        "resource_id": 9999,
    })
    assert resp.status_code == 404


# ---------- Additional: Invalid display_type rejected ----------
def test_invalid_display_type_rejected(client):
    """Invalid display_type 'embed' rejected by schema."""
    uid = _create_user(client, "pr_badtype")
    post = _create_post(client, uid)
    resource = _create_resource(client, uid)
    resp = client.post(f"/api/posts/{post['id']}/resources", json={
        "resource_id": resource["id"],
        "display_type": "embed",
    })
    assert resp.status_code == 422
