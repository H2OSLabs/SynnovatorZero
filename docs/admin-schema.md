# 管理员系统定义与关系 Schema

本文档定义管理员（Admin）在平台中的功能边界、数据模型及与现有内容体系的管理关系。管理员作为系统超级节点，负责维护内容关系、用户权限及资产安全。

## 1. 功能模块定义

基于业务需求，管理员系统划分为八大核心模块：

| 模块名称 | 功能描述 | 关联实体/关系 |
|---------|---------|-------------|
| **数据查看中心** | 平台宏观数据监控（增长、活跃、内容量） | `SystemStats`, `User`, `Event`, `Post` |
| **通知中心** | 官方通知发布、群发消息管理 | `Notification`, `BroadcastTask` |
| **反馈/举报中心** | 处理用户投诉、举报及建议 | `Report`, `Feedback`, `User`, `Target` |
| **权限中心** | 用户角色管理、违规封禁、特定权限控制 | `User.role`, `User.permissions`, `Blacklist` |
| **内容管理** | 内容审核、置顶/推荐、排序逻辑、固定位管理 | `Post`, `Resource`, `SystemConfig` |
| **团队管理** | 团队关系干预、成员纠纷处理 | `Group`, `Group:User` |
| **规则管理** | 活动规则的仲裁、紧急修订 | `Event`, `Rule` |
| **资产管理** | 奖金池冻结、批量发放、资产审计 | `AssetPool`, `Transaction`, `Event:Asset` |

---

## 2. 新增数据实体 Schema

为支撑上述功能，需补充以下管理员专用实体：

### 2.1 Report (举报/投诉)

用户对内容或他人的举报记录。

```yaml
id: string
reporter_id: user_id      # 举报人
target_type: enum         # 举报对象: post | user | group | event | comment
target_id: string         # 对象 ID
reason: enum              # 原因: spam | abuse | illegal | other
description: string       # 详细描述
status: enum              # 处理状态: pending | investigating | resolved | dismissed
result: string            # 处理结果说明
created_at: datetime
resolved_at: datetime
resolved_by: admin_id     # 处理人
```

### 2.2 BroadcastTask (群发任务)

管理员创建的批量通知任务。

```yaml
id: string
type: enum                # 通知类型: system | activity
target_filter: object     # 筛选条件 (e.g., { role: "organizer", last_active: "30d" })
content: string           # 通知内容
status: enum              # 状态: pending | sending | completed | failed
sent_count: integer       # 发送成功数
created_by: admin_id
created_at: datetime
```

### 2.3 AssetPool (活动资产池)

活动对应的资金/奖金池，用于冻结和发放。

```yaml
id: string
event_id: string          # 关联活动
amount: decimal           # 总金额/积分
currency: string          # 货币类型
status: enum              # 状态: pending | frozen | distributing | settled | refunded
                          #   pending      = 草稿/配置中
                          #   frozen       = 活动发布后资金冻结
                          #   distributing = 结算中
                          #   settled      = 已全额发放
                          #   refunded     = 活动取消，资金回退
frozen_at: datetime
settled_at: datetime
```

---

## 3. 管理员与关系的交互模型

管理员作为“关系的维护者”，对系统中的标准关系拥有超越普通用户的干预能力。

### 3.1 权限中心：用户关系管理

管理员可直接干预 `User` 及其属性。

- **权限控制**: 修改 `User.role` 或 `User.permissions`（细粒度权限，如 `can_create_event`）。
- **封禁/限制**: 设置 `User.status = locked`。
- **关系阻断**: 强制解除 `User:User` (Follow) 关系（如清除违规粉）。

### 3.2 内容管理：内容排序与可见性

管理员通过元数据或特殊关系控制内容展示。

- **固定位置 (Fixed Content)**:
  - 通过 `SystemConfig` 维护首页 Banner、公告栏内容。
  - 建立 `System : Post` 虚拟关系（Pinned Posts）。
- **审核 (Moderation)**:
  - 干预 `Post.status` (pending_review -> published/rejected)。
  - 软删除违规内容 (`deleted_at` set)。

### 3.3 团队管理：成员关系仲裁

当团队出现纠纷时，管理员可介入 `Group : User` 关系。

- **强制变更**: 修改 `Group:User.role` (如更换 Owner)。
- **强制移除**: 删除 `Group:User` 关系 (踢出成员)。
- **关系属性**: 可设置 `Group:User` 的特殊标记（如 `is_dispute_locked` 防止变动）。

### 3.4 资产管理：基于规则的批量分发

管理员/系统根据 `Event : Rule` 的结果，批量创建资产转移关系。

- **冻结**: 活动创建时，建立 `Organizer -> AssetPool` 的转移。
- **分发**: 活动结束时，基于排名（Ranking），批量创建 `AssetPool -> User` (Winner) 的 `Transaction` 关系。

### 3.5 规则管理：规则生命周期

- **规则修订**: 在 `Event : Rule` 关系中，允许 Admin 修改关联的 `Rule` 内容，即使在活动进行中（需记录审计日志）。

---

## 4. 管理员视图结构

建议将管理员后台 (Admin Dashboard) 组织为以下层级：

1.  **Dashboard**: 核心数据指标 (Data View)。
2.  **Operations (运营)**:
    -   Content (内容审核、置顶)
    -   Users (用户列表、权限、封禁)
    -   Teams (团队查询、纠纷处理)
3.  **Communication (通讯)**:
    -   Notifications (发布通知、群发)
    -   Inbox (举报处理、反馈回复)
4.  **Finance (财务)**:
    -   Asset Pools (活动资金池监控)
    -   Transactions (流水审计)
5.  **System (系统)**:
    -   Settings (全局配置)
    -   Logs (操作审计)
