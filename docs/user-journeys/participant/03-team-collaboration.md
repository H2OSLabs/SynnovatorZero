# 3. 团队相关

- **角色：** 参赛者
- **前置条件：** 已登录

## 3.1 加入团队

| 步骤 | 用户操作 | 数据操作 | 说明 |
|------|---------|---------|------|
| 1 | 浏览可加入的 Group | `READ group`（公开列表） | 查看可加入的团队/分组 |
| 2 | 选择目标 Group | `READ group`（详情） | 查看 Group 详情、成员列表及**关联的团队提案** |
| 3 | 申请加入 | `CREATE group:user`（关联，role=member, status=pending）<br>+ `CREATE notification`（recipient=owner） | 将 user 关联到 group，状态为 `pending`。<br>触发系统通知发送给团队队长，包含申请人个人主页链接。 |
| 4 | （若需审批）队长审批 | `READ user` (applicant profile)<br>`UPDATE group:user`（status → accepted/rejected）<br>+ `CREATE notification`（recipient=applicant） | 队长收到通知后，点击链接查看申请人详情。<br>队长操作“同意”或“拒绝”。<br>系统自动发送审批结果通知给申请人。 |
| 5 | 加入成功 | `READ group`（成员列表） | 用户成为 Group 成员 |

- **结果：** 用户成为某个 Group 的成员，可以以团队身份参与活动

## 3.2 团队创建与管理

| 用户旅程 | 说明 | 数据操作 |
|---------|------|---------|
| 创建团队 | 发起并命名一个新的团队，添加团队简介 | `CREATE group` |
| 关联团队提案 | 将个人提案作为团队提案与团队进行关联 | `CREATE group:post`（关联） |
| 邀请成员 | 在团队中搜索并邀请他人，等待对方批准 | `CREATE group:user`（status: pending） |
| 成员批准 | 被邀请成员可在通知界面选择加入/拒绝 | `UPDATE group:user`（status: accepted/rejected） |
| 申请加入团队 | 在目标团队主页点击申请，触发系统通知给队长 | `CREATE group:user` (pending) + `CREATE notification` (type: team_apply) |
| 审批成员申请 | 队长收到含申请人主页链接的通知，点击查看详情并操作同意/拒绝。申请人收到结果通知。 | `UPDATE group:user` + `CREATE notification` (type: team_apply_result) |
| 成员退出/移除 | 成员主动退出或被队长移除出组 | `DELETE group:user` |

## 3.3 团队资产管理

| 用户旅程 | 说明 | 数据操作 |
|---------|------|---------|
| 团队共享资产 | 团队成员共享团队资产文件 | `READ resource`（通过 group:resource） |
| 上传团队资产 | 向团队空间上传文件 | `CREATE resource` + `CREATE group:resource` |
| 副本协作机制 | 非作者成员无法直接编辑他人资产，需申请“复制”生成新资产副本进行修改 | `CLONE resource` (owner=current_user) + `CREATE group:resource` |
| 资产解绑 | 队员主动离开或被强制移除时，其创建的资产（作为 owner）自动解除与团队的关联，保留在个人名下 | `DELETE group:resource` (where resource.owner == removed_user) |

## 3.4 团队解散与异常处理 (Constraints & Dissolution)

| 场景 | 规则说明 | 行为限制 |
|------|---------|---------|
| **最后一位管理员** | 团队必须至少保留一名 Owner/Admin | 若当前用户是唯一 Admin，**禁止退出团队**，必须先移交权限或直接解散团队 |
| **团队解散** | Owner 可主动解散团队 | 解散后，团队关联的所有提案和资产自动解除绑定，恢复为作者的个人提案/资产。 |
| **禁止解散** | 团队持有公共资产 | 若团队拥有**公共资产**（如平台发放给团队的特定资源，owner=group），则**禁止解散团队**，必须先消耗或转移该类资产。 |
| **强制移除** | 成员被踢出 | 被踢出成员失去对团队内部（非公开）内容的访问权，**其关联的个人资产自动解绑并归还个人**，但其已贡献的代码/提案版本保留（不可变） |
