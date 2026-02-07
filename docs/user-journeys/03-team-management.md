# 3. 团队相关

- **角色：** 参赛者
- **前置条件：** 已登录

## 3.1 加入团队

| 步骤 | 用户操作 | 数据操作 | 说明 |
|------|---------|---------|------|
| 1 | 浏览可加入的 Group | `READ group`（公开列表） | 查看可加入的团队/分组 |
| 2 | 选择目标 Group | `READ group`（详情） | 查看 Group 详情和成员列表 |
| 3 | 申请加入 | `CREATE group:user`（关联，role=member） | 将 user 关联到 group；`require_approval=true` 时 status 初始为 `pending`，否则自动为 `accepted` |
| 4 | （若需审批）等待审批 | — | Group Owner/Admin 批准：`UPDATE group:user`（status → accepted） |
| 5 | 加入成功 | `READ group`（成员列表） | 用户成为 Group 成员 |

- **结果：** 用户成为某个 Group 的成员，可以以团队身份参与活动

## 3.2 团队创建与管理

| 用户旅程 | 说明 | 数据操作 |
|---------|------|---------|
| 创建团队 | 发起并命名一个新的团队，添加团队简介 | `CREATE group` |
| 关联团队提案 | 将个人提案作为团队提案与团队进行关联 | `CREATE group:post`（关联） |
| 邀请成员 | 在团队中搜索并邀请他人，等待对方批准 | `CREATE group:user`（status: pending） |
| 成员批准 | 被邀请成员可在通知界面选择加入/拒绝 | `UPDATE group:user`（status: accepted/rejected） |
| 申请加入团队 | 在目标团队主页点击申请，等待队长批准 | `CREATE group:user`（status: pending） |
| 审批成员申请 | 队长在通知或管理后台通过或拒绝他人的申请 | `UPDATE group:user`（status: accepted/rejected） |
| 成员退出/移除 | 成员主动退出或被队长移除出组 | `DELETE group:user` |

## 3.3 团队资产管理

| 用户旅程 | 说明 | 数据操作 |
|---------|------|---------|
| 团队共享资产 | 团队成员共享团队资产文件 | `READ resource`（通过 group:resource） |
| 上传团队资产 | 向团队空间上传文件 | `CREATE resource` + `CREATE group:resource` |
