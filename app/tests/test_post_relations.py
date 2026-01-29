"""Post:post relationship tests — covers TC-REL-PP-001 through TC-REL-PP-005"""


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


# ---------- TC-REL-PP-001: Create embed relation ----------
def test_create_embed_relation(client):
    """TC-REL-PP-001: Embed team card into post."""
    uid = _create_user(client, "pp_author1")
    source = _create_post(client, uid, "Main Post")
    target = _create_post(client, uid, "Team Card")

    resp = client.post(f"/api/posts/{source['id']}/related", json={
        "target_post_id": target["id"],
        "relation_type": "embed",
        "position": 1,
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["source_post_id"] == source["id"]
    assert data["target_post_id"] == target["id"]
    assert data["relation_type"] == "embed"
    assert data["position"] == 1


# ---------- TC-REL-PP-002: Create reference relation ----------
def test_create_reference_relation(client):
    """TC-REL-PP-002: Reference another post."""
    uid = _create_user(client, "pp_author2")
    source = _create_post(client, uid, "Citing Post")
    target = _create_post(client, uid, "Cited Post")

    resp = client.post(f"/api/posts/{source['id']}/related", json={
        "target_post_id": target["id"],
        "relation_type": "reference",
    })
    assert resp.status_code == 201
    assert resp.json()["relation_type"] == "reference"


# ---------- TC-REL-PP-003: Create reply relation ----------
def test_create_reply_relation(client):
    """TC-REL-PP-003: Reply to another post."""
    uid = _create_user(client, "pp_author3")
    source = _create_post(client, uid, "Reply Post")
    target = _create_post(client, uid, "Original Post")

    resp = client.post(f"/api/posts/{source['id']}/related", json={
        "target_post_id": target["id"],
        "relation_type": "reply",
    })
    assert resp.status_code == 201
    assert resp.json()["relation_type"] == "reply"


# ---------- TC-REL-PP-004: Update relation type and position ----------
def test_update_relation_type_and_position(client):
    """TC-REL-PP-004: Change embed→reference, position=0."""
    uid = _create_user(client, "pp_author4")
    source = _create_post(client, uid, "Update Source")
    target = _create_post(client, uid, "Update Target")

    create_resp = client.post(f"/api/posts/{source['id']}/related", json={
        "target_post_id": target["id"],
        "relation_type": "embed",
        "position": 1,
    })
    rel_id = create_resp.json()["id"]

    update_resp = client.patch(f"/api/posts/{source['id']}/related/{rel_id}", json={
        "target_post_id": target["id"],
        "relation_type": "reference",
        "position": 0,
    })
    assert update_resp.status_code == 200
    data = update_resp.json()
    assert data["relation_type"] == "reference"
    assert data["position"] == 0


# ---------- TC-REL-PP-005: Delete post:post relation ----------
def test_delete_relation(client):
    """TC-REL-PP-005: Delete post:post relation."""
    uid = _create_user(client, "pp_author5")
    source = _create_post(client, uid, "Del Source")
    target = _create_post(client, uid, "Del Target")

    create_resp = client.post(f"/api/posts/{source['id']}/related", json={
        "target_post_id": target["id"],
    })
    rel_id = create_resp.json()["id"]

    del_resp = client.delete(f"/api/posts/{source['id']}/related/{rel_id}")
    assert del_resp.status_code == 204

    # Relation list empty
    list_resp = client.get(f"/api/posts/{source['id']}/related")
    assert len(list_resp.json()) == 0


# ---------- Additional: List by relation_type filter ----------
def test_list_by_relation_type(client):
    """Filter related posts by relation_type."""
    uid = _create_user(client, "pp_filter")
    source = _create_post(client, uid, "Filter Source")
    t1 = _create_post(client, uid, "Embed Target")
    t2 = _create_post(client, uid, "Ref Target")

    client.post(f"/api/posts/{source['id']}/related", json={
        "target_post_id": t1["id"],
        "relation_type": "embed",
    })
    client.post(f"/api/posts/{source['id']}/related", json={
        "target_post_id": t2["id"],
        "relation_type": "reference",
    })

    # All relations
    resp_all = client.get(f"/api/posts/{source['id']}/related")
    assert len(resp_all.json()) == 2

    # Filter embed only
    resp_embed = client.get(f"/api/posts/{source['id']}/related?relation_type=embed")
    assert len(resp_embed.json()) == 1
    assert resp_embed.json()[0]["relation_type"] == "embed"


# ---------- Additional: Relate to nonexistent post ----------
def test_relate_to_nonexistent_post(client):
    """Creating relation to nonexistent target returns 404."""
    uid = _create_user(client, "pp_notar")
    source = _create_post(client, uid, "No Target")
    resp = client.post(f"/api/posts/{source['id']}/related", json={
        "target_post_id": 9999,
    })
    assert resp.status_code == 404


# ---------- Additional: Invalid relation_type rejected ----------
def test_invalid_relation_type_rejected(client):
    """Invalid relation_type 'fork' rejected by schema."""
    uid = _create_user(client, "pp_badtype")
    source = _create_post(client, uid, "Bad Type Source")
    target = _create_post(client, uid, "Bad Type Target")
    resp = client.post(f"/api/posts/{source['id']}/related", json={
        "target_post_id": target["id"],
        "relation_type": "fork",
    })
    assert resp.status_code == 422


# ---------- Additional: Default relation_type is reference ----------
def test_default_relation_type(client):
    """Default relation_type is 'reference'."""
    uid = _create_user(client, "pp_default")
    source = _create_post(client, uid, "Default Source")
    target = _create_post(client, uid, "Default Target")
    resp = client.post(f"/api/posts/{source['id']}/related", json={
        "target_post_id": target["id"],
    })
    assert resp.status_code == 201
    assert resp.json()["relation_type"] == "reference"
