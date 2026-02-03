# 附录 C：声明式规则引擎

> 基于 TC-ENGINE 测试用例

规则引擎通过 Rule 的 `checks` 字段实现声明式约束，支持 pre（前置校验）和 post（后置动作）两个阶段。

## C.1 条件类型（Condition Types）

| 类型 | 说明 | 参数示例 |
|------|------|---------|
| `time_window` | 时间窗口限制 | `{ start: "2024-01-01", end: "2024-12-31" }` |
| `count` | 计数校验 | `{ entity: group_user, scope: group, filter: { status: accepted }, op: ">=", value: 2 }` |
| `exists` | 存在性检查 | `{ entity: post_resource, scope: post, require: true }` |
| `field_match` | 字段匹配 | `{ entity: category, field: status, op: "==", value: "published" }` |
| `resource_format` | 附件格式校验 | `{ formats: ["pdf", "zip"] }` |
| `resource_required` | 附件数量和格式 | `{ min_count: 2, formats: ["pdf"] }` |
| `aggregate` | 聚合计算 | `{ entity: group_user, agg_func: count, op: ">=", value: 2 }` |

## C.2 固定字段自动展开

Rule 的固定字段会自动展开为 checks：

| 固定字段 | 展开为 |
|---------|-------|
| `max_submissions=2` | `{ trigger: create_relation(category_post), phase: pre, condition: { type: count, ... } }` |
| `min_team_size=2` | `{ trigger: create_relation(category_group), phase: pre, condition: { type: count, ... } }` |

**执行顺序：** 固定字段展开的 check → 自定义 checks（TC-ENGINE-021）

## C.3 多 Rule 合并

当活动关联多条 Rule 时，所有 checks 合并后按 **AND 逻辑** 执行：

```
活动关联 Rule A + Rule B
→ Rule A 的 checks + Rule B 的 checks 全部执行
→ 任一 check 失败则操作被拒绝
```

## C.4 on_fail 行为

| 值 | 行为 | 说明 |
|----|------|------|
| `deny` | 拒绝操作 | 返回错误信息（默认） |
| `warn` | 允许并警告 | 操作成功但返回警告 |
| `flag` | 允许并标记 | 操作成功，对目标添加标记 |

## C.5 post phase 执行规则

- post phase 的 action 在主操作成功后执行
- 若 condition 不满足，action 不执行
- action 执行失败不回滚主操作（TC-ENGINE-042）

## C.6 空 checks 和无 Rule 场景

| 场景 | 行为 |
|------|------|
| Rule 的 checks 为空数组 | 无约束，所有操作通过 |
| 活动未关联任何 Rule | 无约束，所有操作通过 |
