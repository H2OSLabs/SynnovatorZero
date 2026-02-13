# 管理员后台需求文档 (Admin Governance)

本文档基于 Synnovator 管理员后台需求 (v1.0)，定义平台管理员的核心工作流与系统审计功能。

> **参考文档：**
> - 数据结构定义：[data-types.md](../../data-types.md)
> - 实体关系定义：[relationships.md](../../relationships.md)
> - 规则引擎定义：[rule-engine.md](../../rule-engine.md)

---

## 0. 入口与权限 (Access & Permissions)

**前提条件**：当前登录用户的 `user.role` 必须为 `admin`。

### 0.1 进入管理员后台
1. **系统检测**：用户登录后，前端通过 API (`GET /api/me`) 获取用户角色信息。
2. **入口展示**：若检测到 `role: admin`，系统在以下位置显示“管理员后台”入口：
   - 顶部导航栏右侧（Top Navigation Bar）。
   - 用户个人中心菜单（User Dropdown Menu）。
3. **视图切换**：
   - 点击入口后，页面跳转至 `/admin/dashboard`。
   - 界面布局切换为侧边栏管理模式（Sidebar Layout），与普通用户的前台视图（Frontend View）区分。

---

## 1. 全平台数据导航驾驶舱 (Dashboard)

**核心目标**：提供平台运营状态的一站式视觉化监控，支持基础运营数据与增长趋势分析。

### 1.1 基础数据统计 (Real-time Stats)
管理员登录后的首屏概览，展示平台核心指标。

| 指标名称 | 数据来源/计算逻辑 | 对应 Schema |
|---------|-----------------|-------------|
| **实时在线** | WebSocket 连接数或 Session 活跃数 | N/A (System Metric) |
| **累计注册用户** | `COUNT(user)` | [user](../../data-types.md#user) |
| **全平台内容总量** | 聚合统计 `post`, `group`, `event`, `interaction` 总数 | [post](../../data-types.md#post), [event](../../data-types.md#event) |

### 1.2 增长数据分析 (Growth Analytics)
可视化图表展示趋势。

- **活跃度趋势**：展示 DAU (日活), WAU (周活), MAU (月活) 曲线。
- **留存分析**：用户留存率、新用户增长曲线。
- **资源流转**：不同类别 `resource` 的上传量与下载量统计。

### 1.3 活动概览 (Activity Overview)
- **进行中活动**：`COUNT(event WHERE status == 'published')`
- **参与峰值**：当前小时内 `interaction` (type=like/comment) 产生频率最高的活动。
- **热门内容**：基于 `interaction` 统计的 Top 10 热门 Post。

---

## 2. 全平台通知总控中心 (Notification Center)

**核心目标**：集中处理官方下发消息、第三方活动审批及用户反馈。

### 2.1 官方消息群发
由管理员直接发起，支持全局或定向推送。

- **数据模型**：创建 `notification` 记录。
- **筛选维度**：标签 (Tags)、权限级别 (Role)、活跃度 (Last Active)、注册时间。
- **发送渠道**：
  - **系统通知**：`type: system`
  - **站内信**：`type: social` (作为 Admin 发送私信)

### 2.2 活动消息审批流
活动组织者发起的通知需经过管理员审核后下发。

**工作流：**
1. **提交**：组织者提交群发申请（存储为 `pending` 状态的临时通知对象）。
2. **审核**：管理员查看内容与目标人群规则。
3. **处置**：
   - **通过**：系统批量生成 `notification` 记录下发给目标用户。
   - **驳回**：通知组织者修改。

### 2.3 反馈与举报处理
统一收集并处理用户反馈。

**处理流程：**
1. **分类**：意见建议、系统 Bug、投诉举报。
2. **状态管理**：`pending` (待处理) -> `processing` (处理中) -> `resolved` (已解决) / `archived` (已存档)。
3. **联动处置**：
   - 若为举报违规，可直接跳转至 **[用户管理](#31-user-用户管理-权限与关系)** 页面对被举报人执行封禁 (`block` 或 `lock`)。

---

## 3. 全平台数据查询和管理中心 (Data Center)

**核心目标**：实现对用户、内容、团队、活动及资产的精细化配置与关系维护。

### 3.1 User 用户管理 (权限与关系)

**查询维度**：UID、昵称、手机号、权限等级 (`role`)、状态。

**核心操作：**

| 操作 | 对应 Schema/Logic | 说明 |
|------|-------------------|------|
| **关系配置** | [user:user](../../relationships.md#user--user) | 管理关注、好友、拉黑关系 |
| **社群记录** | [user:group](../../relationships.md#group--user) | 查看用户加入的团队及历史记录 |
| **互动足迹** | [target:interaction](../../relationships.md#target--interaction) | 查看用户的发布、点赞、收藏记录 |
| **角色分配** | `UPDATE user SET role = 'organizer'` | 开启/关闭组织者权限（创建活动权） |
| **违规限制** | `UPDATE user SET status = 'banned'` | 禁言、限制登录 |

### 3.2 Post 内容管理

**查询维度**：关键词、内容类型 (`type`)、发布时间、关联活动。

**核心操作：**

| 操作 | 对应 Schema/Logic | 说明 |
|------|-------------------|------|
| **关系配置** | [post:post](../../relationships.md#post--post) | 管理父子页面嵌套、相关推荐 |
| **附件管理** | [post:resource](../../relationships.md#post--resource) | 管理内容关联的附件、资产 |
| **归属管理** | [group:post](../../relationships.md#group--post) | 管理内容归属的团队或频道 |
| **位置置顶** | `UPDATE post_resource SET position = 1` | 利用 `position` 字段或特定 Banner 关系设定固定内容 |
| **内容审核** | `UPDATE post SET status = 'rejected'` | 敏感词过滤、人工隐藏违规内容 |

### 3.3 Group 团队管理

**查询维度**：团队名称、所属活动、成员规模、活跃度。

**核心操作：**

| 操作 | 对应 Schema/Logic | 说明 |
|------|-------------------|------|
| **活动归属** | [event:group](../../relationships.md#event--group) | 查看团队所属的特定活动 |
| **成员管理** | [group:user](../../relationships.md#group--user) | 强制添加/移除成员，变更队长 (`role=owner`) |
| **资产审计** | [group:resource](../../relationships.md#group--resource) | 审计团队拥有的资产/额度 |
| **强制解散** | `DELETE group` (Soft Delete) | 严重违规时强制解散团队 |

### 3.4 Event 活动管理

**核心操作：**
- **规则配置**：编辑 [rule](../../data-types.md#rule) 对象，动态设定时间轴、准入门槛 (`checks`)。
- **交互规则**：针对特定活动配置专有的评分标准 (`scoring_criteria`)。

### 3.5 Interaction 交互管理

**核心操作：**
- **行为审计**：查询原始交互数据 (`like`, `comment`, `rating`)。
- **特殊场景管控**：
  - **投票统计**：针对 `type=vote` 的交互进行防刷票清洗。
  - **竞猜抽奖**：导出交互名单进行随机抽取。

### 3.6 Resource 资产管理

**核心操作：**

| 操作 | 对应 Schema/Logic | 说明 |
|------|-------------------|------|
| **资金池管理** | [asset_pool](../../data-types.md#asset_pool) | 监控活动预算、奖金冻结状态 |
| **关系映射** | `event:resource`, `group:resource` | 查看活动奖励池或团队资产 |
| **批量发放** | `Batch Transfer Workflow` | 管理员一键执行资产分发 |

> **批量发放系统逻辑：**
> 1. **规则结算**：系统基于 `rule.checks` 中的 `compute_ranking` 结果，自动生成待发放清单。
> 2. **人工确认**：管理员在后台复核清单无误。
> 3. **一键执行**：调用 `transfer_asset` 动作，将 `asset_pool` 中的资源批量划转至 User 或 Group 的 Wallet 中。
