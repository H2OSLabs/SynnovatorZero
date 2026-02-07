"""E2E user journey tests — TC-JOUR series.

Each test function exercises a complete user journey through the API,
combining multiple endpoints to verify realistic multi-step workflows.

Fixtures:
    client  -- FastAPI TestClient backed by an in-memory SQLite database
               (injected via conftest.py)
"""


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _create_user(client, username="journey_user", role="organizer"):
    resp = client.post("/api/users", json={
        "username": username,
        "email": f"{username}@example.com",
        "role": role,
    })
    return resp.json()["id"]


def _create_category(client, uid, name="Test Event", status="published"):
    resp = client.post("/api/categories", json={
        "name": name,
        "description": f"Desc {name}",
        "type": "competition",
    }, headers={"X-User-Id": str(uid)})
    cat_id = resp.json()["id"]
    if status != "draft":
        client.patch(
            f"/api/categories/{cat_id}",
            json={"status": status},
            headers={"X-User-Id": str(uid)},
        )
    return cat_id


def _create_rule(client, uid, **fields):
    body = {
        "name": fields.pop("name", "Test Rule"),
        "description": fields.pop("description", "test"),
    }
    body.update(fields)
    resp = client.post("/api/rules", json=body, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201
    return resp.json()["id"]


def _create_post(client, uid, title="Test Post", post_type="general",
                 status="published", visibility="public"):
    resp = client.post("/api/posts", json={
        "title": title,
        "type": post_type,
        "status": "draft",
        "visibility": visibility,
    }, headers={"X-User-Id": str(uid)})
    post_id = resp.json()["id"]
    # Transition: draft -> pending_review -> published (or custom status)
    if status == "published":
        client.patch(
            f"/api/posts/{post_id}",
            json={"status": "pending_review"},
            headers={"X-User-Id": str(uid)},
        )
        client.patch(
            f"/api/posts/{post_id}",
            json={"status": "published"},
            headers={"X-User-Id": str(uid)},
        )
    elif status != "draft":
        client.patch(
            f"/api/posts/{post_id}",
            json={"status": status},
            headers={"X-User-Id": str(uid)},
        )
    return post_id


def _create_group(client, uid, name="Test Team", require_approval=True):
    resp = client.post("/api/groups", json={
        "name": name,
        "description": f"Desc {name}",
        "require_approval": require_approval,
    }, headers={"X-User-Id": str(uid)})
    return resp.json()["id"]


def _create_resource(client, uid, filename="file.pdf"):
    resp = client.post("/api/resources", json={
        "filename": filename,
        "url": f"https://example.com/{filename}",
        "mime_type": "application/pdf",
    }, headers={"X-User-Id": str(uid)})
    return resp.json()["id"]


# ---------------------------------------------------------------------------
# TC-JOUR-002: Anonymous browsing
# ---------------------------------------------------------------------------

def test_anonymous_browsing(client):
    """TC-JOUR-002: Anonymous users can browse published content but cannot
    access draft items by ID.

    Steps:
    1. Create an organizer user.
    2. Create a published category and a draft category.
    3. Create a published post and a draft post.
    4. Without X-User-Id, list categories -- both appear (listing does not
       filter by status, only by soft-delete).
    5. Without X-User-Id, list posts -- both appear (same reason).
    6. Without X-User-Id, GET draft category by ID -> 404.
    7. With creator's X-User-Id, GET draft category by ID -> 200.
    8. Without X-User-Id, GET draft post by ID -> 404.
    9. Without X-User-Id, GET published post by ID -> 200.
    """
    uid = _create_user(client, "anon_organizer", role="organizer")

    # Categories: one published, one draft
    pub_cat = _create_category(client, uid, name="Published Event", status="published")
    draft_cat = _create_category(client, uid, name="Draft Event", status="draft")

    # Posts: one published, one draft
    pub_post = _create_post(client, uid, title="Published Post", status="published")
    draft_post = _create_post(client, uid, title="Draft Post", status="draft")

    # --- List endpoints (no auth) ---
    # The list endpoints return all non-deleted records; they do NOT filter
    # by status.  Both published and draft items appear in the listing.
    cats_resp = client.get("/api/categories")
    assert cats_resp.status_code == 200
    cat_ids = [c["id"] for c in cats_resp.json()["items"]]
    assert pub_cat in cat_ids
    # Draft categories still appear in listing (no status filter on list)
    assert draft_cat in cat_ids

    posts_resp = client.get("/api/posts")
    assert posts_resp.status_code == 200
    post_ids = [p["id"] for p in posts_resp.json()["items"]]
    assert pub_post in post_ids
    # Draft posts still appear in listing (no status filter on list)
    assert draft_post in post_ids

    # --- Single-item endpoints (visibility enforcement) ---
    # Draft category: anonymous -> 404
    resp = client.get(f"/api/categories/{draft_cat}")
    assert resp.status_code == 404

    # Draft category: creator -> 200
    resp = client.get(
        f"/api/categories/{draft_cat}",
        headers={"X-User-Id": str(uid)},
    )
    assert resp.status_code == 200

    # Draft post: anonymous -> 404
    resp = client.get(f"/api/posts/{draft_post}")
    assert resp.status_code == 404

    # Published post: anonymous -> 200
    resp = client.get(f"/api/posts/{pub_post}")
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# TC-JOUR-005: Team join with approval
# ---------------------------------------------------------------------------

def test_team_join_approval_flow(client):
    """TC-JOUR-005: Full team join lifecycle with approval/rejection.

    Steps:
    1. Create Alice (organizer), Bob (participant), Carol (participant).
    2. Alice creates a group with require_approval=True.
    3. Carol applies to join -> status=pending.
    4. Alice approves Carol -> status=accepted, joined_at is set.
    5. Bob applies to join -> status=pending.
    6. Alice rejects Bob -> status=rejected.
    7. Bob wants to re-apply: must be removed first, then re-added.
    8. Verify final member list.
    """
    alice = _create_user(client, "alice", role="organizer")
    bob = _create_user(client, "bob", role="participant")
    carol = _create_user(client, "carol", role="participant")

    gid = _create_group(client, alice, name="Alpha Team", require_approval=True)

    # Carol applies
    resp = client.post(
        f"/api/groups/{gid}/members",
        json={"user_id": carol},
    )
    assert resp.status_code == 201
    assert resp.json()["status"] == "pending"

    # Alice approves Carol
    resp = client.patch(
        f"/api/groups/{gid}/members/{carol}",
        json={"status": "accepted"},
    )
    assert resp.status_code == 200
    carol_member = resp.json()
    assert carol_member["status"] == "accepted"
    assert carol_member["joined_at"] is not None

    # Bob applies
    resp = client.post(
        f"/api/groups/{gid}/members",
        json={"user_id": bob},
    )
    assert resp.status_code == 201
    assert resp.json()["status"] == "pending"

    # Alice rejects Bob
    resp = client.patch(
        f"/api/groups/{gid}/members/{bob}",
        json={"status": "rejected"},
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "rejected"

    # Bob tries to re-apply directly -> 409 (duplicate)
    resp = client.post(
        f"/api/groups/{gid}/members",
        json={"user_id": bob},
    )
    assert resp.status_code == 409

    # Remove Bob's membership record first
    resp = client.delete(f"/api/groups/{gid}/members/{bob}")
    assert resp.status_code == 204

    # Bob re-applies -> pending
    resp = client.post(
        f"/api/groups/{gid}/members",
        json={"user_id": bob},
    )
    assert resp.status_code == 201
    assert resp.json()["status"] == "pending"

    # Verify final member list
    resp = client.get(f"/api/groups/{gid}/members")
    assert resp.status_code == 200
    members = resp.json()
    assert members["total"] == 2  # Carol (accepted) + Bob (pending)


# ---------------------------------------------------------------------------
# TC-JOUR-007: Team registration for competition
# ---------------------------------------------------------------------------

def test_team_registration_flow(client):
    """TC-JOUR-007: A team registers for a competition and submits a post.

    Steps:
    1. Create organizer, Alice (participant), Bob (participant).
    2. Organizer creates group with require_approval=False so members are
       immediately accepted.
    3. Alice and Bob join the group.
    4. Organizer creates a published category.
    5. Organizer creates a rule with max_submissions=1 and links it to
       the category.
    6. Group registers for the category.
    7. Alice creates a submission post linked to the category.
    8. Verify the group appears in category groups.
    9. Verify Alice + Bob are group members.
    """
    organizer = _create_user(client, "org_007", role="organizer")
    alice = _create_user(client, "alice_007", role="participant")
    bob = _create_user(client, "bob_007", role="participant")

    # Create group (no approval required)
    gid = _create_group(client, organizer, name="Team007", require_approval=False)

    # Alice and Bob join
    resp_a = client.post(f"/api/groups/{gid}/members", json={"user_id": alice})
    assert resp_a.status_code == 201
    assert resp_a.json()["status"] == "accepted"

    resp_b = client.post(f"/api/groups/{gid}/members", json={"user_id": bob})
    assert resp_b.status_code == 201
    assert resp_b.json()["status"] == "accepted"

    # Create published category
    cat_id = _create_category(client, organizer, name="Hackathon 2025", status="published")

    # Create rule and link to category
    rule_id = _create_rule(client, organizer, name="Hackathon Rules", max_submissions=1)
    resp = client.post(
        f"/api/categories/{cat_id}/rules",
        json={"rule_id": rule_id, "priority": 1},
    )
    assert resp.status_code == 201

    # Register group for category
    resp = client.post(
        f"/api/categories/{cat_id}/groups",
        json={"group_id": gid},
    )
    assert resp.status_code == 201

    # Alice creates submission post
    post_id = _create_post(
        client, alice,
        title="Our Submission",
        post_type="proposal",
        status="published",
    )

    # Link post to category as submission
    resp = client.post(
        f"/api/categories/{cat_id}/posts",
        json={"post_id": post_id, "relation_type": "submission"},
    )
    assert resp.status_code == 201

    # Verify: group listed under category
    resp = client.get(f"/api/categories/{cat_id}/groups")
    assert resp.status_code == 200
    group_ids = [g["group_id"] for g in resp.json()]
    assert gid in group_ids

    # Verify: Alice + Bob are group members
    resp = client.get(f"/api/groups/{gid}/members")
    assert resp.status_code == 200
    member_user_ids = [m["user_id"] for m in resp.json()["items"]]
    assert alice in member_user_ids
    assert bob in member_user_ids


# ---------------------------------------------------------------------------
# TC-JOUR-009: Create posts (daily + competition)
# ---------------------------------------------------------------------------

def test_create_daily_and_competition_posts(client):
    """TC-JOUR-009: Create a general post and a proposal post linked
    to a competition category.

    Steps:
    1. Create user (organizer, to also create categories).
    2. Create a general post (published) -- publicly visible, no category.
    3. Create a proposal post with tags.
    4. Create a published category with a rule.
    5. Link the proposal post as a submission.
    """
    uid = _create_user(client, "creator_009", role="organizer")

    # General post
    general_pid = _create_post(
        client, uid,
        title="My Daily Thoughts",
        post_type="general",
        status="published",
    )
    resp = client.get(f"/api/posts/{general_pid}")
    assert resp.status_code == 200
    assert resp.json()["type"] == "general"
    assert resp.json()["status"] == "published"

    # proposal post with tags
    resp = client.post("/api/posts", json={
        "title": "Competition Entry",
        "type": "proposal",
        "status": "draft",
        "tags": ["AI", "innovation"],
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201
    comp_pid = resp.json()["id"]
    assert resp.json()["tags"] == ["AI", "innovation"]

    # Transition to published
    client.patch(
        f"/api/posts/{comp_pid}",
        json={"status": "pending_review"},
        headers={"X-User-Id": str(uid)},
    )
    client.patch(
        f"/api/posts/{comp_pid}",
        json={"status": "published"},
        headers={"X-User-Id": str(uid)},
    )

    # Create published category + rule
    cat_id = _create_category(client, uid, name="AI Challenge", status="published")
    rule_id = _create_rule(client, uid, name="Challenge Rules")
    client.post(
        f"/api/categories/{cat_id}/rules",
        json={"rule_id": rule_id, "priority": 1},
    )

    # Link post as submission
    resp = client.post(
        f"/api/categories/{cat_id}/posts",
        json={"post_id": comp_pid, "relation_type": "submission"},
    )
    assert resp.status_code == 201

    # Verify category-post relation
    h = {"X-User-Id": str(uid)}
    resp = client.get(f"/api/categories/{cat_id}/posts", headers=h)
    assert resp.status_code == 200
    post_ids = [r["post_id"] for r in resp.json()]
    assert comp_pid in post_ids


# ---------------------------------------------------------------------------
# TC-JOUR-010: Certificate flow
# ---------------------------------------------------------------------------

def test_certificate_flow(client):
    """TC-JOUR-010: Organizer issues a certificate to a participant after
    a competition closes.

    Steps:
    1. Create organizer, participant.
    2. Create and publish a category, then close it.
    3. Create a certificate resource (PDF).
    4. Create a certificate post.
    5. Link resource to post.
    6. Verify both post and resource are readable.
    """
    organizer = _create_user(client, "org_010", role="organizer")
    participant = _create_user(client, "part_010", role="participant")

    # Create category: draft -> published -> closed
    cat_id = _create_category(client, organizer, name="Design Contest", status="published")
    resp = client.patch(
        f"/api/categories/{cat_id}",
        json={"status": "closed"},
        headers={"X-User-Id": str(organizer)},
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "closed"

    # Create certificate resource
    res_id = _create_resource(client, organizer, filename="certificate_participant.pdf")
    assert res_id is not None

    # Create certificate post
    cert_post_id = _create_post(
        client, organizer,
        title="Certificate for Design Contest",
        post_type="certificate",
        status="published",
    )

    # Link resource to post
    resp = client.post(
        f"/api/posts/{cert_post_id}/resources",
        json={"resource_id": res_id, "display_type": "attachment"},
    )
    assert resp.status_code == 201

    # Verify post readable
    resp = client.get(f"/api/posts/{cert_post_id}")
    assert resp.status_code == 200
    assert resp.json()["type"] == "certificate"

    # Verify resource readable
    resp = client.get(f"/api/resources/{res_id}")
    assert resp.status_code == 200
    assert resp.json()["filename"] == "certificate_participant.pdf"

    # Verify post-resource relation
    resp = client.get(f"/api/posts/{cert_post_id}/resources")
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    assert resp.json()[0]["resource_id"] == res_id


# ---------------------------------------------------------------------------
# TC-JOUR-011-1: Edit own post (versioning via post_post reference)
# ---------------------------------------------------------------------------

def test_edit_own_post_versioning(client):
    """TC-JOUR-011-1: User edits their own post by creating a new version
    and linking it to the original via a post:post reference.

    Steps:
    1. User creates post v1 (published).
    2. User creates post v2 (published).
    3. Link v2 -> v1 via post_post reference.
    4. Both posts are readable.
    5. The relationship is queryable via GET /api/posts/{v2_id}/related.
    """
    uid = _create_user(client, "versioner", role="organizer")

    v1_id = _create_post(client, uid, title="My Post v1", status="published")
    v2_id = _create_post(client, uid, title="My Post v2", status="published")

    # Link v2 -> v1 as reference
    resp = client.post(
        f"/api/posts/{v2_id}/related",
        json={"target_post_id": v1_id, "relation_type": "reference"},
    )
    assert resp.status_code == 201
    rel = resp.json()
    assert rel["source_post_id"] == v2_id
    assert rel["target_post_id"] == v1_id
    assert rel["relation_type"] == "reference"

    # Both posts readable
    assert client.get(f"/api/posts/{v1_id}").status_code == 200
    assert client.get(f"/api/posts/{v2_id}").status_code == 200

    # Relationship queryable
    resp = client.get(f"/api/posts/{v2_id}/related")
    assert resp.status_code == 200
    related = resp.json()
    assert len(related) >= 1
    target_ids = [r["target_post_id"] for r in related]
    assert v1_id in target_ids


# ---------------------------------------------------------------------------
# TC-JOUR-011-2: Edit another's post (copy)
# ---------------------------------------------------------------------------

def test_edit_others_post_copy(client):
    """TC-JOUR-011-2: Bob copies Alice's post and links the copy back to
    Alice's original via a post:post reference.

    Steps:
    1. Alice creates a post.
    2. Bob creates a copy post and links it via post_post reference.
    3. Verify copy post's created_by == Bob.
    """
    alice = _create_user(client, "alice_copy", role="organizer")
    bob = _create_user(client, "bob_copy", role="organizer")

    alice_post = _create_post(client, alice, title="Alice Original", status="published")

    # Bob creates his copy
    bob_post = _create_post(client, bob, title="Bob Copy of Alice", status="published")

    # Link Bob's copy -> Alice's original
    resp = client.post(
        f"/api/posts/{bob_post}/related",
        json={"target_post_id": alice_post, "relation_type": "reference"},
    )
    assert resp.status_code == 201

    # Verify ownership
    resp = client.get(f"/api/posts/{bob_post}")
    assert resp.status_code == 200
    assert resp.json()["created_by"] == bob

    resp = client.get(f"/api/posts/{alice_post}")
    assert resp.status_code == 200
    assert resp.json()["created_by"] == alice


# ---------------------------------------------------------------------------
# TC-JOUR-012: Delete post cascade
# ---------------------------------------------------------------------------

def test_delete_post_full_cascade(client):
    """TC-JOUR-012: Delete a post and verify all related relations are
    cascade-cleaned.

    Steps:
    1. Create user, category, main post.
    2. Link post to category as submission.
    3. Create another post and link via post_post (embed).
    4. Create resource and link to post.
    5. Like, comment, and rate the post.
    6. DELETE the main post -> 204.
    7. Verify: GET main post -> 404.
    8. Verify: category_post relations cleared.
    9. Note: interactions are cascade-deleted with the post.
    """
    uid = _create_user(client, "deleter_012", role="organizer")
    h = {"X-User-Id": str(uid)}

    cat_id = _create_category(client, uid, name="Delete Test Event", status="published")
    post_id = _create_post(client, uid, title="Post to Delete", status="published")

    # Link post to category as submission
    resp = client.post(
        f"/api/categories/{cat_id}/posts",
        json={"post_id": post_id, "relation_type": "submission"},
    )
    assert resp.status_code == 201

    # Create another post and link via post_post embed
    embed_post = _create_post(client, uid, title="Embedded Content", status="published")
    resp = client.post(
        f"/api/posts/{post_id}/related",
        json={"target_post_id": embed_post, "relation_type": "embed"},
    )
    assert resp.status_code == 201

    # Create resource and link to post
    res_id = _create_resource(client, uid, filename="attachment.pdf")
    resp = client.post(
        f"/api/posts/{post_id}/resources",
        json={"resource_id": res_id, "display_type": "attachment"},
    )
    assert resp.status_code == 201

    # Like the post
    resp = client.post(f"/api/posts/{post_id}/like", headers=h)
    assert resp.status_code == 201

    # Comment on the post
    resp = client.post(
        f"/api/posts/{post_id}/comments",
        json={"type": "comment", "value": {"text": "Nice post!"}},
        headers=h,
    )
    assert resp.status_code == 201

    # Rate the post
    resp = client.post(
        f"/api/posts/{post_id}/ratings",
        json={"type": "rating", "value": {"quality": 90, "creativity": 85}},
        headers=h,
    )
    assert resp.status_code == 201

    # Verify relations exist before delete
    assert len(client.get(f"/api/categories/{cat_id}/posts", headers=h).json()) >= 1
    assert len(client.get(f"/api/posts/{post_id}/resources").json()) >= 1
    assert len(client.get(f"/api/posts/{post_id}/related").json()) >= 1
    post_data = client.get(f"/api/posts/{post_id}", headers=h).json()
    assert post_data["like_count"] == 1
    assert post_data["comment_count"] == 1

    # DELETE the post
    resp = client.delete(f"/api/posts/{post_id}", headers=h)
    assert resp.status_code == 204

    # Verify: GET post -> 404
    resp = client.get(f"/api/posts/{post_id}", headers=h)
    assert resp.status_code == 404

    # Verify: category_post relations cleared
    resp = client.get(f"/api/categories/{cat_id}/posts", headers=h)
    assert resp.status_code == 200
    remaining_post_ids = [r["post_id"] for r in resp.json()]
    assert post_id not in remaining_post_ids

    # Verify: embedded post and resource still exist (not cascade-deleted)
    assert client.get(f"/api/posts/{embed_post}", headers=h).status_code == 200
    assert client.get(f"/api/resources/{res_id}").status_code == 200


# ---------------------------------------------------------------------------
# TC-JOUR-013: Community interaction flow
# ---------------------------------------------------------------------------

def test_community_interaction_flow(client):
    """TC-JOUR-013: Multiple users interact with a post (like, comment, rate)
    and cached counters update correctly.

    Steps:
    1. Create Dave (organizer), Bob (participant), Judge (organizer).
    2. Dave creates a published post.
    3. Dave likes the post -> like_count=1.
    4. Dave likes again -> 409 (duplicate).
    5. Bob comments -> comment_count=1.
    6. Judge rates -> average_rating calculated.
    7. GET post -> verify like_count=1, comment_count=1, average_rating.
    8. Dave unlikes -> like_count=0.
    """
    dave = _create_user(client, "dave", role="organizer")
    bob = _create_user(client, "bob_013", role="participant")
    judge = _create_user(client, "judge", role="organizer")

    post_id = _create_post(client, dave, title="Community Post", status="published")

    # Dave likes the post
    resp = client.post(
        f"/api/posts/{post_id}/like",
        headers={"X-User-Id": str(dave)},
    )
    assert resp.status_code == 201
    assert resp.json()["liked"] is True

    # Verify like_count
    post_data = client.get(f"/api/posts/{post_id}").json()
    assert post_data["like_count"] == 1

    # Duplicate like rejected
    resp = client.post(
        f"/api/posts/{post_id}/like",
        headers={"X-User-Id": str(dave)},
    )
    assert resp.status_code == 409

    # Bob comments
    resp = client.post(
        f"/api/posts/{post_id}/comments",
        json={"type": "comment", "value": {"text": "Awesome project!"}},
        headers={"X-User-Id": str(bob)},
    )
    assert resp.status_code == 201
    assert resp.json()["type"] == "comment"

    # Verify comment_count
    post_data = client.get(f"/api/posts/{post_id}").json()
    assert post_data["comment_count"] == 1

    # Judge rates
    resp = client.post(
        f"/api/posts/{post_id}/ratings",
        json={
            "type": "rating",
            "value": {"quality": 90, "creativity": 85},
        },
        headers={"X-User-Id": str(judge)},
    )
    assert resp.status_code == 201

    # Verify all counters
    post_data = client.get(f"/api/posts/{post_id}").json()
    assert post_data["like_count"] == 1
    assert post_data["comment_count"] == 1
    assert post_data["average_rating"] is not None
    # average_rating = mean of (90+85)/2 = 87.5 for one rating
    assert post_data["average_rating"] == 87.5

    # Dave unlikes
    resp = client.delete(
        f"/api/posts/{post_id}/like",
        headers={"X-User-Id": str(dave)},
    )
    assert resp.status_code == 204

    # Verify like_count decremented
    post_data = client.get(f"/api/posts/{post_id}").json()
    assert post_data["like_count"] == 0
    # comment_count and average_rating unchanged
    assert post_data["comment_count"] == 1
    assert post_data["average_rating"] == 87.5
