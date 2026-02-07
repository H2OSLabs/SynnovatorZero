# 测试用例优先级矩阵

> 本文档为 Synnovator 平台所有测试用例的优先级分配，共 552 条测试用例。
>
> **优先级定义：**
> - **P0 关键路径**：MVP 必须，不通过则平台无法使用
> - **P1 核心体验**：主要用户场景，缺失严重影响体验
> - **P2 完整功能**：提升体验，但不阻塞核心流程
> - **P3 高级场景**：特定场景或边缘用例，可后期迭代
> - **P4 负向测试**：异常和边界情况，建议与对应正向用例同步测试

---

## 优先级汇总

| 优先级 | 用例数 | 占比 | 建议时间点 |
|--------|--------|------|------------|
| P0 关键路径 | 97 | 16% | Sprint 1-2 |
| P1 核心体验 | 143 | 24% | Sprint 2-3 |
| P2 完整功能 | 149 | 25% | Sprint 3-4 |
| P3 高级场景 | 69 | 12% | Sprint 4+ |
| P4 负向测试 | 117 | 20% | 随对应正向用例 |

> 注：含 33-frontend-integration.md 新增 22 条前端集成测试用例

---

## P0 关键路径（89 条）

> MVP 必须通过，影响核心业务闭环

### 用户与认证（12 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-USER-001 | 创建 participant 用户 | 01-user.md |
| TC-USER-002 | 创建 organizer 用户 | 01-user.md |
| TC-USER-003 | 创建 admin 用户 | 01-user.md |
| TC-USER-004 | 读取已创建的用户 | 01-user.md |
| TC-AUTH-001 | 手机号密码注册 | 19-auth-profile.md |
| TC-AUTH-002 | 邮箱密码注册 | 19-auth-profile.md |
| TC-AUTH-003 | 手机验证码注册 | 19-auth-profile.md |
| TC-AUTH-010 | 账号密码登录 | 19-auth-profile.md |
| TC-AUTH-011 | 手机验证码登录 | 19-auth-profile.md |
| TC-AUTH-012 | 忘记密码 — 手机号找回 | 19-auth-profile.md |
| TC-AUTH-013 | 忘记密码 — 邮箱找回 | 19-auth-profile.md |
| TC-PROFILE-001 | 创建个人简介 | 19-auth-profile.md |

### 活动管理（15 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-CAT-001 | 创建 competition 类型活动 | 02-category.md |
| TC-CAT-002 | 创建 operation 类型活动 | 02-category.md |
| TC-CAT-003 | 读取已创建的活动 | 02-category.md |
| TC-CAT-010 | 活动状态流转 draft → published → closed | 02-category.md |
| TC-CATMGMT-001 | 发起常规赛道活动（X 类型） | 21-category-management.md |
| TC-CATMGMT-002 | 发起企业命题活动（Y 类型） | 21-category-management.md |
| TC-CATMGMT-003 | 发起悬赏组队活动（Y 类型） | 21-category-management.md |
| TC-CATMGMT-004 | 创建运营活动 | 21-category-management.md |
| TC-CATMGMT-010 | 编写活动说明 | 21-category-management.md |
| TC-CATMGMT-011 | 设定活动规则 — 时间限制 | 21-category-management.md |
| TC-CATMGMT-012 | 设定活动规则 — 团队要求 | 21-category-management.md |
| TC-CATMGMT-013 | 设定活动规则 — 提交要求 | 21-category-management.md |
| TC-CATMGMT-015 | 设定评分标准 | 21-category-management.md |
| TC-CATMGMT-020 | 发布活动 — draft 到 published | 21-category-management.md |
| TC-CATMGMT-021 | 关闭活动 — published 到 closed | 21-category-management.md |

### 规则引擎（10 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-RULE-001 | 创建含完整 scoring_criteria 的规则 | 03-rule.md |
| TC-RULE-002 | 创建 select-only 规则 | 03-rule.md |
| TC-RULE-003 | 读取已创建的规则 | 03-rule.md |
| TC-RULE-100 | 提交截止后创建 category_post 被拒绝 | 03-rule.md |
| TC-RULE-101 | 提交未开始时创建 category_post 被拒绝 | 03-rule.md |
| TC-RULE-102 | 超出 max_submissions 后创建 category_post 被拒绝 | 03-rule.md |
| TC-RULE-103 | 提交格式不符时创建 category_post 被拒绝 | 03-rule.md |
| TC-RULE-104 | 团队人数不足时创建 category_post 被拒绝 | 03-rule.md |
| TC-RULE-108 | 无 rule 关联时 category_post 正常创建 | 03-rule.md |
| TC-REL-CR-001 | 将规则关联到活动 | 08-relations.md |

### 团队基础（10 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-GRP-001 | 创建需审批的公开团队 | 04-group.md |
| TC-GRP-002 | 创建无需审批的私有团队 | 04-group.md |
| TC-GRP-003 | Owner 自动加入 | 04-group.md |
| TC-GRP-004 | 需审批团队 — 成员申请加入为 pending | 04-group.md |
| TC-GRP-005 | Owner 批准成员申请 | 04-group.md |
| TC-TEAM-001 | 创建团队并成为 Owner | 22-team-management.md |
| TC-TEAM-002 | 创建团队并添加团队简介 | 22-team-management.md |
| TC-TEAM-020 | 搜索并邀请成员 | 22-team-management.md |
| TC-TEAM-021 | 被邀请成员接受邀请 | 22-team-management.md |
| TC-REL-CG-001 | 团队报名活动 | 08-relations.md |

### 帖子与内容（18 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-POST-001 | 最小字段创建帖子 | 05-post.md |
| TC-POST-002 | 显式发布帖子 | 05-post.md |
| TC-POST-010 | 创建 team 类型帖子 | 05-post.md |
| TC-POST-011 | 创建 profile 类型帖子 | 05-post.md |
| TC-POST-012 | 创建 proposal 类型帖子 | 05-post.md |
| TC-POST-033 | 草稿发布（draft → published） | 05-post.md |
| TC-RES-001 | 最小字段创建资源 | 06-resource.md |
| TC-REL-CP-001 | 将帖子关联为活动的 submission | 08-relations.md |
| TC-REL-PR-001 | 资源作为 attachment 挂到帖子 | 08-relations.md |
| TC-CREATE-001 | 通过 MD 编辑器创建文档资产 | 24-content-creation.md |
| TC-CREATE-003 | 本地上传文件创建资产 | 24-content-creation.md |
| TC-CREATE-010 | 使用资产发布帖子 | 24-content-creation.md |
| TC-CREATE-011 | 发布日常帖子 | 24-content-creation.md |
| TC-CREATE-020 | 发布提案并创建新资产 | 24-content-creation.md |
| TC-CREATE-021 | 发布提案并放入已有资产 | 24-content-creation.md |
| TC-CREATE-022 | 提案关联活动 | 24-content-creation.md |
| TC-PART-010 | 新建参赛作品帖 | 23-activity-participation.md |
| TC-PART-011 | 选择已有作品关联活动 | 23-activity-participation.md |

### 前端集成 P0（8 条）⭐ 新增

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-FEINT-001 | 前端创建日常帖子调用后端 API | 33-frontend-integration.md |
| TC-FEINT-002 | 前端保存帖子草稿调用后端 API | 33-frontend-integration.md |
| TC-FEINT-010 | 前端创建团队调用后端 API | 33-frontend-integration.md |
| TC-FEINT-030 | 前端登录调用后端 API | 33-frontend-integration.md |
| TC-FEINT-031 | 前端注册调用后端 API | 33-frontend-integration.md |
| TC-FEINT-040 | 前端编辑帖子调用后端 API | 33-frontend-integration.md |
| TC-FEINT-090 | api-client.ts 包含所有 CRUD 方法 | 33-frontend-integration.md |
| TC-FEINT-091 | 前端创建页面无 TODO 遗留 | 33-frontend-integration.md |

### 报名与提交（12 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-PART-001 | 选择团队和提案报名活动 | 23-activity-participation.md |
| TC-PART-002 | 报名时执行规则约束校验 | 23-activity-participation.md |
| TC-PART-003 | 规则校验不满足时拒绝报名 | 23-activity-participation.md |
| TC-PART-012 | 报名成功自动打标 | 23-activity-participation.md |
| TC-PART-020 | 上传演示视频 | 23-activity-participation.md |
| TC-PART-021 | 上传文档资源 | 23-activity-participation.md |
| TC-PART-022 | 上传代码包 | 23-activity-participation.md |
| TC-ENTRY-001 | 报名前必须已加入团队 | 15-entry-rules.md |
| TC-ENTRY-002 | 提交前必须已有团队报名 | 15-entry-rules.md |
| TC-ENTRY-004 | 已满足前置条件时报名成功 | 15-entry-rules.md |
| TC-ENTRY-020 | 一个用户在同一活动中只能有一个参赛提案 | 15-entry-rules.md |
| TC-ENTRY-021 | 同一用户在同一活动中只能属于一个团队 | 15-entry-rules.md |

### 互动基础（12 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-IACT-001 | 对帖子点赞 | 07-interaction.md |
| TC-IACT-003 | 取消点赞后 like_count 递减 | 07-interaction.md |
| TC-IACT-010 | 创建顶层评论 | 07-interaction.md |
| TC-IACT-011 | 创建嵌套回复（一级回复） | 07-interaction.md |
| TC-IACT-013 | comment_count 包含所有层级 | 07-interaction.md |
| TC-IACT-020 | 创建多维度评分 | 07-interaction.md |
| TC-IACT-021 | 多个评分的均值计算 | 07-interaction.md |
| TC-BROWSE-001 | 浏览首页热门内容 | 18-content-browsing.md |
| TC-BROWSE-020 | 查看活动详情 | 18-content-browsing.md |
| TC-BROWSE-021 | 查看帖子详情 | 18-content-browsing.md |
| TC-BROWSE-022 | 查看参赛提案详情 | 18-content-browsing.md |
| TC-JOUR-002 | 匿名访客浏览公开内容 | 11-user-journeys.md |

---

## P1 核心体验（119 条）

> 主要用户场景，缺失会严重影响体验

### 用户资料（11 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-USER-010 | 用户修改自己的个人信息 | 01-user.md |
| TC-PROFILE-002 | 更新个人简介 | 19-auth-profile.md |
| TC-PROFILE-003 | 更改头像 | 19-auth-profile.md |
| TC-PROFILE-004 | 更改显示名称 | 19-auth-profile.md |
| TC-PROFILE-010 | 填写职业信息 | 19-auth-profile.md |
| TC-PROFILE-011 | 填写学校信息 | 19-auth-profile.md |
| TC-PROFILE-012 | 填写兴趣爱好 | 19-auth-profile.md |
| TC-PROFILE-013 | 填写性格标签 | 19-auth-profile.md |
| TC-PROFILE-014 | 活动中收集的信息自动展示 | 19-auth-profile.md |
| TC-PERSONAL-001 | 基本个人信息在主页展示 | 28-personalization.md |
| TC-PERSONAL-002 | 显示名称展示 | 28-personalization.md |

### 活动管理进阶（8 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-CAT-011 | 修改活动名称和描述 | 02-category.md |
| TC-CATMGMT-014 | 设定活动规则 — 内容审核 | 21-category-management.md |
| TC-CATMGMT-022 | 修改已发布活动需创建新版本 | 21-category-management.md |
| TC-CATMGMT-030 | 设置活动审核人员 | 21-category-management.md |
| TC-CATMGMT-031 | 审核人员审核提交内容 | 21-category-management.md |
| TC-CATMGMT-032 | 评委对参赛内容打分 | 21-category-management.md |
| TC-RULE-010 | 修改规则配置字段 | 03-rule.md |
| TC-RULE-011 | 修改 scoring_criteria 权重 | 03-rule.md |

### 规则引擎进阶（10 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-RULE-105 | 团队已满时创建 group_user 被拒绝 | 03-rule.md |
| TC-RULE-106 | allow_public=false 时直接发布被拒绝 | 03-rule.md |
| TC-RULE-107 | allow_public=false 时 pending_review 状态被允许 | 03-rule.md |
| TC-RULE-109 | 多条 rule 全部满足才允许（AND 逻辑） | 03-rule.md |
| TC-ENGINE-001 | time_window 条件 — 开始时间未到 | 17-rule-engine.md |
| TC-ENGINE-002 | time_window 条件 — 截止时间已过 | 17-rule-engine.md |
| TC-ENGINE-005 | exists 条件 — 实体存在时通过 | 17-rule-engine.md |
| TC-ENGINE-006 | exists 条件 — 实体不存在时拒绝 | 17-rule-engine.md |
| TC-ENGINE-020 | 固定字段自动展开为 checks | 17-rule-engine.md |
| TC-ENGINE-030 | 多 Rule 的 checks 合并后 AND 逻辑执行 | 17-rule-engine.md |

### 团队协作（13 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-GRP-006 | Owner 拒绝成员申请 | 04-group.md |
| TC-GRP-007 | 被拒绝后重新申请 | 04-group.md |
| TC-GRP-008 | 无需审批团队 — 成员直接 accepted | 04-group.md |
| TC-GRP-010 | Owner 更新团队信息 | 04-group.md |
| TC-TEAM-010 | 关联个人提案为团队提案 | 22-team-management.md |
| TC-TEAM-011 | 向团队提案添加个人资产 | 22-team-management.md |
| TC-TEAM-012 | 非作者无法编辑他人资产 | 22-team-management.md |
| TC-TEAM-022 | 被邀请成员拒绝邀请 | 22-team-management.md |
| TC-TEAM-030 | 成员主动退出团队 | 22-team-management.md |
| TC-TEAM-031 | 队长移除成员 | 22-team-management.md |
| TC-TEAM-032 | 离开团队后资产解除关联 | 22-team-management.md |
| TC-TEAM-033 | 离开团队后无法使用团队资产 | 22-team-management.md |
| TC-REL-GU-001 | 移出团队成员 | 08-relations.md |

### 帖子管理（16 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-POST-003 | 带 tags 创建帖子 | 05-post.md |
| TC-POST-004 | 按 type 筛选帖子 | 05-post.md |
| TC-POST-030 | 帖子进入 pending_review 状态 | 05-post.md |
| TC-POST-031 | 帖子被审核通过（pending_review → published） | 05-post.md |
| TC-POST-032 | 帖子被驳回（pending_review → rejected） | 05-post.md |
| TC-POST-040 | 通过新帖子实现版本管理 | 05-post.md |
| TC-POST-060 | 更新帖子 title 和 Markdown body | 05-post.md |
| TC-POST-070 | 创建 visibility=private 的帖子 | 05-post.md |
| TC-POST-072 | private 已发布帖子对非作者不可见 | 05-post.md |
| TC-RES-002 | 带完整元信息创建资源 | 06-resource.md |
| TC-RES-030 | 更新资源元信息 | 06-resource.md |
| TC-RES-040 | 关联到 published + public 帖子的 resource 可被任何人读取 | 06-resource.md |
| TC-CREATE-040 | 编辑自己的帖子 | 24-content-creation.md |
| TC-CREATE-041 | 编辑提案标题和简介 | 24-content-creation.md |
| TC-CREATE-042 | 编辑提案中的资产 | 24-content-creation.md |
| TC-CREATE-070 | 删除帖子（软删除） | 24-content-creation.md |

### 内容浏览（12 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-BROWSE-002 | 浏览探索页发现内容 | 18-content-browsing.md |
| TC-BROWSE-003 | 点击热点榜跳转帖子 | 18-content-browsing.md |
| TC-BROWSE-030 | 点击作者进入个人主页 | 18-content-browsing.md |
| TC-BROWSE-031 | 点击团队进入团队主页 | 18-content-browsing.md |
| TC-BROWSE-032 | 在团队页面查看队友信息 | 18-content-browsing.md |
| TC-BROWSE-040 | 通过左侧导航栏跳转页面 | 18-content-browsing.md |
| TC-BROWSE-050 | 登录完成后返回原页面 | 18-content-browsing.md |
| TC-BROWSE-051 | 登录后内容展示增强 | 18-content-browsing.md |
| TC-PLANET-001 | 访问星球页面 | 29-planet-camp.md |
| TC-CAMP-001 | 访问营地页面 | 29-planet-camp.md |
| TC-CAMP-010 | 查看个人提案列表 | 29-planet-camp.md |
| TC-CAMP-012 | 查看参加的团队列表 | 29-planet-camp.md |

### 通知系统（10 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-NOTIF-001 | 点击通知图标查看通知列表 | 20-notification.md |
| TC-NOTIF-002 | 未读通知标记展示 | 20-notification.md |
| TC-NOTIF-003 | 标记单条通知为已读 | 20-notification.md |
| TC-NOTIF-004 | 标记全部通知为已读 | 20-notification.md |
| TC-NOTIF-010 | 点击通知跳转到对应页面 | 20-notification.md |
| TC-NOTIF-011 | 团队申请通知跳转 | 20-notification.md |
| TC-NOTIF-012 | 评论回复通知跳转 | 20-notification.md |
| TC-NOTIF-030 | 接收点赞通知 | 20-notification.md |
| TC-NOTIF-031 | 接收评论通知 | 20-notification.md |
| TC-NOTIF-032 | 接收关注通知 | 20-notification.md |

### 社交互动（11 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-IACT-012 | 创建二级回复（回复的回复） | 07-interaction.md |
| TC-IACT-014 | 删除父评论级联删除子回复 | 07-interaction.md |
| TC-IACT-050 | 修改评论文本 | 07-interaction.md |
| TC-IACT-060 | 对 category（活动）点赞 | 07-interaction.md |
| TC-IACT-061 | 对 category 发表评论 | 07-interaction.md |
| TC-FRIEND-001 | 用户 A 关注用户 B | 13-user-follow.md |
| TC-FRIEND-002 | 用户 B 回关用户 A，双方成为好友 | 13-user-follow.md |
| TC-FRIEND-004 | 取消关注 | 13-user-follow.md |
| TC-SOCIAL-040 | 关注提案 | 25-social-interaction.md |
| TC-SOCIAL-041 | 关注团队 | 25-social-interaction.md |
| TC-SOCIAL-042 | 取消内容关注 | 25-social-interaction.md |

### 结算证书（10 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-CLOSE-020 | 活动关闭后按 average_rating 计算排名 | 16-closure-rules.md |
| TC-CLOSE-030 | 活动关闭后自动颁发证书 | 16-closure-rules.md |
| TC-CLOSE-032 | 证书帖子可被获奖者读取 | 16-closure-rules.md |
| TC-CLOSE-040 | 完整活动结束流程 — 终审 + 排名 + 颁奖 | 16-closure-rules.md |
| TC-SETTLE-001 | 查看评审结果 | 26-settlement-reward.md |
| TC-SETTLE-002 | 查看排名详情 | 26-settlement-reward.md |
| TC-SETTLE-010 | 领取电子证书 | 26-settlement-reward.md |
| TC-SETTLE-011 | 下载电子证书 | 26-settlement-reward.md |
| TC-SETTLE-012 | 证书自动关联到参赛作品 | 26-settlement-reward.md |
| TC-POST-013 | 创建 certificate 类型帖子 | 05-post.md |

### 级联删除（8 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-DEL-001 | 删除 category | 09-cascade-delete.md |
| TC-DEL-003 | 删除 user | 09-cascade-delete.md |
| TC-DEL-004 | 删除 group | 09-cascade-delete.md |
| TC-DEL-010 | 删除 category → 关联 interaction 级联硬删除 | 09-cascade-delete.md |
| TC-DEL-012 | 删除 post → 完整级联链 | 09-cascade-delete.md |
| TC-DEL-015 | 删除父评论 → 级联删除所有子评论 | 09-cascade-delete.md |
| TC-DEL-020 | 读取已删除记录返回 not found | 09-cascade-delete.md |
| TC-JOUR-012 | 删除帖子后验证全部级联 | 11-user-journeys.md |

### 用户旅程（10 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-JOUR-005 | 完整团队加入与审批流程 | 11-user-journeys.md |
| TC-JOUR-007 | 完整团队报名流程 | 11-user-journeys.md |
| TC-JOUR-009 | 创建日常帖子和参赛提案 | 11-user-journeys.md |
| TC-JOUR-010 | 完整证书颁发流程 | 11-user-journeys.md |
| TC-JOUR-011-1 | 编辑自己的帖子（版本管理） | 11-user-journeys.md |
| TC-JOUR-013 | 完整社区互动流程 | 11-user-journeys.md |
| TC-NAV-001 | 从星球页面进入活动详情 | 29-planet-camp.md |
| TC-NAV-002 | 从营地页面进入提案详情 | 29-planet-camp.md |
| TC-NAV-003 | 从营地页面进入团队详情 | 29-planet-camp.md |
| TC-NAV-004 | 星球和营地页面切换 | 29-planet-camp.md |

### 提案迭代（3 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-PROPOSAL-001 | 编辑提案内资产并保存 | 30-proposal-iteration.md |
| TC-PROPOSAL-002 | 多次更新后统一发布 | 30-proposal-iteration.md |
| TC-PROPOSAL-010 | 提案发布产生新版本号 | 30-proposal-iteration.md |

### 页面交互（7 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-PAGEUI-001 | 点击搜索栏展开搜索界面 | 31-page-interaction.md |
| TC-PAGEUI-002 | 输入关键词实时搜索 | 31-page-interaction.md |
| TC-PAGEUI-010 | 导航栏当前位置高亮 | 31-page-interaction.md |
| TC-PAGEUI-011 | 资产页导航入口 | 31-page-interaction.md |
| TC-PAGEUI-022 | 点击消息展示通知页面 | 31-page-interaction.md |
| TC-PAGEUI-023 | 点击发布展示发布页面 | 31-page-interaction.md |
| TC-PAGEUI-025 | 消息图标显示未读数量 | 31-page-interaction.md |

### 资产复制申请（6 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-ASSETCOPY-001 | 在团队提案中查看他人资产 | 32-asset-copy-request.md |
| TC-ASSETCOPY-002 | 发起资产复制申请 | 32-asset-copy-request.md |
| TC-ASSETCOPY-003 | 资产作者收到复制申请通知 | 32-asset-copy-request.md |
| TC-ASSETCOPY-004 | 资产作者批准复制申请 | 32-asset-copy-request.md |
| TC-ASSETCOPY-005 | 资产作者拒绝复制申请 | 32-asset-copy-request.md |
| TC-ASSETCOPY-006 | 申请人获得资产副本 | 32-asset-copy-request.md |

### 前端集成 P1（8 条）⭐ 新增

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-FEINT-003 | 前端创建提案调用后端 API | 33-frontend-integration.md |
| TC-FEINT-004 | 前端创建帖子失败显示错误 | 33-frontend-integration.md |
| TC-FEINT-005 | 前端创建帖子时 API 返回错误 | 33-frontend-integration.md |
| TC-FEINT-011 | 前端创建团队失败显示错误 | 33-frontend-integration.md |
| TC-FEINT-012 | 前端创建私有团队调用后端 API | 33-frontend-integration.md |
| TC-FEINT-032 | 前端登录失败显示错误 | 33-frontend-integration.md |
| TC-FEINT-041 | 前端编辑团队信息调用后端 API | 33-frontend-integration.md |
| TC-FEINT-050 | 前端删除帖子调用后端 API | 33-frontend-integration.md |

---

## P2 完整功能（149 条）

> 提升用户体验，但不阻塞核心流程

### 筛选搜索（12 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-BROWSE-010 | 按标签筛选帖子 | 18-content-browsing.md |
| TC-BROWSE-011 | 按内容类型筛选帖子 | 18-content-browsing.md |
| TC-BROWSE-012 | 关键词搜索内容 | 18-content-browsing.md |
| TC-BROWSE-013 | 组合筛选条件 | 18-content-browsing.md |
| TC-BROWSE-041 | 点击帮助支持入口 | 18-content-browsing.md |
| TC-PLANET-002 | 按进行中状态筛选活动 | 29-planet-camp.md |
| TC-PLANET-003 | 按已结束状态筛选活动 | 29-planet-camp.md |
| TC-PLANET-005 | 按活动类型筛选 | 29-planet-camp.md |
| TC-PLANET-006 | 按时间范围筛选活动 | 29-planet-camp.md |
| TC-PLANET-007 | 组合多条件筛选活动 | 29-planet-camp.md |
| TC-CAMP-011 | 查看团队提案列表 | 29-planet-camp.md |
| TC-REL-CP-003 | 按 relation_type 筛选活动帖子 | 08-relations.md |

### 报名表单配置（6 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-CATMGMT-050 | 组织者配置报名表单字段 | 21-category-management.md |
| TC-CATMGMT-051 | 配置必填与选填字段 | 21-category-management.md |
| TC-CATMGMT-052 | 配置字段类型 | 21-category-management.md |
| TC-CATMGMT-053 | 报名时用户填写自定义字段 | 21-category-management.md |
| TC-CATMGMT-054 | 预览报名表单 | 21-category-management.md |
| TC-PART-023 | 资源关联指定显示方式 | 23-activity-participation.md |

### 个性化设置（14 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-PERSONAL-010 | 更改头像 — 上传图片 | 28-personalization.md |
| TC-PERSONAL-011 | 更改头像 — 选择预设 | 28-personalization.md |
| TC-PERSONAL-030 | 填写职业信息 | 28-personalization.md |
| TC-PERSONAL-031 | 填写学校信息 | 28-personalization.md |
| TC-PERSONAL-032 | 填写性格标签 | 28-personalization.md |
| TC-PERSONAL-033 | 填写兴趣爱好 | 28-personalization.md |
| TC-PERSONAL-034 | 活动收集信息自动展示 | 28-personalization.md |
| TC-PERSONAL-040 | 添加社交媒体链接 | 28-personalization.md |
| TC-PERSONAL-041 | 更新社交媒体链接 | 28-personalization.md |
| TC-PERSONAL-042 | 删除社交媒体链接 | 28-personalization.md |
| TC-PERSONAL-043 | 点击社交媒体链接跳转 | 28-personalization.md |
| TC-PROFILE-020 | 添加社交媒体链接 | 19-auth-profile.md |
| TC-PROFILE-021 | 更新社交媒体链接 | 19-auth-profile.md |
| TC-PROFILE-022 | 删除社交媒体链接 | 19-auth-profile.md |

### 隐私可见性（10 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-PERSONAL-050 | 活动收集信息聚合到个人主页 | 28-personalization.md |
| TC-PERSONAL-051 | 设置单项信息为公开可见 | 28-personalization.md |
| TC-PERSONAL-052 | 设置单项信息为仅自己可见 | 28-personalization.md |
| TC-PERSONAL-053 | 批量设置信息可见性 | 28-personalization.md |
| TC-PERSONAL-054 | 新收集信息的默认可见性 | 28-personalization.md |
| TC-PERSONAL-055 | 团队主页聚合成员公开信息 | 28-personalization.md |
| TC-PERSONAL-056 | 访客只能查看公开信息 | 28-personalization.md |
| TC-POST-071 | private 帖子跳过 pending_review 直接发布 | 05-post.md |
| TC-POST-073 | 将 public 帖子改为 private | 05-post.md |
| TC-POST-074 | 将 private 帖子改为 public | 05-post.md |

### 通知操作（10 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-NOTIF-013 | 活动状态变更通知跳转 | 20-notification.md |
| TC-NOTIF-020 | 在通知中心批准团队申请 | 20-notification.md |
| TC-NOTIF-021 | 在通知中心拒绝团队申请 | 20-notification.md |
| TC-NOTIF-022 | 在通知中心接受团队邀请 | 20-notification.md |
| TC-NOTIF-023 | 在通知中心拒绝团队邀请 | 20-notification.md |
| TC-NOTIF-033 | 接收系统公告通知 | 20-notification.md |
| TC-SOCIAL-012 | 删除评论 | 25-social-interaction.md |
| TC-SOCIAL-021 | 查看评分详情 | 25-social-interaction.md |
| TC-SOCIAL-050 | 分享活动 | 25-social-interaction.md |
| TC-SOCIAL-051 | 分享帖子 | 25-social-interaction.md |

### 版本协作（10 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-POST-041 | 发布新版本 | 05-post.md |
| TC-CREATE-002 | 同步 ELF 内容创建资产 | 24-content-creation.md |
| TC-CREATE-043 | 在提案内创建并关联新资产 | 24-content-creation.md |
| TC-CREATE-051 | 编辑提案产生新版本 | 24-content-creation.md |
| TC-CREATE-052 | 查看历史版本 | 24-content-creation.md |
| TC-CREATE-060 | 请求协作编辑他人帖子 | 24-content-creation.md |
| TC-CREATE-061 | 接受协作编辑请求 | 24-content-creation.md |
| TC-CREATE-062 | 协作者创建编辑副本 | 24-content-creation.md |
| TC-JOUR-011-2 | 编辑他人帖子（副本机制） | 11-user-journeys.md |
| TC-TEAM-013 | 申请复制他人资产 | 22-team-management.md |

### 运营勋章投票（12 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-SETTLE-013 | 分享证书成就 | 26-settlement-reward.md |
| TC-SETTLE-020 | 下载官方资料 | 26-settlement-reward.md |
| TC-SETTLE-021 | 下载他人公开分享资源 | 26-settlement-reward.md |
| TC-SETTLE-030 | 完成运营活动获得资产奖励 | 26-settlement-reward.md |
| TC-SETTLE-031 | 运营活动与比赛活动绑定 | 26-settlement-reward.md |
| TC-SETTLE-040 | 获得勋章资产 | 26-settlement-reward.md |
| TC-SETTLE-041 | 使用勋章投票 | 26-settlement-reward.md |
| TC-SETTLE-042 | 投票活动开启 | 26-settlement-reward.md |
| TC-SETTLE-043 | 勋章限制投票生效 | 26-settlement-reward.md |
| TC-SOCIAL-052 | 分享通知 | 25-social-interaction.md |
| TC-TRANSFER-001 | 证书资源从组织者帖子转移到参赛帖 | 12-resource-transfer.md |
| TC-TRANSFER-003 | 资源同时关联多个 post（共享模式） | 12-resource-transfer.md |

### 关系管理（15 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-REL-CR-002 | 更新 category:rule priority | 08-relations.md |
| TC-REL-CR-003 | 删除 category:rule 关系 | 08-relations.md |
| TC-REL-CP-002 | 将帖子关联为活动的 reference | 08-relations.md |
| TC-REL-CP-004 | 不带筛选读取所有 category:post | 08-relations.md |
| TC-REL-CG-002 | 读取活动已报名团队列表 | 08-relations.md |
| TC-REL-CG-003 | 团队取消报名 | 08-relations.md |
| TC-REL-PP-001 | 创建 embed 关系（嵌入团队卡片） | 08-relations.md |
| TC-REL-PP-002 | 创建 reference 关系（引用另一帖子） | 08-relations.md |
| TC-REL-PP-003 | 创建 reply 关系（帖子回复） | 08-relations.md |
| TC-REL-PP-004 | 更新 post:post 关系类型和位置 | 08-relations.md |
| TC-REL-PP-005 | 删除 post:post 关系 | 08-relations.md |
| TC-REL-PR-002 | 资源作为 inline 挂到帖子 | 08-relations.md |
| TC-REL-PR-003 | 同一帖子挂多个资源，position 排序 | 08-relations.md |
| TC-REL-PR-004 | 更新 post:resource display_type | 08-relations.md |
| TC-REL-PR-005 | 删除 post:resource 关系 | 08-relations.md |

### 规则引擎高级（16 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-ENGINE-003 | count 条件 — 计数满足 | 17-rule-engine.md |
| TC-ENGINE-004 | count 条件 — 计数不满足 | 17-rule-engine.md |
| TC-ENGINE-007 | exists 条件 — require=false 时实体不存在通过 | 17-rule-engine.md |
| TC-ENGINE-008 | field_match 条件 — 字段匹配 | 17-rule-engine.md |
| TC-ENGINE-009 | resource_format 条件 — 格式匹配 | 17-rule-engine.md |
| TC-ENGINE-010 | resource_required 条件 — 数量和格式均满足 | 17-rule-engine.md |
| TC-ENGINE-011 | aggregate 条件 — 聚合计算满足 | 17-rule-engine.md |
| TC-ENGINE-021 | 固定字段展开的 check 排在自定义 checks 之前 | 17-rule-engine.md |
| TC-ENGINE-022 | 纯 checks 定义（无固定字段） | 17-rule-engine.md |
| TC-ENGINE-031 | 多 Rule 中一条有 checks 一条只有固定字段 | 17-rule-engine.md |
| TC-ENGINE-040 | post phase check 在操作成功后执行 | 17-rule-engine.md |
| TC-ENGINE-041 | post phase check 条件不满足时 action 不执行 | 17-rule-engine.md |
| TC-ENGINE-050 | on_fail=deny 时操作被拒绝 | 17-rule-engine.md |
| TC-ENGINE-051 | on_fail=warn 时操作允许但返回警告 | 17-rule-engine.md |
| TC-ENGINE-052 | on_fail=flag 时操作允许并标记 | 17-rule-engine.md |
| TC-ENGINE-060 | Rule 无固定字段且 checks 为空数组 | 17-rule-engine.md |

### 活动关闭校验（10 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-CLOSE-001 | 活动关闭前校验所有团队人数 | 16-closure-rules.md |
| TC-CLOSE-002 | 活动关闭前严格校验（deny 模式） | 16-closure-rules.md |
| TC-CLOSE-010 | 活动关闭后标记不合格团队 | 16-closure-rules.md |
| TC-CLOSE-011 | 活动关闭后标记不合格提案 | 16-closure-rules.md |
| TC-CLOSE-012 | 所有团队均合格时无标记 | 16-closure-rules.md |
| TC-CLOSE-021 | average_rating 相同时排名并列 | 16-closure-rules.md |
| TC-CLOSE-022 | 无评分的帖子不参与排名 | 16-closure-rules.md |
| TC-CLOSE-031 | 无排名结果时不颁发证书 | 16-closure-rules.md |
| TC-ENTRY-010 | 提交时帖子必须包含至少一个 resource | 15-entry-rules.md |
| TC-ENTRY-011 | 提交时帖子必须包含指定格式的 resource | 15-entry-rules.md |

### 其他完整功能（12 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-USER-011 | Admin 修改其他用户的角色 | 01-user.md |
| TC-GRP-011 | 变更审批设置 | 04-group.md |
| TC-GRP-012 | 变更可见性 | 04-group.md |
| TC-POST-050 | 添加标签（+tag 语法） | 05-post.md |
| TC-POST-051 | 移除标签（-tag 语法） | 05-post.md |
| TC-POST-052 | "选择已有帖子"报名（标签打标） | 05-post.md |
| TC-POST-075 | private 帖子的 interaction 对非作者不可见 | 05-post.md |
| TC-POST-076 | 默认 visibility 为 public | 05-post.md |
| TC-IACT-051 | 修改评分重新打分 | 07-interaction.md |
| TC-IACT-062 | 对 resource（资源）点赞 | 07-interaction.md |
| TC-IACT-063 | 对 resource 发表评论 | 07-interaction.md |
| TC-CAMP-020 | 筛选个人提案 | 29-planet-camp.md |

### 提案迭代进阶（6 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-PROPOSAL-003 | 保存资产同步更新关联资产 | 30-proposal-iteration.md |
| TC-PROPOSAL-011 | 系统自动生成迭代日志 | 30-proposal-iteration.md |
| TC-PROPOSAL-012 | 迭代日志不可被用户更改 | 30-proposal-iteration.md |
| TC-PROPOSAL-013 | 迭代日志展示在提案页面 | 30-proposal-iteration.md |
| TC-PROPOSAL-020 | 查看任意两个版本的差异 | 30-proposal-iteration.md |
| TC-PROPOSAL-021 | 查看单个版本的完整快照 | 30-proposal-iteration.md |

### 页面交互进阶（5 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-PAGEUI-003 | 搜索历史记录 | 31-page-interaction.md |
| TC-PAGEUI-004 | 清除搜索历史 | 31-page-interaction.md |
| TC-PAGEUI-020 | 右侧栏常态显示日历 | 31-page-interaction.md |
| TC-PAGEUI-021 | 右侧栏常态显示热度榜 | 31-page-interaction.md |
| TC-PAGEUI-024 | 多功能栏状态可切换 | 31-page-interaction.md |

### 资产副本属性（3 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-ASSETCOPY-010 | 副本与原资产独立 | 32-asset-copy-request.md |
| TC-ASSETCOPY-011 | 副本可关联到其他提案 | 32-asset-copy-request.md |
| TC-ASSETCOPY-012 | 副本保留来源溯源 | 32-asset-copy-request.md |

### 赛道类型标识（2 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-CATTRACK-010 | 常规赛道（X类型）标识展示 | 14-category-association.md |
| TC-CATTRACK-011 | 命题赛道（Y类型）标识展示 | 14-category-association.md |

### 前端集成 P2（3 条）⭐ 新增

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-FEINT-020 | 前端创建活动调用后端 API | 33-frontend-integration.md |
| TC-FEINT-021 | 非组织者无法访问活动创建页 | 33-frontend-integration.md |
| TC-FEINT-051 | 前端删除团队调用后端 API | 33-frontend-integration.md |

### 提案可见性扩展（2 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-VISIBLE-005 | 评委可查看分配给自己的提案 | 27-bounty-enterprise.md |
| TC-VISIBLE-006 | 活动结束后提案可见性变更 | 27-bounty-enterprise.md |

---

## P3 高级场景（69 条）

> 特定场景或边缘用例，可后期迭代

### 悬赏企业活动（25 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-BOUNTY-001 | 发布悬赏活动 | 27-bounty-enterprise.md |
| TC-BOUNTY-002 | 承接悬赏 | 27-bounty-enterprise.md |
| TC-BOUNTY-003 | 悬赏活动提案互不可见 | 27-bounty-enterprise.md |
| TC-BOUNTY-010 | 创建第一阶段悬赏活动 | 27-bounty-enterprise.md |
| TC-BOUNTY-011 | 第一阶段结束选择优秀提案 | 27-bounty-enterprise.md |
| TC-BOUNTY-012 | 创建第二阶段关联活动 | 27-bounty-enterprise.md |
| TC-BOUNTY-013 | 晋级用户自动加入新团队 | 27-bounty-enterprise.md |
| TC-BOUNTY-014 | 悬赏方共享详细需求 | 27-bounty-enterprise.md |
| TC-BOUNTY-015 | 最终确认成果发放奖励 | 27-bounty-enterprise.md |
| TC-BOUNTY-016 | 发放阶段性奖励资源 | 27-bounty-enterprise.md |
| TC-BOUNTY-017 | 团队成员基于详细需求工作 | 27-bounty-enterprise.md |
| TC-ENTERPRISE-001 | 发布企业出题活动 | 27-bounty-enterprise.md |
| TC-ENTERPRISE-002 | 企业出题提案互不可见 | 27-bounty-enterprise.md |
| TC-ENTERPRISE-010 | 创建第一阶段企业出题活动 | 27-bounty-enterprise.md |
| TC-ENTERPRISE-011 | 第一阶段评审选出优秀提案 | 27-bounty-enterprise.md |
| TC-ENTERPRISE-012 | 创建第二阶段关联活动 | 27-bounty-enterprise.md |
| TC-ENTERPRISE-013 | 企业方发送进阶信息到用户资产 | 27-bounty-enterprise.md |
| TC-ENTERPRISE-014 | 后续阶段确认需求与成果 | 27-bounty-enterprise.md |
| TC-VISIBLE-001 | 悬赏活动中参赛者提案对其他参赛者不可见 | 27-bounty-enterprise.md |
| TC-VISIBLE-002 | 企业出题活动中参赛者提案对其他参赛者不可见 | 27-bounty-enterprise.md |
| TC-VISIBLE-003 | 悬赏方可查看所有提案 | 27-bounty-enterprise.md |
| TC-VISIBLE-004 | 企业方可查看所有提案 | 27-bounty-enterprise.md |
| TC-CATMGMT-042 | 一个提案参加多个关联活动 | 21-category-management.md |
| TC-PLANET-004 | 按关联活动筛选 | 29-planet-camp.md |
| TC-CAMP-021 | 筛选团队提案 | 29-planet-camp.md |

### 活动关联（20 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-STAGE-001 | 创建连续赛段关联 | 14-category-association.md |
| TC-STAGE-002 | 按 stage_order 排序读取赛段 | 14-category-association.md |
| TC-STAGE-003 | 赛段未完成时无法进入下一赛段 | 14-category-association.md |
| TC-STAGE-004 | 赛段完成后可进入下一赛段 | 14-category-association.md |
| TC-TRACK-001 | 创建并行赛道关联 | 14-category-association.md |
| TC-TRACK-002 | 团队可同时参加不同赛道 | 14-category-association.md |
| TC-TRACK-003 | 团队在同一赛道内受 Rule 约束 | 14-category-association.md |
| TC-PREREQ-001 | 悬赏活动作为前置条件关联到常规赛 | 14-category-association.md |
| TC-PREREQ-002 | 前置活动完成后团队可报名目标活动 | 14-category-association.md |
| TC-PREREQ-003 | 前置活动未完成时团队报名目标活动被拒绝 | 14-category-association.md |
| TC-PREREQ-004 | 前置活动中组建的团队保持完整进入目标活动 | 14-category-association.md |
| TC-CATREL-010 | 查看活动关联列表 | 14-category-association.md |
| TC-CATREL-011 | 从关联活动跳转 | 14-category-association.md |
| TC-CATREL-012 | 活动关联双向可见 | 14-category-association.md |
| TC-CATREL-020 | 提案在多个关联活动中独立评审 | 14-category-association.md |
| TC-CATREL-021 | 提案在多个活动中独立获奖 | 14-category-association.md |
| TC-ENTRY-003 | 报名前必须已有 profile 帖子 | 15-entry-rules.md |
| TC-ENTRY-012 | 帖子包含符合要求的 resource 时提交成功 | 15-entry-rules.md |
| TC-ENTRY-022 | 不同活动中同一用户可分别提交提案 | 15-entry-rules.md |
| TC-ENTRY-030 | 固定字段和自定义 checks 同时生效（AND 逻辑） | 15-entry-rules.md |

### 用户关系（6 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-FRIEND-003 | 单向关注不构成好友 | 13-user-follow.md |
| TC-FRIEND-005 | 拉黑用户 | 13-user-follow.md |
| TC-FRIEND-006 | 被拉黑用户无法关注 | 13-user-follow.md |
| TC-FRIEND-007 | 删除用户后级联解除 user:user | 13-user-follow.md |
| TC-REL-TI-001 | 创建 target_interaction 关系 | 08-relations.md |
| TC-REL-TI-002 | 删除 target:interaction 关系 | 08-relations.md |

### 资源可见性（8 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-RES-041 | 关联到 draft 帖子的 resource 对非作者不可读 | 06-resource.md |
| TC-RES-042 | 关联到 private 帖子的 resource 对非作者不可读 | 06-resource.md |
| TC-RES-043 | 帖子从 public 改为 private 后，关联 resource 不可见性同步变更 | 06-resource.md |
| TC-RES-044 | resource 同时关联到 public 和 private 帖子时的可见性 | 06-resource.md |
| TC-RES-045 | 帖子删除后 resource 的可访问性 | 06-resource.md |
| TC-TRANSFER-002 | 提案间文件转移 | 12-resource-transfer.md |
| TC-TRANSFER-004 | 转移溯源 | 12-resource-transfer.md |
| TC-CAMP-022 | 筛选团队 | 29-planet-camp.md |

### 其他高级场景（10 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-USER-020 | 删除用户及级联影响 | 01-user.md |
| TC-CAT-020 | 删除活动及级联影响 | 02-category.md |
| TC-RULE-020 | 删除规则及级联 | 03-rule.md |
| TC-GRP-020 | 删除团队及级联 | 04-group.md |
| TC-RES-031 | 删除资源后级联解除 post:resource | 06-resource.md |
| TC-DEL-002 | 删除 rule | 09-cascade-delete.md |
| TC-DEL-005 | 删除 interaction | 09-cascade-delete.md |
| TC-DEL-011 | 删除 user → interaction + group:user 级联处理 | 09-cascade-delete.md |
| TC-DEL-013 | 删除 rule → 级联 category:rule | 09-cascade-delete.md |
| TC-DEL-014 | 删除 group → 级联 category:group | 09-cascade-delete.md |

---

## P4 负向测试（114 条）

> 异常和边界情况，建议与对应正向用例同步测试

### 用户与认证（9 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-USER-900 | 重复 username 被拒绝 | 01-user.md |
| TC-USER-901 | 重复 email 被拒绝 | 01-user.md |
| TC-USER-902 | 非本人/非 Admin 修改用户信息被拒绝 | 01-user.md |
| TC-USER-903 | 缺少必填字段 email | 01-user.md |
| TC-AUTH-900 | 重复手机号注册被拒绝 | 19-auth-profile.md |
| TC-AUTH-902 | 密码格式不符被拒绝 | 19-auth-profile.md |
| TC-AUTH-903 | 验证码过期被拒绝 | 19-auth-profile.md |
| TC-AUTH-904 | 错误密码登录被拒绝 | 19-auth-profile.md |
| TC-AUTH-905 | 不存在的账号登录被拒绝 | 19-auth-profile.md |

### 活动与规则（10 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-CAT-900 | 非法 type 枚举被拒绝 | 02-category.md |
| TC-CAT-901 | 非法 status 枚举被拒绝 | 02-category.md |
| TC-CAT-902 | participant 创建活动被拒绝 | 02-category.md |
| TC-RULE-900 | participant 创建规则被拒绝 | 03-rule.md |
| TC-RULE-901 | scoring_criteria 权重总和不等于 100 | 03-rule.md |
| TC-CATMGMT-901 | closed 状态活动不可修改 | 21-category-management.md |
| TC-CATMGMT-903 | 活动结束时间早于开始时间被拒绝 | 21-category-management.md |
| TC-CATMGMT-904 | 报名时必填字段缺失被拒绝 | 21-category-management.md |
| TC-ENGINE-042 | post phase check 失败不回滚主操作 | 17-rule-engine.md |
| TC-ENGINE-061 | 活动未关联任何 Rule | 17-rule-engine.md |

### 团队（6 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-GRP-900 | 非法 visibility 枚举被拒绝 | 04-group.md |
| TC-GRP-901 | 非 Owner/Admin 修改团队信息被拒绝 | 04-group.md |
| TC-TEAM-902 | 非 Owner 移除成员被拒绝 | 22-team-management.md |
| TC-TEAM-903 | Owner 无法退出团队 | 22-team-management.md |
| TC-REL-GU-900 | 已有成员重复加入被拒绝 | 08-relations.md |
| TC-REL-GU-901 | 创建 group_user 时使用非法 role 枚举 | 08-relations.md |

### 帖子与资源（12 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-POST-900 | 缺少 title 被拒绝 | 05-post.md |
| TC-POST-901 | 非法 type/status 枚举被拒绝 | 05-post.md |
| TC-POST-902 | 未登录用户创建帖子被拒绝 | 05-post.md |
| TC-POST-903 | 非法 visibility 枚举被拒绝 | 05-post.md |
| TC-RES-900 | 缺少 filename 被拒绝 | 06-resource.md |
| TC-RES-901 | 未登录用户创建资源被拒绝 | 06-resource.md |
| TC-RES-902 | 引用不存在的 post_id/resource_id 创建关系被拒绝 | 06-resource.md |
| TC-RES-903 | 非法 display_type 枚举被拒绝 | 06-resource.md |
| TC-CREATE-900 | 非本人编辑帖子被拒绝 | 24-content-creation.md |
| TC-CREATE-901 | 已删除内容无法编辑 | 24-content-creation.md |
| TC-CREATE-903 | 缺少必填字段被拒绝 | 24-content-creation.md |
| TC-CREATE-071 | 删除评论 | 24-content-creation.md |

### 互动（8 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-IACT-002 | 重复点赞被拒绝 | 07-interaction.md |
| TC-IACT-900 | 非法 interaction type 被拒绝 | 07-interaction.md |
| TC-IACT-901 | 非法 target_type 被拒绝 | 07-interaction.md |
| TC-IACT-902 | target_id 不存在被拒绝 | 07-interaction.md |
| TC-IACT-903 | 对已删除的帖子点赞被拒绝 | 07-interaction.md |
| TC-IACT-904 | 缺少 target_id 被拒绝 | 07-interaction.md |
| TC-IACT-905 | 非本人修改 interaction 被拒绝 | 07-interaction.md |
| TC-CREATE-072 | 删除资源 | 24-content-creation.md |

### 关系（14 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-REL-CR-900 | 重复关联同一规则到同一活动被拒绝 | 08-relations.md |
| TC-REL-CP-900 | 规则截止后提交 category_post 被拒绝 | 08-relations.md |
| TC-REL-CP-901 | 格式不符时提交 category_post 被拒绝 | 08-relations.md |
| TC-REL-CP-902 | 超出 max_submissions 时提交 category_post 被拒绝 | 08-relations.md |
| TC-REL-CG-900 | 重复报名同一活动被拒绝 | 08-relations.md |
| TC-REL-CG-901 | 同一用户在同一活动中属于多个团队被拒绝 | 08-relations.md |
| TC-REL-GU-902 | 团队已满时加入被拒绝（Rule Enforcement） | 08-relations.md |
| TC-CATREL-900 | 重复创建同一活动关联被拒绝 | 14-category-association.md |
| TC-CATREL-901 | 自引用被拒绝 | 14-category-association.md |
| TC-CATREL-902 | 赛段循环依赖被拒绝 | 14-category-association.md |
| TC-CATREL-903 | 非法 relation_type 被拒绝 | 14-category-association.md |
| TC-CATREL-904 | 已关闭活动无法添加关联 | 14-category-association.md |
| TC-CATREL-905 | 非关联活动无法共享提案 | 14-category-association.md |
| TC-ENTRY-031 | 固定字段和自定义 checks 均满足时操作成功 | 15-entry-rules.md |

### 权限（12 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-PERM-001 | participant 创建 category 被拒绝 | 10-permissions.md |
| TC-PERM-002 | participant 创建 rule 被拒绝 | 10-permissions.md |
| TC-PERM-003 | participant 更新 category 被拒绝 | 10-permissions.md |
| TC-PERM-012 | 非本人修改用户信息被拒绝 | 10-permissions.md |
| TC-PERM-013 | 非 Owner 修改团队信息被拒绝 | 10-permissions.md |
| TC-PERM-014 | 非本人修改评论被拒绝 | 10-permissions.md |
| TC-PERM-020 | 访客读取 draft 帖子不可见 | 10-permissions.md |
| TC-PERM-021 | 访客读取 draft 活动不可见 | 10-permissions.md |
| TC-PERM-022 | 非成员读取 private 团队不可见 | 10-permissions.md |
| TC-PERM-023 | 已发布活动下的 draft 帖子在列表中不可见 | 10-permissions.md |
| TC-PERM-024 | 已发布活动下的 private 帖子在列表中不可见 | 10-permissions.md |
| TC-PERM-025 | private 帖子的关联 resource 在活动资源列表中不可见 | 10-permissions.md |

### 级联删除（3 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-DEL-021 | 已删除记录不可恢复 | 09-cascade-delete.md |
| TC-DEL-022 | 已删除记录无法被更新 | 09-cascade-delete.md |
| TC-ENTRY-900 | checks 中引用不存在的 condition type 被拒绝 | 15-entry-rules.md |

### 活动关闭（6 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-CLOSE-900 | 非 closed 状态变更不触发关闭 checks | 16-closure-rules.md |
| TC-CLOSE-901 | 活动无关联 Rule 时关闭不触发任何 check | 16-closure-rules.md |
| TC-CLOSE-902 | post phase action 失败不回滚活动关闭 | 16-closure-rules.md |
| TC-ENTRY-901 | checks 缺少必填字段被拒绝 | 15-entry-rules.md |
| TC-ENTRY-902 | pre 阶段 check 缺少 condition 被拒绝 | 15-entry-rules.md |
| TC-SETTLE-900 | 活动未关闭时无法查看最终排名 | 26-settlement-reward.md |

### 浏览与通知（6 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-BROWSE-900 | 访问不存在的内容返回 404 | 18-content-browsing.md |
| TC-BROWSE-901 | 访问已删除内容返回 404 | 18-content-browsing.md |
| TC-NOTIF-900 | 访问不存在的通知返回错误 | 20-notification.md |
| TC-NOTIF-901 | 非本人通知不可操作 | 20-notification.md |
| TC-PLANET-900 | 未登录用户访问营地页面 | 29-planet-camp.md |
| TC-PLANET-901 | 无任何提案时营地页面展示空状态 | 29-planet-camp.md |

### 社交与结算（9 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-FRIEND-900 | 自己关注自己被拒绝 | 13-user-follow.md |
| TC-FRIEND-901 | 重复关注被拒绝 | 13-user-follow.md |
| TC-FRIEND-902 | 非法 relation_type 被拒绝 | 13-user-follow.md |
| TC-SOCIAL-903 | 非本人删除评论被拒绝 | 25-social-interaction.md |
| TC-SOCIAL-905 | 评分权重不符规则被拒绝 | 25-social-interaction.md |
| TC-SETTLE-901 | 非获奖者无法领取证书 | 26-settlement-reward.md |
| TC-SETTLE-902 | 无效勋章投票被拒绝 | 26-settlement-reward.md |
| TC-SETTLE-903 | 重复投票被拒绝 | 26-settlement-reward.md |
| TC-PLANET-902 | 无任何团队时营地页面展示空状态 | 29-planet-camp.md |

### 悬赏企业（7 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-BOUNTY-901 | 非悬赏方无法选择晋级提案 | 27-bounty-enterprise.md |
| TC-BOUNTY-902 | 第一阶段未关闭无法选择晋级 | 27-bounty-enterprise.md |
| TC-ENTERPRISE-900 | 非企业方无法发送资产到用户 | 27-bounty-enterprise.md |
| TC-ENTERPRISE-901 | 参赛者尝试查看其他参赛者提案被拒绝 | 27-bounty-enterprise.md |
| TC-PERSONAL-900 | 头像格式不支持被拒绝 | 28-personalization.md |
| TC-PERSONAL-901 | 头像尺寸过大被拒绝 | 28-personalization.md |
| TC-PERSONAL-902 | 社交媒体链接格式无效被拒绝 | 28-personalization.md |

### 报名参与（3 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-PART-900 | 未加入团队时个人报名被拒绝 | 23-activity-participation.md |
| TC-PART-903 | 未登录用户报名被拒绝 | 23-activity-participation.md |
| TC-PERSONAL-903 | 未授权信息不展示在主页 | 28-personalization.md |

### 提案迭代（3 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-PROPOSAL-900 | 未保存直接关闭编辑器 | 30-proposal-iteration.md |
| TC-PROPOSAL-901 | 空更新发布被提示 | 30-proposal-iteration.md |
| TC-PROPOSAL-902 | 已删除提案无法查看版本历史 | 30-proposal-iteration.md |

### 页面交互（2 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-PAGEUI-900 | 未登录用户无法访问资产页面 | 31-page-interaction.md |
| TC-PAGEUI-901 | 搜索无结果展示空状态 | 31-page-interaction.md |

### 资产复制申请（4 条）

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-ASSETCOPY-900 | 重复申请被拒绝 | 32-asset-copy-request.md |
| TC-ASSETCOPY-901 | 自己资产无法申请复制 | 32-asset-copy-request.md |
| TC-ASSETCOPY-902 | 已删除资产无法申请复制 | 32-asset-copy-request.md |
| TC-ASSETCOPY-903 | 非团队成员无法申请团队提案内资产 | 32-asset-copy-request.md |

### 前端集成 P4（3 条）⭐ 新增

| TC ID | 描述 | 来源文件 |
|-------|------|----------|
| TC-FEINT-900 | 未登录用户创建帖子被拦截 | 33-frontend-integration.md |
| TC-FEINT-901 | API 客户端网络错误处理 | 33-frontend-integration.md |
| TC-FEINT-902 | 重复提交防护 | 33-frontend-integration.md |

---

## 附录：按文件统计

| 文件 | P0 | P1 | P2 | P3 | P4 | 总计 |
|------|----|----|----|----|-----|------|
| 01-user.md | 4 | 1 | 1 | 1 | 4 | 11 |
| 02-category.md | 4 | 1 | 0 | 1 | 3 | 9 |
| 03-rule.md | 9 | 5 | 0 | 1 | 2 | 17 |
| 04-group.md | 5 | 5 | 2 | 0 | 2 | 14 |
| 05-post.md | 6 | 8 | 6 | 0 | 4 | 24 |
| 06-resource.md | 1 | 3 | 0 | 5 | 4 | 13 |
| 07-interaction.md | 6 | 5 | 3 | 0 | 7 | 21 |
| 08-relations.md | 3 | 1 | 14 | 2 | 11 | 31 |
| 09-cascade-delete.md | 0 | 7 | 0 | 5 | 2 | 14 |
| 10-permissions.md | 0 | 0 | 0 | 0 | 12 | 12 |
| 11-user-journeys.md | 1 | 6 | 1 | 0 | 0 | 8 |
| 12-resource-transfer.md | 0 | 0 | 2 | 2 | 0 | 4 |
| 13-user-follow.md | 0 | 3 | 0 | 4 | 3 | 10 |
| 14-category-association.md | 0 | 0 | 2 | 16 | 6 | 24 |
| 15-entry-rules.md | 5 | 0 | 3 | 3 | 4 | 15 |
| 16-closure-rules.md | 0 | 4 | 6 | 0 | 3 | 13 |
| 17-rule-engine.md | 0 | 6 | 14 | 0 | 3 | 23 |
| 18-content-browsing.md | 4 | 8 | 5 | 0 | 2 | 19 |
| 19-auth-profile.md | 12 | 9 | 3 | 0 | 5 | 29 |
| 20-notification.md | 0 | 10 | 6 | 0 | 2 | 18 |
| 21-category-management.md | 13 | 5 | 5 | 1 | 3 | 27 |
| 22-team-management.md | 5 | 8 | 1 | 0 | 2 | 16 |
| 23-activity-participation.md | 10 | 0 | 1 | 0 | 2 | 13 |
| 24-content-creation.md | 7 | 4 | 7 | 0 | 5 | 23 |
| 25-social-interaction.md | 0 | 3 | 5 | 0 | 2 | 10 |
| 26-settlement-reward.md | 0 | 6 | 8 | 0 | 4 | 18 |
| 27-bounty-enterprise.md | 0 | 0 | 2 | 22 | 4 | 28 |
| 28-personalization.md | 0 | 2 | 17 | 0 | 4 | 23 |
| 29-planet-camp.md | 0 | 6 | 8 | 4 | 3 | 21 |
| 30-proposal-iteration.md | 0 | 3 | 6 | 0 | 3 | 12 |
| 31-page-interaction.md | 0 | 7 | 5 | 0 | 2 | 14 |
| 32-asset-copy-request.md | 0 | 6 | 3 | 0 | 4 | 13 |
| 33-frontend-integration.md ⭐ | 8 | 8 | 3 | 0 | 3 | 22 |
| **总计** | **97** | **143** | **148** | **69** | **117** | **574** |

---

*更新时间：2026-02-05*
*测试用例总数：574 条（含 22 条前端集成测试）*
