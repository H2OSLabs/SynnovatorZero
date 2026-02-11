# 附录 B：报名规则定义（Rule Definition）

本节详细说明活动报名环节中 Rule 的定义方式与执行逻辑。Rule 由组织者在创建活动时定义，系统在用户报名时自动执行。

## B.1 规则类型与模板

| 规则模板名称 | 逻辑说明 | 参数示例 |
|-------------|---------|---------|
| **Default**（默认） | 允许用户自由创建新 Post 参赛 | — |
| **Not create Only Select** | 仅允许选择已有 Post，不可新建 | — |
| **Must be Team** | **必须团队报名**，个人无法报名 | `{ allow_individual: false }` |
| **Min Team Size** | **团队中至少有（N）人** | `{ min_size: 3 }` |
| **Team Proposal Required** | **报名必须有关联到报名团队的团队提案** | `{ require_team_post: true }` |
| **Leader Only** | **只有队长可以报名** | `{ role_required: "owner" }` |
| **Leader Proposal Only** | **只有队长的提案可以作为报名提案** | `{ post_owner_role: "owner" }` |
| **Auto Advancement** | **自动晋级**：前序活动晋级者自动获得资格 | `{ source_event_id: 101, condition: "promoted" }` |
| **Prerequisite Participation** | **前置参赛**：必须是某活动（如 X 赛道）的参加者 | `{ source_event_id: 202, condition: "participated" }` |
| **Asset Type Constraint** | **特定资产要求**：提案必须包含特定类型的资产 | `{ asset_type: "model", min_count: 1 }` |
| **File Format Constraint** | **文件格式要求**：提案附件必须包含特定格式文件 | `{ formats: ["ipynb", "py"] }` |
| **Bounty** | 悬赏活动规则，提案互不可见 | `{ visibility: "private" }` |
| **Enterprise Challenge** | 企业出题规则，提案互不可见 | `{ visibility: "private" }` |
| **Custom** | 用户自定义规则 | （见 checks 定义） |

## B.2 规则执行流程

```mermaid
flowchart TD
    A[用户点击报名] --> B[系统读取活动 Rule]
    B --> C{Rule 类型}
    C -->|Default| D[显示新建 Post 入口]
    C -->|Not create Only Select| E[屏蔽新建功能]
    C -->|Bounty/Enterprise| F[启用提案隐私保护]
    D --> G[用户新建 Post for event]
    E --> H[强制跳转：选择已有 Post]
    F --> I[提案创建但互不可见]
    H --> J[用户从自己的 Post 列表中选择]
    J --> K[系统自动为 Post 添加活动 Tag]
    K --> L[报名完成]
    G --> M[Post 关联到 Event]
    I --> M
    M --> L
```

## B.3 组织者配置 Rule

| 步骤 | 用户操作 | 数据操作 | 说明 |
|------|---------|---------|------|
| 1 | 进入 Rule 编辑页 | `READ rule` | 查看当前 Rule 配置 |
| 2 | 选择规则类型 | `UPDATE rule`（type 字段） | 设置为 Default / Not create Only Select / Bounty 等 |
| 3 | 配置附加参数 | `UPDATE rule` | 如：是否允许 public、审核人列表、提交截止时间、团队人数限制 |
| 4 | 配置报名字段 | `UPDATE rule`（registration_fields） | 设置报名时需要用户填写的信息字段 |
| 5 | 保存并关联到活动 | `UPDATE event:rule` | Rule 生效，影响后续所有报名用户 |

- **结果：** 活动规则配置完成，系统将根据 Rule 自动约束用户的报名行为
