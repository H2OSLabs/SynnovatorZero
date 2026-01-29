# Findings & Decisions

## Requirements
- 从零依赖底层模块开始，逐层向上开发 Synnovator 后端
- 每完成一个模块/层级，立即测试对应的测试用例
- 使用 planning-with-files 追踪进度，防止上下文丢失
- 后端包名为 `app/`（与 api-builder 模板一致）

## Research Findings

### 项目当前状态 (2026-01-27)
- `.synnovator/` 已有完整测试数据（7 种内容类型 + 关系 + openapi.yaml）
- `app/` 只有 `__init__.py` 和 `main.py`，尚未用 api-builder 生成完整脚手架
- `frontend/` 有基础 Next.js 项目结构
- synnovator skill 已重构，包含 7 种内容类型、9 种关系类型、规则引擎、级联删除、缓存维护

### 依赖图分析
- Layer 0 (零依赖): user, resource
- Layer 1 (依赖 user): rule, group, category
- Layer 2 (依赖 Layer 0-1): post, interaction
- Layer 3 (简单关系): group_user, user_user, post_resource, post_post
- Layer 4 (复杂关系): category_rule, target_interaction, category_post, category_group
- Layer 5 (图关系): category_category (环检测)
- Layer 6 (跨切面): 软删除+级联、权限、规则引擎
- Layer 7 (集成): 用户旅程、闭幕规则、资源转移

### 方案分析结论
- 不创建编排 Skill（Skills 是静态 prompt，不能动态调度）
- 不继续膨胀工作流文档（已 1000+ 行）
- 使用 planning-with-files 生成具体执行计划（职责分离：workflow doc = HOW, task_plan = WHAT + WHEN）

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| 后端包名 `app/` | api-builder 模板 17 处硬编码 `from app.xxx`，零修改使用 |
| 底层到上层依赖图 8 层开发 | 保证每层测试时依赖已就绪，增量验证 |
| tests-kit 每层增量测试 | 246 个测试用例按层分配，不积压 |
| planning-with-files 管理进度 | 跨会话持久化，session-catchup.py 恢复上下文 |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| 文档中测试用例数量不准确 (267→246) | 已修正为实际数量 246 |
| 工作流文档缺少依赖图 | 已添加 8 层依赖图到 docs/development-workflow.md |

## Resources
- 工作流文档: `docs/development-workflow.md`
- 数据类型定义: `docs/data-types.md`
- 关系类型定义: `docs/relationships.md`
- CRUD 操作: `docs/crud-operations.md`
- 规则引擎: `docs/rule-engine.md`
- 数据完整性: `specs/data-integrity.md`
- 测试用例: `specs/testcases/` (17 个文件)
- synnovator skill: `.claude/skills/synnovator/`
- OpenAPI spec: `.synnovator/openapi.yaml`

---
*Update this file after every 2 view/browser/search operations*
