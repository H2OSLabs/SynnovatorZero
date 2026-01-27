# Synnovator Skill 综合测试报告

> **整合来源：**
> - `Test-Results.md` — Yuxin 两轮测试结果（21 test sections）
> - `test-optimization-log-rh.md` — RH 第三轮 GAP 补全审计（52 test cases）
> - `skill-update-plan-yuxin.md` — Yuxin 修改计划
>
> **日期：** 2026-01-27
> **分支：** `test/biz-test`
> **引擎：** `.claude/skills/synnovator/scripts/engine.py`

---

## 一、测试覆盖总览

| 来源 | 用例数 | 通过 | 失败 | 通过率 |
|------|--------|------|------|--------|
| Yuxin — SynNovator-Skills-Test-Yuxin.md | 8 sections | 8 | 0 | 100% |
| Yuxin — Fill-Gap-Yuxin.md | 15 sections | 14 | 1 | 93% |
| RH — test-optimization-log-rh.md | 52 cases | 38 | 14 | 73% |
| **合计** | **75** | **60** | **15** | **80%** |

### 覆盖维度

| 维度 | Yuxin | RH | 综合 |
|------|-------|----|------|
| 7 种内容类型 CRUD | 全部覆盖 | category, rule, user, group, interaction | 全覆盖 |
| 7 种关系类型 CRUD | 全部覆盖 | category_rule, category_group, group_user, target_interaction | 全覆盖 |
| 枚举验证 | 6 内容类型 + 1 关系类型 | category.type/status, group.visibility | 全覆盖 |
| 级联删除 | post, user, category, rule, group, interaction | category, rule, user（深度审计） | 全覆盖 |
| 唯一性约束 | email, category_rule, group_user | username, email, category_rule, group_user, category_group | 全覆盖 |
| 边界条件 | 8 种错误路径 | 权限边界、恢复操作、可见性 | 互补 |
| RBAC 权限 | 列为未实现功能 | 7 个用例验证缺失 | RH 更深入 |
| 恢复机制 | 列为未实现功能 | 2 个用例验证缺失 | RH 更深入 |
| 缓存计数一致性 | 验证创建时正确 | 发现级联删除后不更新 | RH 更深入 |

---

## 二、确认的 Bug（按优先级排序）

### P0 — 数据完整性

#### BUG-01: `create_relation` 缺少枚举字段验证
- **发现者:** Yuxin
- **位置:** `engine.py:399-429` — `create_relation()`
- **问题:** `update_relation()` (L469-473) 验证枚举字段，但 `create_relation()` 不验证。可通过 create 写入非法值（如 `group_user.role="superadmin"`）。
- **影响:** `group_user.role`, `group_user.status`, `category_post.relation_type`, `post_post.relation_type`, `post_resource.display_type`
- **修复:** 在 `create_relation()` 的 `save_record()` 前添加枚举校验（5 行代码）

#### BUG-02: User 级联删除未更新目标 Post 缓存计数
- **发现者:** RH
- **位置:** `engine.py:384-385` + `engine.py:592-599`
- **问题:** `_cascade_soft_delete_user_interactions()` 软删除了用户的 interaction，但未调用 `_update_cache_stats()`。直接删除 interaction 时（L388-392）会正确调用。
- **影响:** 删除用户后，目标 Post 的 `like_count` / `comment_count` 成为陈旧数据。
- **修复:** 在 `_cascade_soft_delete_user_interactions()` 中，对每个被软删除的 interaction 调用 `_update_cache_stats(removed=True)`

### P1 — 级联行为 + Spec 矛盾

#### BUG-03: `delete group` 未级联 `group_user` 关系
- **发现者:** Yuxin + RH
- **位置:** `engine.py:386-387`
- **Spec 矛盾:**
  - 级联策略表 (L452): "group:user 关系保留（成员可查询历史）"
  - CRUD 操作表 (L634): "DELETE group → 解除所有 group:user、category:group 关系"
- **当前行为:** 仅级联 `category_group`，`group_user` 不处理
- **需要:** Spec Owner 确认后选择方案

#### BUG-04: `delete user` 未级联 `group_user` 关系 + 未标记离组
- **发现者:** Yuxin + RH
- **位置:** `engine.py:384-385`
- **Spec 矛盾:**
  - 级联策略表 (L451): "group:user 关系保留（标记为离组）"
  - CRUD 操作表 (L633): "DELETE user → 解除所有 group:user 关系"
- **当前行为:** 仅级联 interactions，`group_user` 不处理，status 仍为 `accepted`
- **额外问题:** `group_user.status` 枚举不含 `"left"` 值
- **需要:** Spec Owner 确认后选择方案

### P2 — 缺失功能

#### BUG-05: 无 Restore 命令
- **发现者:** Yuxin + RH
- **Spec 位置:** L454-458 定义了恢复操作，但引擎无 `restore` 命令
- **问题:** `update_content()` (L322-323) 阻止对软删除记录的任何更新，无法通过 update 设置 `deleted_at=null`
- **修复:** 添加 `restore_content` 命令，仅 Admin 可调用，支持级联恢复

#### BUG-06: 无 RBAC 权限控制
- **发现者:** Yuxin + RH
- **RH 验证用例:** TC-CAT-902, TC-RULE-900, TC-PERM-001/002, TC-GRP-901, TC-USER-902, TC-IACT-052（共 7 个 FAIL）
- **问题:** `--user` 仅设置 `created_by`，不读取用户 role 做权限检查
- **影响:** participant 可创建 category/rule，非作者可修改/删除他人内容
- **修复:** 添加权限中间件（工作量较大）

#### BUG-07: 无可见性过滤
- **发现者:** RH
- **验证用例:** TC-PERM-020 — Anonymous 可读取 draft 状态 post
- **问题:** 查询不根据 status 和用户上下文过滤结果
- **修复:** `read_content()` 中添加可见性过滤逻辑

#### BUG-08: 无跨组用户唯一性约束
- **发现者:** RH
- **验证用例:** TC-CATGRP-901 — Alice 通过两个 group 报名同一 category 成功
- **问题:** 同一用户可通过不同 group 多次注册同一 category
- **修复:** `create_relation("category_group")` 中检查成员是否已通过其他 group 注册

### P3 — 验证增强

#### BUG-09: `scoring_criteria` 无结构验证
- **发现者:** RH
- **验证用例:** TC-RULE-901 — weights 和 = 110 被接受
- **问题:** 不校验 weights 总和是否为 100，无范围检查
- **修复:** 添加 weights 总和 = 100 校验

#### BUG-10: `target_interaction` 关系需手动创建
- **发现者:** Yuxin
- **问题:** 创建 interaction 后必须手动调用 `create target_interaction`，应自动创建
- **修复:** `create_content("interaction")` 完成后自动建立 `target_interaction` 关系

#### BUG-11: 引用完整性 — 可删除仍有内容的用户
- **发现者:** Yuxin
- **Spec 位置:** L466 "*.created_by → user.id → 限制删除（不可删除仍有内容的用户）"
- **问题:** 不检查用户是否有关联内容，直接允许删除
- **修复:** 删除前检查 `created_by` 引用

---

## 三、Spec 矛盾与模糊性

### 矛盾（需 Spec Owner 统一）

| # | 位置 | 级联策略表 | CRUD 操作表 | 引擎现状 |
|---|------|-----------|------------|---------|
| C-1 | delete group → group_user | 保留（成员可查询历史）(L452) | 解除所有 (L634) | 保留 |
| C-2 | delete user → group_user | 保留（标记为离组）(L451) | 解除所有 (L633) | 保留 |
| C-3 | delete category → 关系 | 关系保留按可见性过滤 (L449) | 解除所有 (L629) | 解除所有 |

**建议:** 统一为 CRUD 操作表的描述，因为该表更具体且 category 已遵循。

### 模糊性（需 Spec 补充）

| # | 主题 | 描述 | 建议 |
|---|------|------|------|
| AMB-1 | 状态机方向性 | category.status "draft→published→closed" 是否严格单向？引擎允许任意方向 | 明确是否允许逆向变更 |
| AMB-2 | target:interaction 级联处理 | category 删除时 target:interaction 未提及，引擎保留了它们 | cascade table 中明确策略 |
| AMB-3 | "标记为离组" 机制 | 未指定用哪个字段/值标记，status 枚举缺 `"left"` | 明确为 status="left" |
| AMB-4 | User 级联删除是否更新缓存 | 级联软删除 interaction 是否算 "interaction DELETE" 触发条件？ | 明确所有路径都应触发 |
| AMB-5 | Restore 实现方式 | Spec 暗示通过 UPDATE 实现，但 UPDATE 阻止软删除记录操作 | 定义为独立命令 |
| AMB-6 | 权限执行层归属 | 权限矩阵是引擎责任还是上层应用层？ | 明确分层 |
| AMB-7 | Rule 缺乏动态逻辑 | rule 仅有静态配置，无条件判断与动作触发能力 | 引入 `logic` 字段 |

---

## 四、修改优先级总表

| 优先级 | 编号 | 修改项 | 难度 | 发现者 |
|--------|------|--------|------|--------|
| **P0** | BUG-01 | `create_relation` 枚举验证 | 低（5 行） | Yuxin |
| **P0** | BUG-02 | User 级联删除更新缓存计数 | 低（10 行） | RH |
| **P1** | BUG-03 | `delete group` 级联 group_user | 低（1 行）| Yuxin+RH |
| **P1** | BUG-04 | `delete user` 级联 group_user + 离组标记 | 中（20 行） | Yuxin+RH |
| **P1** | C-1~3 | 修正 `command.md` 级联策略矛盾 | Spec 修改 | Yuxin+RH |
| **P2** | BUG-05 | Restore 命令 | 中 | Yuxin+RH |
| **P2** | BUG-06 | RBAC 权限控制 | 高 | Yuxin+RH |
| **P2** | BUG-07 | 可见性过滤 | 中 | RH |
| **P2** | BUG-08 | 跨组用户唯一性约束 | 中 | RH |
| **P2** | BUG-10 | target_interaction 自动创建 | 中 | Yuxin |
| **P3** | BUG-09 | scoring_criteria 结构验证 | 低 | RH |
| **P3** | BUG-11 | 引用完整性约束 | 中 | Yuxin |
| **P3** | AMB-1 | 状态机方向性约束 | 低 | RH |
| **P3** | AMB-7 | Rule 动态逻辑字段 | 高 | RH |

---

## 五、各文档独有发现摘要

### 仅 Yuxin 发现

- `create_relation` 枚举验证缺失（BUG-01）— 唯一通过直接测试触发的数据完整性 bug
- `target_interaction` 需手动创建（BUG-10）
- 引用完整性缺失（BUG-11）

### 仅 RH 发现

- User 级联删除后缓存计数陈旧（BUG-02）— 通过深度审计 like_count/comment_count 发现
- 无跨组用户唯一性约束（BUG-08）— 同用户多队报名同一 category
- 无可见性过滤（BUG-07）— anonymous 可读 draft 内容
- scoring_criteria 无校验（BUG-09）— weights 和可超过 100
- 状态机无方向约束（AMB-1）— closed→draft 可逆向
- Rule 无动态逻辑能力（AMB-7）— 仅静态配置，无 IF-THEN 规则
- target:interaction 级联策略未定义（AMB-2）

### 两方共同发现

- 无 RBAC 权限控制（BUG-06）
- group:user 级联问题 + Spec 矛盾（BUG-03/04, C-1/2/3）
- 无 Restore 命令（BUG-05）
