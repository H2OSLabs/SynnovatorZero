# 声明式规则引擎（Declarative Rule Engine）

> **格式约定：** 每条用例仅描述「场景」与「预期结果」，不包含测试方法和执行过程。

> 测试规则引擎的声明式 checks 机制本身的行为，包括条件类型、固定字段展开、多 Rule 合并、post-hook 执行等。

---

## 17.1 条件类型覆盖

**TC-ENGINE-001：time_window 条件 — 开始时间未到**
Rule 的 `checks` 包含 `{ condition: { type: time_window, params: { start: "2030-01-01T00:00:00Z", end: null } } }`。操作被拒绝，返回 "not yet open"。

**TC-ENGINE-002：time_window 条件 — 截止时间已过**
Rule 的 `checks` 包含 `{ condition: { type: time_window, params: { start: null, end: "2020-01-01T00:00:00Z" } } }`。操作被拒绝，返回 "deadline passed"。

**TC-ENGINE-003：count 条件 — 计数满足**
Rule 的 `checks` 包含 `{ condition: { type: count, params: { entity: group_user, scope: group, filter: { status: accepted }, op: ">=", value: 2 } } }`。团队有 3 名 accepted 成员。操作允许。

**TC-ENGINE-004：count 条件 — 计数不满足**
同 TC-ENGINE-003，但团队只有 1 名 accepted 成员。操作被拒绝。

**TC-ENGINE-005：exists 条件 — 实体存在时通过**
Rule 的 `checks` 包含 `{ condition: { type: exists, params: { entity: post_resource, scope: post, require: true } } }`。帖子关联了至少一个 resource。条件通过。

**TC-ENGINE-006：exists 条件 — 实体不存在时拒绝**
同 TC-ENGINE-005，但帖子未关联任何 resource。条件不满足，操作被拒绝。

**TC-ENGINE-007：exists 条件 — require=false 时实体不存在通过**
Rule 的 `checks` 包含 `{ condition: { type: exists, params: { entity: event_post, scope: user, filter: { relation_type: submission }, require: false } } }`（要求用户尚无提交）。用户无现有 submission。条件通过。

**TC-ENGINE-008：field_match 条件 — 字段匹配**
Rule 的 `checks` 包含 `{ condition: { type: field_match, params: { entity: event, target: $target, field: status, op: "==", value: "published" } } }`。目标活动 status 为 published。条件通过。

**TC-ENGINE-009：resource_format 条件 — 格式匹配**
Rule 的 `checks` 包含 `{ condition: { type: resource_format, params: { formats: ["pdf", "zip"] } } }`。帖子关联了 `proposal.pdf` 和 `code.zip`。条件通过。

**TC-ENGINE-010：resource_required 条件 — 数量和格式均满足**
Rule 的 `checks` 包含 `{ condition: { type: resource_required, params: { min_count: 2, formats: ["pdf"] } } }`。帖子关联了 2 个 PDF resource。条件通过。

**TC-ENGINE-011：aggregate 条件 — 聚合计算满足**
Rule 的 `checks` 包含 `{ condition: { type: aggregate, params: { entity: group_user, scope: each_group_in_category, filter: { status: accepted }, field: user_id, agg_func: count, op: ">=", value: 2 } } }`。活动下所有报名团队均有 2+ 名 accepted 成员。条件通过。

## 17.2 固定字段展开

**TC-ENGINE-020：固定字段自动展开为 checks**
创建 Rule 时设置 `max_submissions=2`，不定义 `checks`。创建 `event_post` 时，引擎自动将 `max_submissions` 展开为 `{ trigger: create_relation(event_post), phase: pre, condition: { type: count, ... } }` 并执行校验。用户已提交 2 次，第 3 次被拒绝。

**TC-ENGINE-021：固定字段展开的 check 排在自定义 checks 之前**
Rule 同时设置 `max_submissions=1`（固定字段）和 `checks` 中的 `resource_required`（min_count: 1）。用户已有一次提交但新帖子包含 resource。操作被拒绝时，错误信息来自 `max_submissions`（先执行），而非 `resource_required`。

**TC-ENGINE-022：纯 checks 定义（无固定字段）**
Rule 不设置任何固定字段，仅定义 `checks` 数组。引擎正确执行 checks 中的条件校验。

## 17.3 多 Rule 合并

**TC-ENGINE-030：多 Rule 的 checks 合并后 AND 逻辑执行**
活动关联了两条 Rule：Rule A 的 checks 要求 `resource_required`（min_count: 1），Rule B 的 checks 要求 `count`（max submissions < 2）。用户帖子有 resource 但已提交 2 次。操作被拒绝（Rule B 的 check 失败）。

**TC-ENGINE-031：多 Rule 中一条有 checks 一条只有固定字段**
活动关联了 Rule A（仅固定字段 `submission_format=["pdf"]`）和 Rule B（仅 `checks` 中的 `resource_required`）。两条 Rule 的约束合并：帖子必须有 resource 且格式为 PDF。

## 17.4 post-hook 执行

**TC-ENGINE-040：post phase check 在操作成功后执行**
Rule 的 `checks` 包含一条 `phase: post` 的 check（action: `compute_ranking`）。执行触发操作后，操作成功完成，然后 post-hook 执行排名计算。

**TC-ENGINE-041：post phase check 条件不满足时 action 不执行**
Rule 的 `checks` 包含：`{ trigger: update_content(event.status), phase: post, condition: { type: field_match, params: { field: status, op: "==", value: closed } }, action: compute_ranking }`。将活动从 draft 更新为 published（非 closed）。post-hook 的 condition 不满足，`compute_ranking` action 不执行。

**TC-ENGINE-042：post phase check 失败不回滚主操作**
Rule 的 `checks` 包含 post-phase action。主操作（如活动关闭）成功后，post-hook action 执行时遇到错误（如无排名数据）。主操作结果不受影响（活动仍为 closed 状态）。

## 17.5 on_fail 行为

**TC-ENGINE-050：on_fail=deny 时操作被拒绝**
Rule 的 check 设置 `on_fail: deny`。条件不满足时，操作被拒绝，返回 Rule message 的错误信息。

**TC-ENGINE-051：on_fail=warn 时操作允许但返回警告**
Rule 的 check 设置 `on_fail: warn`。条件不满足时，操作允许执行，但返回结果中包含警告信息。

**TC-ENGINE-052：on_fail=flag 时操作允许并标记**
Rule 的 check 设置 `on_fail: flag`。条件不满足时，操作允许执行，同时对操作目标添加标记（如 tag）。

## 17.6 空 checks 和无 Rule 场景

**TC-ENGINE-060：Rule 无固定字段且 checks 为空数组**
Rule 的 `checks` 为 `[]`，无任何固定约束字段。活动关联该 Rule 后，创建 event_post、group_user 等操作均无约束，正常通过。

**TC-ENGINE-061：活动未关联任何 Rule**
活动不关联 Rule。所有操作无约束校验，正常执行。（与 TC-RULE-108 一致。）
