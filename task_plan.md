# Task Plan: Synnovator 后端底层到上层开发

## Goal
从零依赖模块开始，按 8 层依赖图逐层开发 Synnovator 后端，每层完成后立即用 tests-kit 验证。

## Current Phase
ALL PHASES COMPLETE (293 tests passing)

## Phases

### Phase 1: 后端脚手架生成
- [x] 验证 .synnovator/openapi.yaml 是否最新
- [x] 使用 api-builder 生成 FastAPI 后端到 app/
- [x] 修复生成代码 (9 models, 29 schemas, 8 routers)
- [x] 验证: 服务启动, 28 paths, 45 schemas
- **Status:** complete

### Phase 2: Layer 0 — 零依赖基础模块 (user, resource)
- [x] 验证/完善 user CRUD（唯一性校验: username, email; 软删除; role 验证）
- [x] 验证/完善 resource CRUD（created_by 追踪; 软删除; 认证校验）
- [x] pytest: 25 tests (16 user + 9 resource), 覆盖 TC-USER-001~903, TC-RES-001~901
- **Status:** complete

### Phase 3: Layer 1 — 仅依赖 user 的模块 (rule, group, category)
- [x] 验证/完善 rule CRUD（scoring_criteria 权重校验=100; soft delete; created_by 追踪; auth）
- [x] 验证/完善 group CRUD（visibility Literal 校验; soft delete; created_by 追踪; auth; 成员管理 stub）
- [x] 验证/完善 category CRUD（type/status Literal 校验; 状态机: draft→published→closed; soft delete; created_by; auth）
- [x] pytest: 40 tests (12 rule + 12 group + 16 category), 覆盖 TC-RULE-001~901, TC-GRP-001~901, TC-CAT-001~902
- **Status:** complete

### Phase 4: Layer 2 — 内容创建模块 (post, interaction)
- [x] 验证/完善 post CRUD（缓存字段、状态机 draft→pending_review→published|rejected、类型渲染、visibility）
- [x] 创建统一 Interaction 模型（type: like|comment|rating, JSON value, parent_id）
- [x] 验证/完善 interaction schema（Literal 类型校验）
- [x] pytest: 38 tests (27 post + 11 interaction), 覆盖 TC-POST-001~903, TC-IACT-900
- **Status:** complete

### Phase 5: Layer 3 — 简单关系 (group_user, user_user, post_resource, post_post)
- [x] 实现 group_user 关系（Member 模型 + CRUD + 审批流程: pending→accepted/rejected）
- [x] 实现 user_user 关系（UserUser 模型 + follow/block + 好友判定 + block 优先）
- [x] 实现 post_resource 关系（PostResource 模型 + display_type + position 排序）
- [x] 实现 post_post 关系（PostPost 模型 + reference/reply/embed + position）
- [x] pytest: 44 tests (13 group_member + 14 user_follow + 9 post_resource + 8 post_relation), 覆盖 TC-REL-GU-001~901, TC-FRIEND-001~902, TC-REL-PR-001~005, TC-REL-PP-001~005
- **Status:** complete

### Phase 6: Layer 4 — 复杂关系 (含规则引擎)
- [x] 实现 category_rule 关系（优先级排序 + 重复检查）
- [x] 实现 target_interaction（多态绑定 + like 去重 + 缓存更新: like_count, comment_count, average_rating）
- [x] 实现 category_post（max_submissions 规则引擎校验 + relation_type 过滤）
- [x] 实现 category_group（团队报名 + 重复检查）
- [x] 修复: PaginatedCommentList/RatingList→PaginatedInteractionList; comment/rating POST 添加 response_model
- [x] 修复: Phase 4 interaction tests 补充 X-User-Id header
- [x] pytest: 40 tests (7 category_rule + 10 category_post + 7 category_group + 16 target_interaction), 覆盖 TC-REL-CR-001~900, TC-REL-CP-001~902, TC-REL-CG-001~900, TC-IACT-001~021
- **Status:** complete

### Phase 7: Layer 5-6 — 高级功能 + 跨切面
- [x] category_category 关系（阶段/赛道/前置条件 + 环检测）— 14 tests
- [x] 软删除 + 级联删除 — 16 tests
- [x] 权限层 + 可见性控制 — 17 tests + regression fixes
- [x] 声明式规则引擎完整实现 — 23 tests
- [x] tests-kit Guard: TC-STAGE-*, TC-DEL-*, TC-PERM-*, TC-ENGINE-*
- **Status:** complete

### Phase 8: Layer 7 — 集成验证
- [x] 用户旅程 E2E 测试 (TC-JOUR-002, 005, 007, 009, 010, 011, 012, 013) — 9 tests
- [x] 参赛规则测试 (TC-ENTRY-001~031, 900~902) — 14 tests
- [x] 活动结束规则测试 (TC-CLOSE-001~040, 900~902) — 10 tests
- [x] 资源转移测试 (TC-TRANSFER-001~004) — 4 tests
- [x] 全量 pytest 验证: 293 passed, 0 failed
- **Status:** complete

## Key Questions
1. app/ 目录当前只有 main.py 和 __init__.py，需要用 api-builder 重新生成完整脚手架
2. openapi.yaml 是否需要重新生成？（synnovator skill 已重构）
3. 生成的代码需要多少手工调整才能满足 synnovator skill 的完整能力？

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| 不创建编排 Skill | Skills 是静态 prompt，无法动态调度；planning-with-files 已提供规划能力 |
| 用 planning-with-files 管理进度 | 文件化规划可跨会话持久化，防止上下文丢失 |
| 按 8 层依赖图开发 | 从零依赖底层开始，保证每层测试时依赖已就绪 |
| 每层完成后用 tests-kit 增量测试 | 及时发现问题，不积压到最后 |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| (暂无) | - | - |

## Notes
- 工作流程参考: docs/development-workflow.md
- 测试用例: specs/testcases/ (17 个模块, 246 个用例)
- synnovator skill 是原型参考实现，后端 API 应与其能力对齐
- 所有 Python 命令使用 `uv run python` 执行
