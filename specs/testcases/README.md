# Synnovator 测试用例集

> **格式约定：** 每条用例仅描述「场景」与「预期结果」，不包含测试方法和执行过程。

---

## 目录

### 内容类型模块（Content Types）

| 文件 | 模块 | 用例前缀 |
|------|------|----------|
| [01-user.md](01-user.md) | 用户（User） | TC-USER |
| [02-event.md](02-event.md) | 活动（Event） | TC-CAT |
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
| [14-event-association.md](14-event-association.md) | 活动关联 | TC-STAGE / TC-TRACK / TC-PREREQ / TC-CATREL |

### 规则引擎（Rule Engine）

| 文件 | 模块 | 用例前缀 |
|------|------|----------|
| [15-entry-rules.md](15-entry-rules.md) | 参加活动规则 | TC-ENTRY |
| [16-closure-rules.md](16-closure-rules.md) | 活动结束规则 | TC-CLOSE |
| [17-rule-engine.md](17-rule-engine.md) | 声明式规则引擎 | TC-ENGINE |

### 用户旅程场景（User Journey Scenarios）

| 文件 | 模块 | 用例前缀 |
|------|------|----------|
| [18-content-browsing.md](18-content-browsing.md) | 内容浏览 | TC-BROWSE |
| [19-auth-profile.md](19-auth-profile.md) | 认证与个人资料 | TC-AUTH |
| [20-notification.md](20-notification.md) | 通知系统 | TC-NOTIFY |
| [21-event-management.md](21-event-management.md) | 活动管理 | TC-EVTMGMT |
| [22-team-management.md](22-team-management.md) | 团队管理 | TC-TEAM |
| [23-activity-participation.md](23-activity-participation.md) | 参与活动与提交 | TC-PART |
| [24-content-creation.md](24-content-creation.md) | 内容创作与迭代 | TC-CREATE |
| [25-social-interaction.md](25-social-interaction.md) | 社交互动与反馈 | TC-SOCIAL |
| [26-settlement-reward.md](26-settlement-reward.md) | 活动结算与奖励发放 | TC-SETTLE |
| [27-bounty-enterprise.md](27-bounty-enterprise.md) | 悬赏与企业出题 | TC-BOUNTY |
| [28-personalization.md](28-personalization.md) | 个性化设置 | TC-PERSON |
| [29-planet-camp.md](29-planet-camp.md) | 星球与营地页面 | TC-PLANET |
| [30-proposal-iteration.md](30-proposal-iteration.md) | 提案迭代与版本日志 | TC-PROPOSAL |
| [31-page-interaction.md](31-page-interaction.md) | 页面交互与 UI 组件 | TC-UI |
| [32-asset-copy-request.md](32-asset-copy-request.md) | 资产复制申请 | TC-ASSET |

### 前端集成（Frontend Integration）

| 文件 | 模块 | 用例前缀 |
|------|------|----------|
| [33-frontend-integration.md](33-frontend-integration.md) | 前后端集成测试 | TC-FE |
