# Command

本章定义 Synnovator 平台的数据操作规范，包括七种内容类型和七种关系的 CRUD 操作。

---

## 内容类型 Schema

> **字段命名规范：** 所有内容类型统一使用 `created_by` 表示创建者/作者/上传者。

### category

比赛活动或运营活动，关联不同的 Rule。格式为 YAML frontmatter + Markdown body。

```yaml
---
# === 必填字段 ===
name: string              # 活动名称
description: string       # 活动简介（一句话描述）
type: enum                # 活动类型: competition | operation
                          #   competition = 比赛活动（关联评分、提交类 Rule）
                          #   operation   = 运营活动（关联流程、权限类 Rule）

# === 可选字段 ===
status: enum              # 活动状态: draft | published | closed
                          #   默认: draft
cover_image: string       # 封面图 URL
start_date: datetime      # 活动开始时间
end_date: datetime        # 活动结束时间

# === 自动生成字段 ===
id: string                # 唯一标识（自动生成）
created_by: user_id       # 创建者（自动关联当前用户）
created_at: datetime      # 创建时间
updated_at: datetime      # 最后更新时间
deleted_at: datetime      # 软删除时间（null 表示未删除）
---

<!-- Markdown body: 活动详细说明 -->
```

### post

用户提交的帖子，支持标签系统和自定义渲染。格式为 YAML frontmatter + Markdown body。

```yaml
---
# === 必填字段 ===
title: string             # 帖子标题

# === 可选字段 ===
type: enum                # 帖子类型（可选，不填则为 general）:
                          #   profile      = 个人说明
                          #   team         = 团队介绍
                          #   category     = 活动说明（由活动自动创建）
                          #   for_category = 活动参赛提交
                          #   certificate  = 证书分享
                          #   general      = 日常帖子（默认）
tags: list[string]        # 标签列表（如 ["找队友", "提案", "日记"]）
status: enum              # 帖子状态: draft | pending_review | published | rejected
                          #   draft          = 草稿（默认）
                          #   pending_review = 待审核（Rule 不允许直接发布时）
                          #   published      = 已发布
                          #   rejected       = 审核驳回

# === 自动生成字段 ===
id: string                # 唯一标识
created_by: user_id       # 创建者（自动关联当前用户）
created_at: datetime      # 创建时间
updated_at: datetime      # 最后更新时间
deleted_at: datetime      # 软删除时间（null 表示未删除）

# === 缓存统计字段（自动维护）===
like_count: integer       # 点赞数（默认: 0，interaction 增删时自动更新）
comment_count: integer    # 评论数（默认: 0，interaction 增删时自动更新）
average_rating: number    # 平均评分（默认: null，基于所有 rating interaction 的加权总分均值）
---

<!-- Markdown body: 帖子正文内容 -->
```

**不同 type 的渲染差异：**

| type | 渲染特点 |
|------|----------|
| `profile` | 展示为个人资料卡片 |
| `team` | 展示为团队卡片，含成员列表 |
| `category` | 展示为活动说明页 |
| `for_category` | 展示为参赛作品，含评分/审核状态 |
| `certificate` | 展示为证书卡片，含下载入口 |
| `general` | 标准 Markdown 渲染 |

### resource

上传的附件/文件资源。

```yaml
---
# === 必填字段 ===
filename: string          # 原始文件名

# === 可选字段 ===
display_name: string      # 显示名称（不填则使用 filename）
description: string       # 文件描述

# === 自动生成字段 ===
id: string                # 唯一标识
mime_type: string         # MIME 类型（自动检测）
size: integer             # 文件大小（字节）
url: string               # 文件存储 URL
created_by: user_id       # 创建者（上传者）
created_at: datetime      # 上传时间
updated_at: datetime      # 最后更新时间
deleted_at: datetime      # 软删除时间（null 表示未删除）
---
```

### rule

活动规则，由组织者创建。格式为 YAML frontmatter + Markdown body。固定 schema。

```yaml
---
# === 必填字段 ===
name: string              # 规则名称
description: string       # 规则简介

# === 可选字段（权限控制）===
allow_public: boolean     # 是否允许公开发布（默认: false）
require_review: boolean   # 是否需要审核（默认: false）
reviewers: list[user_id]  # 审核人列表

# === 可选字段（时间限制）===
submission_start: datetime  # 提交开始时间
submission_deadline: datetime # 提交截止时间

# === 可选字段（提交要求）===
submission_format: list[string]   # 允许的提交格式（如 ["markdown", "pdf", "zip"]）
max_submissions: integer          # 最大提交次数（每用户/每团队）
min_team_size: integer            # 最小团队人数
max_team_size: integer            # 最大团队人数

# === 可选字段（评审配置）===
scoring_criteria:                 # 评分标准
  - name: string                  #   标准名称
    weight: number                #   权重（0-100）
    description: string           #   标准说明

# === 自动生成字段 ===
id: string
created_by: user_id
created_at: datetime
updated_at: datetime
deleted_at: datetime      # 软删除时间（null 表示未删除）
---

<!-- Markdown body: 规则详细说明（面向参赛者展示） -->
```

### user

用户信息。

```yaml
---
# === 必填字段 ===
username: string          # 用户名（唯一）
email: string             # 邮箱（唯一）

# === 可选字段 ===
display_name: string      # 显示名称
avatar_url: string        # 头像 URL
bio: string               # 个人简介
role: enum                # 平台角色: participant | organizer | admin
                          #   默认: participant

# === 自动生成字段 ===
id: string
created_at: datetime
updated_at: datetime
deleted_at: datetime      # 软删除时间（null 表示未删除）
---
```

### group

团队/分组，可用于参赛组队、组织方团队、权限分组等。

```yaml
---
# === 必填字段 ===
name: string              # 团队/分组名称

# === 可选字段 ===
description: string       # 团队简介
visibility: enum          # 可见性: public | private（默认: public）
max_members: integer      # 最大成员数
require_approval: boolean # 加入是否需要审批（默认: false）

# === 自动生成字段 ===
id: string
created_by: user_id       # 创建者
created_at: datetime
updated_at: datetime
deleted_at: datetime      # 软删除时间（null 表示未删除）
---
```

### interaction

交互记录，包括点赞、评论、评分等。可指向任意内容类型。

```yaml
---
# === 必填字段 ===
type: enum                # 交互类型: like | comment | rating
target_type: enum         # 目标内容类型: post | category | resource
target_id: string         # 被交互对象的 ID

# === 可选字段 ===
value: string | object    # 交互值（语义取决于 type）:
                          #   like    → 不使用（留空）
                          #   comment → 评论文本内容（string）
                          #   rating  → 多维度评分对象（object），格式见下方说明
parent_id: interaction_id # 父级交互 ID（仅 comment 类型使用，用于嵌套回复）
                          #   不填则为顶层评论

# === 自动生成字段 ===
id: string                # 唯一标识
created_by: user_id       # 创建者（交互发起人）
created_at: datetime      # 创建时间
updated_at: datetime      # 最后更新时间
deleted_at: datetime      # 软删除时间（null 表示未删除）
---
```

**不同 type 的 value 语义：**

| type | value 类型 | 说明 |
|------|-----------|------|
| `like` | — | 不使用（留空） |
| `comment` | `string` | 评论文本（Markdown 格式） |
| `rating` | `object` | 多维度评分对象，Key 与 Rule.scoring_criteria.name 一一对应 |

**rating value 格式规范：**

- value 为 YAML 对象，每个 Key 对应 `rule.scoring_criteria` 中的 `name`
- 每个维度评分范围统一为 **0–100**
- 系统按 `scoring_criteria.weight` 自动加权计算总分：`总分 = Σ(维度分 × weight / 100)`
- value 中还可包含可选的 `_comment` 字段，用于评委留言

```yaml
# rating value 示例
value:
  创新性: 87
  技术实现: 82
  实用价值: 78
  演示效果: 91
  _comment: "架构设计清晰，建议完善错误处理"
# 系统自动加权计算:
#   87×0.30 + 82×0.30 + 78×0.25 + 91×0.15
#   = 26.1 + 24.6 + 19.5 + 13.65 = 83.85
```

### 枚举值汇总

| 内容类型 | 字段 | 可选值 |
|---------|------|-------|
| category | type | `competition`, `operation` |
| category | status | `draft`, `published`, `closed` |
| post | type | `profile`, `team`, `category`, `for_category`, `certificate`, `general` |
| post | status | `draft`, `pending_review`, `published`, `rejected` |
| user | role | `participant`, `organizer`, `admin` |
| group | visibility | `public`, `private` |
| interaction | type | `like`, `comment`, `rating` |
| interaction | target_type | `post`, `category`, `resource` |

| 关系 | 字段 | 可选值 |
|-----|------|-------|
| category:post | relation_type | `submission`, `reference` |
| post:post | relation_type | `reference`, `reply`, `embed` |
| post:resource | display_type | `attachment`, `inline` |
| group:user | role | `owner`, `admin`, `member` |
| group:user | status | `pending`, `accepted`, `rejected` |

---

## 关系 Schema

关系用于连接内容类型，不同关系可以携带属性。

### category : rule

活动关联其规则。一个活动可以关联多条规则。

```yaml
category_id: string       # 活动 ID（必填）
rule_id: string           # 规则 ID（必填）

# === 关系属性 ===
priority: integer         # 规则优先级/排序（默认: 0，数值越小越靠前）
```

### category : post

活动关联帖子（报名内容、参赛提交等）。

```yaml
category_id: string       # 活动 ID（必填）
post_id: string           # 帖子 ID（必填）

# === 关系属性 ===
relation_type: enum       # 关联类型: submission | reference
                          #   submission = 参赛提交
                          #   reference  = 引用/展示
created_at: datetime      # 关联时间（自动生成）
```

### category : group

团队在特定活动中的报名绑定。一个用户在不同活动中可以代表不同团队，通过此关系进行隔离。

```yaml
category_id: string       # 活动 ID（必填）
group_id: string          # 团队 ID（必填）

# === 关系属性 ===
registered_at: datetime   # 报名时间（自动生成）
```

> **业务规则：** 同一 group 在同一 category 中只能注册一次。一个 user 可以通过不同 group 参加不同 category，但在同一 category 中只能属于一个 group。

### post : post

帖子间关联（引用、回复、嵌入等）。

```yaml
source_post_id: string    # 发起关联的帖子 ID（必填）
target_post_id: string    # 被关联的帖子 ID（必填）

# === 关系属性 ===
relation_type: enum       # 关联类型: reference | reply | embed
                          #   reference = 引用
                          #   reply     = 回复
                          #   embed     = 嵌入（如插入团队卡片）
position: integer         # 在帖子中的显示位置/排序
```

### post : resource

帖子关联附件资源。

```yaml
post_id: string           # 帖子 ID（必填）
resource_id: string       # 资源 ID（必填）

# === 关系属性 ===
display_type: enum        # 展示方式: attachment | inline
                          #   attachment = 附件（底部下载列表）
                          #   inline     = 内联（正文中嵌入展示）
position: integer         # 排序位置
```

### group : user

分组关联成员。支持审批流程：当 Group 设置 `require_approval: true` 时，新成员加入需经过 Owner/Admin 审批。

```yaml
group_id: string          # 分组 ID（必填）
user_id: string           # 用户 ID（必填）

# === 关系属性 ===
role: enum                # 成员角色: owner | admin | member
                          #   owner  = 组长/创建者
                          #   admin  = 管理员
                          #   member = 普通成员
status: enum              # 成员状态: pending | accepted | rejected
                          #   pending  = 申请中（等待审批）
                          #   accepted = 已加入（审批通过或无需审批时自动设置）
                          #   rejected = 已拒绝
                          #   当 Group.require_approval = false 时，CREATE 自动设为 accepted
                          #   当 Group.require_approval = true 时，CREATE 默认为 pending
joined_at: datetime       # 加入时间（status 变为 accepted 时自动记录）
status_changed_at: datetime  # 状态变更时间（每次 status 变更时自动更新）
```

**状态流转：**

```
                  require_approval=false
  CREATE ─────────────────────────────────→ accepted
    │
    │             require_approval=true
    └─────────────────────────────────────→ pending
                                              │
                              Owner/Admin ────┤
                              审批            │
                                ┌─────────────┴─────────────┐
                                ↓                           ↓
                            accepted                    rejected
```

### target : interaction

内容对象关联其交互记录（点赞、评论、评分）。这是一个通用关系，target 可以是 post、category 或 resource。

```yaml
target_type: enum         # 目标类型: post | category | resource（必填）
target_id: string         # 目标对象 ID（必填）
interaction_id: string    # 交互记录 ID（必填）
```

> **权限规则：** 只要目标对象（post/category/resource）对当前用户可见，其关联的所有 interaction 即公开可读。

---

## 数据完整性约束

### 唯一性约束

| 类型 | 约束 | 说明 |
|------|-----|------|
| user | `(username)` | 用户名全局唯一 |
| user | `(email)` | 邮箱全局唯一 |
| interaction (like) | `(created_by, target_type, target_id)` | 同一用户对同一目标只能点赞一次 |
| category:rule | `(category_id, rule_id)` | 同一规则不能重复关联到同一活动 |
| category:group | `(category_id, group_id)` | 同一团队不能重复报名同一活动 |
| group:user | `(group_id, user_id)` | 同一用户不能重复加入同一分组 |

> **业务唯一性规则：** 同一用户在同一 category 中只能属于一个 group。此约束需在应用层校验：`CREATE category:group` 时检查该 group 的所有 accepted 成员是否已通过其他 group 参加了同一 category。

### 软删除策略

所有内容类型（category、post、resource、rule、user、group、interaction）均支持**软删除**：

- **软删除**：设置 `deleted_at = 当前时间`，数据保留在数据库中
- **硬删除**：物理删除记录，仅用于关系解除（见下方说明）

**查询过滤规则：**

- 默认查询自动添加 `WHERE deleted_at IS NULL` 过滤
- 管理员可通过特殊参数查询已软删除的记录
- 软删除的内容对非管理员用户不可见

**级联策略：**

| 操作 | 级联行为 |
|------|---------|
| 软删除 category | 关联的 interaction 一并软删除；关系保留但查询时按目标可见性过滤 |
| 软删除 post | 关联的 interaction 一并软删除 |
| 软删除 user | 该用户的所有 interaction 一并软删除；group:user 关系保留（标记为离组） |
| 软删除 group | group:user 关系保留（成员可查询历史） |

**恢复机制：**

- 恢复操作：设置 `deleted_at = NULL`
- 级联恢复：恢复父对象时，一并恢复因级联而软删除的子对象
- 恢复权限：仅 Admin 可执行恢复操作

### 引用完整性

**外键约束：**

| 字段 | 引用目标 | 约束行为 |
|------|---------|---------|
| `*.created_by` | user.id | 限制删除（不可删除仍有内容的用户） |
| category:rule.category_id | category.id | 级联软删除时解除 |
| category:rule.rule_id | rule.id | 级联软删除时解除 |
| category:post.post_id | post.id | 级联软删除时解除 |
| category:group.group_id | group.id | 级联软删除时解除 |
| group:user.user_id | user.id | 保留（标记为离组） |
| interaction.parent_id | interaction.id | 级联软删除子回复 |

**多态引用（interaction）的完整性保障：**

interaction 通过 `(target_type, target_id)` 引用不同内容类型，无法使用数据库级外键。保障策略：

1. **写入校验**：CREATE interaction 时验证 `target_id` 对应的记录存在且未被软删除
2. **读取过滤**：READ interaction 时联查目标对象，过滤目标已软删除的记录
3. **孤儿清理**：定期任务检测并标记目标已不存在的 interaction 记录

### 建议索引

| 索引 | 字段 | 用途 |
|------|-----|------|
| 内容列表查询 | `(type, status, deleted_at, created_at DESC)` | category/post 列表按状态和时间排序 |
| 用户内容查询 | `(created_by, deleted_at, created_at DESC)` | 查询某用户创建的所有内容 |
| 交互记录查询 | `(target_type, target_id, type, deleted_at)` | 查询目标的点赞/评论/评分 |
| 嵌套评论查询 | `(parent_id, deleted_at, created_at)` | 查询评论的子回复 |
| 分组成员查询 | `(group_id, status)` | 查询分组的有效成员 |
| 活动报名查询 | `(category_id)` on category:group | 查询活动的报名团队 |
| 软删除过滤 | `(deleted_at)` on 所有内容类型 | 加速 `deleted_at IS NULL` 过滤 |

---

## 规范化建议

以下字段当前采用**内嵌（denormalized）**形式存储，而非拆分为独立实体：

| 字段 | 所属类型 | 内嵌形式 | 内嵌理由 |
|------|---------|---------|---------|
| `tags` | post | `list[string]` | 标签为自由文本，无需全局去重或独立管理 |
| `reviewers` | rule | `list[user_id]` | 审核人列表规模小（通常 < 10），随规则生命周期管理 |
| `scoring_criteria` | rule | 内嵌对象列表 | 评分标准与规则强绑定，跨规则不复用 |

**拆分为独立实体的时机：**

- **tags**：当需要全局标签管理（合并/重命名/统计）或标签数量超过百级别时，拆分为 `tag` 实体 + `post:tag` 关系
- **reviewers**：当需要审核人工作量统计、审核任务分配等功能时，拆分为 `rule:user` 关系（role=reviewer）
- **scoring_criteria**：当多个规则需要共享同一套评分标准，或需要独立管理评分维度时，拆分为 `criteria` 实体

> **原则：** 在当前规模下优先简单性，避免过早引入关系表带来的查询复杂度。当业务需求明确要求跨实体管理时再进行拆分。

---

## CRUD 操作

### Create

#### 创建内容

| 操作 | 说明 | 权限 |
|------|------|------|
| `CREATE category` | 创建活动，填写 YAML + Markdown | Organizer, Admin |
| `CREATE post` | 创建帖子，编写 Markdown 内容 | 已登录用户 |
| `CREATE resource` | 上传文件资源 | 已登录用户 |
| `CREATE rule` | 创建活动规则 | Organizer, Admin |
| `CREATE user` | 注册新用户 | 任何人 |
| `CREATE group` | 创建团队/分组 | 已登录用户 |
| `CREATE interaction` | 创建交互记录（点赞/评论/评分） | 已登录用户（目标对象须可见） |

#### 创建关系

| 操作 | 说明 | 权限 |
|------|------|------|
| `CREATE category:rule` | 将 Rule 关联到活动 | Category 创建者, Admin |
| `CREATE category:post` | 将 Post 关联到活动（报名/提交） | Post 作者（需符合 Rule） |
| `CREATE category:group` | 团队报名活动（建立团队与活动的绑定） | Group Owner（需符合 Rule 的团队人数要求） |
| `CREATE post:post` | 帖子间建立关联（引用/回复/嵌入） | 发起方 Post 作者 |
| `CREATE post:resource` | 将资源关联到帖子 | Post 作者 |
| `CREATE group:user` | 将用户加入分组（require_approval=true 时 status 初始为 pending） | Group owner/admin, 或自助申请 |
| `CREATE target:interaction` | 将交互记录关联到目标对象 | 交互发起人（目标对象须可见） |

### Read

#### 读取内容

| 操作 | 说明 | 权限 |
|------|------|------|
| `READ category` | 读取活动列表或详情 | 公开活动: 任何人；草稿: 创建者/Admin |
| `READ post` | 读取帖子列表或详情，支持按 tag/type 筛选 | 已发布: 任何人；草稿: 作者/Admin |
| `READ resource` | 读取/下载文件资源 | 关联帖子可见则可读 |
| `READ rule` | 读取活动规则 | 关联活动可见则可读 |
| `READ user` | 读取用户信息 | 公开信息: 任何人；完整信息: 本人/Admin |
| `READ group` | 读取分组信息及成员列表 | public: 任何人；private: 成员/Admin |
| `READ interaction` | 读取交互记录（支持按 type 筛选） | 目标对象可见则可读 |

#### 读取关系

| 操作 | 说明 |
|------|------|
| `READ category:rule` | 查询活动关联的所有规则 |
| `READ category:post` | 查询活动关联的所有帖子（可按 relation_type 筛选） |
| `READ category:group` | 查询活动的报名团队列表 |
| `READ post:post` | 查询帖子的关联帖子（可按 relation_type 筛选） |
| `READ post:resource` | 查询帖子的关联资源 |
| `READ group:user` | 查询分组的成员列表（含角色和状态信息，可按 status 筛选） |
| `READ target:interaction` | 查询目标对象的交互记录（可按 interaction.type 筛选） |

### Update

#### 更新内容

| 操作 | 说明 | 权限 |
|------|------|------|
| `UPDATE category` | 更新活动信息或状态变更（draft→published→closed） | 创建者, Admin |
| `UPDATE post` | 更新帖子内容、添加/修改 tag、状态变更 | 作者（编辑他人帖子需 Rule 允许或副本机制） |
| `UPDATE resource` | 更新资源元信息（display_name, description） | 上传者, Admin |
| `UPDATE rule` | 更新规则配置 | 创建者, Admin |
| `UPDATE user` | 更新用户信息 | 本人, Admin |
| `UPDATE group` | 更新分组信息和设置 | Owner, Admin |
| `UPDATE interaction` | 更新交互内容（如修改评论文本、修改评分） | 交互发起人本人 |

**缓存统计字段规范：**

以下字段为**只读缓存**，不支持手动 UPDATE，仅由系统在 interaction 变更时自动维护。

| 缓存字段 | 触发条件 | 计算逻辑 |
|---------|---------|---------|
| `like_count` | interaction (type=like) 的 CREATE / DELETE | `COUNT(*)` 关联的未删除 like interaction |
| `comment_count` | interaction (type=comment) 的 CREATE / DELETE | `COUNT(*)` 关联的未删除 comment interaction（含嵌套回复） |
| `average_rating` | interaction (type=rating) 的 CREATE / UPDATE / DELETE | 所有未删除 rating interaction 的加权总分均值（权重来自 rule.scoring_criteria） |

**一致性模型：**

- **最终一致性**：缓存字段在 interaction 变更后异步更新，短暂延迟可接受
- **全量重算**：每次触发时对该 post 的所有有效 interaction 重新计算，而非增量更新，确保数据准确
- **缓存重建**：提供管理员命令，可对指定 post 或全量 post 重建缓存统计
- **容错机制**：缓存更新失败时记录日志，不影响 interaction 本身的写入；下次触发时自动修正

#### 更新关系属性

| 操作 | 说明 |
|------|------|
| `UPDATE category:rule` | 修改规则优先级等属性 |
| `UPDATE category:post` | 修改关联类型（如 reference→submission） |
| `UPDATE post:post` | 修改关联类型或排序位置 |
| `UPDATE post:resource` | 修改展示方式或排序位置 |
| `UPDATE group:user` | 修改成员角色（如 member→admin）或审批状态（pending→accepted/rejected） |

**组队审批操作规范：**

| 场景 | 操作 | 权限 | status 变更 |
|------|------|------|------------|
| 申请加入 | `CREATE group:user` | 申请人自身 | → `pending`（require_approval=true 时） |
| 批准加入 | `UPDATE group:user` | Group Owner/Admin | `pending` → `accepted` |
| 拒绝加入 | `UPDATE group:user` | Group Owner/Admin | `pending` → `rejected` |
| 直接加入 | `CREATE group:user` | 申请人自身 | → `accepted`（require_approval=false 时） |
| 重新申请 | `CREATE group:user` | 申请人自身 | 删除旧 rejected 记录，新建 `pending` |

### Delete

#### 删除内容

> **默认软删除：** 内容类型的 DELETE 操作默认执行**软删除**（设置 `deleted_at`），详见"数据完整性约束 > 软删除策略"。

| 操作 | 说明 | 权限 | 级联影响 |
|------|------|------|----------|
| `DELETE category` | 删除活动 | 创建者, Admin | 解除所有 category:rule、category:post、category:group 关系，删除关联 interaction |
| `DELETE post` | 删除帖子 | 作者, Admin | 解除所有 post:post、post:resource、category:post 关系，删除关联 interaction |
| `DELETE resource` | 删除文件资源 | 上传者, Admin | 解除所有 post:resource 关系，删除关联 interaction |
| `DELETE rule` | 删除规则 | 创建者, Admin | 解除所有 category:rule 关系 |
| `DELETE user` | 删除/注销用户 | 本人, Admin | 解除所有 group:user 关系，删除所有该用户的 interaction |
| `DELETE group` | 删除分组 | Owner, Admin | 解除所有 group:user、category:group 关系 |
| `DELETE interaction` | 删除交互记录 | 交互发起人, Admin | 若为父评论，级联删除所有子回复 |

#### 删除关系

> **硬删除：** 关系的 DELETE 操作执行**物理删除**，直接移除关联记录。关系不设 `deleted_at` 字段。

| 操作 | 说明 |
|------|------|
| `DELETE category:rule` | 解除活动与规则的关联 |
| `DELETE category:post` | 解除活动与帖子的关联 |
| `DELETE category:group` | 解除团队与活动的报名绑定 |
| `DELETE post:post` | 解除帖子间的关联 |
| `DELETE post:resource` | 解除帖子与资源的关联 |
| `DELETE group:user` | 将成员移出分组（或撤回申请） |
| `DELETE target:interaction` | 解除目标对象与交互记录的关联 |

---

## Example

### 内容示例

#### 创建一个比赛活动（category）

```yaml
---
name: "2025 AI Hackathon"
description: "面向全球开发者的 AI 创新大赛"
type: competition
status: draft
cover_image: "https://example.com/cover.png"
start_date: "2025-03-01T00:00:00Z"
end_date: "2025-03-15T23:59:59Z"
---

## 活动介绍

本次 Hackathon 面向全球 AI 开发者，鼓励参赛者利用大语言模型构建创新应用。

## 赛道

- **应用创新赛道**：构建面向终端用户的 AI 应用
- **工具赛道**：构建面向开发者的 AI 工具

## 奖项

| 奖项 | 奖金 |
|------|------|
| 一等奖 | ¥50,000 |
| 二等奖 | ¥20,000 |
| 三等奖 | ¥10,000 |
```

#### 创建活动规则（rule）

```yaml
---
name: "AI Hackathon 提交规则"
description: "2025 AI Hackathon 参赛提交规范"
allow_public: true
require_review: true
reviewers: ["user_judge_01", "user_judge_02", "user_judge_03"]
submission_start: "2025-03-01T00:00:00Z"
submission_deadline: "2025-03-14T23:59:59Z"
submission_format: ["markdown", "pdf", "zip"]
max_submissions: 3
min_team_size: 1
max_team_size: 5
scoring_criteria:
  - name: "创新性"
    weight: 30
    description: "方案的原创性和创新程度"
  - name: "技术实现"
    weight: 30
    description: "代码质量、架构设计、技术深度"
  - name: "实用价值"
    weight: 25
    description: "解决实际问题的程度和商业潜力"
  - name: "演示效果"
    weight: 15
    description: "Demo 完成度和展示效果"
---

## 提交要求

1. 提交内容必须包含：项目说明文档（Markdown）、源代码（zip）、演示视频链接
2. 项目说明需涵盖：问题定义、解决方案、技术架构、使用说明
3. 所有提交内容必须为参赛期间原创

## 评审流程

- 初审：提交截止后 3 个工作日内完成
- 复审：初审通过项目进入路演环节
- 终审：路演后由评委打分，按加权总分排名
```

#### 创建参赛提交帖（post, type=for_category）

```yaml
---
title: "AI 代码审查助手 — CodeReview Copilot"
type: for_category
tags: ["AI", "开发者工具", "代码审查"]
status: published
---

## 项目简介

CodeReview Copilot 是一款基于大语言模型的智能代码审查工具，
能自动识别代码中的潜在问题并给出改进建议。

## 技术方案

- 基于 AST 解析 + LLM 理解的双层分析架构
- 支持 Python、JavaScript、Go 等主流语言

## 演示

[Demo 视频](https://example.com/demo.mp4)
```

#### 创建团队介绍帖（post, type=team）

```yaml
---
title: "Team Synnovator"
type: team
tags: ["全栈", "AI"]
status: published
---

## 团队介绍

我们是一支专注于 AI 应用开发的全栈团队，成员来自不同技术背景。

## 成员

- **Alice** — 后端开发，擅长分布式系统
- **Bob** — 前端开发，擅长 React/Next.js
- **Carol** — AI 工程师，擅长 LLM 应用
```

#### 创建个人说明帖（post, type=profile）

```yaml
---
title: "关于我"
type: profile
tags: ["后端", "AI", "开源"]
status: published
---

## 自我介绍

全栈开发者，3 年 AI 应用开发经验，热爱开源。

## 技能

- Python / Go / TypeScript
- LLM 应用开发
- 分布式系统设计

## 联系方式

- GitHub: @alice
- Email: alice@example.com
```

#### 注册用户（user）

```yaml
---
username: "alice"
email: "alice@example.com"
display_name: "Alice Chen"
avatar_url: "https://example.com/avatars/alice.png"
bio: "全栈开发者，AI 爱好者"
role: participant
---
```

#### 创建团队（group）

```yaml
---
name: "Team Synnovator"
description: "AI Hackathon 参赛团队"
visibility: public
max_members: 5
require_approval: true
---
```

#### 上传资源（resource）

```yaml
---
filename: "project-demo.mp4"
display_name: "项目演示视频"
description: "CodeReview Copilot 功能演示，时长 3 分钟"
---
```

### 关系示例

#### 关联规则到活动（category : rule）

```yaml
# 将提交规则绑定到 AI Hackathon
category_id: "cat_ai_hackathon_2025"
rule_id: "rule_submission_01"
priority: 1
```

#### 报名参赛 — 关联帖子到活动（category : post）

```yaml
# 将参赛提交关联到活动
category_id: "cat_ai_hackathon_2025"
post_id: "post_codereview_copilot"
relation_type: submission
```

#### 团队报名活动（category : group）

```yaml
# Team Synnovator 报名参加 AI Hackathon
category_id: "cat_ai_hackathon_2025"
group_id: "grp_team_synnovator"
# registered_at 自动生成
```

#### 帖子中嵌入团队卡片（post : post）

```yaml
# 在参赛帖中嵌入团队介绍
source_post_id: "post_codereview_copilot"
target_post_id: "post_team_synnovator"
relation_type: embed
position: 1
```

#### 帖子引用另一个帖子（post : post）

```yaml
# 帖子中引用已有提案
source_post_id: "post_looking_for_teammates"
target_post_id: "post_codereview_copilot"
relation_type: reference
position: 0
```

#### 帖子关联附件（post : resource）

```yaml
# 将演示视频附加到参赛帖
post_id: "post_codereview_copilot"
resource_id: "res_project_demo_mp4"
display_type: inline
position: 0
```

#### 成员加入团队（group : user）

```yaml
# 创建者自动成为 owner（status 自动设为 accepted）
group_id: "grp_team_synnovator"
user_id: "user_alice"
role: owner
status: accepted
```

```yaml
# 新成员申请加入（require_approval=true 时，status 初始为 pending）
group_id: "grp_team_synnovator"
user_id: "user_bob"
role: member
status: pending
```

#### 组队审批流程（group : user status 变更）

```yaml
# 步骤 1: Bob 申请加入团队（CREATE group:user）
group_id: "grp_team_synnovator"
user_id: "user_bob"
role: member
status: pending              # require_approval=true → 自动为 pending
```

```yaml
# 步骤 2: Alice（Owner）批准 Bob 的申请（UPDATE group:user）
group_id: "grp_team_synnovator"
user_id: "user_bob"
status: accepted             # pending → accepted
# joined_at 自动记录为此刻时间
```

```yaml
# 备选: Alice（Owner）拒绝 Carol 的申请（UPDATE group:user）
group_id: "grp_team_synnovator"
user_id: "user_carol"
status: rejected             # pending → rejected
```

#### 对帖子点赞（target : interaction, type=like）

```yaml
# 交互记录
target_type: post
target_id: "post_codereview_copilot"
interaction_id: "iact_like_001"
```

```yaml
# 对应的 interaction 内容
---
type: like
target_type: post
target_id: "post_codereview_copilot"
---
```

#### 发表评论与嵌套回复（target : interaction, type=comment）

```yaml
# 顶层评论 interaction
---
type: comment
target_type: post
target_id: "post_codereview_copilot"
value: "方案很有创意！AST + LLM 的组合方式值得关注。请问支持哪些 CI/CD 集成？"
---
```

```yaml
# 嵌套回复（parent_id 指向上面的顶层评论）
---
type: comment
target_type: post
target_id: "post_codereview_copilot"
parent_id: "iact_comment_001"
value: "目前支持 GitHub Actions 和 GitLab CI，Jenkins 插件正在开发中。"
---
```

#### 评委多维度评分（target : interaction, type=rating）

```yaml
# 评分 interaction —— value 为多维度对象，Key 与 Rule.scoring_criteria.name 一一对应
# 每个维度统一 0-100 分，系统按 weight 加权计算总分
---
type: rating
target_type: post
target_id: "post_codereview_copilot"
value:
  创新性: 87                # 0-100，对应 Rule scoring_criteria weight=30
  技术实现: 82              # 0-100，对应 weight=30
  实用价值: 78              # 0-100，对应 weight=25
  演示效果: 91              # 0-100，对应 weight=15
  _comment: "架构设计清晰，建议完善错误处理"
---
# 系统自动加权计算:
#   创新性:   87 × 30/100 = 26.10
#   技术实现: 82 × 30/100 = 24.60
#   实用价值: 78 × 25/100 = 19.50
#   演示效果: 91 × 15/100 = 13.65
#   ─────────────────────────────
#   加权总分: 83.85
#
# 此分数计入 post.average_rating 的均值计算
```

### 场景串联示例：从创建活动到互动评审

以下展示一个完整场景中涉及的数据操作序列：

```
=== 阶段一：组织者创建活动 ===
1.  Organizer: CREATE category           → 创建 "2025 AI Hackathon"
2.  Organizer: CREATE rule               → 创建提交规则（含多维度 scoring_criteria）
3.  Organizer: CREATE category:rule      → 将规则关联到活动
4.  Organizer: UPDATE category (status→published) → 发布活动

=== 阶段二：参赛者组队（含审批流程） ===
5.  Participant(Alice): READ category + READ rule → 浏览活动详情和规则
6.  Participant(Alice): CREATE group     → 创建团队（require_approval=true）
7.  Participant(Alice): CREATE group:user (role=owner, status=accepted) → 创建者自动成为组长
8.  Participant(Bob):   CREATE group:user (role=member, status=pending) → Bob 申请加入团队
9.  Participant(Alice): UPDATE group:user (status→accepted) → Alice 批准 Bob 加入
10. Participant(Carol): CREATE group:user (role=member, status=pending) → Carol 申请加入
11. Participant(Alice): UPDATE group:user (status→rejected) → Alice 拒绝 Carol

=== 阶段三：团队报名活动 ===
12. Participant(Alice): CREATE category:group → 团队报名活动（绑定 group 到 category）

=== 阶段四：参赛提交 ===
13. Participant(Alice): CREATE post (type=team)  → 创建团队介绍帖
14. Participant(Alice): CREATE post (type=for_category) → 创建参赛提交帖
15. Participant(Alice): CREATE post:post (embed) → 在参赛帖中嵌入团队卡片
16. Participant(Alice): CREATE resource  → 上传演示视频
17. Participant(Alice): CREATE post:resource → 关联视频到参赛帖
18. Participant(Alice): CREATE category:post (submission) → 将参赛帖关联到活动
19. Participant(Alice): UPDATE post (status→published) → 发布参赛帖

=== 阶段五：社区互动 ===
20. Participant(Dave): CREATE interaction (type=like)    → 对参赛帖点赞
21. Participant(Dave): CREATE target:interaction         → 关联点赞到帖子
    [系统自动] UPDATE post.like_count (+1)              → 更新点赞计数缓存
22. Participant(Eve):  CREATE interaction (type=comment) → 发表评论
23. Participant(Eve):  CREATE target:interaction         → 关联评论到帖子
    [系统自动] UPDATE post.comment_count (+1)           → 更新评论计数缓存
24. Participant(Alice): CREATE interaction (type=comment, parent_id=上一条) → 回复评论
    [系统自动] UPDATE post.comment_count (+1)           → 更新评论计数缓存

=== 阶段六：评审多维度评分 ===
25. Organizer(Judge): CREATE interaction (type=rating)  → 评委多维度打分
    value: { 创新性: 87, 技术实现: 82, 实用价值: 78, 演示效果: 91 }
26. Organizer(Judge): CREATE target:interaction         → 关联评分到参赛帖
    [系统自动] UPDATE post.average_rating               → 重算加权总分均值（83.85）
```
