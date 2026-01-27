# Synnovator Skill 综合修复计划

> **整合来源：**
> - `skill-update-plan-yuxin.md` — Yuxin 两轮测试 (Bug 分析 + Spec 矛盾 + 未实现功能)
> - `skill-update-plan-yilun.md` — Yilun 测试 (ID 生成一致性)
> - `skill-update-plan-ruihua.md` + `test-optimization-log-rh.md` — Ruihua 第三轮 GAP 补全审计 (52 用例, 7 个 Bug, 7 个 Spec 模糊性)
>
> **目标文件：** `.claude/skills/synnovator/scripts/engine.py`
>
> **Spec 文件：** `docs/command.md`
>
> **日期：** 2026-01-27
> **更新：** 2026-01-27 — FIX-06 Spec 矛盾已修复，FIX-04/05 方向已确认
> **分支：** `test/biz-test`

---

## 一、修复总览

| 优先级 | 编号 | 修改项 | 类型 | 难度 | 发现者 |
|--------|------|--------|------|------|--------|
| **P0** | FIX-01 | `create_relation` 枚举验证缺失 | Bug | 低 | Yuxin |
| **P0** | FIX-02 | User 级联删除未更新缓存计数 | Bug | 低 | Ruihua |
| **P0** | FIX-03 | 生成数据 ID 格式不一致 | Bug | 低 | Yilun |
| **P1** | FIX-04 | `delete group` 未级联 `group_user` | Bug | 低 | Yuxin+Ruihua |
| **P1** | FIX-05 | `delete user` 未级联 `group_user` | Bug | 低 | Yuxin+Ruihua |
| ~~P1~~ | ~~FIX-06~~ | ~~`command.md` 级联策略表与 CRUD 操作表矛盾~~ | ~~Spec~~ | — | **DONE** |
| **P2** | FIX-07 | 添加 Restore 命令 | 缺失功能 | 中 | Yuxin+Ruihua |
| **P2** | FIX-08 | `target_interaction` 自动创建 | 缺失功能 | 中 | Yuxin |
| **P2** | FIX-09 | 无跨组用户唯一性约束 | 缺失功能 | 中 | Ruihua |
| **P2** | FIX-10 | 无可见性过滤 | 缺失功能 | 中 | Ruihua |
| **P3** | FIX-11 | RBAC 权限控制 | 缺失功能 | 高 | Yuxin+Ruihua |
| **P3** | FIX-12 | 引用完整性 — 限制删除有内容的用户 | 缺失功能 | 中 | Yuxin |
| **P3** | FIX-13 | `scoring_criteria` 结构验证 | 缺失功能 | 低 | Ruihua |
| **P3** | FIX-14 | 状态机方向性约束 | 缺失功能 | 低 | Ruihua |
| **P3** | FIX-15 | Rule 动态逻辑字段 | Spec 扩展 | 高 | Ruihua |

---

## 二、P0 — 数据完整性（必须修复）

### FIX-01: `create_relation` 缺少枚举字段验证

**位置：** `engine.py` — `create_relation()` 函数 (L399-429)

**问题：** `update_relation()` 在 L469-473 对 `relation_type`, `display_type`, `role`, `status` 等枚举字段做了验证，但 `create_relation()` 完全没有枚举校验。可通过 create 写入非法值。

**复现：**
```bash
uv run python .claude/skills/synnovator/scripts/engine.py \
  --data-dir .synnovator_test \
  create group_user \
  --data '{"group_id":"grp_alpha","user_id":"user_bob","role":"superadmin"}'
# 预期: EXIT=1 (superadmin 不在 ENUMS["group_user.role"] 中)
# 实际: EXIT=0 (记录成功创建)
```

**影响字段：**

| 关系类型 | 字段 | 合法值 |
|---------|------|-------|
| `group_user` | `role` | `owner`, `admin`, `member` |
| `group_user` | `status` | `pending`, `accepted`, `rejected` |
| `category_post` | `relation_type` | `submission`, `reference` |
| `post_post` | `relation_type` | `reference`, `reply`, `embed` |
| `post_resource` | `display_type` | `attachment`, `inline` |

**修复方案：** 在 `create_relation()` 函数中，`save_record()` 调用之前（约 L427），添加与 `update_relation()` L469-473 相同的枚举验证逻辑：

```python
# 在 create_relation() 中，save_record() 之前添加:
for field in ["relation_type", "display_type", "role", "status"]:
    if field in data:
        enum_key = f"{relation_type}.{field}"
        if enum_key in ENUMS and data[field] not in ENUMS[enum_key]:
            raise ValueError(f"Invalid value '{data[field]}' for {enum_key}. Allowed: {ENUMS[enum_key]}")
```

**插入位置：** L421 (`data.setdefault("role", "member")` 之后) 和 L423 (`rel_id = gen_id("rel")` 之前) 之间。

---

### FIX-02: User 级联删除未更新目标 Post 缓存计数

**位置：** `engine.py` L384-385 + L592-599

**问题：** `_cascade_soft_delete_user_interactions()` 软删除了用户的 interaction，但未调用 `_update_cache_stats()`。对比：直接删除 interaction 时（L388-392）会调用 `_update_cache_stats(removed=True)`。

**复现：**
1. 用户 Charlie 对某 Post 点赞 + 评论 → `like_count=1, comment_count=1`
2. Admin 删除 Charlie → interaction 被级联软删除
3. 读取目标 Post → `like_count=1, comment_count=1`（陈旧，应为 0）

**修复方案：** 在 `_cascade_soft_delete_user_interactions()` 中，对每个被软删除的 interaction，调用 `_update_cache_stats(target_id, removed=True)` 更新目标 post 的缓存计数。

---

### FIX-03: 生成数据 ID 格式不一致

**问题：** 执行 `create` 命令后，输出的文件名格式不统一。有些是 `post_submission_01.md`（语义命名），有些是 `post_61dbe7351af8.md`（UUID 格式）。

**预期行为：** 所有 record 的 id 和文件名一致，格式统一为 `{type}_{uuid}.md`。

**修复方案：** 排查 `gen_id()` 函数以及 skill prompt 中是否有指导 AI 生成语义化 ID 的逻辑，统一为 UUID 格式。确保 skill 的 prompt 指令中不会引导生成 `post_submission_01` 这类命名。

---

## 三、P1 — 级联行为修复（Spec 已确认：统一解除关系）

> **决策记录：** FIX-06 已完成。`command.md` 级联策略表、CRUD 操作表、引用完整性表已统一为"解除关系（硬删除）"方案。恢复机制已补充"硬删除的关系不可自动恢复"说明。

### FIX-04: `delete group` 未级联 `group_user` 关系

**位置：** `engine.py` L386-387

**现状：**
```python
elif content_type == "group":
    _cascade_delete_relations(data_dir, "category_group", "group_id", record_id)
```
仅级联删除 `category_group`，未处理 `group_user`。

**修复方案：** 添加 `group_user` 级联删除：
```python
elif content_type == "group":
    _cascade_delete_relations(data_dir, "group_user", "group_id", record_id)
    _cascade_delete_relations(data_dir, "category_group", "group_id", record_id)
```

---

### FIX-05: `delete user` 未级联 `group_user` 关系

**位置：** `engine.py` L384-385

**现状：**
```python
elif content_type == "user":
    _cascade_soft_delete_user_interactions(data_dir, record_id)
```
仅级联软删除 interactions，未处理 `group_user`。

**修复方案：** 添加 `group_user` 级联删除：
```python
elif content_type == "user":
    _cascade_soft_delete_user_interactions(data_dir, record_id)
    _cascade_delete_relations(data_dir, "group_user", "user_id", record_id)
```

---

### ~~FIX-06: 修正 `command.md` 级联策略矛盾~~ — DONE

已于 2026-01-27 修复。`command.md` 变更内容：

1. **级联策略表 (L447-455)** — 从 4 行扩展为 7 行，覆盖全部内容类型，统一为"解除关系"
2. **引用完整性表 (L474-475)** — `group:user.user_id` 从"保留（标记为离组）"改为"级联软删除时解除"；新增 `group:user.group_id` 行
3. **恢复机制 (L459-462)** — 明确级联恢复仅限软删除子对象，硬删除的关系不可自动恢复

---

## 四、P2 — 缺失功能

### FIX-07: 添加 Restore 命令

**Spec 位置：** L454-458

**需求：**
- 恢复操作：设置 `deleted_at = NULL`
- 级联恢复：恢复父对象时，一并恢复因级联而软删除的子对象
- 恢复权限：仅 Admin 可执行

**当前问题：** `update_content()` (L322-323) 对已软删除记录阻止一切更新，且不存在 `restore` 命令。

**修复方案：** 添加 `restore_content()` 函数，作为独立子命令：
1. 检查调用者是否为 Admin 角色（依赖 FIX-11 RBAC 实现；如暂不实现 RBAC，可先不做权限检查）
2. 将目标记录的 `deleted_at` 设为 null
3. 级联恢复因级联而软删除的子对象（如 interaction）
4. **注意：** 级联时被硬删除的关系（如 category:rule、group:user 等）不可自动恢复，需手动重建（见 FIX-06 决策）

---

### FIX-08: `target_interaction` 关系自动创建

**问题：** 当前创建 interaction 后需要手动调用 `create target_interaction` 来建立关系。按 Spec 设计，`create interaction` 应自动创建对应的 `target_interaction` 关系。

**修复方案：** 在 `create_content("interaction")` 完成后，自动调用 `create_relation("target_interaction", ...)` 建立关系，参数从 interaction 的 `target_type` 和 `target_id` 提取。

---

### FIX-09: 无跨组用户唯一性约束

**验证用例：** TC-CATGRP-901 — Alice 通过两个不同 group 报名同一 category，均成功。

**业务规则：** 同一用户在同一 category 中只能属于一个 group。

**修复方案：** 在 `create_relation("category_group")` 中，检查新注册 group 的所有成员是否已通过其他 group 注册了同一 category。

---

### FIX-10: 无可见性过滤

**验证用例：** TC-PERM-020 — Anonymous 可读取 draft 状态 post。

**修复方案：** 在 `read_content()` 中，根据 `--user` 上下文和记录的 `status` / `created_by` 实现可见性过滤：
- `draft` / `pending_review` 状态内容仅 `created_by` 本人和 Admin 可见
- 未提供 `--user` 的匿名请求仅可见 `published` 状态内容

---

## 五、P3 — 验证增强与扩展

### FIX-11: RBAC 权限控制

**影响测试：** TC-CAT-902, TC-RULE-900, TC-PERM-001/002, TC-GRP-901, TC-USER-902, TC-IACT-052（共 7 个 FAIL）

**问题：** `--user` 参数仅用于设置 `created_by`，从不读取用户的 `role` 字段进行授权。

**修复方案：** 添加权限中间件，在 CRUD 操作前：
1. 加载 `--user` 对应的用户记录
2. 检查 `role` 字段
3. 按 `command.md` 权限矩阵对操作进行门控
4. 对 UPDATE/DELETE 操作检查 `created_by` 所有权

**Spec 模糊性 (AMB-6)：** 需确认权限检查是引擎层还是上层应用层的责任。

---

### FIX-12: 引用完整性 — 限制删除有内容的用户

**Spec 位置：** L466 "*.created_by → user.id → 限制删除（不可删除仍有内容的用户）"

**修复方案：** 在 `delete_content("user")` 前，检查该 user_id 是否被其他内容类型的 `created_by` 字段引用。如有，拒绝删除并提示。

---

### FIX-13: `scoring_criteria` 结构验证

**验证用例：** TC-RULE-901 — weights 和 = 110 被接受。

**修复方案：** 在 rule 的 CREATE/UPDATE 流程中，如果 data 包含 `scoring_criteria`：
- 校验 weights 总和 = 100
- 校验每个 weight 在 0-100 范围内

---

### FIX-14: 状态机方向性约束

**问题 (AMB-1)：** `category.status` 描述 "draft → published → closed" 暗示单向流，但引擎允许任意方向变更（如 `closed → draft`）。

**修复方案（需 Spec Owner 确认）：** 如确认为严格单向，添加状态流转校验：
```python
VALID_TRANSITIONS = {
    "category.status": {"draft": ["published"], "published": ["closed"]},
    "post.status": {"draft": ["pending_review"], "pending_review": ["published", "rejected"], ...},
}
```

---

### FIX-15: Rule 动态逻辑字段 (AMB-7)

**问题：** Rule Schema 仅包含静态配置（时间、格式、权重）和 Markdown 文字说明，缺乏 IF-THEN 条件判断与动作触发能力。

**建议：** 在 rule 中引入 `logic` 字段，用于定义简单的 IF-THEN 规则：
```yaml
logic:
  - condition: "applicant.has_team == true"
    action: "deny"
    message: "已拥有团队，不可发起新申请"
```

---

## 六、Spec 模糊性汇总

### 已解决

| # | 主题 | 结论 |
|---|------|------|
| ~~AMB-3~~ | "标记为离组" 机制 | **不再需要。** 级联策略已统一为解除关系（硬删除），无需 `"left"` 状态值 |
| ~~AMB-4~~ | User 级联与缓存计数 | **已确认：** 所有导致 interaction 状态变更的路径都应触发缓存计数更新（FIX-02 修复） |

### 待 Spec 补充

| # | 主题 | 描述 | 建议 |
|---|------|------|------|
| AMB-1 | 状态机方向性 | `category.status` "draft→published→closed" 是否严格单向？ | 明确是否允许逆向变更 |
| AMB-2 | target:interaction 级联 | category 删除时 target:interaction 未提及，引擎保留了它们 | cascade table 中明确策略 |
| AMB-5 | Restore 实现方式 | Spec 暗示通过 UPDATE 实现，但 UPDATE 阻止软删除记录操作 | 定义为独立命令 |
| AMB-6 | 权限执行层归属 | 权限矩阵是引擎层责任还是上层应用层？ | 明确分层 |
| AMB-7 | Rule 动态逻辑 | rule 仅有静态配置，无条件判断与动作触发能力 | 引入 `logic` 字段 |

---

## 七、推荐执行顺序

### 第一批：P0 — 数据完整性（无需 Spec 确认）

1. **FIX-01** — `create_relation` 枚举验证（5 行代码）
2. **FIX-02** — User 级联删除更新缓存计数（10 行代码）
3. **FIX-03** — 统一 ID 格式（排查 skill prompt + `gen_id()`）

### 第二批：P1 — 级联修复（Spec 已确认，可直接执行）

4. ~~**FIX-06**~~ — ~~统一 `command.md` 级联策略矛盾~~ — **DONE**
5. **FIX-04** — `delete group` 添加 `group_user` 级联删除（1 行代码）
6. **FIX-05** — `delete user` 添加 `group_user` 级联删除（1 行代码）

### 第三批：P2 — 功能补全

7. **FIX-08** — `target_interaction` 自动创建
8. **FIX-09** — 跨组用户唯一性约束
9. **FIX-10** — 可见性过滤
10. **FIX-07** — Restore 命令（依赖 FIX-11 的权限检查，可先不做权限门控）

### 第四批：P3 — 验证增强与扩展

11. **FIX-13** — `scoring_criteria` 验证
12. **FIX-14** — 状态机方向性
13. **FIX-12** — 引用完整性约束
14. **FIX-11** — RBAC 权限控制（工作量最大）
15. **FIX-15** — Rule 动态逻辑（Spec 扩展，需设计评审）

---

## 八、各来源独有发现摘要

### 仅 Yilun 发现
- **FIX-03**: ID 生成格式不一致（`post_submission_01.md` vs `post_61dbe7351af8.md`）

### 仅 Yuxin 发现
- **FIX-01**: `create_relation` 枚举验证缺失 — 唯一通过直接测试触发的数据完整性 bug
- **FIX-08**: `target_interaction` 需手动创建
- **FIX-12**: 引用完整性缺失

### 仅 Ruihua 发现
- **FIX-02**: User 级联删除后缓存计数陈旧 — 通过深度审计发现
- **FIX-09**: 无跨组用户唯一性约束 — 同用户多队报名同一 category
- **FIX-10**: 无可见性过滤 — anonymous 可读 draft 内容
- **FIX-13**: `scoring_criteria` 无校验 — weights 和可超过 100
- **FIX-14**: 状态机无方向约束 — closed→draft 可逆向
- **FIX-15**: Rule 无动态逻辑能力
- **AMB-2**: `target:interaction` 级联策略未定义

### 三方共同发现
- **FIX-04/05**: group:user 级联缺失 | **FIX-06**: ~~Spec 矛盾~~ — **DONE**
- **FIX-07**: 无 Restore 命令
- **FIX-11**: 无 RBAC 权限控制
