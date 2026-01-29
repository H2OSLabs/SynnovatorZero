"""Resource transfer tests — covers TC-TRANSFER-001 through TC-TRANSFER-004

These tests verify that resources can be transferred between posts by
removing and re-linking post:resource relations, that shared linking works,
and that provenance can be tracked via post:post reference relations.
"""


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _create_user(client, username="transfer_user", role="organizer"):
    resp = client.post("/api/users", json={
        "username": username,
        "email": f"{username}@example.com",
        "role": role,
    })
    return resp.json()["id"]


def _create_post(client, uid, title="Transfer Post"):
    resp = client.post("/api/posts", json={
        "title": title,
        "type": "general",
        "status": "draft",
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201, f"Create post failed: {resp.json()}"
    return resp.json()["id"]


def _create_resource(client, uid, filename="doc.pdf"):
    resp = client.post("/api/resources", json={
        "filename": filename,
        "url": f"https://example.com/{filename}",
        "mime_type": "application/pdf",
    }, headers={"X-User-Id": str(uid)})
    assert resp.status_code == 201, f"Create resource failed: {resp.json()}"
    return resp.json()["id"]


def _link_resource(client, post_id, resource_id):
    resp = client.post(f"/api/posts/{post_id}/resources", json={
        "resource_id": resource_id,
        "display_type": "attachment",
    })
    assert resp.status_code == 201, f"Link resource failed: {resp.json()}"
    return resp.json()["id"]  # Returns the relation ID


def _get_post_resources(client, post_id):
    resp = client.get(f"/api/posts/{post_id}/resources")
    assert resp.status_code == 200
    return resp.json()


def _remove_post_resource(client, post_id, relation_id):
    resp = client.delete(f"/api/posts/{post_id}/resources/{relation_id}")
    assert resp.status_code == 204


# ---------------------------------------------------------------------------
# TC-TRANSFER-001: Certificate resource transfer from organizer to
#                  participant post
# ---------------------------------------------------------------------------

def test_transfer_001_resource_from_organizer_to_participant_post(client):
    """TC-TRANSFER-001: An organizer creates a certificate resource linked to
    a management post, then transfers it to a participant's submission post.

    Steps:
      1. Create organizer and participant users.
      2. Organizer creates a certificate resource.
      3. Organizer creates a management post and links the resource.
      4. Participant creates a submission post.
      5. Transfer: remove resource link from organizer's post, then add link
         to participant's post.
      6. Verify organizer's post has no resources.
      7. Verify participant's post now has the resource.
      8. Verify the resource entity itself was NOT deleted.
    """
    # -- Setup ---------------------------------------------------------------
    organizer_id = _create_user(client, username="org_user", role="organizer")
    participant_id = _create_user(client, username="part_user", role="participant")

    resource_id = _create_resource(client, organizer_id, filename="certificate.pdf")

    org_post_id = _create_post(client, organizer_id, title="Management Post")
    part_post_id = _create_post(client, participant_id, title="Submission Post")

    # Link resource to organizer's management post
    rel_id = _link_resource(client, org_post_id, resource_id)

    # Confirm the link exists
    org_resources_before = _get_post_resources(client, org_post_id)
    assert len(org_resources_before) == 1
    assert org_resources_before[0]["resource_id"] == resource_id

    # -- Transfer ------------------------------------------------------------
    _remove_post_resource(client, org_post_id, rel_id)
    _link_resource(client, part_post_id, resource_id)

    # -- Verify organizer's post is now empty --------------------------------
    org_resources_after = _get_post_resources(client, org_post_id)
    assert len(org_resources_after) == 0, (
        "Organizer's post should have no resources after transfer"
    )

    # -- Verify participant's post has the resource --------------------------
    part_resources = _get_post_resources(client, part_post_id)
    assert len(part_resources) == 1, (
        "Participant's post should have exactly one resource after transfer"
    )
    assert part_resources[0]["resource_id"] == resource_id

    # -- Verify resource entity itself is NOT deleted ------------------------
    res_resp = client.get(f"/api/resources/{resource_id}")
    assert res_resp.status_code == 200, (
        "Resource entity should still exist after relation transfer"
    )
    assert res_resp.json()["filename"] == "certificate.pdf"


# ---------------------------------------------------------------------------
# TC-TRANSFER-002: Resource transfer between posts owned by the same user
# ---------------------------------------------------------------------------

def test_transfer_002_resource_transfer_between_posts(client):
    """TC-TRANSFER-002: Move resource R from Post A to Post B (same user).

    Steps:
      1. User creates Post A, Post B, and Resource R.
      2. Link R to Post A as attachment.
      3. Link R to Post B (while still on A).
      4. Remove R's link from Post A.
      5. Verify Post A has no resources.
      6. Verify Post B has R.
      7. Verify R is still readable as an entity.
    """
    uid = _create_user(client, username="xfer_user", role="organizer")

    post_a_id = _create_post(client, uid, title="Post A")
    post_b_id = _create_post(client, uid, title="Post B")
    resource_id = _create_resource(client, uid, filename="transfer-doc.pdf")

    # Link to Post A
    rel_a_id = _link_resource(client, post_a_id, resource_id)

    # Also link to Post B (resource can exist on both during transition)
    _link_resource(client, post_b_id, resource_id)

    # Remove from Post A to complete the transfer
    _remove_post_resource(client, post_a_id, rel_a_id)

    # -- Verify Post A is empty ----------------------------------------------
    post_a_resources = _get_post_resources(client, post_a_id)
    assert len(post_a_resources) == 0, (
        "Post A should have no resources after transfer"
    )

    # -- Verify Post B has the resource --------------------------------------
    post_b_resources = _get_post_resources(client, post_b_id)
    assert len(post_b_resources) == 1
    assert post_b_resources[0]["resource_id"] == resource_id

    # -- Verify resource entity still readable -------------------------------
    res_resp = client.get(f"/api/resources/{resource_id}")
    assert res_resp.status_code == 200
    assert res_resp.json()["filename"] == "transfer-doc.pdf"


# ---------------------------------------------------------------------------
# TC-TRANSFER-003: Resource shared between multiple posts simultaneously
# ---------------------------------------------------------------------------

def test_transfer_003_resource_shared_between_posts(client):
    """TC-TRANSFER-003: A single resource linked to two posts at once.

    Steps:
      1. Create Post A and Post B.
      2. Link the same resource R to both posts.
      3. Both posts' resource lists contain R.
      4. Delete R's link from Post A.
      5. Post B still has R.
      6. Resource entity itself is unaffected.
    """
    uid = _create_user(client, username="shared_user", role="organizer")

    post_a_id = _create_post(client, uid, title="Shared Post A")
    post_b_id = _create_post(client, uid, title="Shared Post B")
    resource_id = _create_resource(client, uid, filename="shared-asset.pdf")

    # Link to both posts
    rel_a_id = _link_resource(client, post_a_id, resource_id)
    _link_resource(client, post_b_id, resource_id)

    # -- Both posts should list the resource ---------------------------------
    a_resources = _get_post_resources(client, post_a_id)
    b_resources = _get_post_resources(client, post_b_id)
    assert len(a_resources) == 1
    assert len(b_resources) == 1
    assert a_resources[0]["resource_id"] == resource_id
    assert b_resources[0]["resource_id"] == resource_id

    # -- Remove from Post A --------------------------------------------------
    _remove_post_resource(client, post_a_id, rel_a_id)

    # -- Post A empty, Post B still has it -----------------------------------
    a_resources_after = _get_post_resources(client, post_a_id)
    assert len(a_resources_after) == 0, (
        "Post A should have no resources after unlinking"
    )

    b_resources_after = _get_post_resources(client, post_b_id)
    assert len(b_resources_after) == 1, (
        "Post B should still have the resource"
    )
    assert b_resources_after[0]["resource_id"] == resource_id

    # -- Resource entity unaffected ------------------------------------------
    res_resp = client.get(f"/api/resources/{resource_id}")
    assert res_resp.status_code == 200
    assert res_resp.json()["filename"] == "shared-asset.pdf"


# ---------------------------------------------------------------------------
# TC-TRANSFER-004: Transfer with provenance tracking via post:post reference
# ---------------------------------------------------------------------------

def test_transfer_004_transfer_with_provenance(client):
    """TC-TRANSFER-004: Transfer resource from Post A to Post B and track
    provenance through a post:post reference relation.

    Steps:
      1. User creates Post A with Resource R attached.
      2. User creates Post B.
      3. Link Post B -> Post A via a post:post "reference" relation
         (provenance).
      4. Transfer R: remove from Post A, add to Post B.
      5. Verify Post B's post:post references include Post A.
      6. Verify Post B has R, Post A does not.
    """
    uid = _create_user(client, username="prov_user", role="organizer")

    post_a_id = _create_post(client, uid, title="Source Post A")
    resource_id = _create_resource(client, uid, filename="provenance-doc.pdf")

    # Attach resource to Post A
    rel_a_id = _link_resource(client, post_a_id, resource_id)

    # Create Post B
    post_b_id = _create_post(client, uid, title="Destination Post B")

    # Establish provenance: Post B references Post A
    prov_resp = client.post(f"/api/posts/{post_b_id}/related", json={
        "target_post_id": post_a_id,
        "relation_type": "reference",
    })
    assert prov_resp.status_code == 201, (
        f"Create post:post reference failed: {prov_resp.json()}"
    )
    prov_data = prov_resp.json()
    assert prov_data["source_post_id"] == post_b_id
    assert prov_data["target_post_id"] == post_a_id
    assert prov_data["relation_type"] == "reference"

    # -- Transfer resource: remove from A, add to B -------------------------
    _remove_post_resource(client, post_a_id, rel_a_id)
    _link_resource(client, post_b_id, resource_id)

    # -- Verify provenance: B's related posts include A ----------------------
    related_resp = client.get(f"/api/posts/{post_b_id}/related")
    assert related_resp.status_code == 200
    related = related_resp.json()
    assert len(related) >= 1, (
        "Post B should have at least one related-post entry"
    )
    target_ids = [r["target_post_id"] for r in related]
    assert post_a_id in target_ids, (
        "Post A should appear in Post B's related posts (provenance)"
    )

    # -- Verify resource ownership after transfer ----------------------------
    post_b_resources = _get_post_resources(client, post_b_id)
    assert len(post_b_resources) == 1
    assert post_b_resources[0]["resource_id"] == resource_id

    post_a_resources = _get_post_resources(client, post_a_id)
    assert len(post_a_resources) == 0, (
        "Post A should have no resources after transfer"
    )

    # -- Resource entity still exists ----------------------------------------
    res_resp = client.get(f"/api/resources/{resource_id}")
    assert res_resp.status_code == 200
    assert res_resp.json()["filename"] == "provenance-doc.pdf"
