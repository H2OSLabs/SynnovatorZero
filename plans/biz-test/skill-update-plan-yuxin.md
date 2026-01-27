# Synnovator Skill 修改计划 (Yuxin)

> **来源：** 基于 `SynNovator-Skills-Test-Yuxin.md` 和 `Fill-Gap-Yuxin.md` 两轮测试结果
>
> **目标文件：** `.claude/skills/synnovator/scripts/engine.py`
>
> **原则：** 本文档仅记录需要修改的地方，不直接修改代码。

---

## 一、确认的 Bug（必须修复）

### 1.1 `create_relation` 缺少枚举字段验证

**位置：** `engine.py` 第 399-429 行，`create_relation()` 函数

**问题：** `update_relation()` 在第 469-473 行对 `relation_type`, `display_type`, `role`, `status` 等枚举字段进行了验证，但 `create_relation()` 完全没有做枚举验证。

**复现：**
```bash
uv run python .claude/skills/synnovator/scripts/engine.py \
  --data-dir .synnovator_test \
  create group_user \
  --data '{"group_id":"grp_alpha","user_id":"user_bob","role":"superadmin"}'
# 预期: EXIT=1 (superadmin 不在 ENUMS["group_user.role"] 中)
# 实际: EXIT=0 (记录成功创建，包含无效枚举值)
```

**影响范围：** 所有关系的枚举字段：

| 关系类型 | 字段 | 合法值 |
|---------|------|-------|
| `group_user` | `role` | `owner`, `admin`, `member` |
| `group_user` | `status` | `pending`, `accepted`, `rejected` |
| `category_post` | `relation_type` | `submission`, `reference` |
| `post_post` | `relation_type` | `reference`, `reply`, `embed` |
| `post_resource` | `display_type` | `attachment`, `inline` |

**修改方案：** 在 `create_relation()` 函数中，`save_record()` 调用之前（约第 427 行），添加与 `update_relation()` 第 469-473 行相同的枚举验证逻辑：

```python
# 在 create_relation() 中，save_record() 之前添加:
for field in ["relation_type", "display_type", "role", "status"]:
    if field in data:
        enum_key = f"{relation_type}.{field}"
        if enum_key in ENUMS and data[field] not in ENUMS[enum_key]:
            raise ValueError(f"Invalid value '{data[field]}' for {enum_key}. Allowed: {ENUMS[enum_key]}")
```

**插入位置：** 第 421 行（`data.setdefault("role", "member")` 之后）和第 423 行（`rel_id = gen_id("rel")` 之前）之间。

---

## 二、Spec 与实现不一致（需要确认规格后修复）

### 2.1 `delete group` 未级联 `group_user` 关系

**位置：** `engine.py` 第 386-387 行

**现状：**
```python
elif content_type == "group":
    _cascade_delete_relations(data_dir, "category_group", "group_id", record_id)
```
只级联删除了 `category_group`，未处理 `group_user`。

**Spec 矛盾：**
- `command.md` 级联策略表（第 452 行）："软删除 group → group:user 关系保留（成员可查询历史）"
- `command.md` CRUD 操作表（第 634 行）："DELETE group → 解除所有 group:user、category:group 关系"

**测试验证：** 删除 group 后，`read group_user --filters '{"group_id":"g1"}'` 仍返回完整记录。

**修改方案（二选一，需 Spec Owner 确认）：**

**方案 A — 保留 group_user（遵循级联策略表）：**
不修改代码，但需要在读取 `group_user` 时过滤已删除 group 的记录。当前行为已符合此方案。

**方案 B — 级联删除 group_user（遵循 CRUD 操作表）：**
```python
elif content_type == "group":
    _cascade_delete_relations(data_dir, "group_user", "group_id", record_id)
    _cascade_delete_relations(data_dir, "category_group", "group_id", record_id)
```

### 2.2 `delete user` 未级联 `group_user` 关系

**位置：** `engine.py` 第 384-385 行

**现状：**
```python
elif content_type == "user":
    _cascade_soft_delete_user_interactions(data_dir, record_id)
```
只级联软删除了 interactions，未处理 `group_user`。

**Spec 矛盾：**
- `command.md` 级联策略表（第 451 行）："软删除 user → group:user 关系保留（标记为离组）"
- `command.md` CRUD 操作表（第 633 行）："DELETE user → 解除所有 group:user 关系，删除所有该用户的 interaction"

**测试验证：** 删除 user 后，`read group_user --filters '{"user_id":"u2"}'` 仍返回完整记录。

**修改方案（二选一，需 Spec Owner 确认）：**

**方案 A — 标记为离组（遵循级联策略表）：**
将 group_user 记录的 status 改为特殊值（如 `left`），需要先在 ENUMS 中添加该值：
```python
# ENUMS 修改
"group_user.status": ["pending", "accepted", "rejected", "left"],

# delete_content 修改
elif content_type == "user":
    _cascade_soft_delete_user_interactions(data_dir, record_id)
    _mark_user_left_groups(data_dir, record_id)  # 新函数
```

**方案 B — 级联删除 group_user（遵循 CRUD 操作表）：**
```python
elif content_type == "user":
    _cascade_soft_delete_user_interactions(data_dir, record_id)
    _cascade_delete_relations(data_dir, "group_user", "user_id", record_id)
```

---

## 三、Spec 自身矛盾（需要 Spec 修正）

以下是 `command.md` 中的内部矛盾，需要 Spec Owner 统一口径：

| # | 位置 | 级联策略表说法 | CRUD 操作表说法 | 当前引擎行为 |
|---|------|--------------|---------------|------------|
| 1 | delete group → group_user | 保留（成员可查询历史）(L452) | 解除所有 group:user (L634) | 保留（不级联） |
| 2 | delete user → group_user | 保留（标记为离组）(L451) | 解除所有 group:user (L633) | 保留（不级联） |
| 3 | delete category → 关系 | 关系保留但按可见性过滤 (L449) | 解除所有 category:rule/post/group (L629) | 解除所有（遵循 CRUD 表） |

**建议：** 统一为 CRUD 操作表的描述（解除关系），因为该表更具体，且 category 的实现已遵循该表。

---

## 四、未实现的 Spec 功能（可选优先级较低）

以下功能在 `command.md` 中有描述，但 `engine.py` 中未实现：

### 4.1 恢复机制

**Spec 位置：** 第 454-458 行
- 恢复操作：设置 `deleted_at = NULL`
- 级联恢复：恢复父对象时，一并恢复因级联而软删除的子对象
- 恢复权限：仅 Admin 可执行恢复操作

**建议：** 添加 `restore_content` 命令。

### 4.2 权限控制 (RBAC)

**Spec 位置：** CRUD 操作表的"权限"列（第 627-635 行）

当前 engine.py 的 `--user` 参数仅设置 `created_by`，不做权限检查。例如：
- participant 可以创建 category（应仅 organizer/admin）
- 非作者可以删除别人的 post（应仅作者/admin）

**建议：** 实现基于 role 和 created_by 的权限校验。

### 4.3 引用完整性 — 限制删除有内容的用户

**Spec 位置：** 第 466 行："*.created_by → user.id → 限制删除（不可删除仍有内容的用户）"

当前 engine.py 不检查用户是否仍有关联内容，直接允许删除。

### 4.4 `target_interaction` 关系自动创建

当前创建 interaction 后需要手动调用 `create target_interaction` 来建立关系。按照 Spec 设计，`create interaction` 应自动创建 `target_interaction` 关系。

---

## 五、测试文件改进建议

### 5.1 `SynNovator-Skills-Test-Yuxin.md`

- Section 3.2 的评论内容避免使用 `!` 字符（shell 兼容性）
- 可添加对 `group_user` 删除级联的验证（当前未覆盖）

### 5.2 `Fill-Gap-Yuxin.md`

- Section 6.6 可扩展测试其他关系枚举字段（`category_post.relation_type`, `post_post.relation_type`, `post_resource.display_type`, `group_user.status`）
- 可添加 `delete group` 后检查 `group_user` 是否被级联的测试
- 可添加 `delete user` 后检查 `group_user` 是否被级联的测试

---

## 六、修改优先级

| 优先级 | 编号 | 修改项 | 难度 |
|--------|------|--------|------|
| P0 | 1.1 | `create_relation` 枚举验证 | 低（5 行代码） |
| P1 | 2.1 | `delete group` 级联 group_user（需确认 Spec） | 低（1 行代码） |
| P1 | 2.2 | `delete user` 级联 group_user（需确认 Spec） | 低-中（1-20 行） |
| P1 | 三 | 修正 `command.md` 级联策略矛盾 | Spec 修改 |
| P2 | 4.4 | `target_interaction` 自动创建 | 中 |
| P2 | 4.1 | 恢复机制 | 中 |
| P3 | 4.2 | RBAC 权限控制 | 高 |
| P3 | 4.3 | 引用完整性约束 | 中 |
