# 数据完整性约束

本文档定义 Synnovator 平台的数据完整性规则，供开发实现参考。

> 数据类型定义详见 [docs/data-types.md](../docs/data-types.md)，关系定义详见 [docs/relationships.md](../docs/relationships.md)。

---

## 唯一性约束

| 类型 | 约束 | 说明 |
|------|-----|------|
| user | `(username)` | 用户名全局唯一 |
| user | `(email)` | 邮箱全局唯一 |
| target:interaction (like) | `(created_by, target_type, target_id)` | 同一用户对同一目标只能点赞一次（在创建 `target:interaction` 关系时校验） |
| event:rule | `(event_id, rule_id)` | 同一规则不能重复关联到同一活动 |
| event:group | `(event_id, group_id)` | 同一团队不能重复报名同一活动 |
| group:user | `(group_id, user_id)` | 同一用户不能重复加入同一分组 |
| user:user | `(source_user_id, target_user_id, relation_type)` | 同一用户不能重复关注/拉黑同一用户 |
| event:event | `(source_category_id, target_category_id)` | 同一对活动间不能重复建立关联 |

> **业务唯一性规则：** 同一用户在同一 event 中只能属于一个 group。此约束需在应用层校验：`CREATE event:group` 时检查该 group 的所有 accepted 成员是否已通过其他 group 参加了同一 event。
>
> **自引用限制：** `user:user` 和 `event:event` 关系禁止 source 与 target 为同一记录（不能关注自己、活动不能关联自己）。
>
> **循环依赖检测：** `event:event` 关系中 `relation_type=stage` 和 `prerequisite` 禁止循环依赖（A→B→C→A），需在应用层通过图遍历校验。

---

## 软删除策略

所有内容类型（event、post、resource、rule、user、group、interaction）均支持**软删除**：

- **软删除**：设置 `deleted_at = 当前时间`，数据保留在数据库中
- **硬删除**：物理删除记录，仅用于关系解除（见下方说明）

### 查询过滤规则

- 默认查询自动添加 `WHERE deleted_at IS NULL` 过滤
- 管理员可通过特殊参数查询已软删除的记录
- 软删除的内容对非管理员用户不可见

### 级联策略

| 操作 | 级联行为 |
|------|---------|
| 软删除 event | 解除所有 event:rule、event:post、event:group、event:event（作为 source 或 target）关系；通过 target:interaction 关系查找并软删除关联的 interaction，同时解除 target:interaction 关系 |
| 软删除 post | 解除所有 post:post、post:resource、event:post 关系；通过 target:interaction 关系查找并软删除关联的 interaction，同时解除 target:interaction 关系 |
| 软删除 resource | 解除所有 post:resource 关系；通过 target:interaction 关系查找并软删除关联的 interaction，同时解除 target:interaction 关系 |
| 软删除 rule | 解除所有 event:rule 关系 |
| 软删除 user | 解除所有 group:user、user:user（作为 source 或 target）关系；该用户的所有 interaction 一并软删除 |
| 软删除 group | 解除所有 group:user、event:group 关系 |
| 软删除 interaction | 若为父评论，级联软删除所有子回复 |

### 恢复机制

- 恢复操作：设置 `deleted_at = NULL`
- 级联恢复：恢复父对象时，一并恢复因级联而软删除的子对象（如 interaction）
- 注意：级联时被硬删除的关系（如 event:rule、group:user 等）**不可自动恢复**，需手动重建
- 恢复权限：仅 Admin 可执行恢复操作

---

## 引用完整性

### 外键约束

| 字段 | 引用目标 | 约束行为 |
|------|---------|---------|
| `*.created_by` | user.id | 限制删除（不可删除仍有内容的用户） |
| event:rule.event_id | event.id | 级联软删除时解除 |
| event:rule.rule_id | rule.id | 级联软删除时解除 |
| event:post.post_id | post.id | 级联软删除时解除 |
| event:group.group_id | group.id | 级联软删除时解除 |
| group:user.group_id | group.id | 级联软删除时解除 |
| group:user.user_id | user.id | 级联软删除时解除 |
| user:user.source_user_id | user.id | 级联软删除时解除 |
| user:user.target_user_id | user.id | 级联软删除时解除 |
| event:event.source_category_id | event.id | 级联软删除时解除 |
| event:event.target_category_id | event.id | 级联软删除时解除 |
| interaction.parent_id | interaction.id | 级联软删除子回复 |

### 多态引用（target:interaction）的完整性保障

`target:interaction` 关系通过 `(target_type, target_id)` 引用不同内容类型，无法使用数据库级外键。保障策略：

1. **写入校验**：CREATE `target:interaction` 关系时验证 `target_id` 对应的记录存在且未被软删除
2. **读取过滤**：READ interaction 时通过 `target:interaction` 关系联查目标对象，过滤目标已软删除的记录
3. **孤儿清理**：定期任务检测并标记目标已不存在的 `target:interaction` 关系记录
