# 参加活动规则（Entry Rule Enforcement）

> **格式约定：** 每条用例仅描述「场景」与「预期结果」，不包含测试方法和执行过程。

> 参加活动规则通过 Rule 的 `checks` 字段声明，在 `create_relation(event_group)` 和 `create_relation(event_post)` 操作的 pre 阶段自动执行。用于校验报名/提交的前置条件。

---

## 15.1 必要 post 检查

**TC-ENTRY-001：报名前必须已加入团队**
活动关联了一条 Rule，其 `checks` 包含：`{ trigger: create_relation(event_group), phase: pre, condition: { type: exists, params: { entity: group_user, scope: user, filter: { status: accepted }, require: true } }, on_fail: deny }`。用户尚未加入任何团队，尝试通过其所在的空团队报名活动。系统拒绝操作，返回错误信息包含 Rule 的 message 提示。

**TC-ENTRY-002：提交前必须已有团队报名**
活动关联了一条 Rule，其 `checks` 包含：`{ trigger: create_relation(event_post), phase: pre, condition: { type: exists, params: { entity: event_group, scope: user_group, filter: { event_id: $target_category }, require: true } }, on_fail: deny }`。用户的团队尚未报名该活动，用户尝试提交帖子到该活动。系统拒绝操作，返回错误信息提示需先报名活动。

**TC-ENTRY-003：报名前必须已有 profile 帖子**
活动关联了一条 Rule，其 `checks` 包含：`{ trigger: create_relation(event_group), phase: pre, condition: { type: exists, params: { entity: post, scope: user, filter: { type: profile, status: published }, require: true } }, on_fail: deny }`。用户未发布 profile 帖子，尝试报名活动。系统拒绝操作，返回提示需先完善个人资料。

**TC-ENTRY-004：已满足前置条件时报名成功**
同 TC-ENTRY-003 的 Rule 配置，用户已发布一个 type=profile、status=published 的帖子。用户报名活动。系统允许操作。

## 15.2 提案内容筛选（必要 resource）

**TC-ENTRY-010：提交时帖子必须包含至少一个 resource**
活动关联了一条 Rule，其 `checks` 包含：`{ trigger: create_relation(event_post), phase: pre, condition: { type: resource_required, params: { min_count: 1 } }, on_fail: deny }`。用户帖子未关联任何 resource，尝试提交到活动。系统拒绝操作，返回提示"提案必须包含至少一个附件"。

**TC-ENTRY-011：提交时帖子必须包含指定格式的 resource**
活动关联了一条 Rule，其 `checks` 包含：`{ trigger: create_relation(event_post), phase: pre, condition: { type: resource_required, params: { min_count: 1, formats: ["pdf"] } }, on_fail: deny }`。用户帖子关联了一个 `.pptx` 格式的 resource（但没有 PDF）。系统拒绝操作。

**TC-ENTRY-012：帖子包含符合要求的 resource 时提交成功**
同 TC-ENTRY-011 的 Rule 配置，用户帖子关联了一个 `proposal.pdf` 的 resource。系统允许操作。

## 15.3 post 所有权筛选

**TC-ENTRY-020：一个用户在同一活动中只能有一个参赛提案**
活动关联了一条 Rule，其 `checks` 包含：`{ trigger: create_relation(event_post), phase: pre, condition: { type: count, params: { entity: event_post, scope: user, filter: { relation_type: submission }, op: "<", value: 1 } }, on_fail: deny }`。用户已提交过一次 submission，再次尝试提交新帖子。系统拒绝操作，返回提示"每个用户只能提交一个参赛提案"。

**TC-ENTRY-021：同一用户在同一活动中只能属于一个团队**
此约束已在 TC-REL-CG-901 中覆盖（application-layer 唯一性约束）。此处验证该约束在 checks 框架下仍然有效：活动关联了 `unique_per_scope` 类型的 check，配合已有的 application-layer 约束，双重保障唯一性。

**TC-ENTRY-022：不同活动中同一用户可分别提交提案**
活动 A 和活动 B 各自关联了 `max_submissions=1` 的 Rule。用户在活动 A 中已提交一次。用户在活动 B 中提交帖子。系统允许操作（约束按 event 隔离）。

## 15.4 混合约束（固定字段 + checks）

**TC-ENTRY-030：固定字段和自定义 checks 同时生效（AND 逻辑）**
活动关联了一条 Rule，同时设置了 `max_submissions=1`（固定字段）和 `checks` 中的 `resource_required`（min_count: 1）。用户帖子关联了 resource，但已有一次提交。系统拒绝操作，返回 `max_submissions` 的违规信息（固定字段展开的 check 在自定义 checks 之前执行）。

**TC-ENTRY-031：固定字段和自定义 checks 均满足时操作成功**
同 TC-ENTRY-030 的 Rule 配置，用户首次提交且帖子关联了 resource。系统允许操作。

## 15.5 负向/边界

**TC-ENTRY-900：checks 中引用不存在的 condition type 被拒绝**
创建 Rule 时 `checks` 中指定 condition type 为 "custom_check"（不在条件类型库中）。系统拒绝创建或忽略该 check 并发出警告。

**TC-ENTRY-901：checks 缺少必填字段（trigger/phase/message）被拒绝**
创建 Rule 时 `checks` 中某条目缺少 `trigger` 或 `phase` 字段。系统拒绝创建，返回 checks 格式校验错误。

**TC-ENTRY-902：pre 阶段 check 缺少 condition 被拒绝**
创建 Rule 时 `checks` 中某条 `phase: pre` 的条目缺少 `condition` 字段。系统拒绝创建，返回 pre 阶段 check 必须包含 condition 的错误。
