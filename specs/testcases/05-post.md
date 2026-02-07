# 帖子（Post）模块

> **格式约定：** 每条用例仅描述「场景」与「预期结果」，不包含测试方法和执行过程。

---

## 5.1 基础创建

**TC-POST-001：最小字段创建帖子**
仅提供 title 和正文创建帖子。创建完成后，type 默认为 general，status 默认为 draft，缓存统计字段初始化为 like_count=0、comment_count=0、average_rating=null。

**TC-POST-002：显式发布帖子**
创建时指定 status=published。创建完成后，帖子为已发布状态，公开可读。

**TC-POST-003：带 tags 创建帖子**
创建帖子时附带 tags（如 ["找队友", "提案"]）。创建完成后，可通过 tag 筛选查询命中该帖子。

**TC-POST-004：按 type 筛选帖子**
创建多种 type 的帖子（general、team、proposal、certificate）后，按 type=proposal 筛选。返回结果仅包含 type=proposal 的帖子。

## 5.2 类型语义覆盖

**TC-POST-010：创建 team 类型帖子**
创建一个 type=team 的帖子（团队卡片），包含团队介绍和成员信息。创建成功后，后续可被嵌入到其它帖子（post:post embed 关系）。

**TC-POST-011：创建 profile 类型帖子**
创建一个 type=profile 的帖子（个人资料卡片）。创建成功。

**TC-POST-012：创建 proposal 类型帖子**
创建一个 type=proposal 的帖子（参赛提案）。创建成功后，可被关联到某个活动（category:post relation_type=submission）。

**TC-POST-013：创建 certificate 类型帖子**
创建一个 type=certificate 的帖子（证书分享帖）。创建成功后，可挂载 resource（证书文件）作为附件或内联。

## 5.3 状态流转

**TC-POST-030：帖子进入 pending_review 状态**
创建帖子后将 status 更新为 pending_review。若帖子已关联 category 且 rule 设置了 `require_review=true`，这是正确的提交路径。更新成功。

**TC-POST-031：帖子被审核通过（pending_review → published）**
将 pending_review 状态的帖子更新为 published。此操作代表审核人主动批准，即使 rule 设置 `allow_public=false`，审核通过路径也不受限。更新成功后，status 为 published。

**TC-POST-032：帖子被驳回（pending_review → rejected）**
将 pending_review 状态的帖子更新为 rejected。更新成功后，status 为 rejected。

**TC-POST-033：草稿发布（draft → published）**
将 draft 状态的帖子更新为 published。若帖子未关联任何 category 或关联 category 的 rule 允许公开发布（`allow_public=true`），更新成功，updated_at 变更。若 rule 设置 `allow_public=false`，更新被拒绝（见 TC-RULE-106）。

## 5.4 版本管理

**TC-POST-040：通过新帖子实现版本管理**
创建提案帖子 v1，再创建 v2，通过 post_post（relation_type=reference）关系链接新旧版本。两个帖子有独立 id，通过关系保留版本关联。

**TC-POST-041：发布新版本**
将新版本帖子的 status 更新为 published。更新成功。

## 5.5 标签操作

**TC-POST-050：添加标签（+tag 语法）**
对帖子使用 "+devlog" 和 "+update" 语法分别添加标签。添加后 tags 列表包含新标签。

**TC-POST-051：移除标签（-tag 语法）**
对帖子使用 "-devlog" 语法移除标签。移除后 tags 不再包含 devlog，但仍包含 update。

**TC-POST-052："选择已有帖子"报名（标签打标）**
对已有帖子使用 "+for_ai_hackathon" 标签实现"选择已有帖子"报名活动。更新后 tags 列表中包含 for_ai_hackathon。

## 5.6 更新帖子正文

**TC-POST-060：更新帖子 title 和 Markdown body**
同时更新帖子的 title 和 Markdown 正文内容。更新完成后，title 为新值，has_body 为 true。

## 5.7 可见性控制（Visibility）

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

## 5.8 负向/边界

**TC-POST-900：缺少 title 被拒绝**
创建帖子时不提供 title。系统拒绝创建，返回缺少必填字段错误。

**TC-POST-901：非法 type/status 枚举被拒绝**
创建帖子时指定 type 为 "foo" 或 status 为 "archived"。系统拒绝创建，返回枚举值无效错误。

**TC-POST-903：非法 visibility 枚举被拒绝**
创建帖子时指定 visibility 为 "restricted"。系统拒绝创建，返回枚举值无效错误（合法值为 public | private）。

**TC-POST-902：未登录用户创建帖子被拒绝**
未提供用户身份的情况下创建帖子。系统拒绝操作，返回需要认证的错误。
