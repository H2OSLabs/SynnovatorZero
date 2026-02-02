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


def test_create_for_category_post(client):
    uid = _create_user(client)
    post = _create_post(client, uid, type="for_category", title="My Submission")
    assert post["type"] == "for_category"


def test_create_certificate_post(client):
    uid = _create_user(client)
    post = _create_post(client, uid, type="certificate", title="My Certificate")
    assert post["type"] == "certificate"


# ---------- TC-POST-030: 进入 pending_review 状态 ----------
def test_status_transition_draft_to_pending_review(client):
    uid = _create_user(client)
    post = _create_post(client, uid)
    resp = client.patch(f"/api/posts/{post['id']}", json={"status": "pending_review"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "pending_review"


# ---------- TC-POST-031: pending_review → published ----------
def test_status_transition_pending_review_to_published(client):
    uid = _create_user(client)
    post = _create_post(client, uid)
    client.patch(f"/api/posts/{post['id']}", json={"status": "pending_review"})
    resp = client.patch(f"/api/posts/{post['id']}", json={"status": "published"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "published"


# ---------- TC-POST-032: pending_review → rejected ----------
def test_status_transition_pending_review_to_rejected(client):
    uid = _create_user(client)
    post = _create_post(client, uid)
    client.patch(f"/api/posts/{post['id']}", json={"status": "pending_review"})
    resp = client.patch(f"/api/posts/{post['id']}", json={"status": "rejected"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "rejected"


# ---------- TC-POST-033: rejected → draft (resubmit) ----------
def test_status_transition_rejected_to_draft(client):
    uid = _create_user(client)
    post = _create_post(client, uid)
    client.patch(f"/api/posts/{post['id']}", json={"status": "pending_review"})
    client.patch(f"/api/posts/{post['id']}", json={"status": "rejected"})
    resp = client.patch(f"/api/posts/{post['id']}", json={"status": "draft"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "draft"


# ---------- published is terminal ----------
def test_published_is_terminal_state(client):
    uid = _create_user(client)
    post = _create_post(client, uid, status="published")
    resp = client.patch(f"/api/posts/{post['id']}", json={"status": "draft"})
    assert resp.status_code == 422


# ---------- TC-POST-060: 更新标题和内容 ----------
def test_update_title_and_content(client):
    uid = _create_user(client)
    post = _create_post(client, uid, content="# Original")
    resp = client.patch(f"/api/posts/{post['id']}", json={
        "title": "Updated Title",
        "content": "# Updated Content",
    })
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
    resp = client.patch(f"/api/posts/{post['id']}", json={"status": "published"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "published"


# ---------- TC-POST-073: public → private ----------
def test_change_visibility_public_to_private(client):
    uid = _create_user(client)
    post = _create_post(client, uid)
    resp = client.patch(f"/api/posts/{post['id']}", json={"visibility": "private"})
    assert resp.status_code == 200
    assert resp.json()["visibility"] == "private"


# ---------- TC-POST-074: private → public ----------
def test_change_visibility_private_to_public(client):
    uid = _create_user(client)
    post = _create_post(client, uid, visibility="private")
    resp = client.patch(f"/api/posts/{post['id']}", json={"visibility": "public"})
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
    del_resp = client.delete(f"/api/posts/{post['id']}")
    assert del_resp.status_code == 204

    get_resp = client.get(f"/api/posts/{post['id']}")
    assert get_resp.status_code == 404

    list_resp = client.get("/api/posts")
    titles = [p["title"] for p in list_resp.json()["items"]]
    assert "Delete Me" not in titles


# ---------- list posts filters ----------
def test_list_posts_filter_by_type_and_status(client):
    uid = _create_user(client)
    _create_post(client, uid, title="A", type="general", status="published")
    _create_post(client, uid, title="B", type="for_category", status="published")
    _create_post(client, uid, title="C", type="for_category", status="draft")

    resp = client.get("/api/posts?type=for_category&status=published")
    assert resp.status_code == 200
    items = resp.json()["items"]
    titles = {p["title"] for p in items}
    assert "B" in titles
    assert "A" not in titles
    assert "C" not in titles


def test_list_posts_filter_by_tags(client):
    uid = _create_user(client)
    _create_post(client, uid, title="Tagged", status="published", tags=["find-idea", "demo"])
    _create_post(client, uid, title="Other", status="published", tags=["other"])

    resp = client.get("/api/posts?status=published&tags=find-idea")
    assert resp.status_code == 200
    titles = {p["title"] for p in resp.json()["items"]}
    assert "Tagged" in titles
    assert "Other" not in titles


def test_list_posts_filter_by_category_id(client):
    organizer_id = _create_user(client, username="org", role="organizer")
    author_id = _create_user(client, username="author2", role="participant")
    post = _create_post(client, author_id, title="Submission", type="for_category", status="published")
    cat_resp = client.post(
        "/api/categories",
        json={
            "name": "Hackathon",
            "description": "Test category",
            "type": "competition",
            "status": "published",
        },
        headers={"X-User-Id": str(organizer_id)},
    )
    assert cat_resp.status_code == 201
    category_id = cat_resp.json()["id"]
    link_resp = client.post(f"/api/categories/{category_id}/posts", json={"post_id": post["id"]})
    assert link_resp.status_code == 201

    resp = client.get(f"/api/posts?category_id={category_id}&type=for_category&status=published")
    assert resp.status_code == 200
    titles = {p["title"] for p in resp.json()["items"]}
    assert "Submission" in titles


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
    resp = client.post("/api/posts", json={"title": "No Auth"})
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
    resp = client.get("/api/posts")
    assert resp.status_code == 200
    assert resp.json()["total"] == 2


# ---------- Additional: get nonexistent post ----------
def test_get_nonexistent_post(client):
    resp = client.get("/api/posts/9999")
    assert resp.status_code == 404
