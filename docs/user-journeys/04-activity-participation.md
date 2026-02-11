# 4. 参与活动与提交

- **角色：** 参赛者
- **前置条件：** 已登录，目标活动已发布

```mermaid
flowchart TD
    A[浏览活动详情] --> B[点击报名]
    B --> B0{Rule pre-checks 校验}
    B0 -->|通过| B1{是否以团队身份报名}
    B0 -->|失败| B00[显示错误提示]
    B1 -->|是| B2[团队报名绑定]
    B1 -->|否| C
    B2 --> C{活动 Rule 要求}
    C -->|需要新建提交| D[创建 Post]
    C -->|可选择已有内容| E[选择已有 Post]
    D --> F{提交 pre-checks 校验}
    E --> F
    F -->|通过| G[Post 关联到 Event]
    F -->|失败| F0[显示错误提示]
    G --> H[报名完成]
```

## 4.1 报名参赛与内容提交

| 用户旅程 | 说明 | 数据操作 |
|---------|------|---------|
| 浏览活动详情 | 查看活动说明、规则和奖励 | `READ event` + `READ rule` |
| 点击报名 | 发起报名请求 | 触发 Rule pre-checks |
| 团队报名 | 以团队身份报名活动 | `CREATE event:group` |
| 个人报名 | 以个人身份报名活动 | `CREATE event:user` |
| 提交参赛内容 | 将帖子关联到活动 | `CREATE event:post` |
| **自动打标** | 报名成功后，关联的提案会自动获得该活动的专属标签（如 `#for_category`），用于标识内容归属 | `UPDATE post` (tags append `#for_category`) |

## 4.2 报名规则校验（Entry Rule Enforcement）

> 基于 TC-ENTRY 测试用例

报名和提交操作会触发 Rule 的 `checks` 校验，系统按以下**优先级**顺序执行：

1.  **全局前置校验 (System Checks)**：
    *   **重复报名 (Unique Enrollment)**：检查用户是否已以个人身份报名，或**是否属于任何已报名该活动的团队成员**。若已存在，直接返回失败（Priority 1）。
    *   **活动状态 (Event Status)**：检查活动是否处于报名窗口期内。

2.  **自定义规则校验 (Custom Rule Checks)**：
    *   依次执行 Rule 中定义的 checks（如 `Leader Only`, `Team Size`, `Asset Required`）。
    *   任一 check 失败，立即终止并返回该 check 定义的**错误提示信息**。

| 触发点 | 校验内容 | 失败处理 |
|-------|---------|---------|
| `create_relation(event_group)` | 团队报名前置条件 | `on_fail: deny` 拒绝操作 |
| `create_relation(event_post)` | 帖子提交前置条件 | `on_fail: deny` 拒绝操作 |

### 常见校验场景

| 场景 | condition type | 说明 |
|------|---------------|------|
| **重复报名校验** | `unique_enrollment` | **最高优先级**。若用户所在的任一团队已成功报名，视为用户已报名。 |
| **仅限队长报名** | `role_check` | 检查操作者在团队中的角色是否为 `owner`。若非队长，提示“仅限队长操作”。 |
| **活动状态限制** | `status` | 已结束 (`ended`) 的活动**禁止报名**；未开始但处于报名期 (`enrollment_window`) 的活动允许报名 |
| **报名时间限制** | `time_window` | 必须在 `enrollment_start` 和 `enrollment_end` 之间提交，否则**禁止报名** |
| 必须已有 profile 帖子 | `exists` | 用户需先完善个人资料 |
| 必须包含附件 | `resource_required` | 提案需包含指定数量/格式的附件 |
| 团队人数限制 | `count` | 团队成员数满足 min/max 要求 |

### 校验失败示例

```
❌ 报名失败：当前不在报名时间段内
❌ 报名失败：您所在的团队 "Alpha Team" 已经报名了此活动（重复报名）
❌ 报名失败：根据规则 "Leader Only"，只有团队队长可以执行报名操作
❌ 提交失败：提案必须包含至少一个 PDF 附件（TC-ENTRY-011）
```

- **结果：** 用户（或团队）成功报名活动，其 Post 作为参赛内容与活动关联，并自动获得活动专属标签
