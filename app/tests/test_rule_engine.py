"""Declarative Rule Engine tests — Phase 7

Covers:
- TC-ENGINE-001: time_window — start not reached
- TC-ENGINE-002: time_window — deadline passed
- TC-ENGINE-003: count — count satisfied
- TC-ENGINE-004: count — count not satisfied
- TC-ENGINE-005: exists — entity exists passes
- TC-ENGINE-006: exists — entity not exists rejects
- TC-ENGINE-007: exists — require=false passes when not exists
- TC-ENGINE-008: field_match — field matches
- TC-ENGINE-009: resource_format — format matches
- TC-ENGINE-010: resource_required — min_count and format satisfied
- TC-ENGINE-011: aggregate — all groups satisfy
- TC-ENGINE-020: fixed field auto-expansion
- TC-ENGINE-021: fixed field expanded checks execute before custom
- TC-ENGINE-022: pure checks (no fixed fields)
- TC-ENGINE-030: multi-rule AND logic
- TC-ENGINE-031: multi-rule with mixed fixed+checks
- TC-ENGINE-040: post-hook action executes
- TC-ENGINE-041: post-hook condition not met → action skipped
- TC-ENGINE-042: post-hook failure doesn't rollback main op
- TC-ENGINE-050: on_fail=deny rejects
- TC-ENGINE-051: on_fail=warn allows but returns warning
- TC-ENGINE-060: empty checks → no constraint
- TC-ENGINE-061: no rules → no constraint
"""


def _create_user(client, username="eng_user", role="organizer"):
    resp = client.post("/api/users", json={
        "username": username,
        "email": f"{username}@example.com",
        "role": role,
    })
    return resp.json()["id"]


def _create_event(client, uid, name="Test Event"):
    resp = client.post("/api/events", json={
        "name": name,
        "description": f"Desc of {name}",
        "type": "competition",
    }, headers={"X-User-Id": str(uid)})
    return resp.json()["id"]


def _create_rule(client, uid, **fields):
    body = {
        "name": fields.pop("name", "Test Rule"),
        "description": fields.pop("description", "Test rule desc"),
    }
    body.update(fields)
    resp = client.post("/api/rules", json=body, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201, f"Rule creation failed: {resp.json()}"
    return resp.json()["id"]


def _create_post(client, uid, title="Test Submission"):
    resp = client.post("/api/posts", json={
        "title": title,
    }, headers={"X-User-Id": str(uid)})
    return resp.json()["id"]


def _create_group(client, uid, name="Team"):
    resp = client.post("/api/groups", json={
        "name": name,
        "description": f"Desc of {name}",
        "visibility": "public",
        "require_approval": False,
    }, headers={"X-User-Id": str(uid)})
    return resp.json()["id"]


def _create_resource(client, uid, filename="proposal.pdf"):
    resp = client.post("/api/resources", json={
        "filename": filename,
        "description": "Test resource",
        "url": f"https://example.com/{filename}",
    }, headers={"X-User-Id": str(uid)})
    return resp.json()["id"]


def _link_rule(client, cat_id, rule_id, priority=0):
    resp = client.post(f"/api/events/{cat_id}/rules", json={
        "rule_id": rule_id, "priority": priority,
    })
    assert resp.status_code == 201


def _submit_post(client, cat_id, post_id):
    return client.post(f"/api/events/{cat_id}/posts", json={
        "post_id": post_id, "relation_type": "submission",
    })


# --- 17.1 Condition type coverage ---

def test_time_window_start_not_reached(client):
    """TC-ENGINE-001: time_window — start in the future → rejected."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    rule_id = _create_rule(client, uid, checks=[{
        "trigger": "create_relation(event_post)",
        "phase": "pre",
        "condition": {
            "type": "time_window",
            "params": {"start": "2030-01-01T00:00:00Z", "end": None},
        },
        "on_fail": "deny",
        "message": "not yet open",
    }])
    _link_rule(client, cat_id, rule_id)
    post_id = _create_post(client, uid)
    resp = _submit_post(client, cat_id, post_id)
    assert resp.status_code == 422
    assert "not yet open" in resp.json()["detail"]


def test_time_window_deadline_passed(client):
    """TC-ENGINE-002: time_window — end in the past → rejected."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    rule_id = _create_rule(client, uid, checks=[{
        "trigger": "create_relation(event_post)",
        "phase": "pre",
        "condition": {
            "type": "time_window",
            "params": {"start": None, "end": "2020-01-01T00:00:00Z"},
        },
        "on_fail": "deny",
        "message": "deadline passed",
    }])
    _link_rule(client, cat_id, rule_id)
    post_id = _create_post(client, uid)
    resp = _submit_post(client, cat_id, post_id)
    assert resp.status_code == 422
    assert "deadline passed" in resp.json()["detail"]


def test_count_condition_satisfied(client, db_session):
    """TC-ENGINE-003: count — group has enough members → passes."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    group_id = _create_group(client, uid)
    # Add 3 members
    for i in range(3):
        m_uid = _create_user(client, f"member{i}")
        client.post(f"/api/groups/{group_id}/members", json={"user_id": m_uid})
    # Register group to event
    client.post(f"/api/events/{cat_id}/groups", json={"group_id": group_id})
    # Rule: team must have >= 2 accepted members
    rule_id = _create_rule(client, uid, checks=[{
        "trigger": "create_relation(event_post)",
        "phase": "pre",
        "condition": {
            "type": "count",
            "params": {
                "entity": "group_user",
                "scope": "group",
                "filter": {"status": "accepted"},
                "op": ">=",
                "value": 2,
            },
        },
        "on_fail": "deny",
        "message": "Not enough team members",
    }])
    _link_rule(client, cat_id, rule_id)
    post_id = _create_post(client, uid)
    from app.services.rule_engine import run_pre_checks
    # Should pass with 3 members
    warnings = run_pre_checks(
        db_session,
        trigger="create_relation(event_post)",
        event_id=cat_id,
        context={"user_id": uid, "post_id": post_id, "group_id": group_id},
    )
    assert len(warnings) == 0


def test_count_condition_not_satisfied(client, db_session):
    """TC-ENGINE-004: count — group has too few members → rejected."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    group_id = _create_group(client, uid)
    # Only 1 member (the creator doesn't auto-join)
    m_uid = _create_user(client, "lone_member")
    client.post(f"/api/groups/{group_id}/members", json={"user_id": m_uid})
    # Rule: team must have >= 3 accepted members
    rule_id = _create_rule(client, uid, checks=[{
        "trigger": "create_relation(event_post)",
        "phase": "pre",
        "condition": {
            "type": "count",
            "params": {
                "entity": "group_user",
                "scope": "group",
                "filter": {"status": "accepted"},
                "op": ">=",
                "value": 3,
            },
        },
        "on_fail": "deny",
        "message": "Not enough team members",
    }])
    _link_rule(client, cat_id, rule_id)
    from app.services.rule_engine import run_pre_checks, RuleCheckError
    import pytest
    with pytest.raises(RuleCheckError, match="Not enough team members"):
        run_pre_checks(
            db_session,
            trigger="create_relation(event_post)",
            event_id=cat_id,
            context={"user_id": uid, "post_id": 1, "group_id": group_id},
        )


def test_exists_entity_present_passes(client):
    """TC-ENGINE-005: exists — post has resources → passes."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    post_id = _create_post(client, uid)
    resource_id = _create_resource(client, uid)
    client.post(f"/api/posts/{post_id}/resources", json={
        "resource_id": resource_id, "display_type": "attachment",
    })
    rule_id = _create_rule(client, uid, checks=[{
        "trigger": "create_relation(event_post)",
        "phase": "pre",
        "condition": {
            "type": "exists",
            "params": {"entity": "post_resource", "scope": "post", "require": True},
        },
        "on_fail": "deny",
        "message": "Post must have at least one resource",
    }])
    _link_rule(client, cat_id, rule_id)
    resp = _submit_post(client, cat_id, post_id)
    assert resp.status_code == 201


def test_exists_entity_absent_rejects(client):
    """TC-ENGINE-006: exists — post has no resources → rejected."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    post_id = _create_post(client, uid)
    rule_id = _create_rule(client, uid, checks=[{
        "trigger": "create_relation(event_post)",
        "phase": "pre",
        "condition": {
            "type": "exists",
            "params": {"entity": "post_resource", "scope": "post", "require": True},
        },
        "on_fail": "deny",
        "message": "Post must have at least one resource",
    }])
    _link_rule(client, cat_id, rule_id)
    resp = _submit_post(client, cat_id, post_id)
    assert resp.status_code == 422
    assert "Post must have at least one resource" in resp.json()["detail"]


def test_exists_require_false_passes_when_absent(client):
    """TC-ENGINE-007: exists — require=false, user has no submission → passes."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    post_id = _create_post(client, uid)
    rule_id = _create_rule(client, uid, checks=[{
        "trigger": "create_relation(event_post)",
        "phase": "pre",
        "condition": {
            "type": "exists",
            "params": {
                "entity": "event_post",
                "scope": "user",
                "filter": {"relation_type": "submission"},
                "require": False,
            },
        },
        "on_fail": "deny",
        "message": "User already has a submission",
    }])
    _link_rule(client, cat_id, rule_id)
    # First submission → no existing submission → require=false → passes
    resp = _submit_post(client, cat_id, post_id)
    assert resp.status_code == 201


def test_field_match_condition(client):
    """TC-ENGINE-008: field_match — event status == published."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    h = {"X-User-Id": str(uid)}
    # Publish event
    client.patch(f"/api/events/{cat_id}", json={"status": "published"}, headers=h)
    rule_id = _create_rule(client, uid, checks=[{
        "trigger": "create_relation(event_post)",
        "phase": "pre",
        "condition": {
            "type": "field_match",
            "params": {
                "entity": "event",
                "target": "$target",
                "field": "status",
                "op": "==",
                "value": "published",
            },
        },
        "on_fail": "deny",
        "message": "Event must be published",
    }])
    _link_rule(client, cat_id, rule_id)
    post_id = _create_post(client, uid)
    resp = _submit_post(client, cat_id, post_id)
    assert resp.status_code == 201


def test_resource_format_condition(client):
    """TC-ENGINE-009: resource_format — pdf and zip pass."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    post_id = _create_post(client, uid)
    r1 = _create_resource(client, uid, "proposal.pdf")
    r2 = _create_resource(client, uid, "code.zip")
    client.post(f"/api/posts/{post_id}/resources", json={"resource_id": r1, "display_type": "attachment"})
    client.post(f"/api/posts/{post_id}/resources", json={"resource_id": r2, "display_type": "attachment"})
    rule_id = _create_rule(client, uid, checks=[{
        "trigger": "create_relation(event_post)",
        "phase": "pre",
        "condition": {
            "type": "resource_format",
            "params": {"formats": ["pdf", "zip"]},
        },
        "on_fail": "deny",
        "message": "Invalid resource format",
    }])
    _link_rule(client, cat_id, rule_id)
    resp = _submit_post(client, cat_id, post_id)
    assert resp.status_code == 201


def test_resource_required_condition(client):
    """TC-ENGINE-010: resource_required — min_count=2 pdf resources."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    post_id = _create_post(client, uid)
    r1 = _create_resource(client, uid, "doc1.pdf")
    r2 = _create_resource(client, uid, "doc2.pdf")
    client.post(f"/api/posts/{post_id}/resources", json={"resource_id": r1, "display_type": "attachment"})
    client.post(f"/api/posts/{post_id}/resources", json={"resource_id": r2, "display_type": "attachment"})
    rule_id = _create_rule(client, uid, checks=[{
        "trigger": "create_relation(event_post)",
        "phase": "pre",
        "condition": {
            "type": "resource_required",
            "params": {"min_count": 2, "formats": ["pdf"]},
        },
        "on_fail": "deny",
        "message": "Need at least 2 PDF resources",
    }])
    _link_rule(client, cat_id, rule_id)
    resp = _submit_post(client, cat_id, post_id)
    assert resp.status_code == 201


def test_aggregate_condition(client, db_session):
    """TC-ENGINE-011: aggregate — all groups have >= 2 members."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    g1 = _create_group(client, uid, "Team1")
    g2 = _create_group(client, uid, "Team2")
    # Add 2 members to each group
    for g in [g1, g2]:
        for i in range(2):
            m = _create_user(client, f"agg_m_{g}_{i}")
            client.post(f"/api/groups/{g}/members", json={"user_id": m})
    # Register both to event
    client.post(f"/api/events/{cat_id}/groups", json={"group_id": g1})
    client.post(f"/api/events/{cat_id}/groups", json={"group_id": g2})
    rule_id = _create_rule(client, uid, checks=[{
        "trigger": "create_relation(event_post)",
        "phase": "pre",
        "condition": {
            "type": "aggregate",
            "params": {
                "entity": "group_user",
                "scope": "each_group_in_category",
                "filter": {"status": "accepted"},
                "field": "user_id",
                "agg_func": "count",
                "op": ">=",
                "value": 2,
            },
        },
        "on_fail": "deny",
        "message": "All teams must have 2+ members",
    }])
    _link_rule(client, cat_id, rule_id)
    from app.services.rule_engine import run_pre_checks
    warnings = run_pre_checks(
        db_session, trigger="create_relation(event_post)",
        event_id=cat_id, context={"user_id": uid},
    )
    assert len(warnings) == 0


# --- 17.2 Fixed field expansion ---

def test_fixed_field_auto_expansion(client):
    """TC-ENGINE-020: max_submissions=2 auto-expands to count check."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    rule_id = _create_rule(client, uid, max_submissions=2)
    _link_rule(client, cat_id, rule_id)
    # Submit 2 posts
    for i in range(2):
        post_id = _create_post(client, uid, f"Sub {i}")
        resp = _submit_post(client, cat_id, post_id)
        assert resp.status_code == 201
    # 3rd submission rejected
    post_id = _create_post(client, uid, "Sub 3")
    resp = _submit_post(client, cat_id, post_id)
    assert resp.status_code == 422
    assert "Max submissions" in resp.json()["detail"]


def test_fixed_field_expanded_before_custom(client):
    """TC-ENGINE-021: Fixed field checks execute before custom checks."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    # Rule: max_submissions=1 (fixed) + resource_required (custom)
    rule_id = _create_rule(client, uid, max_submissions=1, checks=[{
        "trigger": "create_relation(event_post)",
        "phase": "pre",
        "condition": {
            "type": "resource_required",
            "params": {"min_count": 1},
        },
        "on_fail": "deny",
        "message": "Post must have resource",
    }])
    _link_rule(client, cat_id, rule_id)
    # First submission (no resource) → resource_required will fail
    p1 = _create_post(client, uid, "First")
    resp1 = _submit_post(client, cat_id, p1)
    # resource_required check fails because no resource attached
    assert resp1.status_code == 422
    assert "Post must have resource" in resp1.json()["detail"]

    # Add resource and submit again
    r = _create_resource(client, uid)
    client.post(f"/api/posts/{p1}/resources", json={"resource_id": r, "display_type": "attachment"})
    resp2 = _submit_post(client, cat_id, p1)
    assert resp2.status_code == 201

    # Second submission → max_submissions fires first (expanded before custom)
    p2 = _create_post(client, uid, "Second")
    r2 = _create_resource(client, uid, "doc2.pdf")
    client.post(f"/api/posts/{p2}/resources", json={"resource_id": r2, "display_type": "attachment"})
    resp3 = _submit_post(client, cat_id, p2)
    assert resp3.status_code == 422
    assert "Max submissions" in resp3.json()["detail"]


def test_pure_checks_no_fixed_fields(client):
    """TC-ENGINE-022: Rule with only checks, no fixed fields."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    rule_id = _create_rule(client, uid, checks=[{
        "trigger": "create_relation(event_post)",
        "phase": "pre",
        "condition": {
            "type": "exists",
            "params": {"entity": "post_resource", "scope": "post", "require": True},
        },
        "on_fail": "deny",
        "message": "Attach a resource first",
    }])
    _link_rule(client, cat_id, rule_id)
    post_id = _create_post(client, uid)
    # No resource → rejected
    resp = _submit_post(client, cat_id, post_id)
    assert resp.status_code == 422
    # Add resource → passes
    r = _create_resource(client, uid)
    client.post(f"/api/posts/{post_id}/resources", json={"resource_id": r, "display_type": "attachment"})
    resp2 = _submit_post(client, cat_id, post_id)
    assert resp2.status_code == 201


# --- 17.3 Multi-rule merge ---

def test_multi_rule_and_logic(client):
    """TC-ENGINE-030: Two rules, both must pass (AND)."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    # Rule A: resource_required
    rule_a = _create_rule(client, uid, name="Rule A", checks=[{
        "trigger": "create_relation(event_post)",
        "phase": "pre",
        "condition": {"type": "resource_required", "params": {"min_count": 1}},
        "on_fail": "deny",
        "message": "Need resource",
    }])
    # Rule B: max_submissions=1 via fixed field
    rule_b = _create_rule(client, uid, name="Rule B", max_submissions=1)
    _link_rule(client, cat_id, rule_a, priority=0)
    _link_rule(client, cat_id, rule_b, priority=1)

    post_id = _create_post(client, uid)
    r = _create_resource(client, uid)
    client.post(f"/api/posts/{post_id}/resources", json={"resource_id": r, "display_type": "attachment"})

    # First submission: passes both rules
    resp = _submit_post(client, cat_id, post_id)
    assert resp.status_code == 201

    # Second submission: Rule B rejects (max_submissions=1)
    p2 = _create_post(client, uid, "Second")
    r2 = _create_resource(client, uid, "doc2.pdf")
    client.post(f"/api/posts/{p2}/resources", json={"resource_id": r2, "display_type": "attachment"})
    resp2 = _submit_post(client, cat_id, p2)
    assert resp2.status_code == 422


def test_multi_rule_mixed_fixed_and_checks(client):
    """TC-ENGINE-031: Rule A (fixed: submission_format) + Rule B (checks: resource_required)."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    # Rule A: submission_format=["pdf"] via fixed field
    rule_a = _create_rule(client, uid, name="Format Rule", submission_format=["pdf"])
    # Rule B: resource_required via checks
    rule_b = _create_rule(client, uid, name="Resource Rule", checks=[{
        "trigger": "create_relation(event_post)",
        "phase": "pre",
        "condition": {"type": "resource_required", "params": {"min_count": 1}},
        "on_fail": "deny",
        "message": "Need at least one resource",
    }])
    _link_rule(client, cat_id, rule_a)
    _link_rule(client, cat_id, rule_b)

    post_id = _create_post(client, uid)
    # Attach a PDF resource
    r = _create_resource(client, uid, "report.pdf")
    client.post(f"/api/posts/{post_id}/resources", json={"resource_id": r, "display_type": "attachment"})
    # Should pass both rules
    resp = _submit_post(client, cat_id, post_id)
    assert resp.status_code == 201


# --- 17.4 Post-hook execution ---

def test_post_hook_executes(client):
    """TC-ENGINE-040: post phase action executes on event close."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    h = {"X-User-Id": str(uid)}
    # Create rule with compute_ranking post-hook on event close
    rule_id = _create_rule(client, uid, checks=[{
        "trigger": "update_content(event.status)",
        "phase": "post",
        "condition": {
            "type": "field_match",
            "params": {"entity": "event", "target": "$current", "field": "status", "op": "==", "value": "closed"},
        },
        "action": "compute_ranking",
        "action_params": {"source_field": "average_rating", "order": "desc", "output_tag_prefix": "rank_"},
        "message": "Compute final ranking",
    }])
    _link_rule(client, cat_id, rule_id)

    # Create 2 posts with ratings
    p1 = _create_post(client, uid, "Post A")
    p2 = _create_post(client, uid, "Post B")
    _submit_post(client, cat_id, p1)
    _submit_post(client, cat_id, p2)

    # Add ratings
    client.post(f"/api/posts/{p1}/ratings", json={
        "type": "rating", "value": {"Quality": 90},
    }, headers=h)
    client.post(f"/api/posts/{p2}/ratings", json={
        "type": "rating", "value": {"Quality": 80},
    }, headers=h)

    # Transition: draft → published → closed
    client.patch(f"/api/events/{cat_id}", json={"status": "published"}, headers=h)
    client.patch(f"/api/events/{cat_id}", json={"status": "closed"}, headers=h)

    # Verify ranking tags were applied
    post_a = client.get(f"/api/posts/{p1}", headers=h).json()
    post_b = client.get(f"/api/posts/{p2}", headers=h).json()
    assert "rank_1" in (post_a.get("tags") or [])
    assert "rank_2" in (post_b.get("tags") or [])


def test_post_hook_condition_not_met(client):
    """TC-ENGINE-041: post-hook condition not met → action skipped."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    h = {"X-User-Id": str(uid)}
    # Rule: compute_ranking only on closed
    rule_id = _create_rule(client, uid, checks=[{
        "trigger": "update_content(event.status)",
        "phase": "post",
        "condition": {
            "type": "field_match",
            "params": {"entity": "event", "target": "$current", "field": "status", "op": "==", "value": "closed"},
        },
        "action": "compute_ranking",
        "action_params": {"source_field": "average_rating", "order": "desc", "output_tag_prefix": "rank_"},
        "message": "Compute ranking",
    }])
    _link_rule(client, cat_id, rule_id)

    p1 = _create_post(client, uid, "Post A")
    _submit_post(client, cat_id, p1)
    client.post(f"/api/posts/{p1}/ratings", json={
        "type": "rating", "value": {"Quality": 90},
    }, headers=h)

    # Transition to published (NOT closed) → hook should NOT fire
    client.patch(f"/api/events/{cat_id}", json={"status": "published"}, headers=h)
    post_a = client.get(f"/api/posts/{p1}", headers=h).json()
    # No ranking tags should be present
    tags = post_a.get("tags") or []
    assert not any(t.startswith("rank_") for t in tags)


def test_post_hook_failure_no_rollback(client):
    """TC-ENGINE-042: post-hook error doesn't rollback main operation."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    h = {"X-User-Id": str(uid)}
    # Rule: compute_ranking on close (no rated posts → no rankings, but shouldn't fail)
    rule_id = _create_rule(client, uid, checks=[{
        "trigger": "update_content(event.status)",
        "phase": "post",
        "condition": {
            "type": "field_match",
            "params": {"entity": "event", "target": "$current", "field": "status", "op": "==", "value": "closed"},
        },
        "action": "compute_ranking",
        "action_params": {"source_field": "average_rating", "order": "desc"},
        "message": "Compute ranking",
    }])
    _link_rule(client, cat_id, rule_id)

    # Close event (no posts, no ratings)
    client.patch(f"/api/events/{cat_id}", json={"status": "published"}, headers=h)
    resp = client.patch(f"/api/events/{cat_id}", json={"status": "closed"}, headers=h)
    # Main operation succeeds regardless
    assert resp.status_code == 200
    assert resp.json()["status"] == "closed"


# --- 17.5 on_fail behavior ---

def test_on_fail_deny_rejects(client):
    """TC-ENGINE-050: on_fail=deny rejects the operation."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    rule_id = _create_rule(client, uid, checks=[{
        "trigger": "create_relation(event_post)",
        "phase": "pre",
        "condition": {
            "type": "time_window",
            "params": {"start": "2030-01-01T00:00:00Z", "end": None},
        },
        "on_fail": "deny",
        "message": "Submissions not open yet",
    }])
    _link_rule(client, cat_id, rule_id)
    post_id = _create_post(client, uid)
    resp = _submit_post(client, cat_id, post_id)
    assert resp.status_code == 422
    assert "Submissions not open yet" in resp.json()["detail"]


def test_on_fail_warn_allows_with_warning(client):
    """TC-ENGINE-051: on_fail=warn allows operation."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    rule_id = _create_rule(client, uid, checks=[{
        "trigger": "create_relation(event_post)",
        "phase": "pre",
        "condition": {
            "type": "time_window",
            "params": {"start": "2030-01-01T00:00:00Z", "end": None},
        },
        "on_fail": "warn",
        "message": "Submissions recommended after official start",
    }])
    _link_rule(client, cat_id, rule_id)
    post_id = _create_post(client, uid)
    # warn → operation should succeed (submission still created)
    resp = _submit_post(client, cat_id, post_id)
    assert resp.status_code == 201


# --- 17.6 Empty/no rules ---

def test_empty_checks_no_constraint(client):
    """TC-ENGINE-060: Rule with empty checks → no constraint."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    rule_id = _create_rule(client, uid, checks=[])
    _link_rule(client, cat_id, rule_id)
    post_id = _create_post(client, uid)
    resp = _submit_post(client, cat_id, post_id)
    assert resp.status_code == 201


def test_no_rules_no_constraint(client):
    """TC-ENGINE-061: Event with no rules → no constraint."""
    uid = _create_user(client)
    cat_id = _create_event(client, uid)
    post_id = _create_post(client, uid)
    resp = _submit_post(client, cat_id, post_id)
    assert resp.status_code == 201
