"""Closure Rule Enforcement tests — Phase 8

Tests that verify rule engine behavior when a event transitions to "closed" status.
Post-phase actions (compute_ranking, flag_disqualified, award_certificate) fire after
the status update. Pre-phase checks validate conditions before allowing the transition.

Covers:
- TC-CLOSE-001: Pre-phase warn on close — warn condition allows close
- TC-CLOSE-002: Pre-phase deny on close — deny condition blocks close
- TC-CLOSE-010: flag_disqualified — teams below min_team_size are flagged
- TC-CLOSE-020: compute_ranking — posts ranked by average_rating
- TC-CLOSE-022: Null rating excluded from ranking
- TC-CLOSE-030: award_certificate — certificate posts created for ranked submissions
- TC-CLOSE-040: Full closure flow (flag + rank + award in sequence)
- TC-CLOSE-900: Non-closed status transition does not trigger post hooks
- TC-CLOSE-901: No rules attached — close succeeds with no side effects
- TC-CLOSE-902: Post-hook failure does not rollback main operation
"""


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _create_user(client, username, role="organizer"):
    resp = client.post("/api/users", json={
        "username": username,
        "email": f"{username}@example.com",
        "role": role,
    })
    assert resp.status_code == 201, f"User creation failed: {resp.text}"
    return resp.json()["id"]


def _create_event(client, uid, name="Closure Test"):
    """Create a event and advance it to 'published' status."""
    resp = client.post("/api/events", json={
        "name": name,
        "description": "test",
        "type": "competition",
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201, f"Event creation failed: {resp.text}"
    cat_id = resp.json()["id"]
    pub_resp = client.patch(
        f"/api/events/{cat_id}",
        json={"status": "published"},
        headers={"X-User-Id": str(uid)},
    )
    assert pub_resp.status_code == 200, f"Event publish failed: {pub_resp.text}"
    return cat_id


def _create_rule(client, uid, checks=None, **fields):
    body = {
        "name": fields.pop("name", "Closure Rule"),
        "description": fields.pop("description", "test"),
    }
    if checks is not None:
        body["checks"] = checks
    body.update(fields)
    resp = client.post("/api/rules", json=body, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201, f"Rule creation failed: {resp.json()}"
    return resp.json()["id"]


def _link_rule(client, cat_id, rule_id):
    resp = client.post(f"/api/events/{cat_id}/rules", json={"rule_id": rule_id})
    assert resp.status_code == 201, f"Link rule failed: {resp.text}"


def _create_group(client, uid, name="Closure Team"):
    resp = client.post("/api/groups", json={
        "name": name,
        "description": "test",
        "require_approval": False,
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201, f"Group creation failed: {resp.text}"
    return resp.json()["id"]


def _add_member(client, gid, uid):
    resp = client.post(f"/api/groups/{gid}/members", json={
        "user_id": uid,
        "role": "member",
    })
    return resp


def _create_post(client, uid, title="Submission", post_type="proposal"):
    resp = client.post("/api/posts", json={
        "title": title,
        "type": post_type,
        "status": "draft",
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201, f"Post creation failed: {resp.text}"
    return resp.json()["id"]


def _submit_to_category(client, cat_id, post_id):
    resp = client.post(f"/api/events/{cat_id}/posts", json={
        "post_id": post_id,
        "relation_type": "submission",
    })
    assert resp.status_code == 201, f"Submit to event failed: {resp.text}"
    return resp.json()


def _register_group(client, cat_id, gid):
    resp = client.post(f"/api/events/{cat_id}/groups", json={
        "group_id": gid,
    })
    assert resp.status_code == 201, f"Register group failed: {resp.text}"


def _rate_post(client, post_id, user_id, scores):
    """Rate a post via the interactions API.

    ``scores`` is a dict of criterion->score, e.g. {"Quality": 90}.
    """
    resp = client.post(
        f"/api/posts/{post_id}/ratings",
        json={"type": "rating", "value": scores},
        headers={"X-User-Id": str(user_id)},
    )
    return resp


def _close_category(client, cat_id, uid):
    return client.patch(
        f"/api/events/{cat_id}",
        json={"status": "closed"},
        headers={"X-User-Id": str(uid)},
    )


def _get_post(client, post_id, uid):
    """Read a post.  Uses ``uid`` as the X-User-Id header.

    NOTE: Draft posts are only visible to their creator.  Pass the
    post creator's uid to read a draft post.
    """
    resp = client.get(
        f"/api/posts/{post_id}",
        headers={"X-User-Id": str(uid)},
    )
    assert resp.status_code == 200, (
        f"GET /api/posts/{post_id} as uid={uid} failed: {resp.status_code} {resp.text}"
    )
    return resp.json()


# ---------------------------------------------------------------------------
# TC-CLOSE-001: Pre-phase warn on close
# ---------------------------------------------------------------------------

def test_close_001_pre_phase_warn_allows_close(client):
    """A pre-phase check with on_fail=warn should allow event close to proceed."""
    org = _create_user(client, "close001_org")
    cat_id = _create_event(client, org, "Warn Close Test")

    rule_id = _create_rule(client, org, checks=[{
        "trigger": "update_content(event.status)",
        "phase": "pre",
        "condition": {
            "type": "field_match",
            "params": {
                "entity": "event",
                "target": "$current",
                "field": "status",
                "op": "==",
                "value": "closed",
            },
        },
        "on_fail": "warn",
        "message": "Event is being closed, proceed with caution",
    }])
    _link_rule(client, cat_id, rule_id)

    resp = _close_category(client, cat_id, org)
    assert resp.status_code == 200, f"Close failed unexpectedly: {resp.text}"
    assert resp.json()["status"] == "closed"


# ---------------------------------------------------------------------------
# TC-CLOSE-002: Pre-phase deny on close
# ---------------------------------------------------------------------------

def test_close_002_pre_phase_deny_blocks_close(client, db_session):
    """A pre-phase check with on_fail=deny should block event close.

    The rule uses a count condition: at least 1 submission must exist.
    We register a group but do not submit anything, so the check fails.
    """
    org = _create_user(client, "close002_org")
    cat_id = _create_event(client, org, "Deny Close Test")

    # Rule: require at least 1 submission before closing
    rule_id = _create_rule(client, org, checks=[{
        "trigger": "update_content(event.status)",
        "phase": "pre",
        "condition": {
            "type": "count",
            "params": {
                "entity": "event_post",
                "scope": "event",
                "filter": {"relation_type": "submission"},
                "op": ">=",
                "value": 1,
            },
        },
        "on_fail": "deny",
        "message": "Cannot close: no submissions received",
    }])
    _link_rule(client, cat_id, rule_id)

    # Register a group but submit nothing
    member = _create_user(client, "close002_member", role="participant")
    gid = _create_group(client, org, "Empty Team")
    _add_member(client, gid, member)
    _register_group(client, cat_id, gid)

    # Attempt close -- should be rejected
    resp = _close_category(client, cat_id, org)
    assert resp.status_code == 422, f"Close should have been blocked: {resp.text}"
    assert "no submissions" in resp.json()["detail"].lower()


# ---------------------------------------------------------------------------
# TC-CLOSE-010: flag_disqualified on close
# ---------------------------------------------------------------------------

def test_close_010_flag_disqualified_team_too_small(client):
    """Teams below min_team_size should have their submission posts flagged.

    Setup:
    - Team A: 3 accepted members (qualifies, min_team_size=2)
    - Team B: 2 accepted members (qualifies)
    - Team C: 1 accepted member (disqualified)

    The rule sets min_team_size=2 which auto-expands to a pre-phase count check on
    event_post submissions.  To avoid blocking submissions, we submit posts BEFORE
    linking the rule to the event.
    """
    org = _create_user(client, "close010_org")
    cat_id = _create_event(client, org, "Flag DQ Test")

    # --- Team A: 3 members ---
    leader_a = _create_user(client, "close010_leader_a", role="participant")
    gid_a = _create_group(client, leader_a, "Team A (3)")
    _add_member(client, gid_a, leader_a)
    for i in range(2):
        m = _create_user(client, f"close010_a_m{i}", role="participant")
        _add_member(client, gid_a, m)
    _register_group(client, cat_id, gid_a)
    post_a = _create_post(client, leader_a, "Submission A")
    _submit_to_category(client, cat_id, post_a)

    # --- Team B: 2 members ---
    leader_b = _create_user(client, "close010_leader_b", role="participant")
    gid_b = _create_group(client, leader_b, "Team B (2)")
    _add_member(client, gid_b, leader_b)
    m_b = _create_user(client, "close010_b_m0", role="participant")
    _add_member(client, gid_b, m_b)
    _register_group(client, cat_id, gid_b)
    post_b = _create_post(client, leader_b, "Submission B")
    _submit_to_category(client, cat_id, post_b)

    # --- Team C: 1 member only (will be disqualified) ---
    leader_c = _create_user(client, "close010_leader_c", role="participant")
    gid_c = _create_group(client, leader_c, "Team C (1)")
    _add_member(client, gid_c, leader_c)
    _register_group(client, cat_id, gid_c)
    post_c = _create_post(client, leader_c, "Submission C")
    _submit_to_category(client, cat_id, post_c)

    # Rate posts so they have average_rating
    rater = _create_user(client, "close010_rater")
    _rate_post(client, post_a, rater, {"Quality": 80})
    _rate_post(client, post_b, rater, {"Quality": 75})
    _rate_post(client, post_c, rater, {"Quality": 90})

    # NOW link the rule (after submissions, so pre-phase min_team_size check does
    # not interfere with event_post creation)
    rule_id = _create_rule(client, org, min_team_size=2, checks=[{
        "trigger": "update_content(event.status)",
        "phase": "post",
        "condition": {
            "type": "field_match",
            "params": {
                "entity": "event",
                "target": "$current",
                "field": "status",
                "op": "==",
                "value": "closed",
            },
        },
        "action": "flag_disqualified",
        "action_params": {"target": "group", "tag": "team_too_small"},
        "message": "Flag disqualified teams",
    }])
    _link_rule(client, cat_id, rule_id)

    # Close event
    resp = _close_category(client, cat_id, org)
    assert resp.status_code == 200

    # Verify: Team C's post should have "team_too_small" tag
    post_c_data = _get_post(client, post_c, leader_c)
    tags_c = post_c_data.get("tags") or []
    assert "team_too_small" in tags_c, f"Expected 'team_too_small' in {tags_c}"

    # Verify: Team A and Team B posts should NOT have the flag
    post_a_data = _get_post(client, post_a, leader_a)
    tags_a = post_a_data.get("tags") or []
    assert "team_too_small" not in tags_a, f"Team A should not be flagged: {tags_a}"

    post_b_data = _get_post(client, post_b, leader_b)
    tags_b = post_b_data.get("tags") or []
    assert "team_too_small" not in tags_b, f"Team B should not be flagged: {tags_b}"


# ---------------------------------------------------------------------------
# TC-CLOSE-020: compute_ranking by average_rating
# ---------------------------------------------------------------------------

def test_close_020_compute_ranking_by_average_rating(client):
    """Three submissions rated 85.5, 90.2, 78.0 should be ranked 1,2,3 (desc).

    Expected: rank_1 = 90.2, rank_2 = 85.5, rank_3 = 78.0
    """
    org = _create_user(client, "close020_org")
    cat_id = _create_event(client, org, "Ranking Test")

    rule_id = _create_rule(client, org, checks=[{
        "trigger": "update_content(event.status)",
        "phase": "post",
        "condition": {
            "type": "field_match",
            "params": {
                "entity": "event",
                "target": "$current",
                "field": "status",
                "op": "==",
                "value": "closed",
            },
        },
        "action": "compute_ranking",
        "action_params": {
            "source_field": "average_rating",
            "order": "desc",
            "output_tag_prefix": "rank_",
        },
        "message": "Compute final ranking",
    }])
    _link_rule(client, cat_id, rule_id)

    # Create 3 users/posts
    user_a = _create_user(client, "close020_ua", role="participant")
    user_b = _create_user(client, "close020_ub", role="participant")
    user_c = _create_user(client, "close020_uc", role="participant")

    post_a = _create_post(client, user_a, "Submission A")
    post_b = _create_post(client, user_b, "Submission B")
    post_c = _create_post(client, user_c, "Submission C")

    _submit_to_category(client, cat_id, post_a)
    _submit_to_category(client, cat_id, post_b)
    _submit_to_category(client, cat_id, post_c)

    # Rate with two raters for more realistic averaging
    rater1 = _create_user(client, "close020_r1")
    rater2 = _create_user(client, "close020_r2")

    # Post A: 85 + 86 => average_rating = (85 + 86) / 2 = 85.5
    _rate_post(client, post_a, rater1, {"Q": 85})
    _rate_post(client, post_a, rater2, {"Q": 86})

    # Post B: 90 + 90.4 => average_rating = (90 + 90.4) / 2 = 90.2
    _rate_post(client, post_b, rater1, {"Q": 90})
    _rate_post(client, post_b, rater2, {"Q": 90.4})

    # Post C: 78 + 78 => average_rating = (78 + 78) / 2 = 78.0
    _rate_post(client, post_c, rater1, {"Q": 78})
    _rate_post(client, post_c, rater2, {"Q": 78})

    # Close
    resp = _close_category(client, cat_id, org)
    assert resp.status_code == 200

    # Verify rankings — draft posts only visible to their creators
    data_a = _get_post(client, post_a, user_a)
    data_b = _get_post(client, post_b, user_b)
    data_c = _get_post(client, post_c, user_c)

    tags_a = data_a.get("tags") or []
    tags_b = data_b.get("tags") or []
    tags_c = data_c.get("tags") or []

    assert "rank_2" in tags_a, f"Post A (85.5) should be rank_2, got tags: {tags_a}"
    assert "rank_1" in tags_b, f"Post B (90.2) should be rank_1, got tags: {tags_b}"
    assert "rank_3" in tags_c, f"Post C (78.0) should be rank_3, got tags: {tags_c}"


# ---------------------------------------------------------------------------
# TC-CLOSE-022: Null rating excluded from ranking
# ---------------------------------------------------------------------------

def test_close_022_null_rating_excluded(client):
    """A submission with no rating (null average_rating) should not receive a rank tag."""
    org = _create_user(client, "close022_org")
    cat_id = _create_event(client, org, "Null Rating Test")

    rule_id = _create_rule(client, org, checks=[{
        "trigger": "update_content(event.status)",
        "phase": "post",
        "condition": {
            "type": "field_match",
            "params": {
                "entity": "event",
                "target": "$current",
                "field": "status",
                "op": "==",
                "value": "closed",
            },
        },
        "action": "compute_ranking",
        "action_params": {
            "source_field": "average_rating",
            "order": "desc",
            "output_tag_prefix": "rank_",
        },
        "message": "Compute ranking",
    }])
    _link_rule(client, cat_id, rule_id)

    user_a = _create_user(client, "close022_ua", role="participant")
    user_b = _create_user(client, "close022_ub", role="participant")
    user_c = _create_user(client, "close022_uc", role="participant")

    post_a = _create_post(client, user_a, "Rated A")
    post_b = _create_post(client, user_b, "Rated B")
    post_c = _create_post(client, user_c, "Unrated C")

    _submit_to_category(client, cat_id, post_a)
    _submit_to_category(client, cat_id, post_b)
    _submit_to_category(client, cat_id, post_c)

    rater = _create_user(client, "close022_rater")
    _rate_post(client, post_a, rater, {"Q": 90})
    _rate_post(client, post_b, rater, {"Q": 80})
    # post_c intentionally not rated

    resp = _close_category(client, cat_id, org)
    assert resp.status_code == 200

    # Draft posts only visible to their creators
    data_a = _get_post(client, post_a, user_a)
    data_b = _get_post(client, post_b, user_b)
    data_c = _get_post(client, post_c, user_c)

    tags_a = data_a.get("tags") or []
    tags_b = data_b.get("tags") or []
    tags_c = data_c.get("tags") or []

    assert "rank_1" in tags_a, f"Post A should be rank_1, got: {tags_a}"
    assert "rank_2" in tags_b, f"Post B should be rank_2, got: {tags_b}"
    # Unrated post should have NO rank tag
    rank_tags_c = [t for t in tags_c if t.startswith("rank_")]
    assert len(rank_tags_c) == 0, f"Unrated post should have no rank tag, got: {tags_c}"


# ---------------------------------------------------------------------------
# TC-CLOSE-030: Award certificate
# ---------------------------------------------------------------------------

def test_close_030_award_certificate(client):
    """After ranking, award_certificate should create certificate posts for ranked submissions."""
    org = _create_user(client, "close030_org")
    cat_id = _create_event(client, org, "Award Cert Test")

    # Two actions: first compute_ranking, then award_certificate
    rule_id = _create_rule(client, org, checks=[
        {
            "trigger": "update_content(event.status)",
            "phase": "post",
            "condition": {
                "type": "field_match",
                "params": {
                    "entity": "event",
                    "target": "$current",
                    "field": "status",
                    "op": "==",
                    "value": "closed",
                },
            },
            "action": "compute_ranking",
            "action_params": {
                "source_field": "average_rating",
                "order": "desc",
                "output_tag_prefix": "rank_",
            },
            "message": "Compute ranking",
        },
        {
            "trigger": "update_content(event.status)",
            "phase": "post",
            "condition": {
                "type": "field_match",
                "params": {
                    "entity": "event",
                    "target": "$current",
                    "field": "status",
                    "op": "==",
                    "value": "closed",
                },
            },
            "action": "award_certificate",
            "action_params": {
                "rules": [
                    {"rank_range": [1, 1], "title": "Gold Award"},
                    {"rank_range": [2, 2], "title": "Silver Award"},
                ],
            },
            "message": "Award certificates",
        },
    ])
    _link_rule(client, cat_id, rule_id)

    user_a = _create_user(client, "close030_ua", role="participant")
    user_b = _create_user(client, "close030_ub", role="participant")

    post_a = _create_post(client, user_a, "Sub Alpha")
    post_b = _create_post(client, user_b, "Sub Beta")

    _submit_to_category(client, cat_id, post_a)
    _submit_to_category(client, cat_id, post_b)

    rater = _create_user(client, "close030_rater")
    _rate_post(client, post_a, rater, {"Q": 95})
    _rate_post(client, post_b, rater, {"Q": 85})

    resp = _close_category(client, cat_id, org)
    assert resp.status_code == 200

    # Verify certificate posts were created by listing event posts with type reference
    cat_posts_resp = client.get(
        f"/api/events/{cat_id}/posts?relation_type=reference",
        headers={"X-User-Id": str(org)},
    )
    assert cat_posts_resp.status_code == 200
    ref_posts = cat_posts_resp.json()

    # There should be at least 2 certificate reference posts
    assert len(ref_posts) >= 2, (
        f"Expected at least 2 certificate posts, found {len(ref_posts)}: {ref_posts}"
    )

    # Verify the certificate posts themselves (certificate posts are published,
    # so any user can see them)
    cert_titles = []
    for ref in ref_posts:
        cert_post = _get_post(client, ref["post_id"], org)
        cert_titles.append(cert_post["title"])
        assert cert_post["type"] == "certificate"
        assert cert_post["status"] == "published"

    # Check that Gold and Silver awards exist
    combined = " ".join(cert_titles)
    assert "Gold Award" in combined, f"Expected Gold Award in: {cert_titles}"
    assert "Silver Award" in combined, f"Expected Silver Award in: {cert_titles}"


# ---------------------------------------------------------------------------
# TC-CLOSE-040: Full closure flow (flag + rank + award)
# ---------------------------------------------------------------------------

def test_close_040_full_closure_flow(client):
    """End-to-end closure: flag_disqualified, compute_ranking, award_certificate.

    Teams:
    - A: 3 members, avg ~90.2 -> qualifies
    - B: 2 members, avg ~85.5 -> qualifies
    - C: 1 member,  avg ~95.0 -> disqualified (team_too_small)
    - D: 2 members, no submission

    The rule sets min_team_size=2 which auto-expands to a pre-phase count check on
    submissions.  We submit posts BEFORE linking the rule to avoid pre-check conflicts.
    """
    org = _create_user(client, "close040_org")
    cat_id = _create_event(client, org, "Full Flow Test")

    # --- Team A: 3 members ---
    leader_a = _create_user(client, "close040_la", role="participant")
    gid_a = _create_group(client, leader_a, "Team A (3)")
    _add_member(client, gid_a, leader_a)
    for i in range(2):
        m = _create_user(client, f"close040_am{i}", role="participant")
        _add_member(client, gid_a, m)
    _register_group(client, cat_id, gid_a)
    post_a = _create_post(client, leader_a, "Submission A")
    _submit_to_category(client, cat_id, post_a)

    # --- Team B: 2 members ---
    leader_b = _create_user(client, "close040_lb", role="participant")
    gid_b = _create_group(client, leader_b, "Team B (2)")
    _add_member(client, gid_b, leader_b)
    m_b = _create_user(client, "close040_bm0", role="participant")
    _add_member(client, gid_b, m_b)
    _register_group(client, cat_id, gid_b)
    post_b = _create_post(client, leader_b, "Submission B")
    _submit_to_category(client, cat_id, post_b)

    # --- Team C: 1 member (disqualified) ---
    leader_c = _create_user(client, "close040_lc", role="participant")
    gid_c = _create_group(client, leader_c, "Team C (1)")
    _add_member(client, gid_c, leader_c)
    _register_group(client, cat_id, gid_c)
    post_c = _create_post(client, leader_c, "Submission C")
    _submit_to_category(client, cat_id, post_c)

    # --- Team D: 2 members, no submission ---
    leader_d = _create_user(client, "close040_ld", role="participant")
    gid_d = _create_group(client, leader_d, "Team D (2, no sub)")
    _add_member(client, gid_d, leader_d)
    m_d = _create_user(client, "close040_dm0", role="participant")
    _add_member(client, gid_d, m_d)
    _register_group(client, cat_id, gid_d)
    # No submission from Team D

    # --- Rate submissions ---
    rater1 = _create_user(client, "close040_r1")
    rater2 = _create_user(client, "close040_r2")

    # Post A: avg ~90.2
    _rate_post(client, post_a, rater1, {"Q": 90})
    _rate_post(client, post_a, rater2, {"Q": 90.4})

    # Post B: avg ~85.5
    _rate_post(client, post_b, rater1, {"Q": 85})
    _rate_post(client, post_b, rater2, {"Q": 86})

    # Post C: avg ~95.0 (high score, but team too small)
    _rate_post(client, post_c, rater1, {"Q": 95})
    _rate_post(client, post_c, rater2, {"Q": 95})

    # NOW link the rule (after all submissions, to avoid pre-phase min_team_size
    # check blocking submissions from solo teams)
    rule_id = _create_rule(client, org, min_team_size=2, checks=[
        # 1. flag_disqualified
        {
            "trigger": "update_content(event.status)",
            "phase": "post",
            "condition": {
                "type": "field_match",
                "params": {
                    "entity": "event",
                    "target": "$current",
                    "field": "status",
                    "op": "==",
                    "value": "closed",
                },
            },
            "action": "flag_disqualified",
            "action_params": {"target": "group", "tag": "team_too_small"},
            "message": "Flag disqualified teams",
        },
        # 2. compute_ranking
        {
            "trigger": "update_content(event.status)",
            "phase": "post",
            "condition": {
                "type": "field_match",
                "params": {
                    "entity": "event",
                    "target": "$current",
                    "field": "status",
                    "op": "==",
                    "value": "closed",
                },
            },
            "action": "compute_ranking",
            "action_params": {
                "source_field": "average_rating",
                "order": "desc",
                "output_tag_prefix": "rank_",
            },
            "message": "Compute ranking",
        },
        # 3. award_certificate
        {
            "trigger": "update_content(event.status)",
            "phase": "post",
            "condition": {
                "type": "field_match",
                "params": {
                    "entity": "event",
                    "target": "$current",
                    "field": "status",
                    "op": "==",
                    "value": "closed",
                },
            },
            "action": "award_certificate",
            "action_params": {
                "rules": [
                    {"rank_range": [1, 1], "title": "Champion"},
                    {"rank_range": [2, 2], "title": "Runner-up"},
                ],
            },
            "message": "Award certificates",
        },
    ])
    _link_rule(client, cat_id, rule_id)

    # --- Close event ---
    resp = _close_category(client, cat_id, org)
    assert resp.status_code == 200

    # --- Verify flag_disqualified ---
    # Draft posts: read as their creators
    data_c = _get_post(client, post_c, leader_c)
    tags_c = data_c.get("tags") or []
    assert "team_too_small" in tags_c, f"Team C should be flagged: {tags_c}"

    data_a = _get_post(client, post_a, leader_a)
    tags_a = data_a.get("tags") or []
    assert "team_too_small" not in tags_a, f"Team A should NOT be flagged: {tags_a}"

    data_b = _get_post(client, post_b, leader_b)
    tags_b = data_b.get("tags") or []
    assert "team_too_small" not in tags_b, f"Team B should NOT be flagged: {tags_b}"

    # --- Verify compute_ranking ---
    # compute_ranking EXCLUDES disqualified posts (those with tags in the
    # disqualification set: "team_too_small", "missing_attachment", "disqualified").
    # Team C is flagged, so it is excluded from ranking.
    # Among eligible posts: A=90.2, B=85.5 (desc) => A=rank_1, B=rank_2
    tags_a = (_get_post(client, post_a, leader_a).get("tags") or [])
    tags_b = (_get_post(client, post_b, leader_b).get("tags") or [])
    tags_c = (_get_post(client, post_c, leader_c).get("tags") or [])

    # A and B should each have exactly one rank tag
    rank_tags_a = [t for t in tags_a if t.startswith("rank_")]
    rank_tags_b = [t for t in tags_b if t.startswith("rank_")]
    assert len(rank_tags_a) == 1, f"Post A should have exactly one rank tag: {tags_a}"
    assert len(rank_tags_b) == 1, f"Post B should have exactly one rank tag: {tags_b}"

    # C is disqualified and excluded from ranking -- no rank tag
    rank_tags_c = [t for t in tags_c if t.startswith("rank_")]
    assert len(rank_tags_c) == 0, (
        f"Disqualified Post C should have no rank tag, got: {tags_c}"
    )

    # A=90.2 -> rank_1, B=85.5 -> rank_2
    assert "rank_1" in tags_a, f"Post A (90.2) expected rank_1, got: {tags_a}"
    assert "rank_2" in tags_b, f"Post B (85.5) expected rank_2, got: {tags_b}"

    # --- Verify award_certificate ---
    cat_posts_resp = client.get(
        f"/api/events/{cat_id}/posts?relation_type=reference",
        headers={"X-User-Id": str(org)},
    )
    assert cat_posts_resp.status_code == 200
    ref_posts = cat_posts_resp.json()

    # rank_1 and rank_2 match award rules, so at least 2 certificates
    assert len(ref_posts) >= 2, f"Expected >=2 certificate posts, got {len(ref_posts)}"

    cert_titles = []
    for ref in ref_posts:
        # Certificate posts are "published", visible to anyone
        cert = _get_post(client, ref["post_id"], org)
        cert_titles.append(cert["title"])
        assert cert["type"] == "certificate"

    combined = " ".join(cert_titles)
    assert "Champion" in combined, f"Expected Champion award in: {cert_titles}"
    assert "Runner-up" in combined, f"Expected Runner-up award in: {cert_titles}"


# ---------------------------------------------------------------------------
# TC-CLOSE-900: Non-closed status does not trigger post hooks
# ---------------------------------------------------------------------------

def test_close_900_non_closed_status_no_trigger(client):
    """Transitioning from draft to published should not trigger closure hooks."""
    org = _create_user(client, "close900_org")
    # Create event in draft state (not yet published)
    resp = client.post("/api/events", json={
        "name": "No Trigger Test",
        "description": "test",
        "type": "competition",
    }, headers={"X-User-Id": str(org)})
    assert resp.status_code == 201
    cat_id = resp.json()["id"]

    # Rule with compute_ranking on status==closed
    rule_id = _create_rule(client, org, checks=[{
        "trigger": "update_content(event.status)",
        "phase": "post",
        "condition": {
            "type": "field_match",
            "params": {
                "entity": "event",
                "target": "$current",
                "field": "status",
                "op": "==",
                "value": "closed",
            },
        },
        "action": "compute_ranking",
        "action_params": {
            "source_field": "average_rating",
            "order": "desc",
            "output_tag_prefix": "rank_",
        },
        "message": "Compute ranking",
    }])
    _link_rule(client, cat_id, rule_id)

    # Create a rated submission
    user_a = _create_user(client, "close900_ua", role="participant")
    post_a = _create_post(client, user_a, "Submission 900")
    client.post(f"/api/events/{cat_id}/posts", json={
        "post_id": post_a, "relation_type": "submission",
    })
    rater = _create_user(client, "close900_rater")
    _rate_post(client, post_a, rater, {"Q": 90})

    # Transition: draft -> published (NOT closed)
    pub_resp = client.patch(
        f"/api/events/{cat_id}",
        json={"status": "published"},
        headers={"X-User-Id": str(org)},
    )
    assert pub_resp.status_code == 200

    # Verify no ranking tags added — read as the post creator (draft visibility)
    data_a = _get_post(client, post_a, user_a)
    tags = data_a.get("tags") or []
    rank_tags = [t for t in tags if t.startswith("rank_")]
    assert len(rank_tags) == 0, f"No rank tags expected on publish, got: {tags}"


# ---------------------------------------------------------------------------
# TC-CLOSE-901: No rules — no checks
# ---------------------------------------------------------------------------

def test_close_901_no_rules_no_checks(client):
    """A event with no rules should close cleanly with no side effects."""
    org = _create_user(client, "close901_org")
    cat_id = _create_event(client, org, "No Rules Test")

    # Submit and rate a post
    user_a = _create_user(client, "close901_ua", role="participant")
    post_a = _create_post(client, user_a, "Submission 901")
    _submit_to_category(client, cat_id, post_a)
    rater = _create_user(client, "close901_rater")
    _rate_post(client, post_a, rater, {"Q": 88})

    # Close -- should succeed
    resp = _close_category(client, cat_id, org)
    assert resp.status_code == 200
    assert resp.json()["status"] == "closed"

    # No ranking tags (no rules) — read as post creator (draft visibility)
    data_a = _get_post(client, post_a, user_a)
    tags = data_a.get("tags") or []
    rank_tags = [t for t in tags if t.startswith("rank_")]
    assert len(rank_tags) == 0, f"No rank tags expected without rules, got: {tags}"


# ---------------------------------------------------------------------------
# TC-CLOSE-902: Post-hook failure does not rollback main operation
# ---------------------------------------------------------------------------

def test_close_902_post_hook_failure_no_rollback(client):
    """If award_certificate encounters bad action_params, the event stays closed."""
    org = _create_user(client, "close902_org")
    cat_id = _create_event(client, org, "Hook Fail Test")

    # Rule with deliberately invalid award_certificate params (missing "rules" key)
    rule_id = _create_rule(client, org, checks=[{
        "trigger": "update_content(event.status)",
        "phase": "post",
        "condition": {
            "type": "field_match",
            "params": {
                "entity": "event",
                "target": "$current",
                "field": "status",
                "op": "==",
                "value": "closed",
            },
        },
        "action": "award_certificate",
        "action_params": {},  # Missing "rules" -- will produce no certificates
        "message": "Award certificates (broken)",
    }])
    _link_rule(client, cat_id, rule_id)

    # Create rated submission
    user_a = _create_user(client, "close902_ua", role="participant")
    post_a = _create_post(client, user_a, "Submission 902")
    _submit_to_category(client, cat_id, post_a)
    rater = _create_user(client, "close902_rater")
    _rate_post(client, post_a, rater, {"Q": 80})

    # Close -- should succeed despite hook not producing certificates
    resp = _close_category(client, cat_id, org)
    assert resp.status_code == 200
    assert resp.json()["status"] == "closed"

    # Verify no certificate posts were created
    cat_posts_resp = client.get(
        f"/api/events/{cat_id}/posts?relation_type=reference",
        headers={"X-User-Id": str(org)},
    )
    assert cat_posts_resp.status_code == 200
    ref_posts = cat_posts_resp.json()
    assert len(ref_posts) == 0, f"No certificate posts expected, got {len(ref_posts)}"
