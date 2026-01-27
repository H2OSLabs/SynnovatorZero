# Synnovator Skill — Test Results (Re-run)

**Date:** 2026-01-27
**Branch:** `test/biz-test`
**Engine:** `.claude/skills/synnovator/scripts/engine.py`
**Test data dir:** `.synnovator_test` (isolated from production `.synnovator/`)

---

## 1. Test Run: SynNovator-Skills-Test-Yuxin.md

**File:** `plans/biz-test/SynNovator-Skills-Test-Yuxin.md`
**Commit:** `e9e4b6c`
**Sections:** 7 (Section 0-7, excluding cleanup)

| Section | Description | Result |
|---------|-------------|--------|
| 0. Init | Clean + init `.synnovator_test` directory | PASS |
| 1. CRUD Basics | Create 5 users, category, group + group_user, resource | PASS |
| 2. Business Logic | Create rules (submission + select-only), posts (profile, submission, v2), versioning via post_post, review workflow (draft→pending_review→published/rejected) | PASS |
| 3. Relations & Cache Stats | Publish post, like + comment + rating interactions, verify `like_count`=1, `comment_count`=1, `average_rating`=83.85, duplicate like rejected | PASS |
| 4. Team Approval | Carol joins (pending→accepted), Bob joins (pending→rejected→re-apply pending) | PASS |
| 5. "Not Create Only Select" | Tag existing post with `+for_ai_hackathon` to simulate select-only enrollment | PASS |
| 6. Delete & Cascade | Soft-delete post → cascade category_post (empty), interaction (soft-deleted), post unreadable | PASS |
| 7. Cleanup | `rm -rf .synnovator_test` | PASS |

### Note — Shell `!` quoting issue

Comment value `"Great project! How does the AST parsing work?"` should avoid `!` in bash double-quoted strings. Workaround: use period instead. This is a shell quoting issue, not an engine bug.

---

## 2. Test Run: Fill-Gap-Yuxin.md

**File:** `plans/biz-test/Fill-Gap-Yuxin.md`
**Commit:** `b2727a3`
**Sections:** 14 (Section 0-14, excluding cleanup)

| Section | Description | Result |
|---------|-------------|--------|
| 0. Init & Setup | Create 6 users (alice, bob, carol, dave, judge, admin), category, rule, 2 groups, 2 posts | PASS |
| 1. UPDATE All Types | Update category (name, status), rule (allow_public, max_submissions), user (display_name, bio), group (visibility), resource (display_name, description), interaction (value), post tags (+/-), post body | PASS |
| 2. DELETE Non-Post | Delete rule (cascade category_rule), user (cascade interactions), group (cascade category_group), category (cascade category_rule + category_post + category_group) | PASS |
| 3. category:group | Register team, duplicate rejected, withdraw (delete category_group) | PASS |
| 4. Certificate Flow | Close category, create certificate resource, link to post via post_resource, create share post | PASS |
| 5. Relation UPDATE/DELETE | Update category_rule priority, add category_post reference, delete category_rule/group_user/post_post/post_resource (all verified empty + originals intact) | PASS |
| 6. Enum Validation | 6.1-6.5: Invalid category.type, post.status, user.role, group.visibility, interaction.type → all EXIT=1 | PASS |
| 6.6 | Invalid group_user.role="superadmin" → **EXIT=0 (BUG)** | **FAIL** |
| 7. Uniqueness | Duplicate category_rule, duplicate group_user (owner re-join), duplicate email → all EXIT=1 | PASS |
| 8. Edge Cases | Like deleted post, like nonexistent post, update deleted post, read nonexistent user, missing email, missing target_id → all EXIT=1 | PASS |
| 8.6-8.7 | 3-level nested comments, delete parent cascades all children (deleted_at set on L1 and L2) | PASS |
| 9. Private/Open Groups | Private group created, open group auto-accepts member (status=accepted, joined_at set) | PASS |
| 10. Non-Post Targets | Like category, comment on resource → both succeed | PASS |
| 11. Admin Role | Admin user readable (role=admin), admin creates category (type=operation, created_by=user_admin) | PASS |
| 12. Reply/Embed | post_post reply + embed (with position=1), read verified | PASS |
| 13. Rating | Rating with weighted dimensions, average_rating=77.5 (90×0.30 + 80×0.30 + 70×0.25 + 60×0.15) | PASS |
| 14. Cleanup | `rm -rf .synnovator_test` | PASS |

---

## 3. Bugs Found

### Bug 1: `create_relation` does not validate enum fields

**Severity:** Medium
**Location:** `engine.py` — `create_relation()` function (lines 399-429)
**Comparison:** `update_relation()` at lines 469-473 validates enum fields; `create_relation()` does not.

**Reproduction:**

```bash
uv run python .claude/skills/synnovator/scripts/engine.py \
  --data-dir .synnovator_test \
  create group_user \
  --data '{"group_id":"grp_alpha","user_id":"user_bob","role":"superadmin"}'
```

**Expected:** Exit code 1 — `superadmin` is not a valid value for `group_user.role`.
**Actual:** Exit code 0 — record created with invalid enum value.

**Affected fields (all relation enum fields per ENUMS definition):**

| Relation Type | Field | Valid Values (from ENUMS) |
|---------------|-------|--------------------------|
| `group_user` | `role` | `owner`, `admin`, `member` |
| `group_user` | `status` | `pending`, `accepted`, `rejected` |
| `category_post` | `relation_type` | `submission`, `reference` |
| `post_post` | `relation_type` | `reference`, `reply`, `embed` |
| `post_resource` | `display_type` | `attachment`, `inline` |

### Bug 2: `delete group` does not cascade `group_user` relations

**Severity:** Medium
**Location:** `engine.py` — `delete_content()` lines 386-387
**Spec reference:** `command.md` CRUD table (line 634): "DELETE group → 解除所有 group:user、category:group 关系"

**Current behavior:** Only cascades `category_group`, not `group_user`.
**Result:** Orphaned `group_user` records remain pointing to a soft-deleted group.

**Note:** The spec has a contradiction — cascade strategy table (line 452) says "group:user 关系保留（成员可查询历史）" vs CRUD table says "解除所有 group:user". Need spec clarification.

### Bug 3: `delete user` does not cascade `group_user` relations

**Severity:** Low
**Location:** `engine.py` — `delete_content()` lines 384-385
**Spec reference:** `command.md` CRUD table (line 633): "DELETE user → 解除所有 group:user 关系"

**Current behavior:** Only cascades user's interactions, not `group_user`.
**Result:** Orphaned `group_user` records remain pointing to a soft-deleted user.

**Note:** Spec contradiction — cascade strategy table (line 451) says "group:user 关系保留（标记为离组）" vs CRUD table says "解除所有 group:user 关系". Need spec clarification.

---

## 4. Summary

| Metric | Value |
|--------|-------|
| Total test sections executed | 21 |
| Sections passed | 20 |
| Sections failed | 1 (Section 6.6) |
| Bugs found | 3 |
| Shell workarounds needed | 1 (`!` in JSON strings) |
| Content types tested | 7/7 |
| Relation types tested | 7/7 |
| CRUD operations tested | Create, Read, Update, Delete (all) |
| Cascade scenarios tested | post→interactions/relations, user→interactions, category→relations, group→category_group, comment→child comments, rule→category_rule |
| Edge cases tested | 8 error paths (missing fields, unknown types, non-existent IDs, deleted targets, duplicates) |
| Enum validation tested | 6 content type enums (all pass) + 1 relation enum on create (FAIL) + relation enums on update (all pass) |
