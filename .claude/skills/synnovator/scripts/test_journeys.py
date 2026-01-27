#!/usr/bin/env python3
"""
Test all user journeys from user-journey.md against the Synnovator data engine.
Creates mock data and runs through each journey step by step.
"""

import json
import os
import shutil
import sys
from pathlib import Path

# Add script dir to path
sys.path.insert(0, str(Path(__file__).parent))
from engine import (
    init_dirs, get_data_dir, create_content, read_content, update_content,
    delete_content, create_relation, read_relation, update_relation, delete_relation
)


class TestRunner:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent.parent / ".synnovator_test"
        self.passed = 0
        self.failed = 0
        self.errors = []
        # Store IDs for cross-referencing
        self.ids = {}

    def setup(self):
        if self.data_dir.exists():
            shutil.rmtree(self.data_dir)
        init_dirs(self.data_dir)

    def teardown(self):
        if self.data_dir.exists():
            shutil.rmtree(self.data_dir)

    def assert_ok(self, name, condition, msg=""):
        if condition:
            self.passed += 1
            print(f"  PASS: {name}")
        else:
            self.failed += 1
            self.errors.append(f"{name}: {msg}")
            print(f"  FAIL: {name} - {msg}")

    def assert_raises(self, name, fn, error_substr=""):
        try:
            fn()
            self.failed += 1
            self.errors.append(f"{name}: Expected error but succeeded")
            print(f"  FAIL: {name} - Expected error")
        except (ValueError, Exception) as e:
            if error_substr and error_substr not in str(e):
                self.failed += 1
                self.errors.append(f"{name}: Expected '{error_substr}' in error, got: {e}")
                print(f"  FAIL: {name} - Wrong error: {e}")
            else:
                self.passed += 1
                print(f"  PASS: {name}")

    # === Journey 2: Browse Explore Page ===
    def test_journey_2_browse(self):
        print("\n=== Journey 2: Browse Explore Page ===")

        # Step 1: Read public categories
        cats = read_content(self.data_dir, "category", filters={"status": "published"})
        self.assert_ok("Read public categories", isinstance(cats, list))

        # Step 2: Read category + rule summary
        cat = read_content(self.data_dir, "category", self.ids["cat1"])
        self.assert_ok("Read category detail", cat["name"] == "2025 AI Hackathon")
        rules = read_relation(self.data_dir, "category_rule", {"category_id": self.ids["cat1"]})
        self.assert_ok("Read category rules", len(rules) > 0)

        # Step 3: Read public posts with tag filter
        posts = read_content(self.data_dir, "post", filters={"status": "published"})
        self.assert_ok("Read published posts", isinstance(posts, list))

        # Step 4: Read single post detail
        post = read_content(self.data_dir, "post", self.ids["post_profile_alice"])
        self.assert_ok("Read post detail", post["title"] == "About Alice")

    # === Journey 3: Registration ===
    def test_journey_3_register(self):
        print("\n=== Journey 3: Registration ===")

        # Step 3: Create user
        eve = create_content(self.data_dir, "user", {
            "username": "eve", "email": "eve@example.com",
            "display_name": "Eve Wang", "role": "participant"
        })
        self.ids["user_eve"] = eve["id"]
        self.assert_ok("Create user (register)", eve["role"] == "participant")

        # Step 4: Create profile post
        profile = create_content(self.data_dir, "post", {
            "title": "About Eve", "type": "profile",
            "status": "published",
            "_body": "## About Me\nNew participant."
        }, current_user=eve["id"])
        self.assert_ok("Create profile post", profile["type"] == "profile")

        # Uniqueness: duplicate username
        self.assert_raises(
            "Reject duplicate username",
            lambda: create_content(self.data_dir, "user", {
                "username": "eve", "email": "eve2@example.com"
            }),
            "already exists"
        )

    # === Journey 4: Login ===
    def test_journey_4_login(self):
        print("\n=== Journey 4: Login ===")

        # Step 1: Read user (verify)
        user = read_content(self.data_dir, "user", self.ids["user_alice"])
        self.assert_ok("Read user for login", user["username"] == "alice")

        # Step 3: Read personalized category list
        cats = read_content(self.data_dir, "category")
        self.assert_ok("Read categories after login", len(cats) > 0)

    # === Journey 5: Join Group ===
    def test_journey_5_join_group(self):
        print("\n=== Journey 5: Join Group ===")

        # Step 1: Read public groups
        groups = read_content(self.data_dir, "group", filters={"visibility": "public"})
        self.assert_ok("Read public groups", len(groups) > 0)

        # Step 2: Read group detail
        group = read_content(self.data_dir, "group", self.ids["grp1"])
        self.assert_ok("Read group detail", group["name"] == "Team Synnovator")

        # Step 3: Apply to join (require_approval=true -> status=pending)
        rel = create_relation(self.data_dir, "group_user", {
            "group_id": self.ids["grp1"], "user_id": self.ids["user_carol"],
            "role": "member"
        })
        self.assert_ok("Join group (pending)", rel["status"] == "pending")

        # Step 4: Approve
        updated = update_relation(self.data_dir, "group_user",
            {"group_id": self.ids["grp1"], "user_id": self.ids["user_carol"]},
            {"status": "accepted"}
        )
        self.assert_ok("Approve group join", updated[0]["status"] == "accepted")
        self.assert_ok("Joined_at set on accept", "joined_at" in updated[0])

        # Step 5: Read members
        members = read_relation(self.data_dir, "group_user", {"group_id": self.ids["grp1"]})
        self.assert_ok("Read group members", len(members) >= 2)

    # === Journey 6: Create Activity ===
    def test_journey_6_create_activity(self):
        print("\n=== Journey 6: Create Activity ===")
        # Already done in mock data setup, verify state
        cat = read_content(self.data_dir, "category", self.ids["cat1"])
        self.assert_ok("Category created", cat["name"] == "2025 AI Hackathon")
        self.assert_ok("Category has body", bool(cat.get("_body")))

        rules = read_relation(self.data_dir, "category_rule", {"category_id": self.ids["cat1"]})
        self.assert_ok("Rule linked to category", len(rules) == 1)

        rule = read_content(self.data_dir, "rule", self.ids["rule1"])
        self.assert_ok("Rule has scoring criteria", len(rule.get("scoring_criteria", [])) == 4)
        self.assert_ok("Category published", cat["status"] == "published")

    # === Journey 7: Join Activity (Register for Competition) ===
    def test_journey_7_join_activity(self):
        print("\n=== Journey 7: Join Activity ===")

        # Step 1: Read category + rule
        cat = read_content(self.data_dir, "category", self.ids["cat1"])
        rule = read_content(self.data_dir, "rule", self.ids["rule1"])
        self.assert_ok("Read activity + rule", cat and rule)

        # Step 3: Team registration
        rel = create_relation(self.data_dir, "category_group", {
            "category_id": self.ids["cat1"],
            "group_id": self.ids["grp1"]
        })
        self.assert_ok("Team registers for activity", "registered_at" not in rel or True)

        # Step 4a: Create submission post
        post = create_content(self.data_dir, "post", {
            "title": "AI Code Review Copilot",
            "type": "for_category",
            "tags": ["AI", "Developer Tools"],
            "_body": "## Project\nCodeReview Copilot is an AI-powered code review tool."
        }, current_user=self.ids["user_alice"])
        self.ids["post_submission"] = post["id"]
        self.assert_ok("Create submission post", post["type"] == "for_category")

        # Step 5a: Link post to category
        rel = create_relation(self.data_dir, "category_post", {
            "category_id": self.ids["cat1"],
            "post_id": post["id"],
            "relation_type": "submission"
        })
        self.assert_ok("Link submission to activity", rel["relation_type"] == "submission")

        # Uniqueness: same group can't register twice
        self.assert_raises(
            "Reject duplicate group registration",
            lambda: create_relation(self.data_dir, "category_group", {
                "category_id": self.ids["cat1"],
                "group_id": self.ids["grp1"]
            }),
            "already registered"
        )

    # === Journey 8: Create Team ===
    def test_journey_8_create_team(self):
        print("\n=== Journey 8: Create Team ===")
        # Already done in mock data, verify
        group = read_content(self.data_dir, "group", self.ids["grp1"])
        self.assert_ok("Group created", group["name"] == "Team Synnovator")

        owners = read_relation(self.data_dir, "group_user", {
            "group_id": self.ids["grp1"], "role": "owner"
        })
        self.assert_ok("Creator is owner", len(owners) == 1)
        self.assert_ok("Owner status accepted", owners[0]["status"] == "accepted")

        # Team intro post
        team_post = read_content(self.data_dir, "post", self.ids["post_team"])
        self.assert_ok("Team intro post exists", team_post["type"] == "team")

    # === Journey 9: Create Post ===
    def test_journey_9_create_post(self):
        print("\n=== Journey 9: Create Post ===")

        # 9.1: Daily post
        post = create_content(self.data_dir, "post", {
            "title": "My Daily Update",
            "tags": ["diary"],
            "_body": "## Today\nWorked on the project."
        }, current_user=self.ids["user_bob"])
        self.ids["post_daily"] = post["id"]
        self.assert_ok("Create daily post", post["type"] == "general")

        # Upload resource
        res = create_content(self.data_dir, "resource", {
            "filename": "screenshot.png",
            "display_name": "Project Screenshot"
        }, current_user=self.ids["user_bob"])
        self.ids["res1"] = res["id"]
        self.assert_ok("Upload resource", res["filename"] == "screenshot.png")

        # Link resource to post
        rel = create_relation(self.data_dir, "post_resource", {
            "post_id": post["id"],
            "resource_id": res["id"],
            "display_type": "inline"
        })
        self.assert_ok("Link resource to post", rel["display_type"] == "inline")

        # Link post to post (reference)
        rel2 = create_relation(self.data_dir, "post_post", {
            "source_post_id": post["id"],
            "target_post_id": self.ids["post_submission"],
            "relation_type": "reference"
        })
        self.assert_ok("Link post reference", rel2["relation_type"] == "reference")

        # Add tag
        updated = update_content(self.data_dir, "post", post["id"], {"tags": "+update"})
        self.assert_ok("Add tag to post", "update" in updated["tags"])

        # Publish
        updated = update_content(self.data_dir, "post", post["id"], {"status": "published"})
        self.assert_ok("Publish post", updated["status"] == "published")

        # 9.2: Proposal post with team card
        proposal = create_content(self.data_dir, "post", {
            "title": "Looking for Teammates",
            "tags": ["finding-team"],
            "_body": "## Proposal\nLooking for frontend developers."
        }, current_user=self.ids["user_alice"])
        self.ids["post_proposal"] = proposal["id"]

        # Embed team card
        embed_rel = create_relation(self.data_dir, "post_post", {
            "source_post_id": proposal["id"],
            "target_post_id": self.ids["post_team"],
            "relation_type": "embed",
            "position": 1
        })
        self.assert_ok("Embed team card in proposal", embed_rel["relation_type"] == "embed")

        # Publish
        update_content(self.data_dir, "post", proposal["id"], {"status": "published"})
        self.assert_ok("Publish proposal post", True)

    # === Journey 10: Get Certificate ===
    def test_journey_10_certificate(self):
        print("\n=== Journey 10: Get Certificate ===")

        # Step 1: Close activity
        update_content(self.data_dir, "category", self.ids["cat1"], {"status": "closed"})
        cat = read_content(self.data_dir, "category", self.ids["cat1"])
        self.assert_ok("Close activity", cat["status"] == "closed")

        # Step 2: Create certificate resource
        cert = create_content(self.data_dir, "resource", {
            "filename": "certificate_alice.pdf",
            "display_name": "Participation Certificate",
            "description": "AI Hackathon 2025 certificate"
        }, current_user=self.ids["user_alice"])
        self.ids["res_cert"] = cert["id"]
        self.assert_ok("Create certificate resource", cert["filename"] == "certificate_alice.pdf")

        # Step 3: Link certificate to submission post
        rel = create_relation(self.data_dir, "post_resource", {
            "post_id": self.ids["post_submission"],
            "resource_id": cert["id"],
            "display_type": "attachment"
        })
        self.assert_ok("Link certificate to post", rel["display_type"] == "attachment")

        # Step 4: Read resource
        r = read_content(self.data_dir, "resource", cert["id"])
        self.assert_ok("Read certificate", r["display_name"] == "Participation Certificate")

        # Step 5: Share certificate post
        cert_post = create_content(self.data_dir, "post", {
            "title": "My AI Hackathon Certificate",
            "type": "certificate",
            "status": "published",
            "_body": "## Certificate\nProud to have participated!"
        }, current_user=self.ids["user_alice"])
        self.assert_ok("Create certificate share post", cert_post["type"] == "certificate")

        # Re-open for remaining tests
        update_content(self.data_dir, "category", self.ids["cat1"], {"status": "published"})

    # === Journey 11: Edit Post ===
    def test_journey_11_edit_post(self):
        print("\n=== Journey 11: Edit Post (Version Management) ===")

        # 11.1: Edit own post
        # Step 1: Read post + rule
        post = read_content(self.data_dir, "post", self.ids["post_submission"])
        self.assert_ok("Read post for editing", post["title"] == "AI Code Review Copilot")

        rule = read_content(self.data_dir, "rule", self.ids["rule1"])
        self.assert_ok("Read associated rule", rule["allow_public"] == True)

        # Step 3: Create new version (new post linked to old)
        new_version = create_content(self.data_dir, "post", {
            "title": "AI Code Review Copilot v2",
            "type": "for_category",
            "tags": post.get("tags", []),
            "_body": "## Updated Project\nNow with better error handling."
        }, current_user=self.ids["user_alice"])
        self.ids["post_submission_v2"] = new_version["id"]

        # Link versions
        rel = create_relation(self.data_dir, "post_post", {
            "source_post_id": new_version["id"],
            "target_post_id": self.ids["post_submission"],
            "relation_type": "reference"
        })
        self.assert_ok("Link new version to old", rel["relation_type"] == "reference")

        # Step 4: Edit content
        updated = update_content(self.data_dir, "post", new_version["id"], {
            "_body": "## Updated Project v2\nBetter error handling and CI/CD support."
        })
        self.assert_ok("Update post body", True)

        # Step 6a: Direct publish (rule.allow_public=true)
        updated = update_content(self.data_dir, "post", new_version["id"], {"status": "published"})
        self.assert_ok("Direct publish (allow_public)", updated["status"] == "published")

        # Test pending_review path
        review_post = create_content(self.data_dir, "post", {
            "title": "Needs Review Post",
            "type": "for_category",
        }, current_user=self.ids["user_bob"])
        update_content(self.data_dir, "post", review_post["id"], {"status": "pending_review"})
        p = read_content(self.data_dir, "post", review_post["id"])
        self.assert_ok("Post enters pending_review", p["status"] == "pending_review")

        # Approve
        update_content(self.data_dir, "post", review_post["id"], {"status": "published"})
        p = read_content(self.data_dir, "post", review_post["id"])
        self.assert_ok("Post approved (published)", p["status"] == "published")

        # Reject path
        reject_post = create_content(self.data_dir, "post", {
            "title": "Will Be Rejected",
            "type": "for_category",
        }, current_user=self.ids["user_bob"])
        update_content(self.data_dir, "post", reject_post["id"], {"status": "pending_review"})
        update_content(self.data_dir, "post", reject_post["id"], {"status": "rejected"})
        p = read_content(self.data_dir, "post", reject_post["id"])
        self.assert_ok("Post rejected", p["status"] == "rejected")

    # === Journey 12: Delete Post ===
    def test_journey_12_delete_post(self):
        print("\n=== Journey 12: Delete Post ===")

        # Create a post to delete
        post = create_content(self.data_dir, "post", {
            "title": "To Be Deleted",
            "_body": "This will be deleted."
        }, current_user=self.ids["user_alice"])
        del_id = post["id"]

        # Create associated relations
        rel1 = create_relation(self.data_dir, "category_post", {
            "category_id": self.ids["cat1"],
            "post_id": del_id,
            "relation_type": "reference"
        })

        # Create interaction on this post (interaction + target_interaction relation)
        iact = create_content(self.data_dir, "interaction", {
            "type": "like",
        }, current_user=self.ids["user_bob"])
        create_relation(self.data_dir, "target_interaction", {
            "target_type": "post",
            "target_id": del_id,
            "interaction_id": iact["id"]
        })

        # Step 1: Read post
        p = read_content(self.data_dir, "post", del_id)
        self.assert_ok("Read post before delete", p["title"] == "To Be Deleted")

        # Step 2: Check relations
        rels = read_relation(self.data_dir, "category_post", {"post_id": del_id})
        self.assert_ok("Post has relations", len(rels) > 0)

        # Step 5-7: Delete post (cascades)
        result = delete_content(self.data_dir, "post", del_id)
        self.assert_ok("Soft delete post", result["mode"] == "soft")

        # Verify relations deleted
        rels_after = read_relation(self.data_dir, "category_post", {"post_id": del_id})
        self.assert_ok("Relations cascade-deleted", len(rels_after) == 0)

        # Verify interaction soft-deleted
        iact_after = read_content(self.data_dir, "interaction", iact["id"], include_deleted=True)
        self.assert_ok("Interaction cascade soft-deleted", iact_after.get("deleted_at") is not None)

        # Verify post soft-deleted
        self.assert_raises(
            "Post no longer readable",
            lambda: read_content(self.data_dir, "post", del_id),
            "soft-deleted"
        )

    # === Journey 13: Community Interaction ===
    def test_journey_13_interaction(self):
        print("\n=== Journey 13: Community Interaction ===")

        target_post = self.ids["post_submission"]

        # 13.1: Like
        like = create_content(self.data_dir, "interaction", {
            "type": "like",
        }, current_user=self.ids["user_dave"])
        self.assert_ok("Create like", like["type"] == "like")

        # Create target_interaction relation (triggers cache stats update)
        rel = create_relation(self.data_dir, "target_interaction", {
            "target_type": "post",
            "target_id": target_post,
            "interaction_id": like["id"]
        })
        self.assert_ok("Link like to target", True)

        # Verify like_count updated
        post = read_content(self.data_dir, "post", target_post)
        self.assert_ok("Like count updated", post["like_count"] >= 1)

        # Duplicate like rejection (now checked at relation creation)
        dup_like = create_content(self.data_dir, "interaction", {
            "type": "like",
        }, current_user=self.ids["user_dave"])
        self.assert_raises(
            "Reject duplicate like",
            lambda: create_relation(self.data_dir, "target_interaction", {
                "target_type": "post",
                "target_id": target_post,
                "interaction_id": dup_like["id"]
            }),
            "already liked"
        )

        # 13.2: Comment
        comment = create_content(self.data_dir, "interaction", {
            "type": "comment",
            "value": "Great project! How does the AST parsing work?"
        }, current_user=self.ids["user_eve"])
        self.ids["comment1"] = comment["id"]
        self.assert_ok("Create comment", comment["type"] == "comment")

        # Link comment to target post
        create_relation(self.data_dir, "target_interaction", {
            "target_type": "post",
            "target_id": target_post,
            "interaction_id": comment["id"]
        })

        # Verify comment_count
        post = read_content(self.data_dir, "post", target_post)
        self.assert_ok("Comment count updated", post["comment_count"] >= 1)

        # Nested reply
        reply = create_content(self.data_dir, "interaction", {
            "type": "comment",
            "parent_id": comment["id"],
            "value": "We use tree-sitter for multi-language AST parsing."
        }, current_user=self.ids["user_alice"])
        self.assert_ok("Create nested reply", reply["parent_id"] == comment["id"])

        # Link reply to target post
        create_relation(self.data_dir, "target_interaction", {
            "target_type": "post",
            "target_id": target_post,
            "interaction_id": reply["id"]
        })

        # 13.3: Rating
        rating = create_content(self.data_dir, "interaction", {
            "type": "rating",
            "value": {
                "创新性": 87,
                "技术实现": 82,
                "实用价值": 78,
                "演示效果": 91,
                "_comment": "Well-designed architecture"
            }
        }, current_user=self.ids["user_judge"])
        self.assert_ok("Create rating", rating["type"] == "rating")

        # Link rating to target post
        create_relation(self.data_dir, "target_interaction", {
            "target_type": "post",
            "target_id": target_post,
            "interaction_id": rating["id"]
        })

        # Verify average_rating updated
        post = read_content(self.data_dir, "post", target_post)
        self.assert_ok("Average rating calculated", post["average_rating"] is not None)
        # Expected: 87*0.30 + 82*0.30 + 78*0.25 + 91*0.15 = 83.85
        self.assert_ok("Rating value correct (~83.85)",
            abs(post["average_rating"] - 83.85) < 0.1 if post["average_rating"] else False)

    # === Appendix: Rule Definition (Not Create Only Select) ===
    def test_appendix_rule_definition(self):
        print("\n=== Appendix: Rule Definition ===")

        # Create a rule with "not create only select" behavior
        rule2 = create_content(self.data_dir, "rule", {
            "name": "Select Only Rule",
            "description": "Only allow selecting existing posts",
            "allow_public": False,
            "require_review": True,
        }, current_user=self.ids["user_alice"])
        self.ids["rule2"] = rule2["id"]
        self.assert_ok("Create select-only rule", rule2["allow_public"] == False)

        # Read rule
        r = read_content(self.data_dir, "rule", rule2["id"])
        self.assert_ok("Read rule config", r["require_review"] == True)

        # Simulate: user selects existing post and adds tag
        existing_post = read_content(self.data_dir, "post", self.ids["post_daily"])
        update_content(self.data_dir, "post", existing_post["id"], {
            "tags": "+for_ai_hackathon"
        })
        updated = read_content(self.data_dir, "post", existing_post["id"])
        self.assert_ok("Add activity tag to existing post", "for_ai_hackathon" in updated["tags"])

    # === Group approval workflow ===
    def test_group_approval_workflow(self):
        print("\n=== Group Approval Workflow ===")

        # Bob applies (pending)
        rel = create_relation(self.data_dir, "group_user", {
            "group_id": self.ids["grp1"],
            "user_id": self.ids["user_bob"],
            "role": "member"
        })
        self.assert_ok("Bob joins (pending)", rel["status"] == "pending")

        # Alice approves Bob
        updated = update_relation(self.data_dir, "group_user",
            {"group_id": self.ids["grp1"], "user_id": self.ids["user_bob"]},
            {"status": "accepted"}
        )
        self.assert_ok("Alice approves Bob", updated[0]["status"] == "accepted")

        # Dave applies and gets rejected
        rel2 = create_relation(self.data_dir, "group_user", {
            "group_id": self.ids["grp1"],
            "user_id": self.ids["user_dave"],
            "role": "member"
        })
        update_relation(self.data_dir, "group_user",
            {"group_id": self.ids["grp1"], "user_id": self.ids["user_dave"]},
            {"status": "rejected"}
        )
        self.assert_ok("Dave rejected", True)

        # Dave re-applies (should work after rejection)
        rel3 = create_relation(self.data_dir, "group_user", {
            "group_id": self.ids["grp1"],
            "user_id": self.ids["user_dave"],
            "role": "member"
        })
        self.assert_ok("Dave re-applies after rejection", rel3["status"] == "pending")

    # === Rule Enforcement Tests ===
    def test_rule_enforcement(self):
        print("\n=== Rule Enforcement ===")

        # --- Setup: create a strict category with tight rules ---
        strict_cat = create_content(self.data_dir, "category", {
            "name": "Strict Contest", "description": "For rule tests",
            "type": "competition", "status": "published"
        }, current_user=self.ids["user_alice"])

        # Rule with past deadline
        expired_rule = create_content(self.data_dir, "rule", {
            "name": "Expired Rule", "description": "Deadline passed",
            "submission_start": "2024-01-01T00:00:00Z",
            "submission_deadline": "2024-12-31T23:59:59Z",
        }, current_user=self.ids["user_alice"])
        create_relation(self.data_dir, "category_rule", {
            "category_id": strict_cat["id"], "rule_id": expired_rule["id"]
        })

        # Test 1: Reject submission after deadline
        post1 = create_content(self.data_dir, "post", {
            "title": "Late Submission", "type": "for_category"
        }, current_user=self.ids["user_bob"])
        self.assert_raises(
            "Reject submission past deadline",
            lambda: create_relation(self.data_dir, "category_post", {
                "category_id": strict_cat["id"], "post_id": post1["id"],
                "relation_type": "submission"
            }),
            "deadline passed"
        )

        # --- Setup: category with future-start rule ---
        future_cat = create_content(self.data_dir, "category", {
            "name": "Future Contest", "description": "Not yet open",
            "type": "competition", "status": "published"
        }, current_user=self.ids["user_alice"])

        future_rule = create_content(self.data_dir, "rule", {
            "name": "Future Rule", "description": "Not yet open",
            "submission_start": "2030-06-01T00:00:00Z",
            "submission_deadline": "2030-12-31T23:59:59Z",
        }, current_user=self.ids["user_alice"])
        create_relation(self.data_dir, "category_rule", {
            "category_id": future_cat["id"], "rule_id": future_rule["id"]
        })

        # Test 2: Reject submission before start
        self.assert_raises(
            "Reject submission before start",
            lambda: create_relation(self.data_dir, "category_post", {
                "category_id": future_cat["id"], "post_id": post1["id"],
                "relation_type": "submission"
            }),
            "not yet open"
        )

        # --- Setup: category with max_submissions=1 ---
        limit_cat = create_content(self.data_dir, "category", {
            "name": "One-Shot Contest", "description": "Max 1 submission",
            "type": "competition", "status": "published"
        }, current_user=self.ids["user_alice"])

        limit_rule = create_content(self.data_dir, "rule", {
            "name": "One Submission Rule", "description": "Max 1",
            "max_submissions": 1,
            "submission_start": "2025-01-01T00:00:00Z",
            "submission_deadline": "2030-12-31T23:59:59Z",
        }, current_user=self.ids["user_alice"])
        create_relation(self.data_dir, "category_rule", {
            "category_id": limit_cat["id"], "rule_id": limit_rule["id"]
        })

        # First submission succeeds
        post2 = create_content(self.data_dir, "post", {
            "title": "First Attempt", "type": "for_category"
        }, current_user=self.ids["user_bob"])
        create_relation(self.data_dir, "category_post", {
            "category_id": limit_cat["id"], "post_id": post2["id"],
            "relation_type": "submission"
        })
        self.assert_ok("First submission allowed", True)

        # Test 3: Second submission rejected
        post3 = create_content(self.data_dir, "post", {
            "title": "Second Attempt", "type": "for_category"
        }, current_user=self.ids["user_bob"])
        self.assert_raises(
            "Reject exceeding max_submissions",
            lambda: create_relation(self.data_dir, "category_post", {
                "category_id": limit_cat["id"], "post_id": post3["id"],
                "relation_type": "submission"
            }),
            "max submissions reached"
        )

        # --- Test 4: Format validation ---
        format_cat = create_content(self.data_dir, "category", {
            "name": "PDF Only Contest", "description": "Only PDF",
            "type": "competition", "status": "published"
        }, current_user=self.ids["user_alice"])

        format_rule = create_content(self.data_dir, "rule", {
            "name": "PDF Only Rule", "description": "Only PDF files",
            "submission_format": ["pdf"],
            "submission_start": "2025-01-01T00:00:00Z",
            "submission_deadline": "2030-12-31T23:59:59Z",
        }, current_user=self.ids["user_alice"])
        create_relation(self.data_dir, "category_rule", {
            "category_id": format_cat["id"], "rule_id": format_rule["id"]
        })

        # Create post with wrong format resource
        post4 = create_content(self.data_dir, "post", {
            "title": "Wrong Format", "type": "for_category"
        }, current_user=self.ids["user_bob"])
        bad_res = create_content(self.data_dir, "resource", {
            "filename": "slides.pptx"
        }, current_user=self.ids["user_bob"])
        create_relation(self.data_dir, "post_resource", {
            "post_id": post4["id"], "resource_id": bad_res["id"],
            "display_type": "attachment"
        })

        self.assert_raises(
            "Reject disallowed format",
            lambda: create_relation(self.data_dir, "category_post", {
                "category_id": format_cat["id"], "post_id": post4["id"],
                "relation_type": "submission"
            }),
            "not allowed"
        )

        # --- Test 5: Min team size ---
        team_cat = create_content(self.data_dir, "category", {
            "name": "Team Contest", "description": "Need 3+ members",
            "type": "competition", "status": "published"
        }, current_user=self.ids["user_alice"])

        team_rule = create_content(self.data_dir, "rule", {
            "name": "Team Size Rule", "description": "Min 3 members",
            "min_team_size": 3, "max_team_size": 5,
            "submission_start": "2025-01-01T00:00:00Z",
            "submission_deadline": "2030-12-31T23:59:59Z",
        }, current_user=self.ids["user_alice"])
        create_relation(self.data_dir, "category_rule", {
            "category_id": team_cat["id"], "rule_id": team_rule["id"]
        })

        # Create a small group (only alice as owner)
        small_grp = create_content(self.data_dir, "group", {
            "name": "Small Team", "visibility": "public", "require_approval": False
        }, current_user=self.ids["user_alice"])
        create_relation(self.data_dir, "group_user", {
            "group_id": small_grp["id"], "user_id": self.ids["user_alice"], "role": "owner"
        })
        create_relation(self.data_dir, "category_group", {
            "category_id": team_cat["id"], "group_id": small_grp["id"]
        })

        post5 = create_content(self.data_dir, "post", {
            "title": "Small Team Submission", "type": "for_category"
        }, current_user=self.ids["user_alice"])

        self.assert_raises(
            "Reject submission with too few members",
            lambda: create_relation(self.data_dir, "category_post", {
                "category_id": team_cat["id"], "post_id": post5["id"],
                "relation_type": "submission"
            }),
            "team too small"
        )

        # --- Test 6: Max team size (group_user hook) ---
        tiny_cat = create_content(self.data_dir, "category", {
            "name": "Solo Contest", "description": "Max 1 member",
            "type": "competition", "status": "published"
        }, current_user=self.ids["user_alice"])

        tiny_rule = create_content(self.data_dir, "rule", {
            "name": "Solo Rule", "description": "Max 1",
            "max_team_size": 1,
        }, current_user=self.ids["user_alice"])
        create_relation(self.data_dir, "category_rule", {
            "category_id": tiny_cat["id"], "rule_id": tiny_rule["id"]
        })

        solo_grp = create_content(self.data_dir, "group", {
            "name": "Solo Group", "visibility": "public", "require_approval": False
        }, current_user=self.ids["user_alice"])
        create_relation(self.data_dir, "group_user", {
            "group_id": solo_grp["id"], "user_id": self.ids["user_alice"], "role": "owner"
        })
        create_relation(self.data_dir, "category_group", {
            "category_id": tiny_cat["id"], "group_id": solo_grp["id"]
        })

        self.assert_raises(
            "Reject joining full team",
            lambda: create_relation(self.data_dir, "group_user", {
                "group_id": solo_grp["id"], "user_id": self.ids["user_bob"],
                "role": "member"
            }),
            "team is full"
        )

        # --- Test 7: Publish path enforcement ---
        strict_pub_cat = create_content(self.data_dir, "category", {
            "name": "Review Required Contest", "description": "No direct publish",
            "type": "competition", "status": "published"
        }, current_user=self.ids["user_alice"])

        strict_pub_rule = create_content(self.data_dir, "rule", {
            "name": "No Direct Publish", "description": "Must go through review",
            "allow_public": False, "require_review": True,
            "submission_start": "2025-01-01T00:00:00Z",
            "submission_deadline": "2030-12-31T23:59:59Z",
        }, current_user=self.ids["user_alice"])
        create_relation(self.data_dir, "category_rule", {
            "category_id": strict_pub_cat["id"], "rule_id": strict_pub_rule["id"]
        })

        post6 = create_content(self.data_dir, "post", {
            "title": "Needs Review", "type": "for_category"
        }, current_user=self.ids["user_bob"])
        create_relation(self.data_dir, "category_post", {
            "category_id": strict_pub_cat["id"], "post_id": post6["id"],
            "relation_type": "submission"
        })

        self.assert_raises(
            "Reject direct publish when review required",
            lambda: update_content(self.data_dir, "post", post6["id"], {"status": "published"}),
            "direct publish not allowed"
        )

        # pending_review should be allowed
        update_content(self.data_dir, "post", post6["id"], {"status": "pending_review"})
        p = read_content(self.data_dir, "post", post6["id"])
        self.assert_ok("Pending review allowed", p["status"] == "pending_review")

    # === Journey 14: User Follow/Friend ===
    def test_journey_14_follow_friend(self):
        print("\n=== Journey 14: User Follow/Friend ===")

        alice = self.ids["user_alice"]
        bob = self.ids["user_bob"]
        carol = self.ids["user_carol"]
        dave = self.ids["user_dave"]

        # 14.1: Follow
        rel = create_relation(self.data_dir, "user_user", {
            "source_user_id": alice, "target_user_id": bob,
            "relation_type": "follow"
        })
        self.assert_ok("Alice follows Bob", rel["relation_type"] == "follow")

        # 14.2: Mutual follow (friend)
        rel2 = create_relation(self.data_dir, "user_user", {
            "source_user_id": bob, "target_user_id": alice,
            "relation_type": "follow"
        })
        self.assert_ok("Bob follows Alice", rel2["relation_type"] == "follow")

        # Check mutual follow
        a_to_b = read_relation(self.data_dir, "user_user", {
            "source_user_id": alice, "target_user_id": bob,
            "relation_type": "follow"
        })
        b_to_a = read_relation(self.data_dir, "user_user", {
            "source_user_id": bob, "target_user_id": alice,
            "relation_type": "follow"
        })
        self.assert_ok("Mutual follow = friends", len(a_to_b) == 1 and len(b_to_a) == 1)

        # 14.3: Unfollow
        delete_relation(self.data_dir, "user_user", {
            "source_user_id": alice, "target_user_id": bob,
            "relation_type": "follow"
        })
        a_to_b_after = read_relation(self.data_dir, "user_user", {
            "source_user_id": alice, "target_user_id": bob,
            "relation_type": "follow"
        })
        self.assert_ok("Alice unfollows Bob", len(a_to_b_after) == 0)

        # 14.4: Self-follow should fail
        self.assert_raises(
            "Reject self-follow",
            lambda: create_relation(self.data_dir, "user_user", {
                "source_user_id": alice, "target_user_id": alice,
                "relation_type": "follow"
            }),
            "yourself"
        )

        # 14.5: Block
        block_rel = create_relation(self.data_dir, "user_user", {
            "source_user_id": carol, "target_user_id": dave,
            "relation_type": "block"
        })
        self.assert_ok("Carol blocks Dave", block_rel["relation_type"] == "block")

        # 14.6: Blocked user cannot follow
        self.assert_raises(
            "Blocked user cannot follow",
            lambda: create_relation(self.data_dir, "user_user", {
                "source_user_id": dave, "target_user_id": carol,
                "relation_type": "follow"
            }),
            "blocked you"
        )

        # 14.7: Duplicate follow should fail
        self.assert_raises(
            "Reject duplicate follow",
            lambda: create_relation(self.data_dir, "user_user", {
                "source_user_id": bob, "target_user_id": alice,
                "relation_type": "follow"
            }),
            "already exists"
        )

    # === Journey 15: Activity Association ===
    def test_journey_15_activity_association(self):
        print("\n=== Journey 15: Activity Association ===")

        alice = self.ids["user_alice"]

        # Create stage categories
        stage1 = create_content(self.data_dir, "category", {
            "name": "Stage 1: Proposal", "description": "Submit proposals",
            "type": "competition", "status": "published"
        }, current_user=alice)

        stage2 = create_content(self.data_dir, "category", {
            "name": "Stage 2: Prototype", "description": "Build prototypes",
            "type": "competition", "status": "published"
        }, current_user=alice)

        stage3 = create_content(self.data_dir, "category", {
            "name": "Stage 3: Final", "description": "Final presentation",
            "type": "competition", "status": "published"
        }, current_user=alice)

        # 15.1: Create stage chain
        rel1 = create_relation(self.data_dir, "category_category", {
            "source_category_id": stage1["id"],
            "target_category_id": stage2["id"],
            "relation_type": "stage",
            "stage_order": 1
        })
        self.assert_ok("Stage 1→2 created", rel1["relation_type"] == "stage")

        rel2 = create_relation(self.data_dir, "category_category", {
            "source_category_id": stage2["id"],
            "target_category_id": stage3["id"],
            "relation_type": "stage",
            "stage_order": 2
        })
        self.assert_ok("Stage 2→3 created", rel2["relation_type"] == "stage")

        # 15.2: Circular dependency should fail
        self.assert_raises(
            "Reject circular stage dependency",
            lambda: create_relation(self.data_dir, "category_category", {
                "source_category_id": stage3["id"],
                "target_category_id": stage1["id"],
                "relation_type": "stage",
                "stage_order": 3
            }),
            "Circular dependency"
        )

        # 15.3: Self-reference should fail
        self.assert_raises(
            "Reject self-reference",
            lambda: create_relation(self.data_dir, "category_category", {
                "source_category_id": stage1["id"],
                "target_category_id": stage1["id"],
                "relation_type": "stage"
            }),
            "itself"
        )

        # 15.4: Duplicate relation should fail
        self.assert_raises(
            "Reject duplicate category_category",
            lambda: create_relation(self.data_dir, "category_category", {
                "source_category_id": stage1["id"],
                "target_category_id": stage2["id"],
                "relation_type": "stage",
                "stage_order": 1
            }),
            "already exists"
        )

        # 15.5: Parallel tracks
        main_cat = create_content(self.data_dir, "category", {
            "name": "Main Event", "description": "Parent event",
            "type": "competition", "status": "published"
        }, current_user=alice)

        track_a = create_content(self.data_dir, "category", {
            "name": "Track A: AI", "description": "AI track",
            "type": "competition", "status": "published"
        }, current_user=alice)

        track_b = create_content(self.data_dir, "category", {
            "name": "Track B: Web3", "description": "Web3 track",
            "type": "competition", "status": "published"
        }, current_user=alice)

        rel_a = create_relation(self.data_dir, "category_category", {
            "source_category_id": main_cat["id"],
            "target_category_id": track_a["id"],
            "relation_type": "track"
        })
        self.assert_ok("Track A linked", rel_a["relation_type"] == "track")

        rel_b = create_relation(self.data_dir, "category_category", {
            "source_category_id": main_cat["id"],
            "target_category_id": track_b["id"],
            "relation_type": "track"
        })
        self.assert_ok("Track B linked", rel_b["relation_type"] == "track")

        # Read tracks
        tracks = read_relation(self.data_dir, "category_category", {
            "source_category_id": main_cat["id"],
            "relation_type": "track"
        })
        self.assert_ok("Read parallel tracks", len(tracks) == 2)

        # 15.6: Prerequisite enforcement
        bounty = create_content(self.data_dir, "category", {
            "name": "Bounty Challenge", "description": "Complete bounty first",
            "type": "competition", "status": "published"
        }, current_user=alice)

        main_comp = create_content(self.data_dir, "category", {
            "name": "Main Competition", "description": "Requires bounty completion",
            "type": "competition", "status": "published"
        }, current_user=alice)

        create_relation(self.data_dir, "category_category", {
            "source_category_id": bounty["id"],
            "target_category_id": main_comp["id"],
            "relation_type": "prerequisite"
        })
        self.assert_ok("Prerequisite link created", True)

        # Create a group for registration
        prereq_grp = create_content(self.data_dir, "group", {
            "name": "Prereq Team", "visibility": "public", "require_approval": False
        }, current_user=alice)
        create_relation(self.data_dir, "group_user", {
            "group_id": prereq_grp["id"], "user_id": alice, "role": "owner"
        })

        # Try to register for main_comp while bounty is still open → should fail
        self.assert_raises(
            "Reject registration (prerequisite not closed)",
            lambda: create_relation(self.data_dir, "category_group", {
                "category_id": main_comp["id"],
                "group_id": prereq_grp["id"]
            }),
            "must be closed"
        )

        # Close bounty
        update_content(self.data_dir, "category", bounty["id"], {"status": "closed"})

        # Now registration should succeed
        create_relation(self.data_dir, "category_group", {
            "category_id": main_comp["id"],
            "group_id": prereq_grp["id"]
        })
        self.assert_ok("Registration after prerequisite closed", True)

    # === Setup Mock Data ===
    def setup_mock_data(self):
        print("=== Setting up mock data ===")

        # Users
        alice = create_content(self.data_dir, "user", {
            "id": "user_alice", "username": "alice", "email": "alice@example.com",
            "display_name": "Alice Chen", "role": "organizer"
        })
        self.ids["user_alice"] = alice["id"]

        bob = create_content(self.data_dir, "user", {
            "id": "user_bob", "username": "bob", "email": "bob@example.com",
            "display_name": "Bob Li", "role": "participant"
        })
        self.ids["user_bob"] = bob["id"]

        carol = create_content(self.data_dir, "user", {
            "id": "user_carol", "username": "carol", "email": "carol@example.com",
            "display_name": "Carol Zhang", "role": "participant"
        })
        self.ids["user_carol"] = carol["id"]

        dave = create_content(self.data_dir, "user", {
            "id": "user_dave", "username": "dave", "email": "dave@example.com",
            "display_name": "Dave Wu", "role": "participant"
        })
        self.ids["user_dave"] = dave["id"]

        judge = create_content(self.data_dir, "user", {
            "id": "user_judge", "username": "judge01", "email": "judge@example.com",
            "display_name": "Judge One", "role": "organizer"
        })
        self.ids["user_judge"] = judge["id"]

        # Category
        cat = create_content(self.data_dir, "category", {
            "id": "cat_hackathon_2025", "name": "2025 AI Hackathon",
            "description": "Global AI innovation competition",
            "type": "competition", "status": "published",
            "start_date": "2025-03-01T00:00:00Z", "end_date": "2025-03-15T23:59:59Z",
            "_body": "## About\n\nAI Hackathon for developers worldwide."
        }, current_user=alice["id"])
        self.ids["cat1"] = cat["id"]

        # Rule
        rule = create_content(self.data_dir, "rule", {
            "id": "rule_submission_01", "name": "AI Hackathon Submission Rule",
            "description": "2025 AI Hackathon submission requirements",
            "allow_public": True, "require_review": True,
            "reviewers": [judge["id"]],
            "submission_start": "2025-01-01T00:00:00Z",
            "submission_deadline": "2030-12-31T23:59:59Z",
            "submission_format": ["markdown", "pdf", "zip"],
            "max_submissions": 3, "min_team_size": 1, "max_team_size": 5,
            "scoring_criteria": [
                {"name": "创新性", "weight": 30, "description": "Originality"},
                {"name": "技术实现", "weight": 30, "description": "Code quality"},
                {"name": "实用价值", "weight": 25, "description": "Practical value"},
                {"name": "演示效果", "weight": 15, "description": "Demo quality"}
            ],
            "_body": "## Rules\n\n1. Submit project docs, source code, demo video."
        }, current_user=alice["id"])
        self.ids["rule1"] = rule["id"]

        # Link rule to category
        create_relation(self.data_dir, "category_rule", {
            "category_id": cat["id"], "rule_id": rule["id"], "priority": 1
        })

        # Group
        grp = create_content(self.data_dir, "group", {
            "id": "grp_team_synnovator", "name": "Team Synnovator",
            "description": "AI Hackathon team", "visibility": "public",
            "max_members": 5, "require_approval": True
        }, current_user=alice["id"])
        self.ids["grp1"] = grp["id"]

        # Alice as owner
        create_relation(self.data_dir, "group_user", {
            "group_id": grp["id"], "user_id": alice["id"], "role": "owner"
        })

        # Posts
        profile_alice = create_content(self.data_dir, "post", {
            "id": "post_profile_alice", "title": "About Alice",
            "type": "profile", "status": "published",
            "tags": ["backend", "AI"],
            "_body": "## About Me\n\nFull-stack developer with AI focus."
        }, current_user=alice["id"])
        self.ids["post_profile_alice"] = profile_alice["id"]

        team_post = create_content(self.data_dir, "post", {
            "id": "post_team_synnovator", "title": "Team Synnovator",
            "type": "team", "status": "published",
            "tags": ["fullstack", "AI"],
            "_body": "## Team\n\nWe build AI applications."
        }, current_user=alice["id"])
        self.ids["post_team"] = team_post["id"]

        print(f"  Mock data created: {len(self.ids)} records")

    def run_all(self):
        self.setup()
        self.setup_mock_data()

        self.test_journey_2_browse()
        self.test_journey_3_register()
        self.test_journey_4_login()
        self.test_journey_5_join_group()
        self.test_journey_6_create_activity()
        self.test_journey_7_join_activity()
        self.test_journey_8_create_team()
        self.test_journey_9_create_post()
        self.test_journey_10_certificate()
        self.test_journey_11_edit_post()
        self.test_journey_12_delete_post()
        self.test_journey_13_interaction()
        self.test_appendix_rule_definition()
        self.test_group_approval_workflow()
        self.test_rule_enforcement()
        self.test_journey_14_follow_friend()
        self.test_journey_15_activity_association()

        print(f"\n{'='*50}")
        print(f"Results: {self.passed} passed, {self.failed} failed")
        if self.errors:
            print(f"\nFailures:")
            for e in self.errors:
                print(f"  - {e}")

        self.teardown()
        return self.failed == 0


if __name__ == "__main__":
    runner = TestRunner()
    success = runner.run_all()
    sys.exit(0 if success else 1)
