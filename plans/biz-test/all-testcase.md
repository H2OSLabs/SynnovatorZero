# Synnovator Skill 完整测试用例集

> **格式约定：** 每条用例仅描述「场景」与「预期结果」，不包含测试方法和执行过程。

---

## 目录

1. [用户（User）模块](#1-用户user模块)
2. [活动（Category）模块](#2-活动category模块)
3. [规则（Rule）模块](#3-规则rule模块)
4. [团队（Group）模块](#4-团队group模块)
5. [帖子（Post）模块](#5-帖子post模块)
6. [资源（Resource）模块](#6-资源resource模块)
7. [互动（Interaction）模块](#7-互动interaction模块)
8. [关系类型测试](#8-关系类型测试)
9. [软删除与级联](#9-软删除与级联)
10. [恢复机制](#10-恢复机制)
11. [权限与可见性](#11-权限与可见性)
12. [用户旅程集成](#12-用户旅程集成)
13. [资产转移（Resource Transfer）](#13-资产转移resource-transfer)
14. [好友（User Follow / Friend）](#14-好友user-follow--friend)
15. [活动关联（Category Association）](#15-活动关联category-association)

---

## 1. 用户（User）模块

### 1.1 创建用户

**TC-USER-001：创建 participant 用户**
创建一个用户 Alice，角色为 participant，提供用户名、邮箱、显示名等信息。创建完成后，系统返回该用户记录，包含自动生成的 id、created_at、updated_at，deleted_at 为空。

**TC-USER-002：创建 organizer 用户**
创建一个用户 Judge，角色为 organizer。创建完成后，role 字段为 organizer。

**TC-USER-003：创建 admin 用户**
创建一个管理员用户，角色为 admin。创建完成后，role 字段为 admin，可通过读取验证。

### 1.2 读取用户

**TC-USER-004：读取已创建的用户**
读取上述创建的用户记录，返回完整的用户信息，包括 username、email、display_name、role 等字段。

### 1.3 更新用户

**TC-USER-010：用户修改自己的个人信息**
用户 Bob 更新自己的 display_name 和 bio 字段。更新完成后，读取该用户可看到新的 display_name 和 bio 值，updated_at 已变更。

**TC-USER-011：Admin 修改其他用户的角色**
管理员将某个 participant 用户的角色修改为 organizer。更新完成后，该用户的 role 变为 organizer。

### 1.4 删除用户

**TC-USER-020：软删除用户及级联影响**
删除用户 Charlie（该用户已加入团队、有点赞和评论记录）。删除完成后：
- 用户被软删除（deleted_at 非空）
- 该用户的所有 interaction（点赞、评论）一并软删除
- group:user 关系保留（标记为离组状态）
- 对应帖子的 like_count 和 comment_count 相应递减

### 1.5 负向/边界

**TC-USER-900：重复 username 被拒绝**
创建一个与已有用户相同 username（"alice"）的新用户。系统拒绝创建，返回 username 唯一性冲突错误。

**TC-USER-901：重复 email 被拒绝**
创建一个与已有用户相同 email（"alice@example.com"）的新用户。系统拒绝创建，返回 email 唯一性冲突错误。

**TC-USER-902：非本人/非 Admin 修改用户信息被拒绝**
用户 Bob 尝试修改用户 Alice 的个人信息。系统拒绝操作，返回权限不足错误。

**TC-USER-903：缺少必填字段 email**
创建用户时只提供 username，不提供 email。系统拒绝创建，返回缺少必填字段错误。

---

## 2. 活动（Category）模块

### 2.1 创建活动

**TC-CAT-001：创建 competition 类型活动**
组织者 Alice 创建一个比赛活动（type=competition），设置名称、描述、起止日期，附带 Markdown 正文。创建完成后，系统返回记录，id 自动生成，type 为 competition，has_body 为 true，created_by 为 Alice。

**TC-CAT-002：创建 operation 类型活动**
组织者创建一个运营活动（type=operation）。创建完成后，type 为 operation。

### 2.2 读取活动

**TC-CAT-003：读取已创建的活动**
读取上述创建的活动，返回完整的活动信息，包括 name、description、type、status、start_date、end_date 等字段。

### 2.3 更新活动

**TC-CAT-010：活动状态流转 draft → published → closed**
将一个 draft 状态的活动依次更新为 published，再更新为 closed。每步更新成功后，status 变为对应值，updated_at 逐步递增。

**TC-CAT-011：修改活动名称和描述**
更新活动的 name 和 description 字段。更新完成后，读取活动返回新值。

### 2.4 删除活动

**TC-CAT-020：删除活动及级联影响**
删除一个已关联 rule（category:rule）、post（category:post）、group（category:group）和 interaction 的活动。删除完成后：
- 活动被软删除（deleted_at 非空）
- category:rule、category:post、category:group 关系均被解除
- 关联的 interaction（如对该活动的点赞）一并软删除

### 2.5 负向/边界

**TC-CAT-900：非法 type 枚举被拒绝**
创建活动时指定 type 为 "workshop"（不在合法枚举范围内）。系统拒绝创建，返回枚举值无效错误。

**TC-CAT-901：非法 status 枚举被拒绝**
创建或更新活动时指定 status 为 "archived"。系统拒绝操作，返回枚举值无效错误。

**TC-CAT-902：participant 创建活动被拒绝**
一个 participant 角色的用户尝试创建活动。系统拒绝操作，返回权限不足错误（CREATE category 仅限 Organizer/Admin）。

---

## 3. 规则（Rule）模块

### 3.1 创建规则

**TC-RULE-001：创建含完整 scoring_criteria 的规则**
组织者创建一个评审规则，包含：规则名称、描述、allow_public=true、require_review=true、评委列表、投稿时间窗口、提交格式限制、最大提交数、团队人数范围，以及 4 个评分维度（创新性 30%、技术实现 30%、实用价值 25%、演示效果 15%）。创建完成后，scoring_criteria 被正确存储，权重总和为 100。

**TC-RULE-002：创建 select-only 规则**
创建一条 allow_public=false、require_review=true 的规则（仅允许选择已有帖子，不允许新建）。创建完成后，字段值符合预期。

### 3.2 读取规则

**TC-RULE-003：读取已创建的规则**
读取规则，返回完整信息，包括 scoring_criteria 数组内的各维度名称、权重和描述。

### 3.3 更新规则

**TC-RULE-010：修改规则配置字段**
更新规则的 allow_public、max_submissions、max_team_size 等字段。更新完成后，读取规则返回新值，updated_at 变更。

**TC-RULE-011：修改 scoring_criteria 权重**
将评分标准的 4 个维度权重从 [30, 30, 25, 15] 修改为 [25, 25, 25, 25]。更新完成后，读取规则返回新的 scoring_criteria，后续 rating 按新权重计算。

### 3.4 删除规则

**TC-RULE-020：删除规则及级联**
删除一个已关联到活动的规则。删除完成后：
- 规则被软删除（deleted_at 非空）
- category:rule 关系被解除
- 普通读取被拒绝（返回 soft-deleted 错误）

### 3.5 负向/边界

**TC-RULE-900：participant 创建规则被拒绝**
一个 participant 角色的用户尝试创建规则。系统拒绝操作，返回权限不足错误。

**TC-RULE-901：scoring_criteria 权重总和不等于 100**
创建规则时提供两个评分维度，权重分别为 50 和 60（总和 110）。系统拒绝创建或发出警告。

### 3.6 规则执行校验（Rule Enforcement）

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

---

## 4. 团队（Group）模块

### 4.1 创建团队

**TC-GRP-001：创建需审批的公开团队**
创建一个团队，设置 visibility=public、require_approval=true、max_members=5。创建完成后，系统返回记录，id 自动生成。

**TC-GRP-002：创建无需审批的私有团队**
创建一个团队，设置 visibility=private、require_approval=false。创建完成后，visibility 为 private，新成员加入时自动变为 accepted 状态。

### 4.2 团队成员管理

**TC-GRP-003：Owner 自动加入**
将用户设为团队 owner。该 group_user 记录的 status 自动为 accepted，joined_at 已赋值。

**TC-GRP-004：需审批团队 — 成员申请加入为 pending**
用户 Carol 申请加入一个 require_approval=true 的团队。创建的 group_user 记录 status 为 pending。

**TC-GRP-005：Owner 批准成员申请**
Alice（Owner）批准 Carol 的加入申请。更新后 status 变为 accepted，joined_at 被赋值。

**TC-GRP-006：Owner 拒绝成员申请**
Alice 拒绝 Bob 的加入申请。更新后 status 变为 rejected。

**TC-GRP-007：被拒绝后重新申请**
Bob 被拒绝后重新申请加入团队。重新申请成功，新的 group_user 记录 status 为 pending。

**TC-GRP-008：无需审批团队 — 成员直接 accepted**
Bob 加入一个 require_approval=false 的团队。创建的 group_user 记录 status 自动为 accepted，joined_at 已赋值。

### 4.3 更新团队

**TC-GRP-010：Owner 更新团队信息**
团队 Owner 更新团队的 description 和 max_members。更新完成后，读取团队返回新值，updated_at 变更。

**TC-GRP-011：变更审批设置**
将 require_approval 从 true 改为 false。更新成功后，后续新成员加入时自动 accepted。

**TC-GRP-012：变更可见性**
将团队 visibility 从 public 改为 private。更新成功后，读取团队返回 visibility=private。

### 4.4 删除团队

**TC-GRP-020：删除团队及级联**
删除一个已注册活动（category:group 关系存在）的团队。删除完成后：
- 团队被软删除
- group:user 关系保留（成员可查询历史）
- category:group 关系被解除

### 4.5 负向/边界

**TC-GRP-900：非法 visibility 枚举被拒绝**
创建团队时指定 visibility 为 "restricted"。系统拒绝创建，返回枚举值无效错误。

**TC-GRP-901：非 Owner/Admin 修改团队信息被拒绝**
普通 member 用户 Bob 尝试更新团队信息。系统拒绝操作，返回权限不足错误。

---

## 5. 帖子（Post）模块

### 5.1 基础创建

**TC-POST-001：最小字段创建帖子**
仅提供 title 和正文创建帖子。创建完成后，type 默认为 general，status 默认为 draft，缓存统计字段初始化为 like_count=0、comment_count=0、average_rating=null。

**TC-POST-002：显式发布帖子**
创建时指定 status=published。创建完成后，帖子为已发布状态，公开可读。

**TC-POST-003：带 tags 创建帖子**
创建帖子时附带 tags（如 ["找队友", "提案"]）。创建完成后，可通过 tag 筛选查询命中该帖子。

**TC-POST-004：按 type 筛选帖子**
创建多种 type 的帖子（general、team、for_category、certificate）后，按 type=for_category 筛选。返回结果仅包含 type=for_category 的帖子。

### 5.2 类型语义覆盖

**TC-POST-010：创建 team 类型帖子**
创建一个 type=team 的帖子（团队卡片），包含团队介绍和成员信息。创建成功后，后续可被嵌入到其它帖子（post:post embed 关系）。

**TC-POST-011：创建 profile 类型帖子**
创建一个 type=profile 的帖子（个人资料卡片）。创建成功。

**TC-POST-012：创建 for_category 类型帖子**
创建一个 type=for_category 的帖子（参赛提案）。创建成功后，可被关联到某个活动（category:post relation_type=submission）。

**TC-POST-013：创建 certificate 类型帖子**
创建一个 type=certificate 的帖子（证书分享帖）。创建成功后，可挂载 resource（证书文件）作为附件或内联。

### 5.3 状态流转

**TC-POST-030：帖子进入 pending_review 状态**
创建帖子后将 status 更新为 pending_review。若帖子已关联 category 且 rule 设置了 `require_review=true`，这是正确的提交路径。更新成功。

**TC-POST-031：帖子被审核通过（pending_review → published）**
将 pending_review 状态的帖子更新为 published。此操作代表审核人主动批准，即使 rule 设置 `allow_public=false`，审核通过路径也不受限。更新成功后，status 为 published。

**TC-POST-032：帖子被驳回（pending_review → rejected）**
将 pending_review 状态的帖子更新为 rejected。更新成功后，status 为 rejected。

**TC-POST-033：草稿发布（draft → published）**
将 draft 状态的帖子更新为 published。若帖子未关联任何 category 或关联 category 的 rule 允许公开发布（`allow_public=true`），更新成功，updated_at 变更。若 rule 设置 `allow_public=false`，更新被拒绝（见 TC-RULE-106）。

### 5.4 版本管理

**TC-POST-040：通过新帖子实现版本管理**
创建提案帖子 v1，再创建 v2，通过 post_post（relation_type=reference）关系链接新旧版本。两个帖子有独立 id，通过关系保留版本关联。

**TC-POST-041：发布新版本**
将新版本帖子的 status 更新为 published。更新成功。

### 5.5 标签操作

**TC-POST-050：添加标签（+tag 语法）**
对帖子使用 "+devlog" 和 "+update" 语法分别添加标签。添加后 tags 列表包含新标签。

**TC-POST-051：移除标签（-tag 语法）**
对帖子使用 "-devlog" 语法移除标签。移除后 tags 不再包含 devlog，但仍包含 update。

**TC-POST-052："选择已有帖子"报名（标签打标）**
对已有帖子使用 "+for_ai_hackathon" 标签实现"选择已有帖子"报名活动。更新后 tags 列表中包含 for_ai_hackathon。

### 5.6 更新帖子正文

**TC-POST-060：更新帖子 title 和 Markdown body**
同时更新帖子的 title 和 Markdown 正文内容。更新完成后，title 为新值，has_body 为 true。

### 5.7 可见性控制（Visibility）

**TC-POST-070：创建 visibility=private 的帖子**
创建帖子时指定 visibility=private。创建完成后，visibility 字段为 private，帖子仅作者和 Admin 可读取，其他用户读取该帖子返回不可见或权限错误。

**TC-POST-071：private 帖子跳过 pending_review 直接发布**
创建一个 visibility=private 的帖子，将其关联到一个 rule 设置了 require_review=true、allow_public=false 的活动（category:post）。将帖子 status 直接从 draft 更新为 published。系统允许操作（private 帖子不受 pending_review 流程约束），status 变为 published。

**TC-POST-072：private 已发布帖子对非作者不可见**
一个 visibility=private、status=published 的帖子。非作者用户（包括已登录用户和访客）尝试读取该帖子。系统不返回该帖子或返回权限错误。Admin 可正常读取。

**TC-POST-073：将 public 帖子改为 private**
将一个已发布的 visibility=public 帖子的 visibility 更新为 private。更新成功后，其他用户无法再读取该帖子，仅作者和 Admin 可见。

**TC-POST-074：将 private 帖子改为 public**
将一个 visibility=private、status=published 的帖子的 visibility 更新为 public。更新成功后，帖子对所有用户可见（遵循 status=published 的标准可见性规则）。

**TC-POST-075：private 帖子的 interaction 对非作者不可见**
对一个 visibility=private 的帖子创建点赞和评论（由作者自己操作）。非作者用户查询该帖子的 interaction 列表时，系统不返回结果（因为目标帖子不可见）。

**TC-POST-076：默认 visibility 为 public**
创建帖子时不指定 visibility。创建完成后，visibility 字段默认为 public。

### 5.8 负向/边界

**TC-POST-900：缺少 title 被拒绝**
创建帖子时不提供 title。系统拒绝创建，返回缺少必填字段错误。

**TC-POST-901：非法 type/status 枚举被拒绝**
创建帖子时指定 type 为 "foo" 或 status 为 "archived"。系统拒绝创建，返回枚举值无效错误。

**TC-POST-903：非法 visibility 枚举被拒绝**
创建帖子时指定 visibility 为 "restricted"。系统拒绝创建，返回枚举值无效错误（合法值为 public | private）。

**TC-POST-902：未登录用户创建帖子被拒绝**
未提供用户身份的情况下创建帖子。系统拒绝操作，返回需要认证的错误。

---

## 6. 资源（Resource）模块

### 6.1 创建资源

**TC-RES-001：最小字段创建资源**
仅提供 filename（如 "test-file.txt"）创建资源。创建完成后，id/created_by/created_at 自动生成，可通过读取获取信息。

**TC-RES-002：带完整元信息创建资源**
提供 filename、display_name、description 和 mime_type 创建资源（如演示视频 demo.mp4）。创建完成后，各字段值正确。

### 6.2 更新资源

**TC-RES-030：更新资源元信息**
更新资源的 display_name 和 description。更新完成后，读取资源返回新值，updated_at 变更。

### 6.3 删除资源

**TC-RES-031：删除资源后级联解除 post:resource**
删除一个已关联到帖子的资源。资源被软删除后，post:resource 关系被解除。

### 6.4 间接可见性（Inherited Visibility）

> Resource 无独立 visibility 字段，其可见性完全继承自关联帖子（"关联帖子可见则可读"）。以下用例验证该继承行为在不同场景下的正确性。

**TC-RES-040：关联到 published + public 帖子的 resource 可被任何人读取**
创建 resource 并通过 post:resource 关联到一个 status=published、visibility=public 的帖子。访客和已登录用户均可读取该 resource。

**TC-RES-041：关联到 draft 帖子的 resource 对非作者不可读**
创建 resource 并通过 post:resource 关联到一个 status=draft 的帖子。非作者用户尝试读取该 resource，系统不返回或返回权限错误。作者和 Admin 可读取。

**TC-RES-042：关联到 private 帖子的 resource 对非作者不可读**
创建 resource 并通过 post:resource 关联到一个 visibility=private、status=published 的帖子。非作者用户尝试读取该 resource，系统不返回或返回权限错误。作者和 Admin 可读取。

**TC-RES-043：帖子从 public 改为 private 后，关联 resource 不可见性同步变更**
resource R 关联到一个 published + public 的帖子，此时任何人可读取 R。将帖子 visibility 更新为 private 后，非作者用户无法再读取 R。

**TC-RES-044：resource 同时关联到 public 和 private 帖子时的可见性**
resource R 同时通过 post:resource 关联到帖子 A（public + published）和帖子 B（private + published）。非作者用户通过帖子 A 的关联可读取 R（因为帖子 A 可见）。R 的可见性取决于其关联帖子中是否有至少一个可见帖子。

**TC-RES-045：帖子软删除后 resource 的可访问性**
resource R 关联到帖子 P（published + public）。删除帖子 P 后，post:resource 关系被解除。R 成为孤立资源（不关联任何帖子）。非作者用户无法通过帖子路径读取 R。resource 实体本身未被删除。

### 6.5 负向/边界

**TC-RES-900：缺少 filename 被拒绝**
创建资源时不提供 filename。系统拒绝创建，返回缺少必填字段错误。

**TC-RES-901：未登录用户创建资源被拒绝**
未提供用户身份的情况下创建资源。系统拒绝操作。

**TC-RES-902：引用不存在的 post_id/resource_id 创建关系被拒绝**
使用不存在的 ID 创建 post:resource 关系。系统拒绝操作，返回对应 ID 不存在的错误。

**TC-RES-903：非法 display_type 枚举被拒绝**
创建 post:resource 关系时指定 display_type 为 "embedded"。系统拒绝操作，返回枚举值无效错误（合法值为 attachment | inline）。

---

## 7. 互动（Interaction）模块

### 7.1 点赞（like）

**TC-IACT-001：对帖子点赞**
用户 Dave 对一个已发布帖子点赞。创建 like interaction 成功，帖子的 like_count 从 0 变为 1。

**TC-IACT-002：重复点赞被拒绝**
同一用户对同一帖子再次点赞。系统拒绝操作，返回"已点赞"错误。

**TC-IACT-003：取消点赞后 like_count 递减**
删除一条 like interaction。帖子的 like_count 相应递减。

### 7.2 评论（comment）

**TC-IACT-010：创建顶层评论**
用户 Bob 对帖子发表评论。创建 comment interaction 成功，帖子的 comment_count +1。

**TC-IACT-011：创建嵌套回复（一级回复）**
用户 Alice 回复 Bob 的评论（指定 parent_id）。创建成功，帖子的 comment_count 再 +1。

**TC-IACT-012：创建二级回复（回复的回复）**
用户 Bob 回复 Alice 的回复（parent_id 指向一级回复）。创建成功，parent_id 正确指向一级回复 ID。

**TC-IACT-013：comment_count 包含所有层级**
读取帖子，comment_count 包含顶层评论和所有嵌套回复的总数。

**TC-IACT-014：删除父评论级联删除子回复**
删除顶层评论。顶层评论和所有嵌套回复（一级、二级）均被软删除（deleted_at 非空）。

### 7.3 评分（rating）

**TC-IACT-020：创建多维度评分**
评委对帖子提交多维度评分（创新性 87、技术实现 82、实用价值 78、演示效果 91），附带评语。创建成功后，帖子的 average_rating 按权重计算为 83.85（87x0.30 + 82x0.30 + 78x0.25 + 91x0.15）。

**TC-IACT-021：多个评分的均值计算**
第二个评委提交不同分数（75、90、85、70）。该评委加权分为 81.25。帖子的 average_rating 更新为两个评分的均值 82.55。

### 7.4 更新互动

**TC-IACT-050：修改评论文本**
评论发起人修改自己评论的 value 文本。更新成功，value 为新文本，updated_at 变更，comment_count 不变。

**TC-IACT-051：修改评分重新打分**
评委修改已提交的评分分值。更新成功，帖子的 average_rating 按新分值重新计算。

### 7.5 非 post 目标的互动

**TC-IACT-060：对 category（活动）点赞**
用户对一个 published 状态的 category 点赞。创建成功，target_type 为 category。

**TC-IACT-061：对 category 发表评论**
用户对一个 category 发表评论。创建成功。

**TC-IACT-062：对 resource（资源）点赞**
用户对一个 resource 点赞。创建成功，target_type 为 resource。

**TC-IACT-063：对 resource 发表评论**
用户对一个 resource 发表评论。创建成功。

### 7.6 负向/边界

**TC-IACT-900：非法 interaction type 被拒绝**
创建 interaction 时指定 type 为 "bookmark"。系统拒绝操作，返回枚举值无效错误（合法值为 like | comment | rating）。

**TC-IACT-901：非法 target_type 被拒绝**
创建 interaction 时指定 target_type 为 "user"。系统拒绝操作，返回枚举值无效错误。

**TC-IACT-902：target_id 不存在被拒绝**
对一个不存在的帖子 ID 点赞。系统拒绝操作，返回目标对象不存在错误。

**TC-IACT-903：对已删除的帖子点赞被拒绝**
对一个已软删除的帖子点赞。系统拒绝操作，返回 soft-deleted 错误。

**TC-IACT-904：缺少 target_id 被拒绝**
创建 interaction 时不提供 target_id。系统拒绝操作，返回缺少必填字段错误。

**TC-IACT-905：非本人修改 interaction 被拒绝**
用户 Alice 尝试修改用户 Bob 的评论。系统拒绝操作，返回权限不足错误。

---

## 8. 关系类型测试

### 8.1 category:rule（活动-规则）

**TC-REL-CR-001：将规则关联到活动**
创建 category:rule 关系，设置 priority。创建成功，读取返回该关联记录。

**TC-REL-CR-002：更新 category:rule priority**
将规则优先级从 1 更新为 10。更新成功，读取返回新 priority 值。

**TC-REL-CR-003：删除 category:rule 关系（不影响规则本身）**
解除活动与规则的关联关系。关系被物理删除，但规则实体本身仍可读取。

**TC-REL-CR-900：重复关联同一规则到同一活动被拒绝**
同一 rule 已关联到同一 category 后，再次创建相同的 category:rule 关系。系统拒绝操作，返回唯一性约束错误。

### 8.2 category:post（活动-帖子）

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

### 8.3 category:group（活动-团队报名）

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

### 8.4 post:post（帖子间关系）

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

### 8.5 post:resource（帖子-资源）

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

### 8.6 group:user（团队-成员）

**TC-REL-GU-001：移出团队成员**
删除 group:user 关系（将一个 accepted 状态的成员移出团队）。关系被物理删除，读取不再返回该成员。

**TC-REL-GU-900：已有成员重复加入被拒绝**
Alice 已是团队 owner，再次以 member 身份加入同一团队。系统拒绝操作，返回"已在该团队"的错误。

**TC-REL-GU-901：创建 group_user 时使用非法 role 枚举**
创建 group_user 时指定 role 为 "superadmin"。系统拒绝操作，返回枚举值无效错误（合法值为 owner | admin | member）。

**TC-REL-GU-902：团队已满时加入被拒绝（Rule Enforcement）**
团队已注册某活动，该活动关联了 `max_team_size=1` 的规则。团队已有 1 名 accepted 成员，另一用户尝试创建 group_user 关系加入该团队。系统拒绝操作，返回 "team is full" 错误。

### 8.7 target:interaction（目标-互动关联）

**TC-REL-TI-001：创建 target_interaction 关系**
将 interaction 关联到目标帖子。创建成功。

**TC-REL-TI-002：删除 target:interaction 关系**
解除目标对象与互动记录的关联。关系被物理删除。

---

## 9. 软删除与级联

### 9.1 各内容类型软删除

**TC-DEL-001：软删除 category**
删除一个活动。deleted_at 被设置为当前时间，默认查询不再返回。

**TC-DEL-002：软删除 rule**
删除一个规则。deleted_at 被设置，默认查询不返回。

**TC-DEL-003：软删除 user**
删除一个用户。deleted_at 被设置，用户的所有 interaction 一并软删除，group:user 关系保留并标记为离组。

**TC-DEL-004：软删除 group**
删除一个团队。deleted_at 被设置，group:user 关系保留，category:group 关系被解除。

**TC-DEL-005：软删除 interaction**
删除一条 like interaction。deleted_at 被设置，对应帖子的 like_count 递减。

### 9.2 级联软删除

**TC-DEL-010：删除 category → 关联 interaction 级联软删除**
删除一个有点赞和评论的活动。活动软删除后，对该活动的 like 和 comment interaction 均被级联软删除。

**TC-DEL-011：删除 user → interaction + group:user 级联处理**
删除一个有多条 interaction 和团队成员身份的用户。用户所有 interaction 被级联软删除，帖子的 like_count/comment_count 相应递减，group:user 关系保留但标记为离组。

**TC-DEL-012：删除 post → 完整级联链**
删除一个关联了 category:post、post:post、post:resource 和多条 interaction 的帖子。删除后：
- 帖子被软删除
- category:post 关系解除
- post:post 关系解除
- post:resource 关系解除
- 所有关联 interaction 被级联软删除

**TC-DEL-013：删除 rule → 级联 category:rule**
删除一个已关联到活动的规则。规则软删除后，category:rule 关系被解除。

**TC-DEL-014：删除 group → 级联 category:group**
删除一个已注册活动的团队。团队软删除后，category:group 关系被解除。

**TC-DEL-015：删除父评论 → 级联删除所有子评论**
删除一条有一级回复和二级回复的顶层评论。顶层评论和所有后代评论均被级联软删除（deleted_at 非空）。

### 9.3 已删除记录的读取行为

**TC-DEL-020：普通读取软删除记录被拒绝**
对一个已软删除的帖子执行普通读取。系统返回 soft-deleted 错误。

**TC-DEL-021：使用 include-deleted 读取软删除记录**
对一个已软删除的 interaction 使用 include-deleted 参数读取。成功返回该记录，deleted_at 字段非空。

**TC-DEL-022：更新已软删除记录被拒绝**
对一个已软删除的帖子尝试更新 title。系统拒绝操作，返回 soft-deleted 错误。

---

## 10. 恢复机制

**TC-RESTORE-001：Admin 恢复软删除的帖子**
管理员将一个已软删除帖子的 deleted_at 设为 null。恢复后，帖子可被默认查询返回。

**TC-RESTORE-002：级联恢复（恢复帖子 → 恢复因级联被软删除的 interaction）**
恢复一个帖子后，因该帖子删除而级联软删除的 interaction 也恢复，帖子的 like_count 恢复。

**TC-RESTORE-003：非 Admin 用户恢复被拒绝**
participant 用户尝试恢复一个软删除的内容。系统拒绝操作，返回"仅 Admin 可执行恢复操作"的错误。

---

## 11. 权限与可见性

### 11.1 角色权限

**TC-PERM-001：participant 创建 category 被拒绝**
participant 尝试创建活动。系统拒绝。

**TC-PERM-002：participant 创建 rule 被拒绝**
participant 尝试创建规则。系统拒绝。

**TC-PERM-003：participant 更新 category 被拒绝**
participant（非活动创建者）尝试更新活动。系统拒绝。

**TC-PERM-010：Admin 执行恢复操作被允许**
Admin 用户执行恢复软删除内容的操作。系统允许。

**TC-PERM-011：participant 执行恢复操作被拒绝**
participant 用户尝试恢复软删除内容。系统拒绝。

### 11.2 所有权检查

**TC-PERM-012：非本人修改用户信息被拒绝**
用户 Bob 尝试修改用户 Alice 的 bio。系统拒绝。

**TC-PERM-013：非 Owner 修改团队信息被拒绝**
团队普通成员 Bob 尝试更新团队 description。系统拒绝。

**TC-PERM-014：非本人修改评论被拒绝**
用户 Bob 尝试修改用户 Alice 发表的评论。系统拒绝。

### 11.3 可见性过滤

**TC-PERM-020：访客读取 draft 帖子不可见**
未登录访客尝试读取一个 status=draft 的帖子。系统不返回该帖子或返回权限错误。

**TC-PERM-021：访客读取 draft 活动不可见**
未登录访客尝试读取一个 status=draft 的活动。系统不返回该活动。

**TC-PERM-022：非成员读取 private 团队不可见**
非团队成员尝试读取一个 visibility=private 的团队。系统不返回该团队或返回权限错误。

**TC-PERM-023：已发布活动下的 draft 帖子在列表中不可见**
一个 published 活动关联了一个 draft 帖子（category:post submission）。访客查询活动的 submission 列表时，该 draft 帖子不出现在结果中。

**TC-PERM-024：已发布活动下的 private 帖子在列表中不可见**
一个 published 活动关联了一个 visibility=private、status=published 的帖子（category:post submission）。非作者访客查询活动的 submission 列表时，该 private 帖子不出现在结果中。作者本人查询时可见。

**TC-PERM-025：private 帖子的关联 resource 在活动资源列表中不可见**
活动关联了一个 visibility=private 的帖子，该帖子挂载了 resource。非作者用户查询该活动下的资源列表时，该 resource 不出现在结果中（因关联帖子不可见）。

---

## 12. 用户旅程集成

### 12.1 Journey 2：匿名浏览

**TC-JOUR-002：匿名访客浏览公开内容**
未登录访客浏览平台。可以看到所有 published 状态的活动和帖子，支持按 tag/type 筛选；draft 内容不可见。

### 12.2 Journey 5：加入团队

**TC-JOUR-005：完整团队加入与审批流程**
Carol 申请加入 require_approval=true 的团队：
- 申请后 status 为 pending
- Owner Alice 批准后 status 变为 accepted，joined_at 赋值
- Bob 申请后被拒绝（status=rejected），再次申请后 status 恢复为 pending
- 读取团队成员列表返回所有成员及状态

### 12.3 Journey 7：团队报名活动

**TC-JOUR-007：完整团队报名流程**
1. Alice 创建团队并自动成为 Owner
2. Bob 申请加入并被 Alice 批准
3. 团队报名活动（创建 category:group 关系）
4. 创建参赛帖子并关联到活动（创建 category_post）— 引擎自动校验关联 rule 的约束（时间窗口、团队人数、提交次数、格式等），全部满足后关联成功
5. 若 rule 约束不满足（如截止日期已过、团队人数不足），关联被拒绝
6. 读取活动报名团队列表能查到该团队
7. 读取团队成员列表返回 Alice(owner) + Bob(member, accepted)

### 12.4 Journey 9：发送帖子

**TC-JOUR-009：创建日常帖子和参赛提案**
- 创建日常帖子（type=general），发布后公开可见（不受 rule 约束，未关联 category）
- 创建参赛提案（type=for_category），关联到活动（category:post submission）— 引擎自动校验该活动关联的 rule 约束（时间窗口、格式、提交次数、团队人数），全部满足后关联成功
- 帖子附带 Markdown 正文和 tags
- 若帖子关联了 category 且 rule 设置 `allow_public=false`，发布需走 `pending_review` 审核路径

### 12.5 Journey 10：获取证书

**TC-JOUR-010：完整证书颁发流程**
1. 关闭活动（status 更新为 closed）
2. 创建证书资源（resource，filename 为 certificate PDF）
3. 将证书资源关联到参赛帖子（post:resource，display_type=attachment）
4. 创建证书分享帖子（type=certificate，status=published）
5. 读取证书帖子和关联资源均可访问

### 12.6 Journey 11：编辑帖子

**TC-JOUR-011-1：编辑自己的帖子（版本管理）**
用户创建帖子 v1，然后创建 v2 并通过 post_post reference 关系链接。v2 发布后，两个版本均可读取，版本关系可查询。

**TC-JOUR-011-2：编辑他人帖子（副本机制）**
Bob 无法直接修改 Alice 的帖子。Bob 创建一个编辑副本（新帖子），通过 post:post reference 关系关联到原帖。副本帖子的 created_by 为 Bob。

### 12.7 Journey 12：删除帖子完整级联

**TC-JOUR-012：删除帖子后验证全部级联**
删除一个关联了 category:post（submission）、post:post（embed + reference）、post:resource（attachment + inline）以及多条 interaction（like + comment + rating）的帖子。删除后：
- 帖子被软删除
- 所有关系被解除
- 所有关联 interaction 被级联软删除

### 12.8 Journey 13：社区互动

**TC-JOUR-013：完整社区互动流程**
1. 用户 Dave 对帖子点赞，like_count 变为 1
2. 用户 Bob 对帖子发表评论，comment_count 变为 1
3. 评委对帖子进行多维度评分，average_rating 按权重计算
4. Dave 重复点赞被拒绝
5. 读取帖子，like_count、comment_count、average_rating 均正确

---

## 13. 资产转移（Resource Transfer）

> 资产转移基于现有 `post:resource` 和 `post:post` 关系实现，不需要 Schema 变更。核心操作为：解除旧 post:resource 关系 → 创建新 post:resource 关系，可选通过 post:post reference 记录溯源。

### 13.1 基础转移

**TC-TRANSFER-001：证书资源从组织者帖子转移到参赛帖**
组织者创建 resource（证书 PDF），先通过 post:resource 关联到自己的管理帖子。然后解除旧 post:resource 关系（DELETE），再创建新 post:resource 关系将该 resource 关联到参赛者的帖子。转移完成后：
- 旧帖子的 post:resource 列表不再包含该资源
- 新帖子的 post:resource 列表包含该资源
- resource 实体本身未被修改或删除

**TC-TRANSFER-002：提案间文件转移**
Post A 关联了 resource R（post:resource，display_type=attachment）。创建 Post B 后，将 R 关联到 Post B（CREATE post:resource），然后解除 Post A 与 R 的关联（DELETE post:resource）。转移完成后：
- Post A 的 post:resource 列表不含 R
- Post B 的 post:resource 列表包含 R
- R 可通过 Post B 正常读取

### 13.2 共享与溯源

**TC-TRANSFER-003：资源同时关联多个 post（共享模式）**
Post A 和 Post B 同时通过 post:resource 关联到同一 resource R。验证：
- 两条 post:resource 关系共存
- 两个帖子均可正常读取 R
- 删除其中一条 post:resource 关系不影响另一条

**TC-TRANSFER-004：转移溯源（通过 post:post reference 记录来源）**
Post A 持有 resource R。创建 Post B，通过 post:post（source=B, target=A, relation_type=reference）记录来源关系，再将 R 从 A 转移到 B（DELETE A 的 post:resource，CREATE B 的 post:resource）。转移完成后：
- 通过 Post B 的 post:post reference 关系可追溯到 Post A（R 的原始来源）
- Post A 不再关联 R，Post B 持有 R

---

## 14. 好友（User Follow / Friend）

> 好友功能基于新增的第 8 种关系 `user:user`（也称 `user_user`）实现。关注为单向关系，互关即好友。

### 14.1 关注

**TC-FRIEND-001：用户 A 关注用户 B**
创建 user:user 关系（source_user_id=A, target_user_id=B, relation_type=follow）。创建成功后，读取 A 的关注列表包含 B。

**TC-FRIEND-002：用户 B 回关用户 A，双方成为好友**
在 TC-FRIEND-001 基础上，创建 user:user（source_user_id=B, target_user_id=A, relation_type=follow）。查询 A 和 B 的互关状态 = true（好友）。

**TC-FRIEND-003：单向关注不构成好友**
仅 A 关注了 B（只有一条 A→B follow 记录）。查询 A 和 B 的好友状态 = false。

### 14.2 取关与拉黑

**TC-FRIEND-004：取消关注**
删除 user:user 关系（source_user_id=A, target_user_id=B, relation_type=follow）。删除后 A 的关注列表不再包含 B，好友关系解除。

**TC-FRIEND-005：拉黑用户**
A 创建 user:user（source_user_id=A, target_user_id=B, relation_type=block）。即使 B 已关注 A，A 的好友列表不含 B（block 优先级高于 follow）。

**TC-FRIEND-006：被拉黑用户无法关注**
A 已 block B。B 尝试创建 follow 关系指向 A（source_user_id=B, target_user_id=A, relation_type=follow）。系统拒绝操作，返回 "blocked" 错误。

### 14.3 级联与删除

**TC-FRIEND-007：软删除用户后级联解除 user:user**
用户 A 被软删除。A 的所有 user:user 关系（作为 source 或 target）被解除（硬删除）。

### 14.4 负向/边界

**TC-FRIEND-900：自己关注自己被拒绝**
用户 A 创建 user:user（source_user_id=A, target_user_id=A, relation_type=follow）。系统拒绝操作，返回 "cannot follow self" 错误。

**TC-FRIEND-901：重复关注被拒绝**
A 已关注 B，再次创建相同的 follow 关系。系统拒绝操作，返回唯一性冲突错误。唯一性约束：(source_user_id, target_user_id, relation_type)。

**TC-FRIEND-902：非法 relation_type 被拒绝**
创建 user:user 时 relation_type 为 "mute"。系统拒绝操作，返回枚举值无效错误（合法值为 follow | block）。

---

## 15. 活动关联（Category Association）

> 活动关联功能基于新增的第 9 种关系 `category:category`（也称 `category_category`）实现。支持三种关联类型：赛段（stage）、赛道（track）、前置条件（prerequisite）。

### 15.1 赛段（Stage）

**TC-STAGE-001：创建连续赛段关联**
创建 3 个 category（A/B/C），创建 category:category 关系：A→B（relation_type=stage, stage_order=1），B→C（relation_type=stage, stage_order=2）。读取赛段链返回 A→B→C 的顺序关系。

**TC-STAGE-002：按 stage_order 排序读取赛段**
查询 category A 的所有 stage 类型 category:category 关系，返回结果按 stage_order 升序排列。

**TC-STAGE-003：赛段未完成时无法进入下一赛段**
活动 A（status=published，进行中），活动 B 为 A 的下一赛段（stage_order=2）。团队尝试报名活动 B（CREATE category:group）。系统拒绝操作，返回 "prerequisite stage not completed" 错误。

**TC-STAGE-004：赛段完成后可进入下一赛段**
将活动 A 更新为 status=closed。团队报名活动 B（CREATE category:group）。系统允许操作。

### 15.2 赛道（Track）

**TC-TRACK-001：创建并行赛道关联**
创建父活动 Main 和 2 个子活动（Track1/Track2）。创建 category:category 关系：Main→Track1（relation_type=track），Main→Track2（relation_type=track）。查询 Main 的赛道列表返回 Track1 和 Track2。

**TC-TRACK-002：团队可同时参加不同赛道**
Team A 报名 Track1（category:group）和 Track2（category:group）。两次报名均成功（不同赛道不受互斥约束，但同一赛道内的 Rule 约束仍然有效）。

**TC-TRACK-003：团队在同一赛道内受 Rule 约束**
Track1 关联了 max_submissions=1 的 Rule。团队已提交一次后再次提交被拒绝。不影响其在 Track2 的提交。

### 15.3 前置条件（Prerequisite）

**TC-PREREQ-001：悬赏活动作为前置条件关联到常规赛**
创建悬赏活动 Bounty（type=operation）和常规赛 Competition（type=competition）。创建 category:category（source_category_id=Bounty, target_category_id=Competition, relation_type=prerequisite）。关系创建成功。

**TC-PREREQ-002：前置活动完成后团队可报名目标活动**
Bounty 活动更新为 status=closed，团队在 Bounty 中有 accepted 的 category:group 记录。团队报名 Competition（CREATE category:group）。系统允许操作。

**TC-PREREQ-003：前置活动未完成时团队报名目标活动被拒绝**
Bounty 活动仍为 status=published（进行中）。团队尝试报名 Competition。系统拒绝操作，返回 "prerequisite not completed" 错误。

**TC-PREREQ-004：前置活动中组建的团队保持完整进入目标活动**
团队在 Bounty 活动中有 3 名 accepted 成员。报名 Competition 后，READ group:user 返回同样的 3 名成员（团队不因活动切换而变化）。

### 15.4 负向/边界

**TC-CATREL-900：重复创建同一活动关联被拒绝**
A→B（stage）关系已存在，再次创建相同的 category:category 关系。系统拒绝操作，返回唯一性冲突错误。唯一性约束：(source_category_id, target_category_id)。

**TC-CATREL-901：自引用被拒绝**
创建 category:category（source_category_id=A, target_category_id=A）。系统拒绝操作，返回 "cannot reference self" 错误。

**TC-CATREL-902：赛段循环依赖被拒绝**
A→B（stage），B→C（stage），尝试创建 C→A（stage）。系统拒绝操作，返回 "circular dependency detected" 错误。

**TC-CATREL-903：非法 relation_type 被拒绝**
创建 category:category 时 relation_type 为 "sponsor"。系统拒绝操作，返回枚举值无效错误（合法值为 stage | track | prerequisite）。

---

## 附录：已知 Bug 与限制

> 以下 Bug 在测试中发现，已记录于 `consolidated-test-report.md`。

| 编号 | 描述 | 严重程度 |
|------|------|----------|
| BUG-01 | `create_relation` 缺少枚举字段验证（如 group_user.role 可传入非法值） | P0 |
| BUG-02 | User 级联删除后未更新目标 Post 缓存计数（like_count/comment_count 陈旧） | P0 |
| BUG-03 | `delete group` 未级联处理 group_user 关系（Spec 矛盾待澄清） | P1 |
| BUG-04 | `delete user` 未级联处理 group_user 关系 + 未标记离组（Spec 矛盾待澄清） | P1 |
| BUG-05 | 引擎无 Restore 命令（Spec 定义了恢复操作但引擎未实现） | P2 |
| BUG-06 | 引擎无 RBAC 权限控制（`--user` 仅设置 created_by，不检查角色） | P2 |
| BUG-07 | 引擎无可见性过滤（draft 内容对所有人可见） | P2 |
| BUG-08 | 无跨组用户唯一性约束（同用户可通过不同团队报名同一活动） | P2 |
| BUG-09 | scoring_criteria 无结构验证（权重和可超过 100） | P3 |
| BUG-10 | target_interaction 关系需手动创建（应自动创建） | P3 |
| BUG-11 | 引用完整性 — 可删除仍有内容的用户 | P3 |
| ~~BUG-12~~ | ~~引擎无 Rule 执行校验（category_post 不校验时间窗口/提交次数/格式/团队人数；group_user 不校验团队上限；post 状态变更不校验发布路径）~~ **已修复：engine.py 新增 pre-operation hook，在 create_relation(category_post)、create_relation(group_user)、update_content(post status) 三个操作点自动校验关联 rule 的所有约束** | ~~P0~~ → Fixed |
