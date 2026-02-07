"""Entry rule enforcement tests — covers TC-ENTRY-001 through TC-ENTRY-902.

Tests the declarative rule engine's ability to enforce entry-gate conditions
when creating category_post, category_group, and group_user relations.

Trigger points tested:
- create_relation(category_group): group registration to a category
- create_relation(category_post): post submission to a category
- create_relation(group_user): adding a member to a group (indirectly via category rules)

Condition types exercised:
- exists (group_user, category_group, post_resource)
- count (category_post scope=user)
- resource_required (min_count, formats)
- resource_format (formats)

Fixed-field expansion tested:
- max_submissions -> count condition
"""


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _create_user(client, username, role="participant"):
    resp = client.post(
        "/api/users",
        json={"username": username, "email": f"{username}@example.com", "role": role},
    )
    return resp.json()["id"]


def _create_category(client, uid, name="Entry Test Category"):
    resp = client.post(
        "/api/categories",
        json={"name": name, "description": "test", "type": "competition"},
        headers={"X-User-Id": str(uid)},
    )
    cat_id = resp.json()["id"]
    # Publish so it is usable
    client.patch(
        f"/api/categories/{cat_id}",
        json={"status": "published"},
        headers={"X-User-Id": str(uid)},
    )
    return cat_id


def _create_rule(client, uid, checks=None, **fields):
    body = {
        "name": fields.pop("name", "Entry Rule"),
        "description": fields.pop("description", "test"),
    }
    if checks is not None:
        body["checks"] = [c if isinstance(c, dict) else c.dict() for c in checks]
    body.update(fields)
    resp = client.post(
        "/api/rules", json=body, headers={"X-User-Id": str(uid)},
    )
    assert resp.status_code == 201, f"Rule creation failed: {resp.json()}"
    return resp.json()["id"]


def _link_rule(client, cat_id, rule_id):
    resp = client.post(
        f"/api/categories/{cat_id}/rules",
        json={"rule_id": rule_id, "priority": 0},
    )
    assert resp.status_code == 201


def _create_group(client, uid, name="Entry Team"):
    resp = client.post(
        "/api/groups",
        json={"name": name, "description": "test", "require_approval": False},
        headers={"X-User-Id": str(uid)},
    )
    return resp.json()["id"]


def _add_member(client, gid, uid, role="member"):
    resp = client.post(
        f"/api/groups/{gid}/members",
        json={"user_id": uid, "role": role},
    )
    return resp


def _create_post(client, uid, title="Entry Submission", post_type="proposal"):
    resp = client.post(
        "/api/posts",
        json={"title": title, "type": post_type, "status": "draft"},
        headers={"X-User-Id": str(uid)},
    )
    return resp.json()["id"]


def _create_resource(client, uid, filename="proposal.pdf"):
    resp = client.post(
        "/api/resources",
        json={
            "filename": filename,
            "url": f"https://example.com/{filename}",
            "mime_type": "application/pdf",
        },
        headers={"X-User-Id": str(uid)},
    )
    return resp.json()["id"]


def _link_resource_to_post(client, post_id, resource_id):
    resp = client.post(
        f"/api/posts/{post_id}/resources",
        json={"resource_id": resource_id, "display_type": "attachment"},
    )
    assert resp.status_code == 201


def _submit_post_to_category(client, cat_id, post_id):
    return client.post(
        f"/api/categories/{cat_id}/posts",
        json={"post_id": post_id, "relation_type": "submission"},
    )


def _register_group_to_category(client, cat_id, group_id):
    return client.post(
        f"/api/categories/{cat_id}/groups",
        json={"group_id": group_id},
    )


# ---------------------------------------------------------------------------
# TC-ENTRY-001: Must join a group before registering for a category
# Trigger: create_relation(category_group)
# Condition: exists(group_user, scope=user, filter={status:accepted}, require=true)
# Expected: denied (422) because the group creator has no accepted membership
# ---------------------------------------------------------------------------
def test_entry_001_must_join_group_before_registration(client):
    """TC-ENTRY-001: create_relation(category_group) -- user not in any group -> deny"""
    organizer = _create_user(client, "org001", role="organizer")
    user = _create_user(client, "user001", role="participant")

    rule_id = _create_rule(
        client,
        organizer,
        checks=[
            {
                "trigger": "create_relation(category_group)",
                "phase": "pre",
                "condition": {
                    "type": "exists",
                    "params": {
                        "entity": "group_user",
                        "scope": "user",
                        "filter": {"status": "accepted"},
                        "require": True,
                    },
                },
                "on_fail": "deny",
                "message": "Must join a group first",
            }
        ],
    )

    cat_id = _create_category(client, organizer)
    _link_rule(client, cat_id, rule_id)

    # User creates a group but is NOT added as an accepted member
    group_id = _create_group(client, user, name="Team001")

    # Attempt to register group for category -- should be rejected
    resp = _register_group_to_category(client, cat_id, group_id)
    assert resp.status_code == 422, (
        f"Expected 422 deny, got {resp.status_code}: {resp.json()}"
    )
    assert "Must join a group first" in resp.json()["detail"]


# ---------------------------------------------------------------------------
# TC-ENTRY-002: Must have team registered before submission
# Trigger: create_relation(category_post)
# Condition: exists(category_group, scope=user_group) -- user's group must be
#            registered to the category
# Expected: denied (422) because user's group is not registered to the category
# ---------------------------------------------------------------------------
def test_entry_002_must_have_team_registered_before_submission(client):
    """TC-ENTRY-002: create_relation(category_post) -- user's group not registered -> deny"""
    organizer = _create_user(client, "org002", role="organizer")
    user = _create_user(client, "user002", role="participant")

    rule_id = _create_rule(
        client,
        organizer,
        checks=[
            {
                "trigger": "create_relation(category_post)",
                "phase": "pre",
                "condition": {
                    "type": "exists",
                    "params": {
                        "entity": "category_group",
                        "scope": "user_group",
                        "require": True,
                    },
                },
                "on_fail": "deny",
                "message": "Your team must be registered for this category",
            }
        ],
    )

    cat_id = _create_category(client, organizer)
    _link_rule(client, cat_id, rule_id)

    # User creates a group and joins it, but does NOT register group to category
    group_id = _create_group(client, user, name="Team002")
    _add_member(client, group_id, user)

    # User creates a post and tries to submit
    post_id = _create_post(client, user)
    resp = _submit_post_to_category(client, cat_id, post_id)
    assert resp.status_code == 422, (
        f"Expected 422 deny, got {resp.status_code}: {resp.json()}"
    )
    assert "Your team must be registered" in resp.json()["detail"]


# ---------------------------------------------------------------------------
# TC-ENTRY-003: Must have a published profile post to register a group
# Trigger: create_relation(category_group)
# Condition: exists(category_post, filter={relation_type:submission}) for user
#            (proxy: user must have submitted at least one post to *any* category)
#
# NOTE: The exists(category_post) evaluator in the rule engine checks category-
# scoped posts; here we require a profile-type post in the category. Since the
# rule engine's exists(category_post) looks for user's posts in the target
# category, we use that with relation_type=submission.
# Expected: denied (422) because user has no published post in the category
# ---------------------------------------------------------------------------
def test_entry_003_must_have_profile_post(client):
    """TC-ENTRY-003: create_relation(category_group) -- user has no published profile post -> deny"""
    organizer = _create_user(client, "org003", role="organizer")
    user = _create_user(client, "user003", role="participant")

    rule_id = _create_rule(
        client,
        organizer,
        checks=[
            {
                "trigger": "create_relation(category_group)",
                "phase": "pre",
                "condition": {
                    "type": "exists",
                    "params": {
                        "entity": "category_post",
                        "scope": "user",
                        "filter": {"relation_type": "submission"},
                        "require": True,
                    },
                },
                "on_fail": "deny",
                "message": "Must have a published profile post",
            }
        ],
    )

    cat_id = _create_category(client, organizer)
    _link_rule(client, cat_id, rule_id)

    # User creates a group but has no post submitted to the category
    group_id = _create_group(client, user, name="Team003")

    resp = _register_group_to_category(client, cat_id, group_id)
    assert resp.status_code == 422, (
        f"Expected 422 deny, got {resp.status_code}: {resp.json()}"
    )
    assert "Must have a published profile post" in resp.json()["detail"]


# ---------------------------------------------------------------------------
# TC-ENTRY-004: Same as 003 but user satisfies the condition
# Trigger: create_relation(category_group)
# Condition: exists(category_post, filter={relation_type:submission}) -- satisfied
# Expected: allow (201) because user has already submitted a post to the category
# ---------------------------------------------------------------------------
def test_entry_004_conditions_satisfied(client):
    """TC-ENTRY-004: Same as 003 but user has a submitted post -> allow"""
    organizer = _create_user(client, "org004", role="organizer")
    user = _create_user(client, "user004", role="participant")

    rule_id = _create_rule(
        client,
        organizer,
        checks=[
            {
                "trigger": "create_relation(category_group)",
                "phase": "pre",
                "condition": {
                    "type": "exists",
                    "params": {
                        "entity": "category_post",
                        "scope": "user",
                        "filter": {"relation_type": "submission"},
                        "require": True,
                    },
                },
                "on_fail": "deny",
                "message": "Must have a published profile post",
            }
        ],
    )

    cat_id = _create_category(client, organizer)
    # Link rule AFTER we submit the post, so the first submission isn't blocked
    # by a different rule. We first submit, then link the rule, then register group.
    # Actually, the rule only fires on category_group creation, so we can link it now.
    _link_rule(client, cat_id, rule_id)

    # User creates and submits a post to the category (no rule blocks category_post here)
    post_id = _create_post(client, user, title="Profile Post")
    submit_resp = _submit_post_to_category(client, cat_id, post_id)
    assert submit_resp.status_code == 201, (
        f"Post submission should succeed (no category_post rule): {submit_resp.json()}"
    )

    # Now user creates a group and registers it -- should pass
    group_id = _create_group(client, user, name="Team004")
    resp = _register_group_to_category(client, cat_id, group_id)
    assert resp.status_code == 201, (
        f"Expected 201 allow, got {resp.status_code}: {resp.json()}"
    )


# ---------------------------------------------------------------------------
# TC-ENTRY-010: Resource required -- post has no resources
# Trigger: create_relation(category_post)
# Condition: resource_required(min_count=1)
# Expected: denied (422) because post has zero resources
# ---------------------------------------------------------------------------
def test_entry_010_resource_required_min_count(client):
    """TC-ENTRY-010: create_relation(category_post) -- post has no resources -> deny"""
    organizer = _create_user(client, "org010", role="organizer")
    user = _create_user(client, "user010", role="participant")

    rule_id = _create_rule(
        client,
        organizer,
        checks=[
            {
                "trigger": "create_relation(category_post)",
                "phase": "pre",
                "condition": {
                    "type": "resource_required",
                    "params": {"min_count": 1},
                },
                "on_fail": "deny",
                "message": "At least one resource attachment is required",
            }
        ],
    )

    cat_id = _create_category(client, organizer)
    _link_rule(client, cat_id, rule_id)

    # Post with no resources
    post_id = _create_post(client, user)
    resp = _submit_post_to_category(client, cat_id, post_id)
    assert resp.status_code == 422, (
        f"Expected 422, got {resp.status_code}: {resp.json()}"
    )
    assert "resource" in resp.json()["detail"].lower()


# ---------------------------------------------------------------------------
# TC-ENTRY-011: Resource format -- post has .pptx but rule requires PDF
# Trigger: create_relation(category_post)
# Condition: resource_format(formats=["pdf"])
# Expected: denied (422) because .pptx is not in the allowed format list
# ---------------------------------------------------------------------------
def test_entry_011_resource_required_format(client):
    """TC-ENTRY-011: create_relation(category_post) -- post has .pptx but rule requires PDF -> deny"""
    organizer = _create_user(client, "org011", role="organizer")
    user = _create_user(client, "user011", role="participant")

    rule_id = _create_rule(
        client,
        organizer,
        checks=[
            {
                "trigger": "create_relation(category_post)",
                "phase": "pre",
                "condition": {
                    "type": "resource_format",
                    "params": {"formats": ["pdf"]},
                },
                "on_fail": "deny",
                "message": "Only PDF attachments are allowed",
            }
        ],
    )

    cat_id = _create_category(client, organizer)
    _link_rule(client, cat_id, rule_id)

    post_id = _create_post(client, user)
    res_id = _create_resource(client, user, filename="slides.pptx")
    _link_resource_to_post(client, post_id, res_id)

    resp = _submit_post_to_category(client, cat_id, post_id)
    assert resp.status_code == 422, (
        f"Expected 422, got {resp.status_code}: {resp.json()}"
    )
    assert "PDF" in resp.json()["detail"] or "pdf" in resp.json()["detail"].lower()


# ---------------------------------------------------------------------------
# TC-ENTRY-012: Resource format satisfied -- post has .pdf and rule requires PDF
# Trigger: create_relation(category_post)
# Condition: resource_format(formats=["pdf"])
# Expected: allow (201)
# ---------------------------------------------------------------------------
def test_entry_012_resource_format_satisfied(client):
    """TC-ENTRY-012: Same as 011 but post has .pdf -> allow"""
    organizer = _create_user(client, "org012", role="organizer")
    user = _create_user(client, "user012", role="participant")

    rule_id = _create_rule(
        client,
        organizer,
        checks=[
            {
                "trigger": "create_relation(category_post)",
                "phase": "pre",
                "condition": {
                    "type": "resource_format",
                    "params": {"formats": ["pdf"]},
                },
                "on_fail": "deny",
                "message": "Only PDF attachments are allowed",
            }
        ],
    )

    cat_id = _create_category(client, organizer)
    _link_rule(client, cat_id, rule_id)

    post_id = _create_post(client, user)
    res_id = _create_resource(client, user, filename="proposal.pdf")
    _link_resource_to_post(client, post_id, res_id)

    resp = _submit_post_to_category(client, cat_id, post_id)
    assert resp.status_code == 201, (
        f"Expected 201 allow, got {resp.status_code}: {resp.json()}"
    )


# ---------------------------------------------------------------------------
# TC-ENTRY-020: One submission per user (max_submissions=1 via fixed field)
# Trigger: create_relation(category_post)
# Condition: expanded from max_submissions=1 -> count(category_post, scope=user, op="<", value=1)
# Expected: second submission denied (422)
# ---------------------------------------------------------------------------
def test_entry_020_one_submission_per_user(client):
    """TC-ENTRY-020: create_relation(category_post) -- user already submitted -> deny"""
    organizer = _create_user(client, "org020", role="organizer")
    user = _create_user(client, "user020", role="participant")

    rule_id = _create_rule(
        client,
        organizer,
        name="Max 1 Submission",
        max_submissions=1,
    )

    cat_id = _create_category(client, organizer)
    _link_rule(client, cat_id, rule_id)

    # First submission should succeed
    post1 = _create_post(client, user, title="First Submission")
    resp1 = _submit_post_to_category(client, cat_id, post1)
    assert resp1.status_code == 201, (
        f"First submission should succeed: {resp1.json()}"
    )

    # Second submission should be denied
    post2 = _create_post(client, user, title="Second Submission")
    resp2 = _submit_post_to_category(client, cat_id, post2)
    assert resp2.status_code == 422, (
        f"Expected 422 deny for second submission, got {resp2.status_code}: {resp2.json()}"
    )
    assert "max" in resp2.json()["detail"].lower() or "submission" in resp2.json()["detail"].lower()


# ---------------------------------------------------------------------------
# TC-ENTRY-022: Different categories are isolated -- max_submissions=1 per category
# Two separate categories each with max_submissions=1. A user submits one post
# to each category. Both should succeed because the count is per-category.
# ---------------------------------------------------------------------------
def test_entry_022_different_categories_isolated(client):
    """TC-ENTRY-022: Two categories each with max_submissions=1, user submits to both -> OK"""
    organizer = _create_user(client, "org022", role="organizer")
    user = _create_user(client, "user022", role="participant")

    rule_id = _create_rule(
        client,
        organizer,
        name="Max 1 Submission",
        max_submissions=1,
    )

    cat_a = _create_category(client, organizer, name="Category A")
    cat_b = _create_category(client, organizer, name="Category B")
    _link_rule(client, cat_a, rule_id)
    _link_rule(client, cat_b, rule_id)

    post_a = _create_post(client, user, title="Submission A")
    resp_a = _submit_post_to_category(client, cat_a, post_a)
    assert resp_a.status_code == 201, (
        f"Submission to category A should succeed: {resp_a.json()}"
    )

    post_b = _create_post(client, user, title="Submission B")
    resp_b = _submit_post_to_category(client, cat_b, post_b)
    assert resp_b.status_code == 201, (
        f"Submission to category B should succeed (isolated): {resp_b.json()}"
    )


# ---------------------------------------------------------------------------
# TC-ENTRY-030: Fixed + custom checks combined -- max_submissions=1 AND resource_required
# User has already submitted once -> deny (the max_submissions check fires first)
# ---------------------------------------------------------------------------
def test_entry_030_fixed_and_custom_checks_and_logic(client):
    """TC-ENTRY-030: max_submissions=1 + resource_required -- user already submitted -> deny"""
    organizer = _create_user(client, "org030", role="organizer")
    user = _create_user(client, "user030", role="participant")

    rule_id = _create_rule(
        client,
        organizer,
        name="Combo Rule",
        max_submissions=1,
        checks=[
            {
                "trigger": "create_relation(category_post)",
                "phase": "pre",
                "condition": {
                    "type": "resource_required",
                    "params": {"min_count": 1},
                },
                "on_fail": "deny",
                "message": "Attachment required",
            }
        ],
    )

    cat_id = _create_category(client, organizer)
    _link_rule(client, cat_id, rule_id)

    # First submission: includes a resource -> should pass both checks
    post1 = _create_post(client, user, title="First with resource")
    res1 = _create_resource(client, user, filename="doc1.pdf")
    _link_resource_to_post(client, post1, res1)
    resp1 = _submit_post_to_category(client, cat_id, post1)
    assert resp1.status_code == 201, (
        f"First submission with resource should succeed: {resp1.json()}"
    )

    # Second submission: includes a resource BUT max_submissions already reached
    post2 = _create_post(client, user, title="Second with resource")
    res2 = _create_resource(client, user, filename="doc2.pdf")
    _link_resource_to_post(client, post2, res2)
    resp2 = _submit_post_to_category(client, cat_id, post2)
    assert resp2.status_code == 422, (
        f"Expected 422 deny (max reached), got {resp2.status_code}: {resp2.json()}"
    )


# ---------------------------------------------------------------------------
# TC-ENTRY-031: Fixed + custom checks both satisfied -- first submission with resource
# max_submissions=1 (not reached) AND resource_required (has resource) -> allow
# ---------------------------------------------------------------------------
def test_entry_031_fixed_and_custom_checks_both_satisfied(client):
    """TC-ENTRY-031: max_submissions=1 + resource_required -- first submission with resource -> allow"""
    organizer = _create_user(client, "org031", role="organizer")
    user = _create_user(client, "user031", role="participant")

    rule_id = _create_rule(
        client,
        organizer,
        name="Combo Rule OK",
        max_submissions=1,
        checks=[
            {
                "trigger": "create_relation(category_post)",
                "phase": "pre",
                "condition": {
                    "type": "resource_required",
                    "params": {"min_count": 1},
                },
                "on_fail": "deny",
                "message": "Attachment required",
            }
        ],
    )

    cat_id = _create_category(client, organizer)
    _link_rule(client, cat_id, rule_id)

    post_id = _create_post(client, user, title="Submission with resource")
    res_id = _create_resource(client, user, filename="attachment.pdf")
    _link_resource_to_post(client, post_id, res_id)

    resp = _submit_post_to_category(client, cat_id, post_id)
    assert resp.status_code == 201, (
        f"Expected 201 allow, got {resp.status_code}: {resp.json()}"
    )


# ---------------------------------------------------------------------------
# TC-ENTRY-900: Rule with unknown condition type -- silently ignored (pass)
# The rule engine returns True for unknown condition types, so the check passes
# and the submission should be allowed.
# ---------------------------------------------------------------------------
def test_entry_900_unknown_condition_type(client, db_session):
    """TC-ENTRY-900: Rule with unknown condition type -- silently ignored"""
    organizer = _create_user(client, "org900", role="organizer")
    user = _create_user(client, "user900", role="participant")

    rule_id = _create_rule(
        client,
        organizer,
        checks=[
            {
                "trigger": "create_relation(category_post)",
                "phase": "pre",
                "condition": {
                    "type": "nonexistent_check_type",
                    "params": {"foo": "bar"},
                },
                "on_fail": "deny",
                "message": "Should never fire",
            }
        ],
    )

    cat_id = _create_category(client, organizer)
    _link_rule(client, cat_id, rule_id)

    post_id = _create_post(client, user, title="Unknown check")
    resp = _submit_post_to_category(client, cat_id, post_id)
    # Unknown condition type -> evaluates to True -> check passes -> submission allowed
    assert resp.status_code == 201, (
        f"Expected 201 (unknown condition ignored), got {resp.status_code}: {resp.json()}"
    )


# ---------------------------------------------------------------------------
# TC-ENTRY-901: Check with missing trigger -- should not match any trigger and
# thus not block any operation.
# ---------------------------------------------------------------------------
def test_entry_901_missing_trigger_field(client):
    """TC-ENTRY-901: Check with non-matching trigger -- should not match and thus not block.

    NOTE: The CheckDefinition schema requires `trigger` as a mandatory field, so
    we cannot omit it entirely at the API level. Instead, we use a trigger value
    that does not match any real operation point. The rule engine filters checks
    by trigger string, so this check will never fire.
    """
    organizer = _create_user(client, "org901", role="organizer")
    user = _create_user(client, "user901", role="participant")

    rule_id = _create_rule(
        client,
        organizer,
        checks=[
            {
                "trigger": "nonexistent_trigger_that_never_fires",
                "phase": "pre",
                "condition": {
                    "type": "resource_required",
                    "params": {"min_count": 999},
                },
                "on_fail": "deny",
                "message": "Should never fire because trigger does not match",
            }
        ],
    )

    cat_id = _create_category(client, organizer)
    _link_rule(client, cat_id, rule_id)

    post_id = _create_post(client, user, title="No trigger match")
    resp = _submit_post_to_category(client, cat_id, post_id)
    # Check's trigger does not match "create_relation(category_post)"
    # so the check is skipped and submission is allowed
    assert resp.status_code == 201, (
        f"Expected 201 (trigger mismatch), got {resp.status_code}: {resp.json()}"
    )


# ---------------------------------------------------------------------------
# TC-ENTRY-902: Pre check without condition is skipped
# A check definition with phase="pre" but no condition should be skipped
# by the rule engine (it iterates checks and calls `continue` when condition
# is None).
# ---------------------------------------------------------------------------
def test_entry_902_pre_phase_without_condition(client, db_session):
    """TC-ENTRY-902: Pre check without condition is skipped"""
    organizer = _create_user(client, "org902", role="organizer")
    user = _create_user(client, "user902", role="participant")

    rule_id = _create_rule(
        client,
        organizer,
        checks=[
            {
                "trigger": "create_relation(category_post)",
                "phase": "pre",
                # No "condition" key
                "on_fail": "deny",
                "message": "No condition means this check is skipped",
            }
        ],
    )

    cat_id = _create_category(client, organizer)
    _link_rule(client, cat_id, rule_id)

    post_id = _create_post(client, user, title="Condition-less check")
    resp = _submit_post_to_category(client, cat_id, post_id)
    # condition is None -> engine skips this check -> submission allowed
    assert resp.status_code == 201, (
        f"Expected 201 (condition-less check skipped), got {resp.status_code}: {resp.json()}"
    )
