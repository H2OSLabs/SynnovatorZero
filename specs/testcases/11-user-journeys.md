# 用户旅程集成

> **格式约定：** 每条用例仅描述「场景」与「预期结果」，不包含测试方法和执行过程。

---

## 11.1 Journey 2：匿名浏览

**TC-JOUR-002：匿名访客浏览公开内容**
未登录访客浏览平台。可以看到所有 published 状态的活动和帖子，支持按 tag/type 筛选；draft 内容不可见。

## 11.2 Journey 5：加入团队

**TC-JOUR-005：完整团队加入与审批流程**
Carol 申请加入 require_approval=true 的团队：
- 申请后 status 为 pending
- Owner Alice 批准后 status 变为 accepted，joined_at 赋值
- Bob 申请后被拒绝（status=rejected），再次申请后 status 恢复为 pending
- 读取团队成员列表返回所有成员及状态

## 11.3 Journey 7：团队报名活动

**TC-JOUR-007：完整团队报名流程**
1. Alice 创建团队并自动成为 Owner
2. Bob 申请加入并被 Alice 批准
3. 团队报名活动（创建 category:group 关系）
4. 创建参赛帖子并关联到活动（创建 category_post）— 引擎自动校验关联 rule 的约束（时间窗口、团队人数、提交次数、格式等），全部满足后关联成功
5. 若 rule 约束不满足（如截止日期已过、团队人数不足），关联被拒绝
6. 读取活动报名团队列表能查到该团队
7. 读取团队成员列表返回 Alice(owner) + Bob(member, accepted)

## 11.4 Journey 9：发送帖子

**TC-JOUR-009：创建日常帖子和参赛提案**
- 创建日常帖子（type=general），发布后公开可见（不受 rule 约束，未关联 category）
- 创建参赛提案（type=for_category），关联到活动（category:post submission）— 引擎自动校验该活动关联的 rule 约束（时间窗口、格式、提交次数、团队人数），全部满足后关联成功
- 帖子附带 Markdown 正文和 tags
- 若帖子关联了 category 且 rule 设置 `allow_public=false`，发布需走 `pending_review` 审核路径

## 11.5 Journey 10：获取证书

**TC-JOUR-010：完整证书颁发流程**
1. 关闭活动（status 更新为 closed）
2. 创建证书资源（resource，filename 为 certificate PDF）
3. 将证书资源关联到参赛帖子（post:resource，display_type=attachment）
4. 创建证书分享帖子（type=certificate，status=published）
5. 读取证书帖子和关联资源均可访问

## 11.6 Journey 11：编辑帖子

**TC-JOUR-011-1：编辑自己的帖子（版本管理）**
用户创建帖子 v1，然后创建 v2 并通过 post_post reference 关系链接。v2 发布后，两个版本均可读取，版本关系可查询。

**TC-JOUR-011-2：编辑他人帖子（副本机制）**
Bob 无法直接修改 Alice 的帖子。Bob 创建一个编辑副本（新帖子），通过 post:post reference 关系关联到原帖。副本帖子的 created_by 为 Bob。

## 11.7 Journey 12：删除帖子完整级联

**TC-JOUR-012：删除帖子后验证全部级联**
删除一个关联了 category:post（submission）、post:post（embed + reference）、post:resource（attachment + inline）以及多条 interaction（like + comment + rating）的帖子。删除后：
- 帖子被物理删除
- 所有关系被解除
- 所有关联 interaction 被级联硬删除

## 11.8 Journey 13：社区互动

**TC-JOUR-013：完整社区互动流程**
1. 用户 Dave 对帖子点赞，like_count 变为 1
2. 用户 Bob 对帖子发表评论，comment_count 变为 1
3. 评委对帖子进行多维度评分，average_rating 按权重计算
4. Dave 重复点赞被拒绝
5. 读取帖子，like_count、comment_count、average_rating 均正确
