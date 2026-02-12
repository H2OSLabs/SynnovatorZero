# 内容类型 Schema

本文档定义 Synnovator 平台的八种内容类型及其 Schema。

> **字段命名规范：** 所有内容类型统一使用 `created_by` 表示创建者/作者/上传者。

---

## event

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
status: enum              # 活动状态: draft | pending_review | published | rejected | closed
                          #   draft          = 草稿（默认）
                          #   pending_review = 待审核（提交后）
                          #   published      = 已发布（审核通过，资产冻结）
                          #   rejected       = 审核驳回
                          #   closed         = 已结束（资产结算）
cover_image: string       # 封面图 URL
start_date: datetime      # 活动开始时间
end_date: datetime        # 活动结束时间
asset_pool_id: string     # 关联的资产池 ID（用于奖金管理）

# === 自动生成字段 ===
id: string                # 唯一标识（自动生成）
created_by: user_id       # 创建者（自动关联当前用户）
created_at: datetime      # 创建时间
updated_at: datetime      # 最后更新时间
deleted_at: datetime      # 软删除时间（null 表示未删除）
---

<!-- Markdown body: 活动详细说明 -->
```

## post

用户提交的帖子，支持标签系统和自定义渲染。格式为 YAML frontmatter + Markdown body。

```yaml
---
# === 必填字段 ===
title: string             # 帖子标题

# === 可选字段 ===
type: enum                # 帖子类型（可选，不填则为 general）:
                          #   profile      = 个人说明
                          #   team         = 团队介绍
                          #   event     = 活动说明（由活动自动创建）
                          #   proposal     = 提案（可独立存在，也可关联活动参赛）
                          #   certificate  = 证书分享
                          #   general      = 日常帖子（默认）
                          #   可用枚举可通过 GET /api/meta/post-types 获取
                          #   兼容说明：如历史数据中存在未知 type，API 会在返回时回退为 general
tags: list[string]        # 标签列表（如 ["找队友", "提案", "日记"]）
status: enum              # 帖子状态: draft | pending_review | published | rejected
                          #   draft          = 草稿（默认）
                          #   pending_review = 待审核（Rule 不允许直接发布时）
                          #   published      = 已发布（终态，不可逆转）
                          #   rejected       = 审核驳回（可修订后重置为 draft）
                          #   状态机: draft → pending_review → published | rejected
                          #           rejected → draft（修订重提）
                          #           private 帖子可跳过 pending_review: draft → published
                          #   如需修改已发布帖子，应创建新版本（重置为 draft）。
visibility: enum          # 可见性: public | private（默认: public）
                          #   public  = 遵循 status 控制的标准可见性规则
                          #   private = 仅作者和 Admin 可见；
                          #             发布时跳过 pending_review 流程，
                          #             可直接 draft → published

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
| `event` | 展示为活动说明页 |
| `proposal` | 展示为提案卡片，含评分/审核状态 |
| `certificate` | 展示为证书卡片，含下载入口 |
| `general` | 标准 Markdown 渲染 |

## resource

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

## rule

活动规则，由组织者创建。格式为 YAML frontmatter + Markdown body。

支持两种约束定义方式：**固定字段**（向后兼容的语法糖）和 **声明式 checks**（可扩展的条件-动作组合）。详见 [rule-engine.md](./rule-engine.md)。

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

# === 可选字段（声明式规则引擎）===
checks:                           # 声明式条件-动作列表
  - trigger: string               #   操作点（如 create_relation(event_post)）
    phase: enum                   #   执行阶段: pre | post
    condition:                    #   条件定义（pre 阶段必填）
      type: string                #     条件类型（time_window | count | exists | field_match |
                                  #       resource_format | resource_required | unique_per_scope | aggregate）
      params: object              #     条件参数（因类型而异）
    on_fail: enum                 #   失败行为: deny | warn | flag（默认: deny）
    action: string                #   动作类型（仅 post 阶段使用: flag_disqualified |
                                  #     compute_ranking | award_certificate | notify | transfer_asset）
    action_params: object         #   动作参数
    message: string               #   人类可读提示信息

# === 自动生成字段 ===
id: string
created_by: user_id
created_at: datetime
updated_at: datetime
deleted_at: datetime      # 软删除时间（null 表示未删除）
---

<!-- Markdown body: 规则详细说明（面向参赛者展示） -->
```

> **固定字段与 checks 的关系：** 固定字段（`submission_deadline`、`max_submissions` 等）是 checks 的语法糖，引擎内部自动展开为等价的 checks 条目。两种方式可混合使用，固定字段展开的 checks 排在用户自定义 checks 之前。详细展开规则见 [rule-engine.md](./rule-engine.md#固定字段展开规则)。

## user

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

## group

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

## interaction

交互记录，包括点赞、评论、评分等。interaction 本身不存储目标信息，与目标内容的关联通过 `target:interaction` 关系维护。

```yaml
---
# === 必填字段 ===
type: enum                # 交互类型: like | comment | rating

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

> **设计说明：** interaction 与目标内容（post/event/resource）的关联完全由 `target:interaction` 关系表维护，interaction 实体不冗余存储 `target_type` 和 `target_id`。这使得七种关系保持对称一致——所有实体间的连接均通过独立关系表管理。

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

---

## notification

系统通知，用于推送活动状态变更、团队邀请、评审结果等消息给用户。

```yaml
---
# === 必填字段 ===
type: enum                # 通知类型: system | activity | team | social
                          #   system   = 系统通知（平台公告、维护提醒）
                          #   activity = 活动通知（报名成功、活动开始/结束、颁奖）
                          #   team     = 团队通知（邀请、申请、审批结果）
                          #   social   = 社交通知（关注、评论、点赞）
content: string           # 通知内容

# === 可选字段 ===
title: string             # 通知标题（不填则使用 type 默认标题）
related_url: string       # 相关链接（点击跳转目标）
is_read: boolean          # 是否已读（默认: false）

# === 自动生成字段 ===
id: string                # 唯一标识
user_id: user_id          # 接收者（目标用户）
created_at: datetime      # 创建时间
---
```

> **设计说明：** notification 不支持软删除，已读通知可通过定期清理任务归档。用户可批量标记已读，但不能删除系统发送的通知。

## notification_template

系统通知模板，用于标准化各类通知内容。

```yaml
---
# === 必填字段 ===
key: string               # 模板唯一键 (e.g., "activity_approved")
title_template: string    # 标题模板 (支持 {{var}} 替换)
content_template: string  # 内容模板 (支持 {{var}} 替换)
type: enum                # 默认通知类型: system | activity | team | social

# === 自动生成字段 ===
id: string
updated_at: datetime
---
```

## asset_pool

活动资产池，用于管理活动奖金和资源冻结。

```yaml
---
# === 必填字段 ===
event_id: string          # 关联活动
amount: decimal           # 总金额/积分
currency: string          # 货币类型

# === 可选字段 ===
status: enum              # 状态: pending | frozen | distributing | settled | refunded
                          #   pending      = 草稿/配置中
                          #   frozen       = 活动发布后资金冻结
                          #   distributing = 结算中
                          #   settled      = 已全额发放
                          #   refunded     = 活动取消，资金回退

# === 自动生成字段 ===
id: string
created_at: datetime
frozen_at: datetime
settled_at: datetime
---
```

---

## 枚举值汇总

| 内容类型 | 字段 | 可选值 |
|---------|------|-------|
| event | type | `competition`, `operation` |
| event | status | `draft`, `pending_review`, `published`, `rejected`, `closed` |
| post | type | `profile`, `team`, `event`, `proposal`, `certificate`, `general` |
| post | status | `draft`, `pending_review`, `published`, `rejected` |
| post | visibility | `public`, `private` |
| user | role | `participant`, `organizer`, `admin` |
| group | visibility | `public`, `private` |
| interaction | type | `like`, `comment`, `rating` |
| notification | type | `system`, `activity`, `team`, `social` |
| asset_pool | status | `pending`, `frozen`, `distributing`, `settled`, `refunded` |
| rule.checks | phase | `pre`, `post` |
| rule.checks | on_fail | `deny`, `warn`, `flag` |
| rule.checks | condition.type | `time_window`, `count`, `exists`, `field_match`, `resource_format`, `resource_required`, `unique_per_scope`, `aggregate` |
| rule.checks | action | `flag_disqualified`, `compute_ranking`, `award_certificate`, `notify`, `transfer_asset` |

| 关系 | 字段 | 可选值 |
|-----|------|-------|
| event:post | relation_type | `submission`, `reference` |
| event:event | relation_type | `stage`, `track`, `prerequisite` |
| event:resource | display_type | `banner`, `attachment`, `inline` |
| post:post | relation_type | `reference`, `reply`, `embed` |
| post:resource | display_type | `attachment`, `inline` |
| group:user | role | `owner`, `admin`, `member` |
| group:user | status | `pending`, `accepted`, `rejected` |
| group:post | relation_type | `team_submission`, `announcement`, `reference` |
| group:resource | access_level | `read_only`, `read_write` |
| user:user | relation_type | `follow`, `block` |
| target:interaction | target_type | `post`, `event`, `resource` |

---

## 角色定义

| 角色 | 说明 | 核心权限范围 |
|------|------|-------------|
| **参赛者（Participant）** | 普通用户，参与活动 | 浏览、注册、报名、创建/编辑自己的 Post、组队 |
| **组织者（Organizer）** | 活动发起人，管理活动 | 创建/管理 Event 和 Rule、审核活动内容、管理活动相关 Post |
| **管理员（Admin）** | 平台运营，管理平台 | 平台级用户管理、全局内容管理、系统配置、活动审核、资产仲裁 |
