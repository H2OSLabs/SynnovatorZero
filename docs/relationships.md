# 关系 Schema

本文档定义 Synnovator 平台九种内容类型之间的关系及其属性。

关系用于连接内容类型，不同关系可以携带属性。

---

## category : rule

活动关联其规则。一个活动可以关联多条规则。

```yaml
category_id: string       # 活动 ID（必填）
rule_id: string           # 规则 ID（必填）

# === 关系属性 ===
priority: integer         # 规则优先级/排序（默认: 0，数值越小越靠前）
```

## category : post

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

## category : group

团队在特定活动中的报名绑定。一个用户在不同活动中可以代表不同团队，通过此关系进行隔离。

```yaml
category_id: string       # 活动 ID（必填）
group_id: string          # 团队 ID（必填）

# === 关系属性 ===
registered_at: datetime   # 报名时间（自动生成）
```

> **业务规则：** 同一 group 在同一 category 中只能注册一次。一个 user 可以通过不同 group 参加不同 category，但在同一 category 中只能属于一个 group。

## post : post

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

## post : resource

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

## group : user

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

## target : interaction

内容对象与交互记录（点赞、评论、评分）之间的**唯一关联路径**。interaction 实体本身不存储目标信息，所有 interaction 与目标内容的连接均通过此关系维护。target 可以是 post、category 或 resource。

```yaml
target_type: enum         # 目标类型: post | category | resource（必填）
target_id: string         # 目标对象 ID（必填）
interaction_id: string    # 交互记录 ID（必填）
```

> **权限规则：** 只要目标对象（post/category/resource）对当前用户可见，其关联的所有 interaction 即公开可读。
>
> **副作用：** 创建此关系时，系统自动执行以下操作：
> - **目标验证**：校验 `target_id` 对应的记录存在且未被软删除
> - **去重校验**：若关联的 interaction 为 like 类型，检查同一用户是否已对同一目标点赞
> - **缓存更新**：若 target_type 为 post，自动重算目标 post 的 `like_count`、`comment_count`、`average_rating`

## user : user

用户间关注/拉黑关系。关注为单向关系，双方互相 follow 时构成好友。

```yaml
source_user_id: string    # 发起关注的用户 ID（必填）
target_user_id: string    # 被关注的用户 ID（必填）

# === 关系属性 ===
relation_type: enum       # 关系类型: follow | block
                          #   follow = 关注
                          #   block  = 拉黑（优先级高于 follow）
created_at: datetime      # 创建时间（自动生成）
```

> **好友判定规则：** 若 A→B 和 B→A 的 `follow` 关系同时存在，则 A 和 B 互为好友。
>
> **拉黑规则：**
> - A block B 后，B 无法创建指向 A 的 follow 关系（系统拒绝）
> - block 关系存在时，即使双向 follow 存在，也不构成好友
>
> **自引用限制：** `source_user_id` 不能等于 `target_user_id`（不能关注/拉黑自己）

## category : category

活动间关联关系，支持赛段（有序执行）、赛道（并行执行）和前置条件（依赖关系）。

```yaml
source_category_id: string    # 发起关联的活动 ID（必填）
target_category_id: string    # 被关联的活动 ID（必填）

# === 关系属性 ===
relation_type: enum           # 关联类型: stage | track | prerequisite
                              #   stage        = 赛段（有序，先后执行）
                              #   track        = 赛道（并行，同级别）
                              #   prerequisite = 前置条件（必须完成 source 才能参加 target）
stage_order: integer          # 赛段序号（仅 stage 类型使用，数值越小越先）
```

> **赛段逻辑：** `relation_type=stage` 的多条关系通过 `stage_order` 排序形成序列链（Stage 1 → Stage 2 → Stage 3）。报名后续赛段时，系统校验前置赛段（source）已 closed。
>
> **赛道逻辑：** `relation_type=track` 的关系共享同一个 source（父活动），target 为各赛道子活动。赛道之间无互斥约束，团队可同时参加多个赛道。
>
> **前置条件逻辑：** `relation_type=prerequisite`，报名 target 活动时系统校验团队已在 source 活动中完成注册且 source 已 closed。
>
> **自引用限制：** `source_category_id` 不能等于 `target_category_id`。
>
> **循环依赖检测：** stage 和 prerequisite 类型禁止循环依赖（A→B→C→A）。
