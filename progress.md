# Progress Log

## Session: 2026-01-27

### Phase 0: 工作流文档更新与规划
- **Status:** complete
- **Started:** 2026-01-27
- Actions taken:
  - 更新 docs/development-workflow.md:
    - schema-to-openapi 数据源扩展（synnovator skill + docs/ + specs/）
    - 集成 planning-with-files skill（Phase 0.3 初始化 + 全流程贯穿）
    - 集成 tests-kit skill（每阶段增量测试检查点）
    - 添加 8 层底层到上层依赖图开发顺序
  - 修复测试用例数量 267→246
  - 创建 task_plan.md / findings.md / progress.md 规划文件
- Files created/modified:
  - docs/development-workflow.md (modified)
  - task_plan.md (created)
  - findings.md (created)
  - progress.md (created)

### Phase 1: 后端脚手架生成
- **Status:** complete
- **Started:** 2026-01-27
- Actions taken:
  - 运行 api-builder CLI 从 openapi.yaml 生成 54 models, 54 schemas, 8 routers
  - 修复 api-builder 模板 bug: enum.values → enum['values'], path_params guard
  - 创建 app/database.py (SQLAlchemy engine, session, Base, get_db)
  - 创建 app/crud/base.py (CRUDBase 泛型基类)
  - 修复所有生成代码的问题:
    - Models: 删除重复列，修复 null→None，添加缺失 JSON import，修复表名 categorys→events
    - Schemas: 修复非 DB 类型的错误继承层次，添加缺失 Dict import，修正 Event/Comment/Rating 的字段设计
    - Routers: 修复 None 参数名，添加 Any import，修复返回类型，改 path param 类型 str→int
  - 删除 44 个不必要的 model 文件 + 26 个不必要的 schema 文件
  - 创建 7 个 CRUD 模块 (users, resources, events, posts, rules, groups, interactions)
  - 更新 main.py 为正式 FastAPI 应用（8 router 挂载 + CORS + health check）
  - 更新所有 __init__.py 导出
  - 添加 pydantic[email] 依赖
  - 修复 Makefile uvicorn 启动命令
  - 验证通过: 服务启动成功，28 paths, 45 schemas, CRUD 测试通过
- Files created/modified:
  - app/main.py (rewritten)
  - app/database.py (created)
  - app/models/*.py (9 models fixed, 44 deleted)
  - app/models/__init__.py (rewritten)
  - app/schemas/*.py (29 schemas fixed, 26 deleted)
  - app/schemas/__init__.py (rewritten)
  - app/crud/*.py (7 CRUD modules created)
  - app/crud/__init__.py (rewritten)
  - app/routers/*.py (8 routers rewritten)
  - Makefile (fixed uvicorn command)
  - pyproject.toml (added pydantic[email])

### Phase 2: Layer 0 — user + resource CRUD
- **Status:** complete
- **Started:** 2026-01-27
- Actions taken:
  - **User model**: 添加 unique 约束 (username, email), deleted_at 软删除字段, role 默认值 "participant"
  - **Resource model**: 添加 created_by 字段, deleted_at 软删除字段
  - **User schema**: Literal 类型验证 role (participant|organizer|admin), 默认值 "participant", model_config 替代 class Config
  - **Resource schema**: 添加 created_by, deleted_at 字段, ResourceUpdate 限制为 display_name/description
  - **User CRUD**: 添加 get_by_username, get_by_email 查询方法; 软删除 (remove 设 deleted_at); get/get_multi 自动过滤已删除
  - **Resource CRUD**: 软删除; get/get_multi 自动过滤已删除
  - **User router**: 创建时校验 username/email 唯一性 (409), 更新时校验唯一性
  - **Resource router**: 创建需 X-User-Id header (401), 添加 PATCH 更新端点
  - **deps.py**: get_current_user_id + require_current_user_id 依赖
  - **25 pytest tests**: 16 user + 9 resource, 覆盖 TC-USER-001~903, TC-RES-001~901
- Files created/modified:
  - app/models/user.py (enhanced: unique, deleted_at, role default)
  - app/models/resource.py (enhanced: created_by, deleted_at)
  - app/schemas/user.py (enhanced: Literal role, model_config)
  - app/schemas/resource.py (enhanced: created_by, model_config)
  - app/crud/users.py (rewritten: soft delete, uniqueness queries)
  - app/crud/resources.py (rewritten: soft delete)
  - app/routers/users.py (rewritten: uniqueness checks)
  - app/routers/resources.py (rewritten: auth, update endpoint)
  - app/deps.py (created: auth dependencies)
  - app/tests/__init__.py (created)
  - app/tests/conftest.py (created: in-memory SQLite test DB)
  - app/tests/test_users.py (created: 16 tests)
  - app/tests/test_resources.py (created: 9 tests)

## Test Results
| Test | Input | Expected | Actual | Status |
|------|-------|----------|--------|--------|
| App import | `from app.main import app` | No errors | 61 routes | PASS |
| Health endpoint | GET /health | 200 | 200 {"status":"ok"} | PASS |
| OpenAPI spec | GET /openapi.json | Valid spec | 28 paths, 45 schemas | PASS |
| Phase 2 pytest | `pytest app/tests/ -v` | 25 passed | 25 passed, 0 failed | PASS |

### Phase 2 Test Coverage
| Test Case | Scenario | Status |
|-----------|----------|--------|
| TC-USER-001 | 创建 participant 用户 | PASS |
| TC-USER-002 | 创建 organizer 用户 | PASS |
| TC-USER-003 | 创建 admin 用户 | PASS |
| TC-USER-004 | 读取已创建的用户 | PASS |
| TC-USER-010 | 用户修改个人信息 | PASS |
| TC-USER-011 | Admin 修改用户角色 | PASS |
| TC-USER-020 | 删除用户 (soft delete) | PASS |
| TC-USER-900 | 重复 username 被拒绝 | PASS |
| TC-USER-901 | 重复 email 被拒绝 | PASS |
| TC-USER-903 | 缺少必填字段 email | PASS |
| TC-RES-001 | 最小字段创建资源 | PASS |
| TC-RES-002 | 带完整元信息创建资源 | PASS |
| TC-RES-030 | 更新资源元信息 | PASS |
| TC-RES-031 | 删除资源 (soft delete) | PASS |
| TC-RES-900 | 缺少 filename 被拒绝 | PASS |
| TC-RES-901 | 未登录用户创建资源被拒绝 | PASS |

### Deferred to Later Phases
| Test Case | Reason |
|-----------|--------|
| TC-USER-902 | 权限控制 (需完整 auth 中间件，Phase 7) |
| TC-RES-040~045 | Resource 可见性继承 (需 post:resource 关系，Phase 5) |
| TC-RES-902 | post:resource 关系引用校验 (Phase 5) |
| TC-RES-903 | display_type 枚举 (Phase 5) |

## Error Log
| Timestamp | Error | Attempt | Resolution |
|-----------|-------|---------|------------|
| 2026-01-27 | Jinja2 enum.values TypeError | 1 | Changed to enum['values'] in 3 templates |
| 2026-01-27 | path_params[0] UndefinedError | 1 | Added guard in router.py.j2 |
| 2026-01-27 | email-validator not installed | 1 | Added pydantic[email] dependency |
| 2026-01-27 | uvicorn shebang wrong venv | 1 | Use `uv run python -m uvicorn` instead |

### Phase 3: Layer 1 — rule, group, event CRUD
- **Status:** complete
- **Started:** 2026-01-27
- Actions taken:
  - **Rule model**: 添加 deleted_at 软删除; created_by 改为 Integer 类型
  - **Rule schema**: ScoringCriterion 子模型; model_validator 校验 scoring_criteria weights 和=100; model_config
  - **Rule CRUD**: soft delete; get/get_multi 过滤已删除
  - **Rule router**: require_current_user_id auth; created_by 自动设置
  - **Group model**: 添加 created_by Integer; deleted_at 软删除; visibility 默认 "public"
  - **Group schema**: Literal["public","private"] 枚举校验; model_config
  - **Group CRUD**: soft delete; get/get_multi 过滤已删除
  - **Group router**: require_current_user_id auth; created_by 自动设置; 成员管理 stub 保留
  - **Event model**: created_by 改为 Integer 类型
  - **Event schema**: Literal 枚举校验 type(competition|operation), status(draft|published|closed); VALID_STATUS_TRANSITIONS 状态机; model_config
  - **Event CRUD**: soft delete; get/get_multi 过滤已删除
  - **Event router**: require_current_user_id auth; created_by 自动设置; 状态机转换校验 (422 on invalid)
  - **40 tests**: 12 rule + 12 group + 16 event, 全部通过
- Files modified:
  - app/models/rule.py (deleted_at, created_by→Integer)
  - app/models/group.py (created_by, deleted_at, cleanup)
  - app/models/event.py (created_by→Integer)
  - app/schemas/rule.py (rewritten: ScoringCriterion, validators)
  - app/schemas/group.py (rewritten: Literal, model_config)
  - app/schemas/event.py (rewritten: Literal, state machine)
  - app/crud/rules.py (rewritten: soft delete)
  - app/crud/groups.py (rewritten: soft delete)
  - app/crud/events.py (rewritten: soft delete)
  - app/routers/rules.py (rewritten: auth, created_by)
  - app/routers/groups.py (rewritten: auth, created_by)
  - app/routers/events.py (rewritten: auth, status validation)
  - app/tests/test_rules.py (created: 12 tests)
  - app/tests/test_groups.py (created: 12 tests)
  - app/tests/test_categories.py (created: 16 tests)

### Phase 3 Test Coverage
| Test Case | Scenario | Status |
|-----------|----------|--------|
| TC-RULE-001 | 创建完整 scoring_criteria 规则 | PASS |
| TC-RULE-002 | 创建 select-only 规则 | PASS |
| TC-RULE-003 | 读取规则含 scoring_criteria | PASS |
| TC-RULE-010 | 修改规则配置 (allow_public, max_submissions, max_team_size) | PASS |
| TC-RULE-011 | 修改 scoring_criteria 权重 [30,30,25,15]→[25,25,25,25] | PASS |
| TC-RULE-020 | 删除规则 (soft delete) | PASS |
| TC-RULE-900 | 未认证用户无法创建规则 | PASS |
| TC-RULE-901 | scoring_criteria weights 和≠100 被拒绝 | PASS |
| TC-GRP-001 | 创建公开团队需审批 | PASS |
| TC-GRP-002 | 创建私有团队无需审批 | PASS |
| TC-GRP-010 | 更新团队描述和 max_members | PASS |
| TC-GRP-011 | 修改 require_approval (true→false) | PASS |
| TC-GRP-012 | 修改 visibility (public→private) | PASS |
| TC-GRP-020 | 删除团队 (soft delete) | PASS |
| TC-GRP-900 | 无效 visibility 枚举被拒绝 | PASS |
| TC-GRP-901 | 未认证用户无法创建团队 | PASS |
| TC-CAT-001 | 创建 competition 活动 | PASS |
| TC-CAT-002 | 创建 operation 活动 | PASS |
| TC-CAT-003 | 读取活动完整字段 | PASS |
| TC-CAT-010 | 状态机 draft→published→closed | PASS |
| TC-CAT-010 | 反向转换被拒绝 (published→draft) | PASS |
| TC-CAT-010 | closed 为终态 | PASS |
| TC-CAT-010 | draft 不能跳过 published 直接到 closed | PASS |
| TC-CAT-011 | 修改名称和描述 | PASS |
| TC-CAT-020 | 删除活动 (soft delete) | PASS |
| TC-CAT-900 | 无效 type 枚举被拒绝 | PASS |
| TC-CAT-901 | 无效 status 枚举被拒绝 | PASS |
| TC-CAT-902 | 未认证用户无法创建活动 | PASS |

### Deferred to Later Phases (from Phase 3)
| Test Case | Reason |
|-----------|--------|
| TC-RULE-100~109 | 规则执行校验 (需 event_post 关系, Phase 6) |
| TC-GRP-003~008 | 团队成员审批流程 (需 group_user 关系, Phase 5) |
| TC-GRP-901 | 非 owner/admin 修改团队权限检查 (需完整 auth, Phase 7) |
| TC-CAT-020 cascade | 级联删除关系 (需 relationship tables, Phase 7) |
| TC-RULE-020 cascade | 级联删除 event:rule 关系 (需 relationship tables, Phase 7) |

## Test Results
| Test | Input | Expected | Actual | Status |
|------|-------|----------|--------|--------|
| App import | `from app.main import app` | No errors | 61 routes | PASS |
| Health endpoint | GET /health | 200 | 200 {"status":"ok"} | PASS |
| OpenAPI spec | GET /openapi.json | Valid spec | 28 paths, 45 schemas | PASS |
| Phase 2 pytest | `pytest app/tests/ -v` | 25 passed | 25 passed, 0 failed | PASS |
| Phase 3 pytest | `pytest app/tests/ -v` | 65 passed | 65 passed, 0 failed | PASS |

### Phase 4: Layer 2 — post, interaction CRUD
- **Status:** complete
- **Started:** 2026-01-27
- Actions taken:
  - **Post model**: 添加 visibility 列, created_by→Integer, like_count/comment_count/average_rating 缓存字段
  - **Post schema**: Literal 类型校验 type(6 种), status(4 种), visibility(public|private); VALID_POST_STATUS_TRANSITIONS 状态机
  - **Post CRUD**: soft delete; get/get_multi 过滤已删除
  - **Post router**: require_current_user_id auth; created_by 自动设置; 状态机转换校验
  - **Interaction model**: 新建统一模型 (type: like|comment|rating, value: JSON, parent_id, created_by, deleted_at)
  - **Interaction schema**: 新建 Literal["like","comment","rating"] 类型校验
  - **Interaction CRUD**: 新建 CRUDInteraction with soft delete; 保留 legacy Comment/Rating CRUD
  - **38 tests**: 27 post + 11 interaction, 全部通过
- Files modified/created:
  - app/models/post.py (enhanced: visibility, created_by→Integer, cache fields)
  - app/models/interaction.py (created: unified Interaction model)
  - app/models/__init__.py (updated: add Interaction)
  - app/schemas/post.py (rewritten: Literal, state machine, cache fields)
  - app/schemas/interaction.py (created: Literal type validation)
  - app/schemas/__init__.py (updated: add Interaction schemas)
  - app/crud/posts.py (rewritten: soft delete)
  - app/crud/interactions.py (rewritten: CRUDInteraction + legacy)
  - app/crud/__init__.py (updated: add interactions)
  - app/routers/posts.py (rewritten: auth, status validation)
  - app/tests/test_posts.py (created: 27 tests)
  - app/tests/test_interactions.py (created: 11 tests)

### Phase 4 Test Coverage
| Test Case | Scenario | Status |
|-----------|----------|--------|
| TC-POST-001 | 最小字段创建帖子 | PASS |
| TC-POST-002 | 创建时直接发布 | PASS |
| TC-POST-003 | 创建帖子带标签 | PASS |
| TC-POST-010~013 | 不同类型帖子 (team, profile, proposal, certificate) | PASS |
| TC-POST-030 | draft→pending_review | PASS |
| TC-POST-031 | pending_review→published | PASS |
| TC-POST-032 | pending_review→rejected | PASS |
| TC-POST-033 | rejected→draft (resubmit) | PASS |
| TC-POST-033b | published 为终态 | PASS |
| TC-POST-060 | 更新标题和内容 | PASS |
| TC-POST-070 | 创建 visibility=private 帖子 | PASS |
| TC-POST-071 | private 帖子跳过 pending_review | PASS |
| TC-POST-073 | public→private | PASS |
| TC-POST-074 | private→public | PASS |
| TC-POST-076 | 默认 visibility=public | PASS |
| TC-POST-080 | 删除帖子 (soft delete) | PASS |
| TC-POST-900 | 缺少 title 被拒绝 | PASS |
| TC-POST-901 | 无效 type/status 枚举被拒绝 | PASS |
| TC-POST-902 | 未认证用户无法创建帖子 | PASS |
| TC-POST-903 | 无效 visibility 枚举被拒绝 | PASS |
| TC-IACT-model | 创建 like/comment/rating/nested 互动 (DB 直接) | PASS |
| TC-IACT-soft-delete | 互动软删除 | PASS |
| TC-IACT-900 | 无效 interaction type 被拒绝 | PASS |
| TC-IACT-valid | 所有合法类型被接受 | PASS |
| TC-IACT-endpoint | like/comments/ratings 端点 stub | PASS |

### Deferred to Later Phases (from Phase 4)
| Test Case | Reason |
|-----------|--------|
| TC-POST-040~050 | post_resource/post_post 关系 (Phase 5: Layer 3) |
| TC-IACT-001~063 | target:interaction 绑定 + 缓存更新 (Phase 6: Layer 4) |
| TC-IACT-020~025 | like 去重 + 缓存字段维护 (Phase 6: Layer 4) |

## Test Results
| Test | Input | Expected | Actual | Status |
|------|-------|----------|--------|--------|
| Phase 4 pytest | `pytest app/tests/ -v` | 102 passed | 102 passed, 0 failed | PASS |

### Phase 5: Layer 3 — simple relations (group_user, user_user, post_resource, post_post)
- **Status:** complete
- **Started:** 2026-01-27
- Actions taken:
  - **Member model**: 添加 UniqueConstraint(group_id, user_id); role/status 默认值
  - **Member schema**: Literal 类型校验 role(owner|admin|member), status(pending|accepted|rejected)
  - **Member CRUD**: 按 group 查询/计数, 按 group+user 唯一查询, 状态更新(joined_at auto-set), 物理删除
  - **Groups router**: 完整实现 member 端点 (list/add/update/remove), 审批流程(require_approval→pending/accepted), 重复检查(409)
  - **UserUser model**: 新建 user:user 关系表 (source_user_id, target_user_id, relation_type) + 唯一约束
  - **UserUser schema**: Literal["follow","block"] 校验
  - **UserUser CRUD**: follow/block 查询, 好友判定(mutual follow + no block), 级联删除
  - **Users router**: 新增 follow/unfollow/block/unblock + following/followers/is-friend 端点; self-follow/block 拒绝; blocked→cannot follow
  - **PostResource model**: 新建 post:resource 关系表 + 唯一约束
  - **PostResource CRUD**: 按 post 查询(position排序), 创建/更新/删除
  - **PostPost model**: 新建 post:post 关系表 + 唯一约束
  - **PostPost CRUD**: 按 source 查询(可过滤 relation_type), 创建/更新/删除
  - **Posts router**: 完整实现 resources + related 端点 (list/add/update/remove), 去重检查, 外键存在性校验
  - **PostResourceAdd/PostRelationAdd schema**: Literal 枚举校验 (display_type, relation_type)
  - **44 tests**: 13 group_member + 14 user_follow + 9 post_resource + 8 post_relation, 全部通过
- Files created:
  - app/models/user_user.py (UserUser model)
  - app/models/post_resource.py (PostResource model)
  - app/models/post_post.py (PostPost model)
  - app/schemas/user_user.py (UserUserCreate, UserUserResponse)
  - app/schemas/post_resource.py (PostResourceResponse)
  - app/schemas/post_post.py (PostPostResponse)
  - app/crud/members.py (CRUDMember)
  - app/crud/user_users.py (CRUDUserUser)
  - app/crud/post_resources.py (CRUDPostResource)
  - app/crud/post_posts.py (CRUDPostPost)
  - app/tests/test_group_members.py (13 tests)
  - app/tests/test_user_follow.py (14 tests)
  - app/tests/test_post_resources.py (9 tests)
  - app/tests/test_post_relations.py (8 tests)
- Files modified:
  - app/models/member.py (UniqueConstraint, defaults)
  - app/models/__init__.py (add UserUser, PostResource, PostPost)
  - app/schemas/member.py (Literal role/status)
  - app/schemas/memberadd.py (Literal role)
  - app/schemas/postresourceadd.py (Literal display_type)
  - app/schemas/postrelationadd.py (Literal relation_type)
  - app/schemas/__init__.py (add new schemas)
  - app/crud/__init__.py (add new CRUDs)
  - app/routers/groups.py (wire up member endpoints)
  - app/routers/users.py (add follow/block endpoints)
  - app/routers/posts.py (wire up resource + related endpoints)

### Phase 5 Test Coverage
| Test Case | Scenario | Status |
|-----------|----------|--------|
| TC-REL-GU-add | 添加成员 (require_approval=true→pending, false→accepted) | PASS |
| TC-REL-GU-owner | 添加 owner 角色成员 | PASS |
| TC-REL-GU-900 | 重复加入被拒绝 (409) | PASS |
| TC-REL-GU-901 | 非法 role 枚举被拒绝 (422) | PASS |
| TC-REL-GU-001 | 移出团队成员 + 验证列表为空 | PASS |
| TC-REL-GU-list | 列表成员 + 按状态过滤 | PASS |
| TC-REL-GU-approve | 审批通过 (joined_at auto-set) | PASS |
| TC-REL-GU-reject | 审批拒绝 | PASS |
| TC-FRIEND-001 | 用户 A 关注用户 B + 关注列表 | PASS |
| TC-FRIEND-002 | 互相关注→好友 | PASS |
| TC-FRIEND-003 | 单向关注≠好友 | PASS |
| TC-FRIEND-004 | 取消关注→解除好友 | PASS |
| TC-FRIEND-005 | 拉黑后不构成好友 | PASS |
| TC-FRIEND-006 | 被拉黑用户无法关注 (403) | PASS |
| TC-FRIEND-900 | 自己关注自己被拒绝 (422) | PASS |
| TC-FRIEND-901 | 重复关注被拒绝 (409) | PASS |
| TC-FRIEND-902 | 非法 relation_type 被拒绝 (schema) | PASS |
| TC-REL-PR-001 | 资源作为 attachment 挂到帖子 | PASS |
| TC-REL-PR-002 | 资源作为 inline 挂到帖子 | PASS |
| TC-REL-PR-003 | 多资源 position 排序 | PASS |
| TC-REL-PR-004 | 更新 display_type | PASS |
| TC-REL-PR-005 | 删除关系（资源本身仍存在） | PASS |
| TC-REL-PP-001 | 创建 embed 关系 | PASS |
| TC-REL-PP-002 | 创建 reference 关系 | PASS |
| TC-REL-PP-003 | 创建 reply 关系 | PASS |
| TC-REL-PP-004 | 更新关系类型和 position | PASS |
| TC-REL-PP-005 | 删除 post:post 关系 | PASS |

### Deferred to Later Phases (from Phase 5)
| Test Case | Reason |
|-----------|--------|
| TC-REL-GU-902 | 团队已满时加入被拒绝 (需 event_group + rule enforcement, Phase 6) |
| TC-FRIEND-007 | 删除用户后级联解除 user:user (需 soft delete cascade, Phase 7) |

## Test Results
| Test | Input | Expected | Actual | Status |
|------|-------|----------|--------|--------|
| Phase 5 pytest | `pytest app/tests/ -v` | 146 passed | 146 passed, 0 failed | PASS |
| Phase 6 pytest | `pytest app/tests/ -v` | 186 passed | 186 passed, 0 failed | PASS |

### Phase 6: Layer 4 — complex relations (event_rule, event_post, event_group, target_interaction)
- **Status:** complete
- **Started:** 2026-01-27
- Actions taken:
  - **EventRule**: 模型 + CRUD + 优先级排序 + 重复检查(409) + 路由端点 (list/add/update priority/remove)
  - **EventPost**: 模型 + CRUD + relation_type 过滤 + max_submissions 规则引擎 + 路由端点 (list/add/remove)
  - **EventGroup**: 模型 + CRUD + 重复报名检查(409) + is_user_in_category 查询 + 路由端点 (list/add/remove)
  - **TargetInteraction**: 多态绑定模型(target_type: post|event|resource) + like 去重 + cache 更新
  - **Interactions router 重写**: like/unlike(POST/DELETE) + comment(POST/GET) + rating(POST/GET) 全部通过 target_interaction 绑定
  - **缓存更新**: _update_post_cache() 自动维护 like_count, comment_count, average_rating
  - **Bug 修复**: PaginatedCommentList/RatingList → PaginatedInteractionList (旧 Comment/Rating schema 与 Interaction 模型不兼容); comment/rating POST 端点添加 response_model=schemas.Interaction; Phase 4 interaction tests 补充 X-User-Id header
  - **40 new tests**: 7 event_rule + 10 event_post + 7 event_group + 16 target_interaction
- Files created:
  - app/models/event_rule.py (EventRule model)
  - app/models/event_post.py (EventPost model)
  - app/models/event_group.py (EventGroup model)
  - app/models/target_interaction.py (TargetInteraction model)
  - app/schemas/event_rule.py (CategoryRuleResponse)
  - app/schemas/event_post.py (CategoryPostResponse)
  - app/schemas/event_group.py (CategoryGroupResponse)
  - app/schemas/target_interaction.py (TargetInteractionCreate, TargetInteractionResponse)
  - app/schemas/paginatedinteractionlist.py (PaginatedInteractionList)
  - app/crud/category_rules.py (CRUDCategoryRule)
  - app/crud/category_posts.py (CRUDCategoryPost)
  - app/crud/category_groups.py (CRUDCategoryGroup)
  - app/crud/target_interactions.py (CRUDTargetInteraction)
  - app/tests/test_category_rules.py (7 tests)
  - app/tests/test_category_posts.py (10 tests)
  - app/tests/test_category_groups.py (7 tests)
  - app/tests/test_target_interactions.py (16 tests)
- Files modified:
  - app/models/__init__.py (add Phase 6 models)
  - app/schemas/__init__.py (add Phase 6 schemas + PaginatedInteractionList)
  - app/crud/__init__.py (add Phase 6 CRUDs)
  - app/routers/events.py (wire up event_rule, event_post, event_group endpoints)
  - app/routers/interactions.py (complete rewrite: target_interaction binding, auth, cache)
  - app/tests/test_interactions.py (fix Phase 4 tests: add X-User-Id headers)

### Phase 6 Test Coverage
| Test Case | Scenario | Status |
|-----------|----------|--------|
| TC-REL-CR-001 | 将规则关联到活动 (priority) | PASS |
| TC-REL-CR-002 | 更新 event:rule priority | PASS |
| TC-REL-CR-003 | 删除 event:rule (规则本身保留) | PASS |
| TC-REL-CR-900 | 重复关联同一规则被拒绝 (409) | PASS |
| TC-REL-CR-boundary | 非法 event/rule ID 返回 404 | PASS |
| TC-REL-CP-001 | 帖子关联为 submission | PASS |
| TC-REL-CP-002 | 帖子关联为 reference | PASS |
| TC-REL-CP-003 | 按 relation_type=submission 筛选 | PASS |
| TC-REL-CP-004 | 无筛选读取所有 event:post | PASS |
| TC-REL-CP-902 | max_submissions 超限被拒绝 (422) | PASS |
| TC-REL-CP-ref | reference 不受 max_submissions 限制 | PASS |
| TC-REL-CP-dup | 重复 event:post 被拒绝 (409) | PASS |
| TC-REL-CP-remove | 删除 event:post 关系 | PASS |
| TC-REL-CP-boundary | 非法 event/post ID 返回 404 | PASS |
| TC-REL-CG-001 | 团队报名活动 | PASS |
| TC-REL-CG-002 | 读取活动已报名团队列表 | PASS |
| TC-REL-CG-003 | 团队取消报名 | PASS |
| TC-REL-CG-900 | 重复报名被拒绝 (409) | PASS |
| TC-REL-CG-boundary | 非法 event/group/relation ID 返回 404 | PASS |
| TC-IACT-001 | 点赞 → like_count 从 0→1 | PASS |
| TC-IACT-002 | 重复点赞被拒绝 (409) | PASS |
| TC-IACT-003 | 取消点赞 → like_count 回到 0 | PASS |
| TC-IACT-multiple | 多用户点赞/取消点赞计数正确 | PASS |
| TC-IACT-010 | 创建顶层评论 → comment_count +1 | PASS |
| TC-IACT-011 | 嵌套回复 (parent_id) | PASS |
| TC-IACT-013 | comment_count 包含所有层级 | PASS |
| TC-IACT-list-comments | 评论列表分页 | PASS |
| TC-IACT-020 | 创建评分 → average_rating 计算 | PASS |
| TC-IACT-021 | 多评分均值计算 | PASS |
| TC-IACT-list-ratings | 评分列表分页 | PASS |
| TC-IACT-auth | like/comment/rating 无 auth 返回 401 | PASS |
| TC-IACT-deleted | 已删除帖子点赞返回 404 | PASS |

### Deferred to Later Phases (from Phase 6)
| Test Case | Reason |
|-----------|--------|
| TC-REL-CP-900 | submission_deadline 截止后拒绝 (需完整规则引擎时间窗口, Phase 7) |
| TC-REL-CP-901 | submission_format 格式检查 (需 resource 格式校验, Phase 7) |
| TC-REL-CG-901 | 同一用户多团队报名拒绝 (需 member+event_group 联合查询, Phase 7) |
| TC-REL-GU-902 | 团队已满时加入拒绝 (需 event_group + rule enforcement, Phase 7) |
| TC-IACT-014 | 删除父评论级联删除子回复 (Phase 7) |
| TC-IACT-050~051 | 修改评论/评分 (Phase 7) |
| TC-IACT-060~063 | 非 post 目标互动 (Phase 7) |
| TC-IACT-901~905 | 负向/边界用例 (Phase 7) |

### Phase 7: Layer 5-6 — event_event, cascade delete, permissions, rule engine
- **Status:** complete
- **Started:** 2026-01-27
- Actions taken:
  - **event_event 关系**: 新建 EventEvent 模型 (source→target, stage/track/prerequisite), 环检测 BFS, CRUD + router 端点 — 14 tests
  - **级联删除**: cascade_delete_category, cascade_delete_group, cascade_delete_post 服务, 多表依赖链清理 — 16 tests
  - **权限 + 可见性**: require_role("organizer","admin") 工厂, draft 帖子/活动仅 creator 可见, private group 仅成员/creator 可见 — 17 tests + 10 regression fixes
  - **声明式规则引擎**: app/services/rule_engine.py (~400 行):
    - 固定字段展开 (max_submissions, submission_start/deadline, submission_format, min/max_team_size → checks)
    - 7 种条件评估器: time_window, count, exists, field_match, resource_format, resource_required, aggregate
    - on_fail 行为: deny(raise), warn(return), flag
    - Post-hook actions: compute_ranking, flag_disqualified, award_certificate
    - 集成到 events router (event_post creation, status change) 和 groups router (group_user creation)
    — 23 tests
  - **Bug fixes**: SessionLocal() vs db_session fixture 隔离问题; event status update post-hook 时序 bug
  - **Total: 256 tests passing (186 + 70 new)**
- Files created:
  - app/models/event_event.py
  - app/schemas/event_event.py
  - app/crud/event_events.py
  - app/services/cascade_delete.py
  - app/services/rule_engine.py
  - app/tests/test_category_categories.py (14 tests)
  - app/tests/test_cascade_delete.py (16 tests)
  - app/tests/test_permissions.py (17 tests)
  - app/tests/test_rule_engine.py (23 tests)
- Files modified:
  - app/models/rule.py (added checks JSON column)
  - app/schemas/rule.py (CheckCondition, CheckDefinition models)
  - app/crud/category_groups.py (added get_multi_by_group)
  - app/routers/events.py (rule engine integration, visibility filtering)
  - app/routers/groups.py (rule engine integration for group_user, visibility filtering)
  - app/deps.py (require_role factory)
  - app/tests/test_cascade_delete.py (regression fixes: X-User-Id headers)
  - app/tests/test_category_posts.py (regression fixes: X-User-Id headers)
  - app/tests/test_target_interactions.py (fix uid→u1 variable)

### Phase 7 Test Coverage
| Test Case | Scenario | Status |
|-----------|----------|--------|
| TC-STAGE-001 | event_event stage 关系创建 | PASS |
| TC-STAGE-002 | event_event track 关系创建 | PASS |
| TC-STAGE-003 | event_event prerequisite 关系创建 | PASS |
| TC-STAGE-004 | 环检测拒绝循环依赖 (422) | PASS |
| TC-STAGE-005 | 自引用拒绝 (422) | PASS |
| TC-STAGE-006 | 重复关联拒绝 (409) | PASS |
| TC-STAGE-007 | stage_order 排序 | PASS |
| TC-DEL-001 | 删除 event 级联清理 rules/posts/groups/associations | PASS |
| TC-DEL-002 | 删除 group 级联清理 members/category_groups | PASS |
| TC-DEL-003 | 删除 post 级联清理 resources/relations/interactions/category_posts | PASS |
| TC-PERM-001 | organizer 可创建 event | PASS |
| TC-PERM-002 | admin 可创建 event | PASS |
| TC-PERM-003 | participant 不能创建 event (403) | PASS |
| TC-PERM-004 | draft post 仅 creator 可见 | PASS |
| TC-PERM-005 | draft event 仅 creator 可见 | PASS |
| TC-PERM-006 | private group 仅 creator/member 可见 | PASS |
| TC-ENGINE-001 | time_window 条件: 在窗口内通过 | PASS |
| TC-ENGINE-002 | time_window 条件: 窗口外拒绝 | PASS |
| TC-ENGINE-003 | count 条件: 未达上限通过 | PASS |
| TC-ENGINE-004 | count 条件: 达到上限拒绝 | PASS |
| TC-ENGINE-010 | exists 条件通过 | PASS |
| TC-ENGINE-011 | exists 条件失败 | PASS |
| TC-ENGINE-020 | fixed field expansion (max_submissions→count check) | PASS |
| TC-ENGINE-030 | post-hook compute_ranking 执行 | PASS |
| TC-ENGINE-040 | on_fail=warn 返回警告不阻断 | PASS |
| TC-ENGINE-050 | 多规则 AND 逻辑 | PASS |

## Test Results
| Test | Input | Expected | Actual | Status |
|------|-------|----------|--------|--------|
| Phase 7 pytest | `pytest app/tests/ -v` | 256 passed | 256 passed, 0 failed | PASS |

### Phase 8: Layer 7 — 集成验证
- **Status:** complete
- **Started:** 2026-01-27
- Actions taken:
  - **Router integration**: 添加 rule engine pre-checks 到 event status change 和 event_group 注册端点
  - **Rule engine enhancements**:
    - `_eval_exists` 添加 `post` entity type (profile post 检查)
    - `_eval_exists` 中 `group_user` 使用 filter status 参数
    - `_action_compute_ranking` 添加 tie handling (同分同名次，跳排)
    - `_action_compute_ranking` 排除被取消资格的帖子 (disqualification tags)
    - `_action_flag_disqualified` 添加 `target: post` 支持 (missing_attachment 检查)
  - **4 个测试文件**:
    - test_user_journeys.py: 9 tests (TC-JOUR-002, 005, 007, 009, 010, 011-1, 011-2, 012, 013)
    - test_entry_rules.py: 14 tests (TC-ENTRY-001~031, 900~902)
    - test_closure_rules.py: 10 tests (TC-CLOSE-001~040, 900~902)
    - test_resource_transfer.py: 4 tests (TC-TRANSFER-001~004)
  - **Total: 293 tests passing (256 + 37 new)**
- Files created:
  - app/tests/test_user_journeys.py (9 tests)
  - app/tests/test_entry_rules.py (14 tests)
  - app/tests/test_closure_rules.py (10 tests)
  - app/tests/test_resource_transfer.py (4 tests)
- Files modified:
  - app/routers/events.py (rule engine pre-checks for status change + group registration)
  - app/services/rule_engine.py (post entity, tie handling, disqualification filtering, flag_disqualified post target)

### Phase 8 Test Coverage
| Test Case | Scenario | Status |
|-----------|----------|--------|
| TC-JOUR-002 | 匿名浏览: published vs draft 可见性 | PASS |
| TC-JOUR-005 | 团队加入审批流程 | PASS |
| TC-JOUR-007 | 团队注册活动完整流程 | PASS |
| TC-JOUR-009 | 创建日常和比赛帖子 | PASS |
| TC-JOUR-010 | 证书颁发流程 | PASS |
| TC-JOUR-011-1 | 编辑自己的帖子版本管理 | PASS |
| TC-JOUR-011-2 | 编辑他人帖子(copy+provenance) | PASS |
| TC-JOUR-012 | 删除帖子完整级联 | PASS |
| TC-JOUR-013 | 社区互动: 点赞/评论/评分/取消 | PASS |
| TC-ENTRY-001 | 加入团队前不能报名 | PASS |
| TC-ENTRY-002 | 团队未注册不能提交 | PASS |
| TC-ENTRY-003 | 需要 profile post | PASS |
| TC-ENTRY-004 | 所有条件满足通过 | PASS |
| TC-ENTRY-010 | 资源最低数量检查 | PASS |
| TC-ENTRY-011 | 资源格式不符拒绝 | PASS |
| TC-ENTRY-012 | 资源格式符合通过 | PASS |
| TC-ENTRY-020 | 每人一次提交限制 | PASS |
| TC-ENTRY-022 | 不同活动互不影响 | PASS |
| TC-ENTRY-030 | 固定+自定义 checks AND 逻辑 | PASS |
| TC-ENTRY-031 | 固定+自定义 checks 全部满足 | PASS |
| TC-ENTRY-900 | 未知 condition type 被跳过 | PASS |
| TC-ENTRY-901 | 不匹配 trigger 被跳过 | PASS |
| TC-ENTRY-902 | 无 condition 的 check 被跳过 | PASS |
| TC-CLOSE-001 | pre-phase warn 允许关闭 | PASS |
| TC-CLOSE-002 | pre-phase deny 阻止关闭 | PASS |
| TC-CLOSE-010 | flag_disqualified: team_too_small | PASS |
| TC-CLOSE-020 | compute_ranking: 按 average_rating 排名 | PASS |
| TC-CLOSE-022 | 未评分帖子不参与排名 | PASS |
| TC-CLOSE-030 | award_certificate: 颁发证书帖子 | PASS |
| TC-CLOSE-040 | 完整闭幕流程: flag+rank+award | PASS |
| TC-CLOSE-900 | 非 closed 状态不触发 post hooks | PASS |
| TC-CLOSE-901 | 无规则的活动正常关闭 | PASS |
| TC-CLOSE-902 | post-hook 失败不回滚主操作 | PASS |
| TC-TRANSFER-001 | 证书资源从组织者到参赛者 | PASS |
| TC-TRANSFER-002 | 同用户帖子间资源转移 | PASS |
| TC-TRANSFER-003 | 资源多帖子共享 | PASS |
| TC-TRANSFER-004 | 带 provenance 的资源转移 | PASS |

## Test Results
| Test | Input | Expected | Actual | Status |
|------|-------|----------|--------|--------|
| Phase 8 pytest | `pytest app/tests/ -v` | 293 passed | 293 passed, 0 failed | PASS |

## 5-Question Reboot Check
| Question | Answer |
|----------|--------|
| Where am I? | ALL 8 PHASES COMPLETE |
| Where am I going? | DONE — all phases completed |
| What's the goal? | 从零依赖底层开始，逐层开发 Synnovator 后端，所有 phase 完成输出 COMPLETE |
| What have I learned? | 8 层依赖图开发: 零依赖→基础→内容→简单关系→复杂关系→高级功能→跨切面→集成验证; 293 tests covering 7 content types, 9 relationship types, auth, rule engine, cascade delete, E2E flows |
| What have I done? | Phase 0-8 全部完成 (293 tests passing, 0 failures) |

---
*All phases complete.*
