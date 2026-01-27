# Synnovator Skill 闭环测试审计日志 (Round 3 -- GAP 补全)

> 测试时间: 2026-01-27
> 测试分支: test/biz-test
> 数据源: plans/biz-test/Skill test cases.md (含 test-gap.md 合并)
> 参考规范: docs/command.md
> 引擎路径: .claude/skills/synnovator/scripts/engine.py

---

## 测试概览

| Phase | 描述 | 用例数 | 通过 | 失败 | 通过率 |
|-------|------|--------|------|------|--------|
| 0 | Mock data 准备 (额外用户/团队) | 5 | 5 | 0 | 100% |
| 1 | Category GAP 测试 | 6 | 5 | 1 | 83% |
| 2 | Rule GAP 测试 | 5 | 3 | 2 | 60% |
| 3 | User DELETE 级联深度审计 | 14 | 10 | 2+2partial | 71% |
| 4 | Group + Category:Group + Relation 测试 | 11 | 9 | 2 | 82% |
| 5 | Soft Delete / Recovery / Permission Boundary | 11 | 6 | 5 | 55% |
| **合计** | | **52** | **38** | **12+2** | **73%** |

---

## Phase 0: Mock Data 准备

创建测试所需的额外用户和团队。

| ID | 用例 | 结果 |
|----|------|------|
| MOCK-001 | CREATE user charlie (participant) | PASS -- `user_482047dc8fc2` |
| MOCK-002 | CREATE user admin_01 (admin) | PASS -- `user_6679b6bc7408` |
| MOCK-003 | CREATE user judge_01 (organizer) | PASS -- `user_336da4417c17` |
| MOCK-004 | CREATE user judge_02 (organizer) | PASS -- `user_0c412c7af221` |
| MOCK-005 | CREATE group Team Alpha | PASS -- `grp_162b622bee66` |

---

## Phase 1: Category GAP 测试

### TC-CAT-002: CREATE category (operation type)
**PASS**

- 创建 `type=operation` 的 category 成功 (`cat_d4480dab398e`)
- `created_by` 正确设置为 organizer
- Markdown body 正确存储

### TC-CAT-010: UPDATE category status flow (draft -> published -> closed)
**PASS**

- 三步状态变更均成功，`updated_at` 逐步递增
- **发现**: 引擎不强制单向状态机（可能允许 `closed -> draft` 逆向变更）

### TC-CAT-020: DELETE category with cascade
**PASS**

- Category 软删除：`deleted_at` 正确设置
- `category:rule` 关系：硬删除（文件移除） -- 级联正确
- Interaction (like)：软删除，`deleted_at` 正确设置 -- 级联正确
- `target:interaction` 关系：**保留未删除** -- 符合 spec "关系保留但查询时按目标可见性过滤"

### TC-CAT-900: Invalid type enum ("workshop")
**PASS** -- 正确拒绝，错误信息明确

### TC-CAT-901: Invalid status enum ("archived")
**PASS** -- 正确拒绝，错误信息明确

### TC-CAT-902: Participant CREATE category (权限检查)
**FAIL**

- **预期**: 拒绝 (participant 无权创建 category)
- **实际**: 成功创建 `cat_bef1d5c554c1`
- **根因**: 引擎无 RBAC 层，`--user` 仅用于设置 `created_by`

---

## Phase 2: Rule GAP 测试

### TC-RULE-010: UPDATE rule config (max_team_size)
**PASS**

- `max_team_size` 从 5 更新为 6，`updated_at` 变更
- Read-back 确认值正确
- 恢复原值成功

### TC-RULE-011: UPDATE rule scoring_criteria
**PASS**

- 复杂嵌套 JSON 数组（4个评分维度）原子性替换成功
- 权重从 `[30,30,25,15]` 改为 `[25,25,25,25]` 后恢复

### TC-RULE-020: DELETE rule with cascade
**PASS**

- Rule 软删除：`deleted_at` 正确设置
- `category_rule` 关系：硬删除 -- 级联正确
- 正常 READ 被拒（返回 "rule is soft-deleted"）

### TC-RULE-900: Participant CREATE rule (权限检查)
**FAIL**

- **预期**: 拒绝
- **实际**: 成功创建 `rule_5ef1a9d5b32e`
- **根因**: 同 TC-CAT-902，无 RBAC

### TC-RULE-901: scoring_criteria weights sum != 100
**FAIL**

- **预期**: 拒绝或警告（权重和 110 > 100）
- **实际**: 成功创建，weights 50+60=110 被原样存储
- **根因**: 引擎无 `scoring_criteria` 结构验证（无权重和校验、无范围校验）

---

## Phase 3: User DELETE 级联深度审计 (核心审计)

### 前置步骤

| 步骤 | 操作 | 结果 |
|------|------|------|
| TC-USER-010 | UPDATE user info (display_name, bio) | **PASS** |
| TC-USER-900 | Duplicate username 检查 | **PASS** -- "Username 'alice' already exists" |
| TC-USER-901 | Duplicate email 检查 | **PASS** -- "Email 'alice@example.com' already exists" |
| TC-USER-902 | Non-owner UPDATE user (Bob 改 Alice 资料) | **FAIL** -- 成功修改，无权限检查 |
| 5a | Charlie 加入 group (pending) | **PASS** -- status=pending |
| 5b | Alice 批准 Charlie | **PASS** -- status=accepted, joined_at 设置 |
| 5d | Charlie 点赞 post | **PASS** -- iact_c123a51ed524 |
| 5f | Charlie 评论 post | **PASS** -- iact_17c2fa161687 |
| 5h | 删除前 post 计数 | **PASS** -- like_count=1, comment_count=1 |

### 核心删除操作

| 步骤 | 检查项 | 预期 | 实际 | 结果 |
|------|--------|------|------|------|
| 6a | Admin 删除 charlie | 软删除 | `mode: "soft"`, deleted_at 设置 | **PASS** |
| 6b | 读取已删除 charlie | deleted_at 非空 | `deleted_at: "2026-01-27T08:51:25.329319+00:00"` | **PASS** |
| 6c | Charlie 的 interaction 级联删除 | 全部 deleted_at 设置 | **两个 interaction 均有 deleted_at** | **PASS** |
| 6d | group:user 关系保留 | 保留并标记为"离组" | **保留但 status 仍为 "accepted"** | **PARTIAL** |
| 6e | Post 缓存计数更新 | like_count=0, comment_count=0 | **like_count=1, comment_count=1（陈旧）** | **FAIL** |

### 深度审计结论

1. **Interaction 级联软删除: 正确实现**
   - `_cascade_soft_delete_user_interactions()` (engine.py L592-599) 正确遍历 `created_by == user_id` 的所有 interaction 并设置 `deleted_at`
   - 默认查询（不含 `--include-deleted`）正确过滤已删除的 interaction

2. **group:user 关系保留: 部分实现** ⚠️
   - 关系记录被保留（未硬删除）-- 符合 spec
   - **但 status 未标记为"离组"** -- spec 说 "group:user 关系保留（标记为离组）"，但引擎未更新 status
   - 额外问题: `group_user.status` 枚举只有 `pending | accepted | rejected`，缺少 `"left"` 值

3. **缓存计数未更新: BUG** 🐛
   - User 删除级联软删除了 interaction，但**未触发 `_update_cache_stats()`**
   - 对比: 直接删除 interaction 时（L388-392）会调用 `_update_cache_stats(removed=True)`
   - User 级联路径（L384-385）只调用 `_cascade_soft_delete_user_interactions()`，缺少计数更新步骤

---

## Phase 4: Group + Category:Group + Relation 测试

### Group 模块

| ID | 用例 | 结果 |
|----|------|------|
| TC-GRP-010 | UPDATE group info (owner) | **PASS** -- description/max_members 更新成功 |
| TC-GRP-900 | Invalid visibility enum ("restricted") | **PASS** -- 正确拒绝 |
| TC-GRP-901 | Non-owner UPDATE group (Bob 改 Alice 的 group) | **FAIL** -- 成功修改，无所有权检查 |

### Category:Group 关系

| ID | 用例 | 结果 |
|----|------|------|
| TC-CATGRP-001 | CREATE category:group (团队报名) | **PASS** |
| TC-CATGRP-002 | READ category:group | **PASS** |
| TC-CATGRP-900 | 重复团队报名 | **PASS** -- "This group is already registered for this category" |
| TC-CATGRP-901 | 同用户多队同赛 (Alice 在两个队报名同一 category) | **FAIL** -- 成功报名，无跨组唯一性检查 |
| TC-CATGRP-010 | DELETE category:group (取消报名) | **PASS** -- 硬删除确认 |

### Relation UPDATE/DELETE

| ID | 用例 | 结果 |
|----|------|------|
| TC-REL-001 | UPDATE category:rule priority | **PASS** |
| TC-REL-003 | category:rule uniqueness (重复) | **PASS** -- "This rule is already linked to this category" |
| TC-REL-041 | group:user uniqueness (重复加入) | **PASS** -- "This user is already in this group" |

---

## Phase 5: Soft Delete / Recovery / Permission Boundary

### Soft Delete 测试

| ID | 用例 | 结果 |
|----|------|------|
| TC-DEL-001 | Soft delete category + 验证 deleted_at | **PASS** |
| TC-DEL-005 | Soft delete interaction | **PASS** |
| TC-DEL-010 | Category 删除级联到 interaction | **PASS** -- 两个 interaction 均被级联软删除 |

### Recovery 测试

| ID | 用例 | 结果 |
|----|------|------|
| TC-DEL-020 | Admin 恢复软删除的 post (set deleted_at=null) | **FAIL** -- "post is soft-deleted" 拒绝更新 |
| TC-DEL-022 | Non-admin 恢复尝试 | **PASS*** -- 被拒绝，但原因是"所有更新被阻塞"而非"权限不足" |

**关键发现**: 引擎没有 `restore` 命令。`update_content()` (L322-323) 对所有已软删除记录阻止更新，无法通过 update 设置 `deleted_at=null`。

### Permission Boundary 测试

| ID | 用例 | 结果 |
|----|------|------|
| TC-PERM-001 | Participant CREATE category | **FAIL** -- 成功创建，无权限检查 |
| TC-PERM-002 | Participant CREATE rule | **FAIL** -- 成功创建，无权限检查 |
| TC-PERM-020 | Anonymous READ draft post | **FAIL** -- 返回完整数据，无可见性过滤 |

### Interaction 补充测试

| ID | 用例 | 结果 |
|----|------|------|
| TC-IACT-050 | UPDATE comment text | **PASS** -- value 从"原始评论"更新为"修改后的评论" |
| TC-IACT-052 | Non-owner UPDATE interaction (Bob 改 Alice 的评论) | **FAIL** -- 成功修改，无所有权检查 |
| TC-IACT-060 | Like on category (非 post 目标) | **PASS** |

---

## BUG 汇总

### BUG-1: 无角色权限控制 (RBAC) [Critical]

**影响测试**: TC-CAT-902, TC-RULE-900, TC-PERM-001, TC-PERM-002, TC-GRP-901, TC-USER-902, TC-IACT-052

引擎的 `--user` 参数仅用于设置 `created_by`，从不读取用户的 `role` 字段进行授权。`command.md` 中定义的权限矩阵（如 CREATE category = Organizer/Admin）完全未实现。

**建议**: 添加权限中间件，在 CRUD 操作前加载用户记录、检查 role、对所有权限门控操作比对 `created_by`。

### BUG-2: User 级联删除未更新缓存计数 [High]

**影响测试**: Phase 3 Step 6e

`_cascade_soft_delete_user_interactions()` (L592-599) 软删除了用户的 interaction 但**未调用 `_update_cache_stats()`**。导致目标 post 的 `like_count`/`comment_count` 成为陈旧数据。

**建议**: 在 `_cascade_soft_delete_user_interactions()` 中，对每个被软删除 interaction 的目标 post 调用 `_update_cache_stats(target_id, removed=True)`。

### BUG-3: group:user 未标记"离组" [Medium]

**影响测试**: Phase 3 Step 6d

User 删除时 group:user 关系被保留，但 status 仍为 `"accepted"` 而非标记为离组。

**建议**:
1. 在 `group_user.status` 枚举中添加 `"left"` 值
2. User 删除级联中将相关 group_user 的 status 更新为 `"left"`

### BUG-4: 无跨组用户唯一性约束 [Medium]

**影响测试**: TC-CATGRP-901

同一用户可以通过不同 group 多次报名同一 category，违反 "同一用户在同一 category 中只能属于一个 group" 的业务规则。

**建议**: 在 `create_relation("category_group")` 中检查新注册 group 的成员是否已通过其他 group 注册了同一 category。

### BUG-5: 无 Restore 命令 [High]

**影响测试**: TC-DEL-020

`command.md` 定义了恢复操作（设置 `deleted_at = NULL`，仅 Admin 可执行），但引擎的 `update_content()` 阻止对已软删除记录的任何更新，且不存在 `restore` 命令。

**建议**: 添加 `restore` 子命令，仅 Admin 可调用，将 `deleted_at` 设为 null，可选级联恢复子对象。

### BUG-6: 无可见性过滤 [Medium]

**影响测试**: TC-PERM-020

Draft 状态的 post/category 对所有用户可见，引擎不根据 status 和用户上下文过滤查询结果。

**建议**: 在 `read_content()` 中根据 `--user` 上下文和记录的 `status`/`created_by` 实现可见性过滤。

### BUG-7: scoring_criteria 无结构验证 [Low]

**影响测试**: TC-RULE-901

`scoring_criteria` 数组的 weights 和不校验（可以超过 100 或不足 100），无个体权重范围检查。

**建议**: 添加 `scoring_criteria` 验证逻辑：weights 总和必须等于 100，每个 weight 在 0-100 范围内。

---

## command.md 模糊性标记

### AMB-1: 状态机方向性

**位置**: command.md 中 category.status 描述
**描述**: "状态变更（draft -> published -> closed）" 暗示单向流，但未明确禁止逆向变更。引擎当前接受任意方向的状态变更。
**建议**: 明确是否允许逆向变更（如 `closed -> draft`），或在 spec 中声明为严格单向。

### AMB-2: target:interaction 关系在级联删除中的处理

**位置**: command.md DELETE cascade table
**描述**: Category 删除时 cascade table 提到"解除所有 category:rule、category:post、category:group 关系，删除关联 interaction"，但未提及 `target:interaction` 关系。实际引擎保留了 `target:interaction` 关系（指向已软删除的 interaction）。这与 "关系保留但查询时按目标可见性过滤" 一致，但不够显式。
**建议**: 在 cascade table 中明确 `target:interaction` 的处理策略。

### AMB-3: "标记为离组" 的机制未定义

**位置**: command.md L451
**描述**: "group:user 关系保留（标记为离组）" -- 未指定：
  - 使用什么字段标记（status? 新字段 left_at?）
  - 如果使用 status，当前枚举 `pending | accepted | rejected` 不包含 `"left"` 值
**建议**: 在 group_user.status 枚举中添加 `"left"`，并明确 User 删除时将 group_user.status 设为 `"left"`。

### AMB-4: User 级联删除是否应更新缓存计数

**位置**: command.md 缓存统计字段规范 (L590-592)
**描述**: 触发条件为 "interaction CREATE/DELETE" -- 模糊的是：User 删除导致的级联软删除 interaction 是否算作 "interaction DELETE" 的触发条件。
**建议**: 明确所有导致 interaction 状态变更的路径（直接删除、级联删除、User 级联）都应触发缓存计数更新。

### AMB-5: Restore 操作的实现方式

**位置**: command.md L456
**描述**: Spec 说 "恢复操作: 设置 `deleted_at = NULL`"，暗示通过 UPDATE 实现。但引擎的 UPDATE 路径阻止对已软删除记录的操作。Spec 未定义独立的 `restore` 命令。
**建议**: 定义 `restore` 为独立命令（或 UPDATE 的特殊 flag），明确其行为和权限要求。

### AMB-6: 权限执行层的责任归属

**位置**: command.md 权限矩阵
**描述**: Spec 定义了每个操作的角色权限（如 CREATE category = Organizer/Admin），但未指定这是引擎层的责任还是上层应用层的责任。当前引擎未实现任何权限检查。
**建议**: 明确权限检查是否为引擎的核心职责，还是留给调用层实现。

### AMB-7: Rule 缺乏动态逻辑控制能力（Logic-less Rules） [High]

**位置**: rule Schema
**描述**: 当前 rule Schema 仅包含静态配置（如时间、格式、权重）和 Markdown 文字说明。在真实的 AI 竞赛场景中，Rule 需要包含"条件判断"与"动作触发"逻辑。
  - **示例场景**：在报名规则中，如果"申请人已拥有团队"，则"禁止发起新团队申请"；否则"允许创建团队"。
  - **示例逻辑**：如果"投稿作品未关联 Resource"，则"Post 状态强制设为 draft"；否则"允许发布"。
**建议**:
  1. 在 rule 中引入一个 `logic` 字段，用于定义简单的 IF-THEN 规则。
  2. 明确 Skill 在执行 CRUD 操作时，应如何调用该 Logic 字段进行预检查（Pre-check）。

---

## 测试数据 ID 映射

| 逻辑名称 | ID |
|----------|----|
| user_alice (participant) | `user_d300d6fbf99a` |
| user_bob (participant) | `user_ac55164d933e` |
| user_org_01 (organizer) | `user_1778adfafa89` |
| user_charlie (participant, 已删除) | `user_482047dc8fc2` |
| user_admin_01 (admin) | `user_6679b6bc7408` |
| user_judge_01 (organizer) | `user_336da4417c17` |
| user_judge_02 (organizer) | `user_0c412c7af221` |
| cat_ai_hackathon_2025 | `cat_130ff6b240ec` |
| grp_team_synnovator | `grp_2c442a1049ac` |
| grp_team_alpha | `grp_162b622bee66` |
| rule_submission_01 | `rule_8da90dbedc0b` |
