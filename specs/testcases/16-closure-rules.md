# 活动结束规则（Closure Rule Enforcement）

> **格式约定：** 每条用例仅描述「场景」与「预期结果」，不包含测试方法和执行过程。

> 活动结束规则通过 Rule 的 `checks` 字段声明，在 `update_content(event.status)` 操作点触发。pre 阶段用于关闭前校验，post 阶段用于关闭后的终审、排名和颁奖。

---

## 16.1 活动关闭前校验（pre phase）

**TC-CLOSE-001：活动关闭前校验所有团队人数**
活动关联了一条 Rule，其 `checks` 包含：`{ trigger: update_content(event.status), phase: pre, condition: { type: field_match, params: { entity: event, target: $current, field: status, op: "==", value: closed } }, on_fail: warn, message: "部分团队人数不足" }`。将活动 status 从 published 更新为 closed。由于 `on_fail: warn`，操作允许执行但返回警告信息。

**TC-CLOSE-002：活动关闭前严格校验（deny 模式）**
活动关联了一条 Rule，其 `checks` 包含 pre phase + `on_fail: deny` 的条件：所有报名团队必须有至少一个 submission。某团队已报名但未提交任何帖子。将活动 status 更新为 closed 被拒绝，返回 "not all teams have submissions" 错误。

## 16.2 活动关闭后终审（post phase — flag_disqualified）

**TC-CLOSE-010：活动关闭后标记不合格团队（团队人数不足）**
活动关联了一条 Rule，其 `checks` 包含：`{ trigger: update_content(event.status), phase: post, condition: { type: field_match, params: { entity: event, target: $current, field: status, op: "==", value: closed } }, action: flag_disqualified, action_params: { target: group, tag: "team_too_small" } }`。活动下有 3 个报名团队，其中 Team C 只有 1 名成员（Rule 要求 min_team_size=2）。活动关闭后，Team C 被添加 "team_too_small" 标记，Team A 和 Team B 不受影响。

**TC-CLOSE-011：活动关闭后标记不合格提案（缺少必要 resource）**
类似 TC-CLOSE-010，但 `action_params: { target: post, tag: "missing_attachment" }`。活动关闭后，未关联 resource 的 submission 帖子被标记为 "missing_attachment"。

**TC-CLOSE-012：所有团队均合格时无标记**
同 TC-CLOSE-010 的 Rule 配置，但所有团队人数均满足 min_team_size。活动关闭后，无任何团队被标记。

## 16.3 排名计算（post phase — compute_ranking）

**TC-CLOSE-020：活动关闭后按 average_rating 计算排名**
活动关联了一条 Rule，其 `checks` 包含：`{ trigger: update_content(event.status), phase: post, condition: { type: field_match, params: { entity: event, target: $current, field: status, op: "==", value: closed } }, action: compute_ranking, action_params: { source_field: average_rating, order: desc, output_tag_prefix: "rank_" } }`。活动下有 3 个 submission 帖子，average_rating 分别为 85.5、90.2、78.0。活动关闭后，帖子被分别添加 tag "rank_2"、"rank_1"、"rank_3"。

**TC-CLOSE-021：average_rating 相同时排名并列**
活动下有 2 个 submission 帖子，average_rating 均为 85.0。活动关闭后，两个帖子均被添加 tag "rank_1"，下一个排名为 "rank_3"（跳过 rank_2）。

**TC-CLOSE-022：无评分的帖子不参与排名**
活动下有 3 个 submission 帖子，其中 1 个 average_rating 为 null。活动关闭后，只有 2 个帖子被添加排名 tag，average_rating 为 null 的帖子不参与排名。

## 16.4 奖励发放（post phase — award_certificate）

**TC-CLOSE-030：活动关闭后自动颁发证书**
活动关联了一条 Rule，其 `checks` 包含 `compute_ranking` 和 `award_certificate` 两个 post-phase action。`award_certificate` 的 `action_params` 定义了 3 个奖项：rank_range [1,1] 一等奖、rank_range [2,3] 二等奖、rank_range [4,10] 优秀奖。活动下排名前 3 的帖子对应 3 个参赛团队。活动关闭后：
- 为排名第 1 的团队自动创建 resource（证书 PDF）、post（type=certificate, status=published）和 post_resource 关系
- 为排名第 2、3 的团队各自创建二等奖证书
- 排名第 4 及之后且在 rank_range 内的团队获得优秀奖证书
- 不在任何 rank_range 内的团队不颁发证书

**TC-CLOSE-031：无排名结果时不颁发证书**
活动下没有 submission 帖子（或所有 submission 的 average_rating 为 null）。活动关闭后，`compute_ranking` 无排名结果，`award_certificate` 不执行任何颁发操作。

**TC-CLOSE-032：证书帖子可被获奖者读取**
TC-CLOSE-030 颁发的证书帖子（type=certificate, status=published, visibility=public）可被获奖者和任何用户正常读取。关联的证书 resource 可通过 post_resource 正常下载。

## 16.5 完整活动结束流程（集成）

**TC-CLOSE-040：完整活动结束流程 — 终审 + 排名 + 颁奖**
活动关联了一条 Rule，包含 3 个 post-phase checks（按顺序）：
1. `flag_disqualified`（标记人数不足的团队）
2. `compute_ranking`（对合格 submission 按 average_rating 排名）
3. `award_certificate`（按排名颁发证书）

活动下有 4 个报名团队：
- Team A: 3 人, submission average_rating=90.2
- Team B: 2 人, submission average_rating=85.5
- Team C: 1 人（不满足 min_team_size=2），submission average_rating=95.0
- Team D: 2 人, 未提交 submission

活动关闭后：
1. Team C 被标记 "team_too_small"，Team D 的 submission 不存在不参与排名
2. 排名结果：rank_1=Team A（90.2），rank_2=Team B（85.5）。Team C 虽然分数最高但已被标记不合格，不参与排名
3. Team A 获得一等奖证书，Team B 获得二等奖证书

## 16.6 负向/边界

**TC-CLOSE-900：非 closed 状态变更不触发关闭 checks**
活动关联了 `update_content(event.status)` trigger 的 checks。将活动从 draft 更新为 published。post-phase 的 `compute_ranking` 和 `award_certificate` 不触发（condition 中 `field_match` 要求 status=="closed" 不满足）。

**TC-CLOSE-901：活动无关联 Rule 时关闭不触发任何 check**
活动未关联任何 Rule。将活动 status 更新为 closed。操作正常成功，无任何 check 执行。

**TC-CLOSE-902：post phase action 失败不回滚活动关闭**
活动关联了 `award_certificate` 的 post-phase check，但 `action_params` 中的 template 格式无效。活动关闭操作成功（status 变为 closed），但颁奖 action 执行失败并记录错误日志。活动状态不回滚。
