请检查当前 @plans/biz-test/ 中的测试计划，是否完整覆盖了 @docs/command.md 和 @docs/user-journey.md 的所有设计
  ⎿  Listed directory plans/biz-test/
  ⎿  Read docs/command.md (1056 lines)
  ⎿  Read docs/user-journey.md (507 lines)

⏺ Let me read the test plan files to analyze coverage.

⏺ Read 2 files (ctrl+o to expand)

⏺ Now let me also check if there are any existing test data files to understand what's already been tested.

⏺ Searched for 1 pattern, read 1 file (ctrl+o to expand)

⏺ Below is the coverage analysis result, structured by the three dimensions defined in command.md and user-journey.md.

  ---
  Coverage Analysis Report

  Test Files Reviewed
  File: Skill test cases.md
  Focus: Post CRUD, Resource CRUD, category:post listing, Interaction & cache stats
  ────────────────────────────────────────
  File: Synnovator-Skills-Test-Yuxin.md
  Focus: Executable end-to-end test: user/category/group/rule/post/interaction, team approval, delete cascade
  ---
  1. Content Types CRUD Coverage (7 types)
  ┌─────────────┬───────────┬────────┬────────────────┬───────────────────┬──────────────────────────────────────────┐
  │  Content    │  CREATE   │  READ  │     UPDATE     │      DELETE       │             Coverage Source              │
  │    Type     │           │        │                │                   │                                          │
  ├─────────────┼───────────┼────────┼────────────────┼───────────────────┼──────────────────────────────────────────┤
  │ category    │ Yuxin 1.2 │ Yuxin  │ Yuxin (publish │ MISSING           │ No status flow draft->published->closed; │
  │             │           │ 1.2    │  only)         │                   │  no DELETE cascade test                  │
  ├─────────────┼───────────┼────────┼────────────────┼───────────────────┼──────────────────────────────────────────┤
  │ post        │ Both docs │ Both   │ Both docs      │ Yuxin 6           │ Good coverage                            │
  │             │           │ docs   │                │                   │                                          │
  ├─────────────┼───────────┼────────┼────────────────┼───────────────────┼──────────────────────────────────────────┤
  │ resource    │ Both docs │ Both   │ Skill          │ Skill TC-RES-031  │ Good coverage                            │
  │             │           │ docs   │ TC-RES-030     │                   │                                          │
  ├─────────────┼───────────┼────────┼────────────────┼───────────────────┼──────────────────────────────────────────┤
  │ rule        │ Yuxin     │ Yuxin  │ MISSING        │ MISSING           │ No UPDATE rule / DELETE rule tests       │
  │             │ 2.1, 2.2  │ 2.1    │                │                   │                                          │
  ├─────────────┼───────────┼────────┼────────────────┼───────────────────┼──────────────────────────────────────────┤
  │ user        │ Both docs │ Yuxin  │ MISSING        │ MISSING           │ No UPDATE user / DELETE user (cascade)   │
  │             │           │ 1.1    │                │                   │ tests                                    │
  ├─────────────┼───────────┼────────┼────────────────┼───────────────────┼──────────────────────────────────────────┤
  │ group       │ Yuxin 1.3 │ Yuxin  │ MISSING        │ MISSING           │ No UPDATE group / DELETE group tests     │
  │             │           │ 1.3    │                │                   │                                          │
  ├─────────────┼───────────┼────────┼────────────────┼───────────────────┼──────────────────────────────────────────┤
  │ interaction │ Both docs │ Both   │ MISSING        │ Skill             │ No UPDATE interaction (修改评论/评分)    │
  │             │           │ docs   │                │ TC-IACT-003/012   │ test                                     │
  └─────────────┴───────────┴────────┴────────────────┴───────────────────┴──────────────────────────────────────────┘
  2. Relationships Coverage (7 types)
  ┌────────────────────┬─────────────────┬────────────────────┬──────────┬──────────────────┬───────────────────────┐
  │    Relationship    │     CREATE      │        READ        │  UPDATE  │      DELETE      │          Gap          │
  ├────────────────────┼─────────────────┼────────────────────┼──────────┼──────────────────┼───────────────────────┤
  │ category:rule      │ Yuxin 2.1       │ Yuxin 2.1          │ MISSING  │ MISSING          │ No priority update /  │
  │                    │                 │                    │          │                  │ relation delete test  │
  ├────────────────────┼─────────────────┼────────────────────┼──────────┼──────────────────┼───────────────────────┤
  │ category:post      │ Both docs       │ Both docs (filter  │ MISSING  │ Yuxin 6 (cascade │ No UPDATE             │
  │                    │                 │ by relation_type)  │          │  only)           │ relation_type test    │
  ├────────────────────┼─────────────────┼────────────────────┼──────────┼──────────────────┼───────────────────────┤
  │ category:group     │ MISSING         │ MISSING            │ MISSING  │ MISSING          │ Completely absent     │
  ├────────────────────┼─────────────────┼────────────────────┼──────────┼──────────────────┼───────────────────────┤
  │ post:post          │ Both docs       │ Both docs          │ MISSING  │ MISSING          │ No UPDATE/DELETE      │
  │                    │                 │                    │          │                  │ relation test         │
  ├────────────────────┼─────────────────┼────────────────────┼──────────┼──────────────────┼───────────────────────┤
  │                    │ Skill           │ Skill              │          │ Skill TC-RES-031 │ No direct relation    │
  │ post:resource      │ TC-RES-010~012  │ TC-RES-010~012     │ MISSING  │  (via resource   │ DELETE; no UPDATE     │
  │                    │                 │                    │          │ delete)          │ display_type          │
  ├────────────────────┼─────────────────┼────────────────────┼──────────┼──────────────────┼───────────────────────┤
  │ group:user         │ Both docs       │ Yuxin 4.1          │ Yuxin    │ MISSING          │ No DELETE group:user  │
  │                    │                 │                    │ 4.1/4.2  │                  │ (移出成员) test       │
  ├────────────────────┼─────────────────┼────────────────────┼──────────┼──────────────────┼───────────────────────┤
  │ target:interaction │ Both docs       │ Both docs          │ N/A      │ MISSING          │ No direct relation    │
  │                    │                 │                    │          │                  │ DELETE test           │
  └────────────────────┴─────────────────┴────────────────────┴──────────┴──────────────────┴───────────────────────┘
  3. User Journeys Coverage (13 journeys)
  #: 1
  Journey: User Lifetime Overview
  Status: Implicit
  Gap: No end-to-end journey test
  ────────────────────────────────────────
  #: 2
  Journey: Browse Explore Page
  Status: MISSING
  Gap: Anonymous browsing, public listing, tag/type filters for visitors
  ────────────────────────────────────────
  #: 3
  Journey: Registration
  Status: Partial
  Gap: User creation covered; no registration flow (profile post auto-creation)
  ────────────────────────────────────────
  #: 4
  Journey: Login
  Status: MISSING
  Gap: No READ user authentication test
  ────────────────────────────────────────
  #: 5
  Journey: Join Group
  Status: Covered
  Gap: Yuxin 4.1/4.2 covers approval flow
  ────────────────────────────────────────
  #: 6
  Journey: Create Activity
  Status: Partial
  Gap: Category + rule created, but no complete flow: create -> edit -> add rule -> publish
  ────────────────────────────────────────
  #: 7
  Journey: Join Activity (Team Registration)
  Status: MISSING
  Gap: category:group relationship entirely untested
  ────────────────────────────────────────
  #: 8
  Journey: Create Team
  Status: Partial
  Gap: Group creation + owner covered; no invite/share link flow
  ────────────────────────────────────────
  #: 9
  Journey: Send Post
  Status: Covered
  Gap: Both daily and proposal posts tested
  ────────────────────────────────────────
  #: 10
  Journey: Get Certificate
  Status: MISSING
  Gap: No test for: close activity -> create cert resource -> link to user -> share cert post
  ────────────────────────────────────────
  #: 11
  Journey: Edit Post
  Status: Partial
  Gap: 11.1 self-edit version mgmt covered; 11.2 edit others' post entirely MISSING (permission request, copy
  creation)
  ────────────────────────────────────────
  #: 12
  Journey: Delete Post
  Status: Partial
  Gap: Soft delete + some cascade in Yuxin 6; but full cascade chain (category:post + post:post + post:resource + all
    interactions) not verified together
  ────────────────────────────────────────
  #: 13
  Journey: Community Interaction
  Status: Covered
  Gap: Like, comment (nested), rating all tested
  4. Data Integrity Constraints
  ┌─────────────────────────────────────────────────────┬──────────────────┬─────────────────────────────────────────┐
  │                     Constraint                      │      Status      │                   Gap                   │
  ├─────────────────────────────────────────────────────┼──────────────────┼─────────────────────────────────────────┤
  │ user username uniqueness                            │ Skill            │ Covered                                 │
  │                                                     │ TC-POST-903      │                                         │
  ├─────────────────────────────────────────────────────┼──────────────────┼─────────────────────────────────────────┤
  │ user email uniqueness                               │ Skill            │ Covered                                 │
  │                                                     │ TC-POST-903      │                                         │
  ├─────────────────────────────────────────────────────┼──────────────────┼─────────────────────────────────────────┤
  │ like uniqueness (created_by, target_type,           │ Both docs        │ Covered                                 │
  │ target_id)                                          │                  │                                         │
  ├─────────────────────────────────────────────────────┼──────────────────┼─────────────────────────────────────────┤
  │ category:rule uniqueness                            │ MISSING          │ No duplicate rule binding test          │
  ├─────────────────────────────────────────────────────┼──────────────────┼─────────────────────────────────────────┤
  │ category:group uniqueness                           │ MISSING          │ category:group entirely absent          │
  ├─────────────────────────────────────────────────────┼──────────────────┼─────────────────────────────────────────┤
  │ group:user uniqueness                               │ MISSING          │ No explicit duplicate member test       │
  ├─────────────────────────────────────────────────────┼──────────────────┼─────────────────────────────────────────┤
  │ Same user one group per category                    │ MISSING          │ Business-level cross constraint         │
  │                                                     │                  │ untested                                │
  └─────────────────────────────────────────────────────┴──────────────────┴─────────────────────────────────────────┘
  5. Soft Delete & Recovery
  Feature: Soft delete content types
  Status: Yuxin 6 (post only)
  Gap: Only post tested; category/rule/user/group/interaction soft delete untested
  ────────────────────────────────────────
  Feature: Cascade soft delete (post -> interactions)
  Status: Yuxin 6.3
  Gap: Partially covered
  ────────────────────────────────────────
  Feature: Cascade soft delete (category -> interactions)
  Status: MISSING
  Gap:
  ────────────────────────────────────────
  Feature: Cascade soft delete (user -> interactions + group:user)
  Status: MISSING
  Gap:
  ────────────────────────────────────────
  Feature: Recovery mechanism (restore deleted_at=NULL)
  Status: MISSING
  Gap: Entirely absent
  ────────────────────────────────────────
  Feature: Cascade recovery
  Status: MISSING
  Gap: Entirely absent
  ────────────────────────────────────────
  Feature: Admin-only recovery permission
  Status: MISSING
  Gap:
  6. Other Gaps
  Area: Interaction on non-post targets
  Gap: All tests use target_type=post; no tests for target_type=category or target_type=resource
  ────────────────────────────────────────
  Area: Permission boundary tests
  Gap: No systematic role-based permission tests (Organizer-only operations, Admin-only operations, cross-user
    visibility)
  ────────────────────────────────────────
  Area: Enumeration boundary
  Gap: Skill doc covers post type/status enums, but no tests for category.type, category.status, group.visibility,
    interaction.type/target_type invalid enums
  ────────────────────────────────────────
  Area: "Not create Only Select" rule
  Gap: Yuxin 5 simulates by tagging, but no actual rule enforcement test (engine doesn't block CREATE post based on
    rule)
  ---
  Summary

  Covered well (6/13 journeys, ~50% of CRUD):
  - Post full lifecycle (create all types, edit, version, status flow, delete)
  - Resource CRUD + post:resource relation
  - Interaction (like/comment/rating) + cache stats
  - Group:user approval workflow
  - category:post submission listing

  Critical gaps:

  1. category:group relationship -- entirely missing; blocks Journey 7 (team registration for activities)
  2. Certificate flow (Journey 10) -- no tests at all
  3. Anonymous browsing (Journey 2) and Login (Journey 4) -- not tested
  4. Edit others' post (Journey 11.2) -- permission request + copy model untested
  5. Soft delete for non-post types + recovery mechanism -- absent
  6. UPDATE/DELETE for rule, user, group, category -- largely missing
  7. Interaction on category/resource targets -- only post-targeted interactions tested
  8. Role-based permission enforcement -- no systematic coverage

  The test plans cover roughly 50-60% of what command.md and user-journey.md define. The most significant structural
  gap is the complete absence of category:group (team-activity binding), which is central to the competition
  participation flow.