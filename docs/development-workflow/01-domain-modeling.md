# 阶段 0.5: 领域建模与数据架构

> **关键阶段**：领域模型是整个系统的基础，后续所有阶段都依赖于此。

## 使用 domain-modeler Skill

```bash
# 调用 domain-modeler skill
# 输入: docs/user-journeys/
# 输出: 领域模型文档
```

## 输入

| 文件 | 描述 |
|------|------|
| `docs/user-journeys/*.md` | 用户旅程文档（手写需求） |

## 输出

| 文件 | 描述 |
|------|------|
| `docs/data-types.md` | 7 种内容类型的字段定义 |
| `docs/relationships.md` | 9 种关系类型定义 |
| `docs/crud-operations.md` | CRUD 操作与权限矩阵 |
| `specs/data-integrity.md` | 数据完整性约束（唯一性、软删除、级联） |
| `specs/cache-strategy.md` | 缓存字段维护策略 |
| `docs/rule-engine.md` | 声明式规则引擎规范（如需要） |

## 交叉验证

确保每个用户旅程步骤都能被领域模型支撑：

```bash
# 验证用户旅程覆盖度
uv run python .claude/skills/journey-validator/scripts/validate.py
```

| 检查项 | 验证内容 |
|--------|---------|
| 实体完整性 | 旅程中提到的所有实体都在 data-types.md 中定义 |
| 关系覆盖 | 旅程中的操作（加入团队、提交作品）有对应关系类型 |
| 权限映射 | CRUD 操作权限与旅程中的角色一致 |

## 7 种内容类型

| 类型 | 描述 | 关键字段 |
|------|------|---------|
| `user` | 用户 | username, email, role |
| `event` | 活动 | name, type, status, start_date, end_date |
| `post` | 帖子 | title, content, type, status |
| `rule` | 规则 | name, type, config |
| `resource` | 资源 | filename, file_type, url |
| `group` | 团队 | name, visibility, max_members |
| `interaction` | 交互 | type (like/comment/rating), value |

## 9 种关系类型

| 关系 | 描述 |
|------|------|
| `event:rule` | 活动绑定规则 |
| `event:post` | 活动关联帖子（提交） |
| `event:group` | 活动关联团队（参赛） |
| `event:event` | 活动关联（阶段/赛道/前置条件） |
| `post:post` | 帖子关联（引用/回复/嵌入） |
| `post:resource` | 帖子附件 |
| `group:user` | 团队成员 |
| `user:user` | 用户关系（关注/屏蔽） |
| `target:interaction` | 多态交互（对帖子/活动/资源的点赞/评论/评分） |

## 下一步

完成领域建模后，进入 [阶段 1: API 设计](02-api-design.md)。
