# 规则引擎（Rule Engine）

本文档定义 Synnovator 平台的声明式规则引擎规范，包括条件类型、动作类型、Hook 操作点，以及 Rule 中 `checks` 字段的声明语法。

> **设计目标：** 运营人员可通过组合条件类型 + 操作点 + 动作类型，声明式地定义新业务规则，无需修改引擎代码。

---

## 概述

### 当前架构

Rule 通过 `event_rule` 关联到活动后，引擎在固定操作点执行 pre-operation 校验。所有关联 rule 必须全部满足（AND 逻辑），任一违规即拒绝操作。

### 扩展架构

在保留现有固定字段（`max_submissions`、`min_team_size` 等）的基础上，新增 `checks` 字段，支持声明式条件-动作组合。固定字段作为语法糖保留，引擎内部自动展开为等价的 `checks` 条目。

```
Rule
├── 固定字段（向后兼容，自动展开为 checks）
│   ├── submission_deadline  → time_window check
│   ├── max_submissions      → count check
│   ├── submission_format    → resource_format check
│   ├── min_team_size        → count check
│   └── max_team_size        → count check
└── checks（声明式条件-动作列表）
    ├── check_1: { trigger, phase, condition, on_fail, message }
    ├── check_2: ...
    └── ...
```

---

## Hook 操作点

### 操作点矩阵

| 操作点 | Phase | 现有/新增 | 说明 |
|--------|-------|----------|------|
| `create_relation(event_post)` | pre | 现有 | 帖子提交到活动前校验 |
| `create_relation(event_post)` | post | **新增** | 帖子提交成功后触发动作 |
| `create_relation(group_user)` | pre | 现有 | 成员加入团队前校验 |
| `create_relation(group_user)` | post | **新增** | 成员加入团队后触发动作 |
| `create_relation(event_group)` | pre | 现有 | 团队报名活动前校验（含 prerequisite） |
| `create_relation(event_group)` | post | **新增** | 团队报名成功后触发动作 |
| `update_content(post.status)` | pre | 现有 | 帖子状态变更前校验 |
| `update_content(post.status)` | post | **新增** | 帖子状态变更后触发动作 |
| `update_content(event.status)` | pre | **新增** | 活动状态变更前校验 |
| `update_content(event.status)` | post | **新增** | 活动状态变更后触发动作（活动关闭时的终审/颁奖） |

### Phase 定义

- **pre**：操作执行前校验。条件不满足时阻止操作（`on_fail: deny`）或发出警告（`on_fail: warn`）。
- **post**：操作执行成功后触发。用于触发后续动作（如计算排名、发放奖励、标记不合格）。post 阶段的 check 不阻止已完成的操作。

### 校验链（Validation Chain）

```
create event_post:
  event → event_rule → rule.checks[trigger=create_relation(event_post), phase=pre]

create group_user:
  group → event_group → event → event_rule → rule.checks[trigger=create_relation(group_user), phase=pre]

create event_group:
  event → event_event(prerequisite) → prerequisite.status == closed?
  event → event_rule → rule.checks[trigger=create_relation(event_group), phase=pre]

update post.status:
  post → event_post → event → event_rule → rule.checks[trigger=update_content(post.status), phase=pre]

update event.status:
  event → event_rule → rule.checks[trigger=update_content(event.status), phase=pre|post]
```

---

## Check 声明语法

Rule 的 `checks` 字段为数组，每个元素定义一条声明式校验规则：

```yaml
checks:
  - trigger: string          # 操作点（见操作点矩阵）
    phase: enum              # pre | post
    condition:
      type: string           # 条件类型（见条件类型库）
      params: object         # 条件参数（因类型而异）
    on_fail: enum            # deny | warn | flag（默认: deny）
    action: string           # 动作类型（仅 post phase 使用，见动作类型库）
    action_params: object    # 动作参数（仅 action 存在时使用）
    message: string          # 失败/动作提示信息
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `trigger` | 是 | 触发的操作点，格式为 `create_relation(<type>)` 或 `update_content(<type>.<field>)` |
| `phase` | 是 | `pre`（操作前校验）或 `post`（操作后触发） |
| `condition` | pre 阶段必填 | 条件定义，包含 `type` 和 `params` |
| `on_fail` | 否 | pre 阶段的失败行为：`deny`（拒绝，默认）、`warn`（警告但允许）、`flag`（标记但允许） |
| `action` | post 阶段可选 | 后续触发的动作类型 |
| `action_params` | 否 | 动作的参数 |
| `message` | 是 | 人类可读的提示信息 |

---

## 条件类型库

### time_window — 时间窗口检查

校验当前时间是否在指定范围内。

```yaml
condition:
  type: time_window
  params:
    start: datetime | null    # 开始时间（null 表示不限）
    end: datetime | null      # 结束时间（null 表示不限）
```

**等价固定字段：** `submission_start` + `submission_deadline`

### count — 计数检查

校验指定关系/实体的数量是否满足条件。

```yaml
condition:
  type: count
  params:
    entity: string            # 关系类型或内容类型（如 event_post, group_user）
    scope: string             # 计数范围: user | team | group | event
    filter: object            # 过滤条件（如 { status: accepted, relation_type: submission }）
    op: string                # 比较运算符: < | <= | == | >= | >
    value: integer | "$rule.<field>"  # 目标值，支持引用 rule 自身字段
```

**等价固定字段：** `max_submissions`（count + event_post + user + <= + N）、`min_team_size` / `max_team_size`（count + group_user + group + >=/<= + N）

**示例：**

```yaml
# 每用户最多提交 1 次
condition:
  type: count
  params:
    entity: event_post
    scope: user
    filter: { relation_type: submission }
    op: "<"
    value: 1
```

### exists — 存在性检查

校验指定关系/实体是否存在。

```yaml
condition:
  type: exists
  params:
    entity: string            # 关系类型或内容类型
    scope: string             # 检查范围: user | team | group | post
    filter: object            # 过滤条件
    require: boolean          # true=必须存在 / false=必须不存在（默认: true）
```

**示例：**

```yaml
# 提交前必须已有团队报名
condition:
  type: exists
  params:
    entity: event_group
    scope: user_group         # 当前用户所在团队
    filter: { event_id: $target_category }
    require: true

# 帖子必须至少关联一个 resource
condition:
  type: exists
  params:
    entity: post_resource
    scope: post               # 当前操作的帖子
    require: true
```

### field_match — 字段匹配检查

校验指定实体的字段值是否满足条件。

```yaml
condition:
  type: field_match
  params:
    entity: string            # 内容类型（如 event, post, group）
    target: string            # 目标实体选择: $source | $target | $current
    field: string             # 字段名
    op: string                # 比较运算符: == | != | in | not_in | < | > | <= | >=
    value: any                # 目标值
```

**示例：**

```yaml
# 活动必须处于 published 状态
condition:
  type: field_match
  params:
    entity: event
    target: $target
    field: status
    op: "=="
    value: published
```

### resource_format — 资源格式检查

校验帖子关联的 resource 文件格式。

```yaml
condition:
  type: resource_format
  params:
    formats: list[string]     # 允许的格式列表（文件扩展名，不含点号）
    require_any: boolean      # true=至少一个 resource 格式匹配 / false=所有 resource 格式均需匹配（默认: false）
```

**等价固定字段：** `submission_format`

### resource_required — 必要资源检查

校验帖子是否关联了必要的 resource。

```yaml
condition:
  type: resource_required
  params:
    min_count: integer        # 最少 resource 数量（默认: 1）
    formats: list[string]     # 可选：要求的格式列表（至少一个 resource 匹配其中一种格式）
```

**示例：**

```yaml
# 提案必须包含至少一个 PDF 附件
condition:
  type: resource_required
  params:
    min_count: 1
    formats: ["pdf"]
```

### unique_per_scope — 范围内唯一性检查

校验某维度下的唯一性约束。

```yaml
condition:
  type: unique_per_scope
  params:
    entity: string            # 关系类型
    scope: string             # 唯一性范围: user_in_category | team_in_category
    key: string               # 唯一性键: user_id | group_id
```

**等价已有约束：** CG-901（同一 event 内一个 user 只能属于一个 group）

### aggregate — 聚合检查

对一组实体的字段值进行聚合计算并校验。

```yaml
condition:
  type: aggregate
  params:
    entity: string            # 关系类型或内容类型
    scope: string             # 聚合范围: event | group
    filter: object            # 过滤条件
    field: string             # 聚合字段
    agg_func: string          # 聚合函数: count | sum | avg | min | max
    op: string                # 比较运算符
    value: number             # 目标值
```

**示例：**

```yaml
# 活动结束时校验：每个报名团队至少有 min_team_size 人
condition:
  type: aggregate
  params:
    entity: group_user
    scope: each_group_in_category    # 遍历活动下每个报名团队
    filter: { status: accepted }
    field: user_id
    agg_func: count
    op: ">="
    value: "$rule.min_team_size"
```

---

## 动作类型库

动作类型仅在 `phase: post` 时使用，操作成功后触发。

### flag_disqualified — 标记不合格

遍历活动下的参赛实体，将不满足条件的标记为不合格。

```yaml
action: flag_disqualified
action_params:
  target: string              # 标记目标: post | group
  tag: string                 # 添加的标签（如 "disqualified"）
  reason_field: string        # 写入不合格原因的字段名（可选）
```

### compute_ranking — 计算排名

基于帖子的 `average_rating` 或其他字段计算排名。

```yaml
action: compute_ranking
action_params:
  source_field: string        # 排名依据字段（默认: average_rating）
  order: string               # 排序方向: desc | asc（默认: desc）
  scope: string               # 排名范围: event（默认）
  output_tag_prefix: string   # 排名结果写入 tag 的前缀（如 "rank_"，则第一名 tag 为 "rank_1"）
```

### award_certificate — 颁发奖励

根据排名区间自动创建证书 resource 和 certificate 帖子。

```yaml
action: award_certificate
action_params:
  rules:                      # 奖励规则列表
    - rank_range: [1, 1]      # 排名区间 [起始, 结束]（含两端）
      template: string        # 证书模板名称
      title: string           # 证书帖子标题
    - rank_range: [2, 3]
      template: string
      title: string
  certificate_type: string    # 证书资源类型（默认: "application/pdf"）
```

**执行流程：**
1. 依赖 `compute_ranking` 的排名结果
2. 按 `rank_range` 匹配获奖团队/用户
3. 为每个获奖者自动创建：
   - `resource`（证书文件，filename 含模板名称）
   - `post`（type=certificate, status=published）
   - `post_resource` 关系（display_type=attachment）

### notify — 发送通知（保留）

通知机制预留，当前版本不实现。

```yaml
action: notify
action_params:
  target: string              # user | group | event
  template: string            # 通知模板
```

---

## 固定字段展开规则

引擎加载 Rule 时，自动将固定字段展开为等价的 `checks` 条目。用户定义的 `checks` 与展开后的条目合并（用户定义的 `checks` 优先级更高，追加在展开条目之后）。

| 固定字段 | 展开为 |
|---------|--------|
| `submission_start` + `submission_deadline` | `{ trigger: create_relation(event_post), phase: pre, condition: { type: time_window, params: { start: $submission_start, end: $submission_deadline } }, on_fail: deny }` |
| `max_submissions` | `{ trigger: create_relation(event_post), phase: pre, condition: { type: count, params: { entity: event_post, scope: user, filter: { relation_type: submission }, op: "<", value: $max_submissions } }, on_fail: deny }` |
| `submission_format` | `{ trigger: create_relation(event_post), phase: pre, condition: { type: resource_format, params: { formats: $submission_format } }, on_fail: deny }` |
| `min_team_size` | `{ trigger: create_relation(event_post), phase: pre, condition: { type: count, params: { entity: group_user, scope: group, filter: { status: accepted }, op: ">=", value: $min_team_size } }, on_fail: deny }` |
| `max_team_size` | `{ trigger: create_relation(group_user), phase: pre, condition: { type: count, params: { entity: group_user, scope: group, filter: { status: accepted }, op: "<", value: $max_team_size } }, on_fail: deny }` |
| `allow_public` + `require_review` | `{ trigger: update_content(post.status), phase: pre, condition: { type: field_match, ... }, on_fail: deny }` |

---

## 完整示例

### 示例 1：标准比赛规则（固定字段 + 自定义 checks）

```yaml
---
name: AI Hackathon 2025 参赛规则
description: 比赛提交规则
allow_public: false
require_review: true
submission_start: '2025-03-01T00:00:00Z'
submission_deadline: '2025-06-01T23:59:59Z'
submission_format: ["pdf", "zip"]
max_submissions: 1
min_team_size: 2
max_team_size: 5
scoring_criteria:
  - name: 创新性
    weight: 30
    description: 方案的独创性和新颖程度
  - name: 技术实现
    weight: 30
    description: 技术方案的可行性和实现质量
  - name: 实用价值
    weight: 25
    description: 解决实际问题的能力
  - name: 演示效果
    weight: 15
    description: 演示和展示的效果

checks:
  # 提交时要求帖子至少关联一个 resource
  - trigger: create_relation(event_post)
    phase: pre
    condition:
      type: resource_required
      params:
        min_count: 1
    on_fail: deny
    message: "提案必须包含至少一个附件"

  # 报名时要求用户已加入团队
  - trigger: create_relation(event_group)
    phase: pre
    condition:
      type: exists
      params:
        entity: group_user
        scope: user
        filter: { status: accepted }
        require: true
    on_fail: deny
    message: "报名前必须先加入一个团队"

  # 活动关闭时校验团队人数
  - trigger: update_content(event.status)
    phase: post
    condition:
      type: field_match
      params:
        entity: event
        target: $current
        field: status
        op: "=="
        value: closed
    action: flag_disqualified
    action_params:
      target: group
      tag: "team_too_small"
    message: "团队人数不足，标记为不合格"

  # 活动关闭时计算排名
  - trigger: update_content(event.status)
    phase: post
    condition:
      type: field_match
      params:
        entity: event
        target: $current
        field: status
        op: "=="
        value: closed
    action: compute_ranking
    action_params:
      source_field: average_rating
      order: desc
      output_tag_prefix: "rank_"
    message: "计算最终排名"

  # 活动关闭时颁发证书
  - trigger: update_content(event.status)
    phase: post
    condition:
      type: field_match
      params:
        entity: event
        target: $current
        field: status
        op: "=="
        value: closed
    action: award_certificate
    action_params:
      rules:
        - rank_range: [1, 1]
          template: first_place
          title: "一等奖证书"
        - rank_range: [2, 3]
          template: runner_up
          title: "二等奖证书"
        - rank_range: [4, 10]
          template: excellence
          title: "优秀奖证书"
    message: "颁发获奖证书"
---

## 参赛规则详细说明

...Markdown 正文内容...
```

### 示例 2：运营活动规则（仅 checks，无固定字段）

```yaml
---
name: 悬赏任务参与规则
description: 完成指定任务即可获得奖励

checks:
  # 参与时必须有已发布的个人资料帖
  - trigger: create_relation(event_group)
    phase: pre
    condition:
      type: exists
      params:
        entity: post
        scope: user
        filter: { type: profile, status: published }
        require: true
    on_fail: deny
    message: "参与前请先完善个人资料（发布 profile 类型帖子）"

  # 提交时帖子必须包含附件
  - trigger: create_relation(event_post)
    phase: pre
    condition:
      type: resource_required
      params:
        min_count: 1
    on_fail: deny
    message: "提交成果必须包含附件"
---
```

---

## 设计约束

1. **AND 逻辑：** 同一操作点的所有 checks 必须全部通过，任一失败即按 `on_fail` 处理。
2. **多 Rule AND：** 一个活动可关联多条 Rule，所有 Rule 的 checks 合并后按 AND 逻辑执行。
3. **固定字段优先展开：** 固定字段展开的 checks 排在用户自定义 checks 之前。
4. **post phase 不阻止：** `phase: post` 的 check 即使条件不满足，也不回滚已完成的操作，仅记录日志或执行标记动作。
5. **空 checks 等同于无约束：** 如果 Rule 既无固定字段也无 checks，则不施加任何约束。
6. **变量引用：** `$rule.<field>` 引用 Rule 自身字段，`$target_category` 引用当前操作的目标活动 ID，`$current` 引用当前操作的实体。
