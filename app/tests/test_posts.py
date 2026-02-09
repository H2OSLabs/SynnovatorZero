"""Post API tests — covers TC-POST-001 through TC-POST-903"""


def _create_user(client, username="author", role="participant"):
    resp = client.post("/api/users", json={
        "username": username,
        "email": f"{username}@example.com",
        "role": role,
    })
    return resp.json()["id"]


def _create_post(client, uid, **overrides):
    payload = {"title": "Test Post"}
    payload.update(overrides)
    resp = client.post("/api/posts", json=payload, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201
    return resp.json()


# ---------- TC-POST-001: 最小字段创建帖子 ----------
def test_create_post_minimal(client):
    uid = _create_user(client)
    resp = client.post("/api/posts", json={
        "title": "My First Post",
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "My First Post"
    assert data["type"] == "general"
    assert data["status"] == "draft"
    assert data["visibility"] == "public"
    assert data["like_count"] == 0
    assert data["comment_count"] == 0
    assert data["average_rating"] is None
    assert data["created_by"] == uid
    assert "id" in data
    assert "created_at" in data


# ---------- TC-POST-002: 创建时直接发布 ----------
def test_create_post_published(client):
    uid = _create_user(client)
    resp = client.post("/api/posts", json={
        "title": "Published Post",
        "status": "published",
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201
    assert resp.json()["status"] == "published"


# ---------- TC-POST-003: 创建帖子带标签 ----------
def test_create_post_with_tags(client):
    uid = _create_user(client)
    resp = client.post("/api/posts", json={
        "title": "Tagged Post",
        "tags": ["ai", "demo", "hackathon"],
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201
    data = resp.json()
    assert data["tags"] == ["ai", "demo", "hackathon"]


# ---------- TC-POST-010~013: 不同类型帖子 ----------
def test_create_team_post(client):
    uid = _create_user(client)
    post = _create_post(client, uid, type="team", title="Team Intro")
    assert post["type"] == "team"


def test_create_profile_post(client):
    uid = _create_user(client)
    post = _create_post(client, uid, type="profile", title="My Profile")
    assert post["type"] == "profile"


def test_create_proposal_post(client):
    uid = _create_user(client)
    post = _create_post(client, uid, type="proposal", title="My Submission")
    assert post["type"] == "proposal"


def test_create_certificate_post(client):
    uid = _create_user(client)
    post = _create_post(client, uid, type="certificate", title="My Certificate")
    assert post["type"] == "certificate"


# ---------- TC-POST-030: 进入 pending_review 状态 ----------
def test_status_transition_draft_to_pending_review(client):
    uid = _create_user(client)
    post = _create_post(client, uid)
    resp = client.patch(f"/api/posts/{post['id']}", json={"status": "pending_review"}, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 200
    assert resp.json()["status"] == "pending_review"


# ---------- TC-POST-031: pending_review → published ----------
def test_status_transition_pending_review_to_published(client):
    uid = _create_user(client)
    post = _create_post(client, uid)
    client.patch(f"/api/posts/{post['id']}", json={"status": "pending_review"}, headers={"X-User-Id": str(uid)})
    resp = client.patch(f"/api/posts/{post['id']}", json={"status": "published"}, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 200
    assert resp.json()["status"] == "published"


# ---------- TC-POST-032: pending_review → rejected ----------
def test_status_transition_pending_review_to_rejected(client):
    uid = _create_user(client)
    post = _create_post(client, uid)
    client.patch(f"/api/posts/{post['id']}", json={"status": "pending_review"}, headers={"X-User-Id": str(uid)})
    resp = client.patch(f"/api/posts/{post['id']}", json={"status": "rejected"}, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 200
    assert resp.json()["status"] == "rejected"


# ---------- TC-POST-033: rejected → draft (resubmit) ----------
def test_status_transition_rejected_to_draft(client):
    uid = _create_user(client)
    post = _create_post(client, uid)
    client.patch(f"/api/posts/{post['id']}", json={"status": "pending_review"}, headers={"X-User-Id": str(uid)})
    client.patch(f"/api/posts/{post['id']}", json={"status": "rejected"}, headers={"X-User-Id": str(uid)})
    resp = client.patch(f"/api/posts/{post['id']}", json={"status": "draft"}, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 200
    assert resp.json()["status"] == "draft"


# ---------- published is terminal ----------
def test_published_is_terminal_state(client):
    uid = _create_user(client)
    post = _create_post(client, uid, status="published")
    resp = client.patch(f"/api/posts/{post['id']}", json={"status": "draft"}, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 422


# ---------- TC-POST-060: 更新标题和内容 ----------
def test_update_title_and_content(client):
    uid = _create_user(client)
    post = _create_post(client, uid, content="# Original")
    resp = client.patch(f"/api/posts/{post['id']}", json={
        "title": "Updated Title",
        "content": "# Updated Content",
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Updated Title"
    assert data["content"] == "# Updated Content"


# ---------- TC-POST-070: 创建 visibility=private 帖子 ----------
def test_create_private_post(client):
    uid = _create_user(client)
    post = _create_post(client, uid, visibility="private")
    assert post["visibility"] == "private"


# ---------- TC-POST-071: private 帖子跳过 pending_review ----------
def test_private_post_can_publish_directly(client):
    uid = _create_user(client)
    post = _create_post(client, uid, visibility="private")
    resp = client.patch(f"/api/posts/{post['id']}", json={"status": "published"}, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 200
    assert resp.json()["status"] == "published"


# ---------- TC-POST-073: public → private ----------
def test_change_visibility_public_to_private(client):
    uid = _create_user(client)
    post = _create_post(client, uid)
    resp = client.patch(f"/api/posts/{post['id']}", json={"visibility": "private"}, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 200
    assert resp.json()["visibility"] == "private"


# ---------- TC-POST-074: private → public ----------
def test_change_visibility_private_to_public(client):
    uid = _create_user(client)
    post = _create_post(client, uid, visibility="private")
    resp = client.patch(f"/api/posts/{post['id']}", json={"visibility": "public"}, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 200
    assert resp.json()["visibility"] == "public"


# ---------- TC-POST-076: 默认 visibility=public ----------
def test_default_visibility_is_public(client):
    uid = _create_user(client)
    post = _create_post(client, uid)
    assert post["visibility"] == "public"


# ---------- 删除帖子 (soft delete) ----------
def test_delete_post(client):
    uid = _create_user(client)
    post = _create_post(client, uid, title="Delete Me")
    del_resp = client.delete(f"/api/posts/{post['id']}", headers={"X-User-Id": str(uid)})
    assert del_resp.status_code == 204

    get_resp = client.get(f"/api/posts/{post['id']}")
    assert get_resp.status_code == 404

    list_resp = client.get("/api/posts")
    titles = [p["title"] for p in list_resp.json()["items"]]
    assert "Delete Me" not in titles


# ---------- TC-POST-900: 缺少 title 被拒绝 ----------
def test_missing_title_rejected(client):
    uid = _create_user(client)
    resp = client.post("/api/posts", json={}, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 422


# ---------- TC-POST-901: 无效 type/status 枚举被拒绝 ----------
def test_invalid_type_rejected(client):
    uid = _create_user(client)
    resp = client.post("/api/posts", json={
        "title": "Bad Type",
        "type": "blog",
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 422


def test_invalid_status_rejected(client):
    uid = _create_user(client)
    resp = client.post("/api/posts", json={
        "title": "Bad Status",
        "status": "archived",
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 422


# ---------- TC-POST-902: 未认证用户无法创建帖子 ----------
def test_unauthenticated_cannot_create_post(client):
    """Creating post with invalid user returns 401.

    Note: In mock mode, requests without X-User-Id header auto-create a mock user.
    This test verifies auth failure by providing an invalid (non-existent) user ID.
    """
    resp = client.post("/api/posts", json={"title": "No Auth"}, headers={"X-User-Id": "99999"})
    assert resp.status_code == 401


# ---------- TC-POST-903: 无效 visibility 枚举被拒绝 ----------
def test_invalid_visibility_rejected(client):
    uid = _create_user(client)
    resp = client.post("/api/posts", json={
        "title": "Bad Vis",
        "visibility": "restricted",
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 422


# ---------- Additional: list posts ----------
def test_list_posts(client):
    uid = _create_user(client)
    _create_post(client, uid, title="P1")
    _create_post(client, uid, title="P2")
    resp = client.get("/api/posts", headers={"X-User-Id": str(uid)})
    assert resp.status_code == 200
    assert resp.json()["total"] == 2


def test_list_posts_legacy_unknown_type_falls_back_to_general(client, db_session):
    uid = _create_user(client)
    from app.models.post import Post as PostModel
    db_session.add(PostModel(title="Legacy", type="for_category", status="published", visibility="public", created_by=uid))
    db_session.commit()

    resp = client.get("/api/posts?status=published")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["type"] == "general"


def test_list_posts_filter_by_status(client):
    uid = _create_user(client)
    _create_post(client, uid, title="Draft1", status="draft")
    _create_post(client, uid, title="Published1", status="published")
    resp = client.get("/api/posts?status=published")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["status"] == "published"


def test_list_posts_filter_by_type(client):
    uid = _create_user(client)
    _create_post(client, uid, title="Team1", type="team")
    _create_post(client, uid, title="General1", type="general")
    resp = client.get("/api/posts?type=team", headers={"X-User-Id": str(uid)})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["type"] == "team"


def test_list_posts_filter_by_tags(client):
    uid = _create_user(client)
    _create_post(client, uid, title="AI Post", status="published", tags=["ai", "demo"])
    _create_post(client, uid, title="Web3 Post", status="published", tags=["web3"])
    _create_post(client, uid, title="No Tag Post", status="published", tags=[])

    resp = client.get("/api/posts?tags=ai")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "AI Post"

    resp2 = client.get("/api/posts?tags=AI,web3")
    assert resp2.status_code == 200
    data2 = resp2.json()
    titles = {p["title"] for p in data2["items"]}
    assert titles == {"AI Post", "Web3 Post"}


def test_list_posts_filter_by_q(client):
    uid = _create_user(client)
    _create_post(client, uid, title="Build a LLM Agent", status="published", content="hello world", tags=["ai"])
    _create_post(client, uid, title="Random Post", status="published", content="deep dive into web3", tags=["web3"])
    _create_post(client, uid, title="Draft Not Visible", status="draft", content="llm", tags=["ai"])

    resp = client.get("/api/posts?q=llm")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Build a LLM Agent"


def test_list_posts_filter_invalid_value_rejected(client):
    uid = _create_user(client)
    _create_post(client, uid, title="P1")
    resp = client.get("/api/posts?status=archived")
    assert resp.status_code == 422
    resp2 = client.get("/api/posts?type=workshop")
    assert resp2.status_code == 422


# ---------- Additional: get nonexistent post ----------
def test_get_nonexistent_post(client):
    resp = client.get("/api/posts/9999")
    assert resp.status_code == 404
