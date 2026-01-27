# 关系类型测试

> **格式约定：** 每条用例仅描述「场景」与「预期结果」，不包含测试方法和执行过程。

---

## 8.1 category:rule（活动-规则）

**TC-REL-CR-001：将规则关联到活动**
创建 category:rule 关系，设置 priority。创建成功，读取返回该关联记录。

**TC-REL-CR-002：更新 category:rule priority**
将规则优先级从 1 更新为 10。更新成功，读取返回新 priority 值。

**TC-REL-CR-003：删除 category:rule 关系（不影响规则本身）**
解除活动与规则的关联关系。关系被物理删除，但规则实体本身仍可读取。

**TC-REL-CR-900：重复关联同一规则到同一活动被拒绝**
同一 rule 已关联到同一 category 后，再次创建相同的 category:rule 关系。系统拒绝操作，返回唯一性约束错误。

## 8.2 category:post（活动-帖子）

**TC-REL-CP-001：将帖子关联为活动的 submission**
创建 category:post 关系，relation_type=submission。前提：该 category 关联的 rule 的时间窗口、格式、提交次数、团队人数等约束均满足。创建成功。

**TC-REL-CP-002：将帖子关联为活动的 reference**
创建 category:post 关系，relation_type=reference。创建成功。

**TC-REL-CP-003：按 relation_type 筛选活动帖子**
同一活动下有 submission 和 reference 两种关系。按 relation_type=submission 筛选时，仅返回 submission 类型记录，不含 reference。

**TC-REL-CP-004：不带筛选读取所有 category:post**
不传 relation_type 过滤条件读取。返回结果包含 submission 和 reference 两类。

**TC-REL-CP-900：规则截止后提交 category_post 被拒绝**
活动关联了 `submission_deadline` 已过期的规则，用户尝试创建 category:post 关系。系统拒绝操作，返回 "deadline passed" 错误。

**TC-REL-CP-901：格式不符时提交 category_post 被拒绝**
活动关联了 `submission_format=["pdf"]` 的规则，帖子关联的 resource 为 `.pptx` 格式。系统拒绝操作，返回 "not allowed" 错误。

**TC-REL-CP-902：超出 max_submissions 时提交 category_post 被拒绝**
活动关联了 `max_submissions=1` 的规则，用户已有一次提交。系统拒绝第二次操作，返回 "max submissions reached" 错误。

## 8.3 category:group（活动-团队报名）

**TC-REL-CG-001：团队报名活动**
创建 category:group 关系。创建成功，读取活动已报名团队列表能查到该团队。

**TC-REL-CG-002：读取活动已报名团队列表**
查询某活动下所有已报名团队，返回完整团队列表。

**TC-REL-CG-003：团队取消报名（DELETE category:group）**
删除 category:group 关系。关系被物理删除，读取不再返回该团队。

**TC-REL-CG-900：重复报名同一活动被拒绝**
同一团队对同一活动创建两次 category:group 关系。系统拒绝第二次操作，返回已注册错误。

**TC-REL-CG-901：同一用户在同一活动中属于多个团队被拒绝**
用户 Alice 同时属于 Team Synnovator 和 Team Alpha，两个团队都报名同一活动。系统拒绝第二个团队的报名，返回"同一用户在同一 category 中只能属于一个 group"的错误。

## 8.4 post:post（帖子间关系）

**TC-REL-PP-001：创建 embed 关系（嵌入团队卡片）**
创建 post:post 关系，relation_type=embed，设置 position=1。创建成功，读取返回 embed 关系和 position。

**TC-REL-PP-002：创建 reference 关系（引用另一帖子）**
创建 post:post 关系，relation_type=reference。创建成功。

**TC-REL-PP-003：创建 reply 关系（帖子回复）**
创建 post:post 关系，relation_type=reply。创建成功。

**TC-REL-PP-004：更新 post:post 关系类型和位置**
将 embed 关系修改为 reference，position 修改为 0。更新成功。

**TC-REL-PP-005：删除 post:post 关系**
解除帖子间关联。关系被物理删除。

## 8.5 post:resource（帖子-资源）

**TC-REL-PR-001：资源作为 attachment 挂到帖子**
创建 post:resource 关系，display_type=attachment。创建成功。

**TC-REL-PR-002：资源作为 inline 挂到帖子**
创建 post:resource 关系，display_type=inline。创建成功。

**TC-REL-PR-003：同一帖子挂多个资源，position 排序**
同一帖子关联两个资源，分别设置 position=0 和 position=1。读取 post:resource 返回结果包含 position 信息，可用于排序。

**TC-REL-PR-004：更新 post:resource display_type**
将 display_type 从 attachment 改为 inline。更新成功。

**TC-REL-PR-005：删除 post:resource 关系（不影响资源本身）**
解除帖子与资源的关联。关系被物理删除，但资源实体本身仍可读取。

## 8.6 group:user（团队-成员）

**TC-REL-GU-001：移出团队成员**
删除 group:user 关系（将一个 accepted 状态的成员移出团队）。关系被物理删除，读取不再返回该成员。

**TC-REL-GU-900：已有成员重复加入被拒绝**
Alice 已是团队 owner，再次以 member 身份加入同一团队。系统拒绝操作，返回"已在该团队"的错误。

**TC-REL-GU-901：创建 group_user 时使用非法 role 枚举**
创建 group_user 时指定 role 为 "superadmin"。系统拒绝操作，返回枚举值无效错误（合法值为 owner | admin | member）。

**TC-REL-GU-902：团队已满时加入被拒绝（Rule Enforcement）**
团队已注册某活动，该活动关联了 `max_team_size=1` 的规则。团队已有 1 名 accepted 成员，另一用户尝试创建 group_user 关系加入该团队。系统拒绝操作，返回 "team is full" 错误。

## 8.7 target:interaction（目标-互动关联）

**TC-REL-TI-001：创建 target_interaction 关系**
将 interaction 关联到目标帖子。创建成功。

**TC-REL-TI-002：删除 target:interaction 关系**
解除目标对象与互动记录的关联。关系被物理删除。
