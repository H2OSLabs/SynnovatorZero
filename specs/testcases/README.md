# Synnovator 测试用例集

> **格式约定：** 每条用例仅描述「场景」与「预期结果」，不包含测试方法和执行过程。

---

## 目录

### 内容类型模块（Content Types）

| 文件 | 模块 | 用例前缀 |
|------|------|----------|
| [01-user.md](01-user.md) | 用户（User） | TC-USER |
| [02-category.md](02-category.md) | 活动（Category） | TC-CAT |
| [03-rule.md](03-rule.md) | 规则（Rule） | TC-RULE |
| [04-group.md](04-group.md) | 团队（Group） | TC-GRP |
| [05-post.md](05-post.md) | 帖子（Post） | TC-POST |
| [06-resource.md](06-resource.md) | 资源（Resource） | TC-RES |
| [07-interaction.md](07-interaction.md) | 互动（Interaction） | TC-IACT |

### 关系类型测试（Relations）

| 文件 | 模块 | 用例前缀 |
|------|------|----------|
| [08-relations.md](08-relations.md) | 关系类型测试 | TC-REL |

### 横切关注点（Cross-Cutting）

| 文件 | 模块 | 用例前缀 |
|------|------|----------|
| [09-cascade-delete.md](09-cascade-delete.md) | 删除与级联 | TC-DEL |
| [10-permissions.md](10-permissions.md) | 权限与可见性 | TC-PERM |

### 集成测试（Integration）

| 文件 | 模块 | 用例前缀 |
|------|------|----------|
| [11-user-journeys.md](11-user-journeys.md) | 用户旅程集成 | TC-JOUR |

### 高级功能（Advanced Features）

| 文件 | 模块 | 用例前缀 |
|------|------|----------|
| [12-resource-transfer.md](12-resource-transfer.md) | 资产转移 | TC-TRANSFER |
| [13-user-follow.md](13-user-follow.md) | 好友（User Follow） | TC-FRIEND |
| [14-category-association.md](14-category-association.md) | 活动关联 | TC-STAGE / TC-TRACK / TC-PREREQ / TC-CATREL |

### 规则引擎（Rule Engine）

| 文件 | 模块 | 用例前缀 |
|------|------|----------|
| [15-entry-rules.md](15-entry-rules.md) | 参加活动规则 | TC-ENTRY |
| [16-closure-rules.md](16-closure-rules.md) | 活动结束规则 | TC-CLOSE |
| [17-rule-engine.md](17-rule-engine.md) | 声明式规则引擎 | TC-ENGINE |
