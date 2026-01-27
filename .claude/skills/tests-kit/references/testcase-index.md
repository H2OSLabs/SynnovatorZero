# Test Case Index

> Auto-generated index of all test cases in `specs/testcases/`.
> Grep pattern to find a TC by ID: `grep -rn "TC-XXX-NNN" specs/testcases/`

## 01-user.md (User)

| TC ID | Description |
|-------|-------------|
| TC-USER-001 | 创建 participant 用户 |
| TC-USER-002 | 创建 organizer 用户 |
| TC-USER-003 | 创建 admin 用户 |
| TC-USER-004 | 读取已创建的用户 |
| TC-USER-010 | 用户修改自己的个人信息 |
| TC-USER-011 | Admin 修改其他用户的角色 |
| TC-USER-020 | 删除用户及级联影响 |
| TC-USER-900 | 重复 username 被拒绝 |
| TC-USER-901 | 重复 email 被拒绝 |
| TC-USER-902 | 非本人/非 Admin 修改用户信息被拒绝 |
| TC-USER-903 | 缺少必填字段 email |

## 02-category.md (Category)

| TC ID | Description |
|-------|-------------|
| TC-CAT-001 | 创建 competition 类型活动 |
| TC-CAT-002 | 创建 operation 类型活动 |
| TC-CAT-003 | 读取已创建的活动 |
| TC-CAT-010 | 活动状态流转 draft → published → closed |
| TC-CAT-011 | 修改活动名称和描述 |
| TC-CAT-020 | 删除活动及级联影响 |
| TC-CAT-900 | 非法 type 枚举被拒绝 |
| TC-CAT-901 | 非法 status 枚举被拒绝 |
| TC-CAT-902 | participant 创建活动被拒绝 |

## 03-rule.md (Rule)

| TC ID | Description |
|-------|-------------|
| TC-RULE-001 | 创建含完整 scoring_criteria 的规则 |
| TC-RULE-002 | 创建 select-only 规则 |
| TC-RULE-003 | 读取已创建的规则 |
| TC-RULE-010 | 修改规则配置字段 |
| TC-RULE-011 | 修改 scoring_criteria 权重 |
| TC-RULE-020 | 删除规则及级联 |
| TC-RULE-100 | 提交截止后创建 category_post 被拒绝 |
| TC-RULE-101 | 提交未开始时创建 category_post 被拒绝 |
| TC-RULE-102 | 超出 max_submissions 后创建 category_post 被拒绝 |
| TC-RULE-103 | 提交格式不符时创建 category_post 被拒绝 |
| TC-RULE-104 | 团队人数不足时创建 category_post 被拒绝 |
| TC-RULE-105 | 团队已满时创建 group_user 被拒绝 |
| TC-RULE-106 | allow_public=false 时直接发布被拒绝 |
| TC-RULE-107 | allow_public=false 时 pending_review 状态被允许 |
| TC-RULE-108 | 无 rule 关联时 category_post 正常创建 |
| TC-RULE-109 | 多条 rule 全部满足才允许（AND 逻辑） |
| TC-RULE-900 | participant 创建规则被拒绝 |
| TC-RULE-901 | scoring_criteria 权重总和不等于 100 |

## 04-group.md (Group)

| TC ID | Description |
|-------|-------------|
| TC-GRP-001 | 创建需审批的公开团队 |
| TC-GRP-002 | 创建无需审批的私有团队 |
| TC-GRP-003 | Owner 自动加入 |
| TC-GRP-004 | 需审批团队 — 成员申请加入为 pending |
| TC-GRP-005 | Owner 批准成员申请 |
| TC-GRP-006 | Owner 拒绝成员申请 |
| TC-GRP-007 | 被拒绝后重新申请 |
| TC-GRP-008 | 无需审批团队 — 成员直接 accepted |
| TC-GRP-010 | Owner 更新团队信息 |
| TC-GRP-011 | 变更审批设置 |
| TC-GRP-012 | 变更可见性 |
| TC-GRP-020 | 删除团队及级联 |
| TC-GRP-900 | 非法 visibility 枚举被拒绝 |
| TC-GRP-901 | 非 Owner/Admin 修改团队信息被拒绝 |

## 05-post.md (Post)

| TC ID | Description |
|-------|-------------|
| TC-POST-001 | 最小字段创建帖子 |
| TC-POST-002 | 显式发布帖子 |
| TC-POST-003 | 带 tags 创建帖子 |
| TC-POST-004 | 按 type 筛选帖子 |
| TC-POST-010 | 创建 team 类型帖子 |
| TC-POST-011 | 创建 profile 类型帖子 |
| TC-POST-012 | 创建 for_category 类型帖子 |
| TC-POST-013 | 创建 certificate 类型帖子 |
| TC-POST-030 | 帖子进入 pending_review 状态 |
| TC-POST-031 | 帖子被审核通过 |
| TC-POST-032 | 帖子被驳回 |
| TC-POST-033 | 草稿发布 |
| TC-POST-040 | 通过新帖子实现版本管理 |
| TC-POST-041 | 发布新版本 |
| TC-POST-050 | 添加标签（+tag 语法） |
| TC-POST-051 | 移除标签（-tag 语法） |
| TC-POST-052 | "选择已有帖子"报名（标签打标） |
| TC-POST-060 | 更新帖子 title 和 Markdown body |
| TC-POST-070 | 创建 visibility=private 的帖子 |
| TC-POST-071 | private 帖子跳过 pending_review 直接发布 |
| TC-POST-072 | private 已发布帖子对非作者不可见 |
| TC-POST-073 | 将 public 帖子改为 private |
| TC-POST-074 | 将 private 帖子改为 public |
| TC-POST-075 | private 帖子的 interaction 对非作者不可见 |
| TC-POST-076 | 默认 visibility 为 public |
| TC-POST-900 | 缺少 title 被拒绝 |
| TC-POST-901 | 非法 type/status 枚举被拒绝 |
| TC-POST-902 | 未登录用户创建帖子被拒绝 |
| TC-POST-903 | 非法 visibility 枚举被拒绝 |

## 06-resource.md (Resource)

| TC ID | Description |
|-------|-------------|
| TC-RES-001 | 最小字段创建资源 |
| TC-RES-002 | 带完整元信息创建资源 |
| TC-RES-030 | 更新资源元信息 |
| TC-RES-031 | 删除资源后级联解除 post:resource |
| TC-RES-040 | 关联到 published + public 帖子的 resource 可被任何人读取 |
| TC-RES-041 | 关联到 draft 帖子的 resource 对非作者不可读 |
| TC-RES-042 | 关联到 private 帖子的 resource 对非作者不可读 |
| TC-RES-043 | 帖子从 public 改为 private 后 resource 不可见性同步变更 |
| TC-RES-044 | resource 同时关联到 public 和 private 帖子时的可见性 |
| TC-RES-045 | 帖子删除后 resource 的可访问性 |
| TC-RES-900 | 缺少 filename 被拒绝 |
| TC-RES-901 | 未登录用户创建资源被拒绝 |
| TC-RES-902 | 引用不存在的 post_id/resource_id 创建关系被拒绝 |
| TC-RES-903 | 非法 display_type 枚举被拒绝 |

## 07-interaction.md (Interaction)

| TC ID | Description |
|-------|-------------|
| TC-IACT-001 | 对帖子点赞 |
| TC-IACT-002 | 重复点赞被拒绝 |
| TC-IACT-003 | 取消点赞后 like_count 递减 |
| TC-IACT-010 | 创建顶层评论 |
| TC-IACT-011 | 创建嵌套回复（一级回复） |
| TC-IACT-012 | 创建二级回复 |
| TC-IACT-013 | comment_count 包含所有层级 |
| TC-IACT-014 | 删除父评论级联删除子回复 |
| TC-IACT-020 | 创建多维度评分 |
| TC-IACT-021 | 多个评分的均值计算 |
| TC-IACT-050 | 修改评论文本 |
| TC-IACT-051 | 修改评分重新打分 |
| TC-IACT-060 | 对 category 点赞 |
| TC-IACT-061 | 对 category 发表评论 |
| TC-IACT-062 | 对 resource 点赞 |
| TC-IACT-063 | 对 resource 发表评论 |
| TC-IACT-900 | 非法 interaction type 被拒绝 |
| TC-IACT-901 | 非法 target_type 被拒绝 |
| TC-IACT-902 | target_id 不存在被拒绝 |
| TC-IACT-903 | 对已删除的帖子点赞被拒绝 |
| TC-IACT-904 | 缺少 target_id 被拒绝 |
| TC-IACT-905 | 非本人修改 interaction 被拒绝 |

## 08-relations.md (Relations)

| TC ID | Description |
|-------|-------------|
| TC-REL-CR-001 | 将规则关联到活动 |
| TC-REL-CR-002 | 更新 category:rule priority |
| TC-REL-CR-003 | 删除 category:rule 关系 |
| TC-REL-CR-900 | 重复关联同一规则到同一活动被拒绝 |
| TC-REL-CP-001 | 将帖子关联为活动的 submission |
| TC-REL-CP-002 | 将帖子关联为活动的 reference |
| TC-REL-CP-003 | 按 relation_type 筛选活动帖子 |
| TC-REL-CP-004 | 不带筛选读取所有 category:post |
| TC-REL-CP-900 | 规则截止后提交 category_post 被拒绝 |
| TC-REL-CP-901 | 格式不符时提交 category_post 被拒绝 |
| TC-REL-CP-902 | 超出 max_submissions 时提交 category_post 被拒绝 |
| TC-REL-CG-001 | 团队报名活动 |
| TC-REL-CG-002 | 读取活动已报名团队列表 |
| TC-REL-CG-003 | 团队取消报名 |
| TC-REL-CG-900 | 重复报名同一活动被拒绝 |
| TC-REL-CG-901 | 同一用户在同一活动中属于多个团队被拒绝 |
| TC-REL-PP-001 | 创建 embed 关系 |
| TC-REL-PP-002 | 创建 reference 关系 |
| TC-REL-PP-003 | 创建 reply 关系 |
| TC-REL-PP-004 | 更新 post:post 关系类型和位置 |
| TC-REL-PP-005 | 删除 post:post 关系 |
| TC-REL-PR-001 | 资源作为 attachment 挂到帖子 |
| TC-REL-PR-002 | 资源作为 inline 挂到帖子 |
| TC-REL-PR-003 | 同一帖子挂多个资源 position 排序 |
| TC-REL-PR-004 | 更新 post:resource display_type |
| TC-REL-PR-005 | 删除 post:resource 关系 |
| TC-REL-GU-001 | 移出团队成员 |
| TC-REL-GU-900 | 已有成员重复加入被拒绝 |
| TC-REL-GU-901 | 创建 group_user 时使用非法 role 枚举 |
| TC-REL-GU-902 | 团队已满时加入被拒绝 |
| TC-REL-TI-001 | 创建 target_interaction 关系 |
| TC-REL-TI-002 | 删除 target:interaction 关系 |

## 09-cascade-delete.md (Cascade Delete)

| TC ID | Description |
|-------|-------------|
| TC-DEL-001 | 删除 category |
| TC-DEL-002 | 删除 rule |
| TC-DEL-003 | 删除 user |
| TC-DEL-004 | 删除 group |
| TC-DEL-005 | 删除 interaction |
| TC-DEL-010 | 删除 category → 关联 interaction 级联硬删除 |
| TC-DEL-011 | 删除 user → interaction + group:user 级联处理 |
| TC-DEL-012 | 删除 post → 完整级联链 |
| TC-DEL-013 | 删除 rule → 级联 category:rule |
| TC-DEL-014 | 删除 group → 级联 category:group |
| TC-DEL-015 | 删除父评论 → 级联删除所有子评论 |
| TC-DEL-020 | 读取已删除记录返回 not found |
| TC-DEL-021 | 已删除记录不可恢复 |
| TC-DEL-022 | 已删除记录无法被更新 |

## 10-permissions.md (Permissions)

| TC ID | Description |
|-------|-------------|
| TC-PERM-001 | participant 创建 category 被拒绝 |
| TC-PERM-002 | participant 创建 rule 被拒绝 |
| TC-PERM-003 | participant 更新 category 被拒绝 |
| TC-PERM-012 | 非本人修改用户信息被拒绝 |
| TC-PERM-013 | 非 Owner 修改团队信息被拒绝 |
| TC-PERM-014 | 非本人修改评论被拒绝 |
| TC-PERM-020 | 访客读取 draft 帖子不可见 |
| TC-PERM-021 | 访客读取 draft 活动不可见 |
| TC-PERM-022 | 非成员读取 private 团队不可见 |
| TC-PERM-023 | 已发布活动下的 draft 帖子在列表中不可见 |
| TC-PERM-024 | 已发布活动下的 private 帖子在列表中不可见 |
| TC-PERM-025 | private 帖子的关联 resource 在活动资源列表中不可见 |

## 11-user-journeys.md (User Journeys)

| TC ID | Description |
|-------|-------------|
| TC-JOUR-002 | 匿名访客浏览公开内容 |
| TC-JOUR-005 | 完整团队加入与审批流程 |
| TC-JOUR-007 | 完整团队报名流程 |
| TC-JOUR-009 | 创建日常帖子和参赛提案 |
| TC-JOUR-010 | 完整证书颁发流程 |
| TC-JOUR-011-1 | 编辑自己的帖子（版本管理） |
| TC-JOUR-011-2 | 编辑他人帖子（副本机制） |
| TC-JOUR-012 | 删除帖子后验证全部级联 |
| TC-JOUR-013 | 完整社区互动流程 |

## 12-resource-transfer.md (Resource Transfer)

| TC ID | Description |
|-------|-------------|
| TC-TRANSFER-001 | 证书资源从组织者帖子转移到参赛帖 |
| TC-TRANSFER-002 | 提案间文件转移 |
| TC-TRANSFER-003 | 资源同时关联多个 post（共享模式） |
| TC-TRANSFER-004 | 转移溯源 |

## 13-user-follow.md (User Follow)

| TC ID | Description |
|-------|-------------|
| TC-FRIEND-001 | 用户 A 关注用户 B |
| TC-FRIEND-002 | 用户 B 回关用户 A 成为好友 |
| TC-FRIEND-003 | 单向关注不构成好友 |
| TC-FRIEND-004 | 取消关注 |
| TC-FRIEND-005 | 拉黑用户 |
| TC-FRIEND-006 | 被拉黑用户无法关注 |
| TC-FRIEND-007 | 删除用户后级联解除 user:user |
| TC-FRIEND-900 | 自己关注自己被拒绝 |
| TC-FRIEND-901 | 重复关注被拒绝 |
| TC-FRIEND-902 | 非法 relation_type 被拒绝 |

## 14-category-association.md (Category Association)

| TC ID | Description |
|-------|-------------|
| TC-STAGE-001 | 创建连续赛段关联 |
| TC-STAGE-002 | 按 stage_order 排序读取赛段 |
| TC-STAGE-003 | 赛段未完成时无法进入下一赛段 |
| TC-STAGE-004 | 赛段完成后可进入下一赛段 |
| TC-TRACK-001 | 创建并行赛道关联 |
| TC-TRACK-002 | 团队可同时参加不同赛道 |
| TC-TRACK-003 | 团队在同一赛道内受 Rule 约束 |
| TC-PREREQ-001 | 悬赏活动作为前置条件关联到常规赛 |
| TC-PREREQ-002 | 前置活动完成后团队可报名目标活动 |
| TC-PREREQ-003 | 前置活动未完成时团队报名目标活动被拒绝 |
| TC-PREREQ-004 | 前置活动中组建的团队保持完整进入目标活动 |
| TC-CATREL-900 | 重复创建同一活动关联被拒绝 |
| TC-CATREL-901 | 自引用被拒绝 |
| TC-CATREL-902 | 赛段循环依赖被拒绝 |
| TC-CATREL-903 | 非法 relation_type 被拒绝 |

## 15-entry-rules.md (Entry Rules)

| TC ID | Description |
|-------|-------------|
| TC-ENTRY-001 | 报名前必须已加入团队 |
| TC-ENTRY-002 | 提交前必须已有团队报名 |
| TC-ENTRY-003 | 报名前必须已有 profile 帖子 |
| TC-ENTRY-004 | 已满足前置条件时报名成功 |
| TC-ENTRY-010 | 提交时帖子必须包含至少一个 resource |
| TC-ENTRY-011 | 提交时帖子必须包含指定格式的 resource |
| TC-ENTRY-012 | 帖子包含符合要求的 resource 时提交成功 |
| TC-ENTRY-020 | 一个用户在同一活动中只能有一个参赛提案 |
| TC-ENTRY-021 | 同一用户在同一活动中只能属于一个团队 |
| TC-ENTRY-022 | 不同活动中同一用户可分别提交提案 |
| TC-ENTRY-030 | 固定字段和自定义 checks 同时生效 |
| TC-ENTRY-031 | 固定字段和自定义 checks 均满足时操作成功 |
| TC-ENTRY-900 | checks 中引用不存在的 condition type 被拒绝 |
| TC-ENTRY-901 | checks 缺少必填字段被拒绝 |
| TC-ENTRY-902 | pre 阶段 check 缺少 condition 被拒绝 |

## 16-closure-rules.md (Closure Rules)

| TC ID | Description |
|-------|-------------|
| TC-CLOSE-001 | 活动关闭前校验所有团队人数 |
| TC-CLOSE-002 | 活动关闭前严格校验（deny 模式） |
| TC-CLOSE-010 | 活动关闭后标记不合格团队 |
| TC-CLOSE-011 | 活动关闭后标记不合格提案 |
| TC-CLOSE-012 | 所有团队均合格时无标记 |
| TC-CLOSE-020 | 活动关闭后按 average_rating 计算排名 |
| TC-CLOSE-021 | average_rating 相同时排名并列 |
| TC-CLOSE-022 | 无评分的帖子不参与排名 |
| TC-CLOSE-030 | 活动关闭后自动颁发证书 |
| TC-CLOSE-031 | 无排名结果时不颁发证书 |
| TC-CLOSE-032 | 证书帖子可被获奖者读取 |
| TC-CLOSE-040 | 完整活动结束流程 |
| TC-CLOSE-900 | 非 closed 状态变更不触发关闭 checks |
| TC-CLOSE-901 | 活动无关联 Rule 时关闭不触发任何 check |
| TC-CLOSE-902 | post phase action 失败不回滚活动关闭 |

## 17-rule-engine.md (Rule Engine)

| TC ID | Description |
|-------|-------------|
| TC-ENGINE-001 | time_window 条件 — 开始时间未到 |
| TC-ENGINE-002 | time_window 条件 — 截止时间已过 |
| TC-ENGINE-003 | count 条件 — 计数满足 |
| TC-ENGINE-004 | count 条件 — 计数不满足 |
| TC-ENGINE-005 | exists 条件 — 实体存在时通过 |
| TC-ENGINE-006 | exists 条件 — 实体不存在时拒绝 |
| TC-ENGINE-007 | exists 条件 — require=false 时实体不存在通过 |
| TC-ENGINE-008 | field_match 条件 — 字段匹配 |
| TC-ENGINE-009 | resource_format 条件 — 格式匹配 |
| TC-ENGINE-010 | resource_required 条件 — 数量和格式均满足 |
| TC-ENGINE-011 | aggregate 条件 — 聚合计算满足 |
| TC-ENGINE-020 | 固定字段自动展开为 checks |
| TC-ENGINE-021 | 固定字段展开的 check 排在自定义 checks 之前 |
| TC-ENGINE-022 | 纯 checks 定义（无固定字段） |
| TC-ENGINE-030 | 多 Rule 的 checks 合并后 AND 逻辑执行 |
| TC-ENGINE-031 | 多 Rule 中一条有 checks 一条只有固定字段 |
| TC-ENGINE-040 | post phase check 在操作成功后执行 |
| TC-ENGINE-041 | post phase check 条件不满足时 action 不执行 |
| TC-ENGINE-042 | post phase check 失败不回滚主操作 |
| TC-ENGINE-050 | on_fail=deny 时操作被拒绝 |
| TC-ENGINE-051 | on_fail=warn 时操作允许但返回警告 |
| TC-ENGINE-052 | on_fail=flag 时操作允许并标记 |
| TC-ENGINE-060 | Rule 无固定字段且 checks 为空数组 |
| TC-ENGINE-061 | 活动未关联任何 Rule |
