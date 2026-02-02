"""Rule API tests — covers TC-RULE-001 through TC-RULE-901"""

AUTH_HEADER = {"X-User-Id": "1"}


def _create_organizer(client):
    """Helper: create an organizer user and return their ID."""
    resp = client.post("/api/users", json={
        "username": "organizer",
        "email": "organizer@example.com",
        "role": "organizer",
    })
    return resp.json()["id"]


# ---------- TC-RULE-001: 创建完整 scoring_criteria 规则 ----------
def test_create_rule_with_scoring_criteria(client):
    uid = _create_organizer(client)
    resp = client.post("/api/rules", json={
        "name": "AI Hackathon Scoring",
        "description": "Scoring rules for AI hackathon",
        "allow_public": False,
        "require_review": True,
        "max_submissions": 1,
        "max_team_size": 5,
        "scoring_criteria": [
            {"name": "Innovation", "weight": 30, "description": "Novelty of the idea"},
            {"name": "Technical Implementation", "weight": 30, "description": "Code quality"},
            {"name": "Practical Value", "weight": 25, "description": "Real-world impact"},
            {"name": "Presentation", "weight": 15, "description": "Demo quality"},
        ],
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "AI Hackathon Scoring"
    assert data["allow_public"] is False
    assert data["require_review"] is True
    assert data["max_submissions"] == 1
    assert data["max_team_size"] == 5
    assert len(data["scoring_criteria"]) == 4
    assert data["created_by"] == uid
    assert "id" in data
    assert "created_at" in data


# ---------- TC-RULE-002: 创建 select-only 规则 ----------
def test_create_select_only_rule(client):
    uid = _create_organizer(client)
    resp = client.post("/api/rules", json={
        "name": "Invite Only Rule",
        "description": "Only selected participants",
        "allow_public": False,
        "require_review": True,
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201
    data = resp.json()
    assert data["allow_public"] is False
    assert data["require_review"] is True


# ---------- TC-RULE-003: 读取已创建的规则 ----------
def test_read_rule(client):
    uid = _create_organizer(client)
    create_resp = client.post("/api/rules", json={
        "name": "Test Rule",
        "description": "A test rule",
        "scoring_criteria": [
            {"name": "Quality", "weight": 60},
            {"name": "Creativity", "weight": 40},
        ],
    }, headers={"X-User-Id": str(uid)})
    rule_id = create_resp.json()["id"]

    resp = client.get(f"/api/rules/{rule_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Test Rule"
    assert data["description"] == "A test rule"
    assert len(data["scoring_criteria"]) == 2
    assert data["scoring_criteria"][0]["name"] == "Quality"
    assert data["scoring_criteria"][0]["weight"] == 60


# ---------- TC-RULE-010: 修改规则配置字段 ----------
def test_update_rule_config(client):
    uid = _create_organizer(client)
    create_resp = client.post("/api/rules", json={
        "name": "Original Rule",
        "description": "Original desc",
        "allow_public": False,
        "max_submissions": 1,
        "max_team_size": 3,
    }, headers={"X-User-Id": str(uid)})
    rule_id = create_resp.json()["id"]

    resp = client.patch(f"/api/rules/{rule_id}", json={
        "allow_public": True,
        "max_submissions": 3,
        "max_team_size": 5,
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 200
    data = resp.json()
    assert data["allow_public"] is True
    assert data["max_submissions"] == 3
    assert data["max_team_size"] == 5


# ---------- TC-RULE-011: 修改 scoring_criteria 权重 ----------
def test_update_scoring_criteria_weights(client):
    uid = _create_organizer(client)
    create_resp = client.post("/api/rules", json={
        "name": "Score Rule",
        "description": "Has scoring",
        "scoring_criteria": [
            {"name": "A", "weight": 30},
            {"name": "B", "weight": 30},
            {"name": "C", "weight": 25},
            {"name": "D", "weight": 15},
        ],
    }, headers={"X-User-Id": str(uid)})
    rule_id = create_resp.json()["id"]

    # Update to equal weights
    resp = client.patch(f"/api/rules/{rule_id}", json={
        "scoring_criteria": [
            {"name": "A", "weight": 25},
            {"name": "B", "weight": 25},
            {"name": "C", "weight": 25},
            {"name": "D", "weight": 25},
        ],
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 200
    data = resp.json()
    weights = [c["weight"] for c in data["scoring_criteria"]]
    assert weights == [25, 25, 25, 25]


# ---------- TC-RULE-020: 删除规则 (soft delete) ----------
def test_delete_rule(client):
    uid = _create_organizer(client)
    create_resp = client.post("/api/rules", json={
        "name": "Delete Me",
        "description": "Will be deleted",
    }, headers={"X-User-Id": str(uid)})
    rule_id = create_resp.json()["id"]

    del_resp = client.delete(f"/api/rules/{rule_id}", headers={"X-User-Id": str(uid)})
    assert del_resp.status_code == 204

    # Rule should no longer be accessible
    get_resp = client.get(f"/api/rules/{rule_id}")
    assert get_resp.status_code == 404

    # Rule should not appear in list
    list_resp = client.get("/api/rules")
    assert list_resp.status_code == 200
    names = [r["name"] for r in list_resp.json()["items"]]
    assert "Delete Me" not in names


# ---------- TC-RULE-900: 未认证用户无法创建规则 ----------
def test_unauthenticated_cannot_create_rule(client):
    """Creating rule with invalid user returns 401.

    Note: In mock mode, requests without X-User-Id header auto-create a mock user.
    This test verifies auth failure by providing an invalid (non-existent) user ID.
    """
    resp = client.post("/api/rules", json={
        "name": "Should Fail",
        "description": "No auth",
    }, headers={"X-User-Id": "99999"})
    assert resp.status_code == 401


# ---------- TC-RULE-901: scoring_criteria 权重之和必须为 100 ----------
def test_scoring_criteria_weights_must_sum_to_100(client):
    uid = _create_organizer(client)
    resp = client.post("/api/rules", json={
        "name": "Bad Weights",
        "description": "Weights do not sum to 100",
        "scoring_criteria": [
            {"name": "A", "weight": 30},
            {"name": "B", "weight": 30},
            {"name": "C", "weight": 20},
        ],
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 422


# ---------- Additional: list rules ----------
def test_list_rules(client):
    uid = _create_organizer(client)
    client.post("/api/rules", json={"name": "R1", "description": "D1"}, headers={"X-User-Id": str(uid)})
    client.post("/api/rules", json={"name": "R2", "description": "D2"}, headers={"X-User-Id": str(uid)})
    resp = client.get("/api/rules")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2


# ---------- Additional: get nonexistent rule ----------
def test_get_nonexistent_rule(client):
    resp = client.get("/api/rules/9999")
    assert resp.status_code == 404


# ---------- Additional: update nonexistent rule ----------
def test_update_nonexistent_rule(client):
    uid = _create_organizer(client)
    resp = client.patch("/api/rules/9999", json={"name": "Nothing"}, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 404


# ---------- Additional: scoring_criteria weights validation on update ----------
def test_update_scoring_criteria_bad_weights(client):
    uid = _create_organizer(client)
    create_resp = client.post("/api/rules", json={
        "name": "Score Rule",
        "description": "Has scoring",
        "scoring_criteria": [
            {"name": "A", "weight": 50},
            {"name": "B", "weight": 50},
        ],
    }, headers={"X-User-Id": str(uid)})
    rule_id = create_resp.json()["id"]

    resp = client.patch(f"/api/rules/{rule_id}", json={
        "scoring_criteria": [
            {"name": "A", "weight": 50},
            {"name": "B", "weight": 40},
        ],
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 422
