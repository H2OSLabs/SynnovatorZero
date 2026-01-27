# 规则（Rule）模块

> **格式约定：** 每条用例仅描述「场景」与「预期结果」，不包含测试方法和执行过程。

---

## 3.1 创建规则

**TC-RULE-001：创建含完整 scoring_criteria 的规则**
组织者创建一个评审规则，包含：规则名称、描述、allow_public=true、require_review=true、评委列表、投稿时间窗口、提交格式限制、最大提交数、团队人数范围，以及 4 个评分维度（创新性 30%、技术实现 30%、实用价值 25%、演示效果 15%）。创建完成后，scoring_criteria 被正确存储，权重总和为 100。

**TC-RULE-002：创建 select-only 规则**
创建一条 allow_public=false、require_review=true 的规则（仅允许选择已有帖子，不允许新建）。创建完成后，字段值符合预期。

## 3.2 读取规则

**TC-RULE-003：读取已创建的规则**
读取规则，返回完整信息，包括 scoring_criteria 数组内的各维度名称、权重和描述。

## 3.3 更新规则

**TC-RULE-010：修改规则配置字段**
更新规则的 allow_public、max_submissions、max_team_size 等字段。更新完成后，读取规则返回新值，updated_at 变更。

**TC-RULE-011：修改 scoring_criteria 权重**
将评分标准的 4 个维度权重从 [30, 30, 25, 15] 修改为 [25, 25, 25, 25]。更新完成后，读取规则返回新的 scoring_criteria，后续 rating 按新权重计算。

## 3.4 删除规则

**TC-RULE-020：删除规则及级联**
删除一个已关联到活动的规则。删除完成后：
- 规则记录被物理删除
- category:rule 关系被解除
- 读取返回 "not found" 错误

## 3.5 负向/边界

**TC-RULE-900：participant 创建规则被拒绝**
一个 participant 角色的用户尝试创建规则。系统拒绝操作，返回权限不足错误。

**TC-RULE-901：scoring_criteria 权重总和不等于 100**
创建规则时提供两个评分维度，权重分别为 50 和 60（总和 110）。系统拒绝创建或发出警告。

## 3.6 规则执行校验（Rule Enforcement）

> 规则通过 `category_rule` 关联到活动后，引擎在 `create_relation(category_post)`、`create_relation(group_user)`、`update_content(post status)` 三个操作点自动执行 pre-operation 校验。所有关联的 rule 必须全部满足（AND 逻辑），任一违规即拒绝操作。

**TC-RULE-100：提交截止后创建 category_post 被拒绝**
活动关联了一条 `submission_deadline` 已过期的规则。用户创建帖子并尝试通过 `category_post` 关联到该活动。系统拒绝操作，返回错误信息包含 "deadline passed"。

**TC-RULE-101：提交未开始时创建 category_post 被拒绝**
活动关联了一条 `submission_start` 为未来时间的规则。用户尝试提前提交。系统拒绝操作，返回错误信息包含 "not yet open"。

**TC-RULE-102：超出 max_submissions 后创建 category_post 被拒绝**
活动关联了一条 `max_submissions=1` 的规则。用户已有一次提交后，再次创建新帖子并关联到该活动。系统拒绝操作，返回错误信息包含 "max submissions reached"。

**TC-RULE-103：提交格式不符时创建 category_post 被拒绝**
活动关联了一条 `submission_format=["pdf"]` 的规则。用户的帖子关联了一个 filename 为 "slides.pptx" 的 resource。尝试通过 `category_post` 关联到该活动时，系统拒绝操作，返回错误信息包含 "not allowed"。

**TC-RULE-104：团队人数不足时创建 category_post 被拒绝**
活动关联了一条 `min_team_size=3` 的规则。用户所在团队仅有 1 人（owner），团队已注册该活动。用户尝试提交作品时，系统拒绝操作，返回错误信息包含 "team too small"。

**TC-RULE-105：团队已满时创建 group_user 被拒绝**
团队已注册一个活动，该活动关联了一条 `max_team_size=1` 的规则。团队已有 1 名 accepted 成员，另一用户尝试加入该团队。系统拒绝操作，返回错误信息包含 "team is full"。

**TC-RULE-106：allow_public=false 时直接发布被拒绝**
帖子已通过 `category_post` 关联到活动，活动关联了一条 `allow_public=false, require_review=true` 的规则。用户尝试将帖子 status 直接更新为 published。系统拒绝操作，返回错误信息包含 "direct publish not allowed"。

**TC-RULE-107：allow_public=false 时 pending_review 状态被允许**
同上场景，用户将帖子 status 更新为 `pending_review`。系统允许操作，帖子进入待审核状态。

**TC-RULE-108：无 rule 关联时 category_post 正常创建**
活动未关联任何规则。用户创建帖子并通过 `category_post` 关联到该活动。系统正常允许，无约束校验。

**TC-RULE-109：多条 rule 全部满足才允许（AND 逻辑）**
活动关联了两条规则：规则 A 限制 `submission_format=["pdf"]`，规则 B 限制 `max_submissions=2`。用户的帖子格式符合规则 A，但提交次数已达规则 B 上限。系统拒绝操作，返回规则 B 的违规信息。
