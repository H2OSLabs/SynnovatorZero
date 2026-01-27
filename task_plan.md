# Task Plan: Synnovator 后端底层到上层开发

## Goal
从零依赖模块开始，按 8 层依赖图逐层开发 Synnovator 后端，每层完成后立即用 tests-kit 验证。

## Current Phase
Phase 1 (OpenAPI 规范生成 + api-builder 后端脚手架)

## Phases

### Phase 1: 后端脚手架生成
- [ ] 验证 .synnovator/openapi.yaml 是否最新
- [ ] 使用 api-builder 生成 FastAPI 后端到 app/
- [ ] 设置 Alembic 迁移 + 运行初始迁移
- [ ] 验证数据库表结构正确
- **Status:** in_progress

### Phase 2: Layer 0 — 零依赖基础模块 (user, resource)
- [ ] 验证/完善 user CRUD（唯一性校验: username, email）
- [ ] 验证/完善 resource CRUD（文件存储集成）
- [ ] tests-kit Guard: TC-USER-*, TC-RES-*
- [ ] pytest: app/tests/test_api/test_users_api.py, test_resources_api.py
- **Status:** pending

### Phase 3: Layer 1 — 仅依赖 user 的模块 (rule, group, category)
- [ ] 验证/完善 rule CRUD（scoring_criteria 验证）
- [ ] 验证/完善 group CRUD（成员角色定义）
- [ ] 验证/完善 category CRUD（状态机: draft→published→closed）
- [ ] tests-kit Guard: TC-RULE-*, TC-GRP-*, TC-CAT-*
- **Status:** pending

### Phase 4: Layer 2 — 内容创建模块 (post, interaction)
- [ ] 验证/完善 post CRUD（缓存字段、状态机、类型渲染）
- [ ] 验证/完善 interaction CRUD（点赞/评论/评分）
- [ ] tests-kit Guard: TC-POST-*, TC-IACT-*
- **Status:** pending

### Phase 5: Layer 3 — 简单关系 (group_user, user_user, post_resource, post_post)
- [ ] 实现 group_user 关系 + 审批流程
- [ ] 实现 user_user 关系（关注/屏蔽 + block 强制执行）
- [ ] 实现 post_resource 关系
- [ ] 实现 post_post 关系（引用/回复/嵌入 + 防循环）
- [ ] tests-kit Guard: TC-REL-GU-*, TC-FRIEND-*, TC-REL-PR-*, TC-REL-PP-*
- **Status:** pending

### Phase 6: Layer 4 — 复杂关系 (含规则引擎)
- [ ] 实现 category_rule 关系（优先级排序）
- [ ] 实现 target_interaction（多态绑定 + like 去重 + 缓存更新）
- [ ] 实现 category_post（规则引擎校验: 时间窗口、提交数限制、格式检查）
- [ ] 实现 category_group（前置条件检查、团队大小校验）
- [ ] tests-kit Guard: TC-REL-CR-*, TC-REL-TI-*, TC-REL-CP-*, TC-REL-CG-*, TC-ENTRY-*
- **Status:** pending

### Phase 7: Layer 5-6 — 高级功能 + 跨切面
- [ ] category_category 关系（阶段/赛道/前置条件 + 环检测）
- [ ] 软删除 + 级联删除
- [ ] 权限层 + 可见性控制
- [ ] 声明式规则引擎完整实现
- [ ] tests-kit Guard: TC-STAGE-*, TC-DEL-*, TC-PERM-*, TC-ENGINE-*
- **Status:** pending

### Phase 8: Layer 7 — 集成验证
- [ ] 数据注入（data-importer）
- [ ] 13 个用户旅程端到端测试
- [ ] 闭幕规则、资源转移、评分排名
- [ ] tests-kit 全量 Guard 检查
- **Status:** pending

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
