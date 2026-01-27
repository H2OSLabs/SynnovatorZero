# 数据操作示例

本文档提供 Synnovator 平台各内容类型和关系的操作示例，以及完整的场景串联演示。

> 数据类型 Schema 详见 [data-types.md](./data-types.md)，关系 Schema 详见 [relationships.md](./relationships.md)，CRUD 操作详见 [crud-operations.md](./crud-operations.md)。

---

## 内容示例

### 创建一个比赛活动（category）

```yaml
---
name: "2025 AI Hackathon"
description: "面向全球开发者的 AI 创新大赛"
type: competition
status: draft
cover_image: "https://example.com/cover.png"
start_date: "2025-03-01T00:00:00Z"
end_date: "2025-03-15T23:59:59Z"
---

## 活动介绍

本次 Hackathon 面向全球 AI 开发者，鼓励参赛者利用大语言模型构建创新应用。

## 赛道

- **应用创新赛道**：构建面向终端用户的 AI 应用
- **工具赛道**：构建面向开发者的 AI 工具

## 奖项

| 奖项 | 奖金 |
|------|------|
| 一等奖 | ¥50,000 |
| 二等奖 | ¥20,000 |
| 三等奖 | ¥10,000 |
```

### 创建活动规则（rule）

```yaml
---
name: "AI Hackathon 提交规则"
description: "2025 AI Hackathon 参赛提交规范"
allow_public: true
require_review: true
reviewers: ["user_judge_01", "user_judge_02", "user_judge_03"]
submission_start: "2025-03-01T00:00:00Z"
submission_deadline: "2025-03-14T23:59:59Z"
submission_format: ["markdown", "pdf", "zip"]
max_submissions: 3
min_team_size: 1
max_team_size: 5
scoring_criteria:
  - name: "创新性"
    weight: 30
    description: "方案的原创性和创新程度"
  - name: "技术实现"
    weight: 30
    description: "代码质量、架构设计、技术深度"
  - name: "实用价值"
    weight: 25
    description: "解决实际问题的程度和商业潜力"
  - name: "演示效果"
    weight: 15
    description: "Demo 完成度和展示效果"
---

## 提交要求

1. 提交内容必须包含：项目说明文档（Markdown）、源代码（zip）、演示视频链接
2. 项目说明需涵盖：问题定义、解决方案、技术架构、使用说明
3. 所有提交内容必须为参赛期间原创

## 评审流程

- 初审：提交截止后 3 个工作日内完成
- 复审：初审通过项目进入路演环节
- 终审：路演后由评委打分，按加权总分排名
```

### 创建参赛提交帖（post, type=for_category）

```yaml
---
title: "AI 代码审查助手 — CodeReview Copilot"
type: for_category
tags: ["AI", "开发者工具", "代码审查"]
status: published
---

## 项目简介

CodeReview Copilot 是一款基于大语言模型的智能代码审查工具，
能自动识别代码中的潜在问题并给出改进建议。

## 技术方案

- 基于 AST 解析 + LLM 理解的双层分析架构
- 支持 Python、JavaScript、Go 等主流语言

## 演示

[Demo 视频](https://example.com/demo.mp4)
```

### 创建团队介绍帖（post, type=team）

```yaml
---
title: "Team Synnovator"
type: team
tags: ["全栈", "AI"]
status: published
---

## 团队介绍

我们是一支专注于 AI 应用开发的全栈团队，成员来自不同技术背景。

## 成员

- **Alice** — 后端开发，擅长分布式系统
- **Bob** — 前端开发，擅长 React/Next.js
- **Carol** — AI 工程师，擅长 LLM 应用
```

### 创建个人说明帖（post, type=profile）

```yaml
---
title: "关于我"
type: profile
tags: ["后端", "AI", "开源"]
status: published
---

## 自我介绍

全栈开发者，3 年 AI 应用开发经验，热爱开源。

## 技能

- Python / Go / TypeScript
- LLM 应用开发
- 分布式系统设计

## 联系方式

- GitHub: @alice
- Email: alice@example.com
```

### 注册用户（user）

```yaml
---
username: "alice"
email: "alice@example.com"
display_name: "Alice Chen"
avatar_url: "https://example.com/avatars/alice.png"
bio: "全栈开发者，AI 爱好者"
role: participant
---
```

### 创建团队（group）

```yaml
---
name: "Team Synnovator"
description: "AI Hackathon 参赛团队"
visibility: public
max_members: 5
require_approval: true
---
```

### 上传资源（resource）

```yaml
---
filename: "project-demo.mp4"
display_name: "项目演示视频"
description: "CodeReview Copilot 功能演示，时长 3 分钟"
---
```

---

## 关系示例

### 关联规则到活动（category : rule）

```yaml
# 将提交规则绑定到 AI Hackathon
category_id: "cat_ai_hackathon_2025"
rule_id: "rule_submission_01"
priority: 1
```

### 报名参赛 — 关联帖子到活动（category : post）

```yaml
# 将参赛提交关联到活动
category_id: "cat_ai_hackathon_2025"
post_id: "post_codereview_copilot"
relation_type: submission
```

### 团队报名活动（category : group）

```yaml
# Team Synnovator 报名参加 AI Hackathon
category_id: "cat_ai_hackathon_2025"
group_id: "grp_team_synnovator"
# registered_at 自动生成
```

### 帖子中嵌入团队卡片（post : post）

```yaml
# 在参赛帖中嵌入团队介绍
source_post_id: "post_codereview_copilot"
target_post_id: "post_team_synnovator"
relation_type: embed
position: 1
```

### 帖子引用另一个帖子（post : post）

```yaml
# 帖子中引用已有提案
source_post_id: "post_looking_for_teammates"
target_post_id: "post_codereview_copilot"
relation_type: reference
position: 0
```

### 帖子关联附件（post : resource）

```yaml
# 将演示视频附加到参赛帖
post_id: "post_codereview_copilot"
resource_id: "res_project_demo_mp4"
display_type: inline
position: 0
```

### 成员加入团队（group : user）

```yaml
# 创建者自动成为 owner（status 自动设为 accepted）
group_id: "grp_team_synnovator"
user_id: "user_alice"
role: owner
status: accepted
```

```yaml
# 新成员申请加入（require_approval=true 时，status 初始为 pending）
group_id: "grp_team_synnovator"
user_id: "user_bob"
role: member
status: pending
```

### 组队审批流程（group : user status 变更）

```yaml
# 步骤 1: Bob 申请加入团队（CREATE group:user）
group_id: "grp_team_synnovator"
user_id: "user_bob"
role: member
status: pending              # require_approval=true → 自动为 pending
```

```yaml
# 步骤 2: Alice（Owner）批准 Bob 的申请（UPDATE group:user）
group_id: "grp_team_synnovator"
user_id: "user_bob"
status: accepted             # pending → accepted
# joined_at 自动记录为此刻时间
```

```yaml
# 备选: Alice（Owner）拒绝 Carol 的申请（UPDATE group:user）
group_id: "grp_team_synnovator"
user_id: "user_carol"
status: rejected             # pending → rejected
```

### 对帖子点赞（target : interaction, type=like）

```yaml
# 步骤 1: 创建 interaction 记录
---
type: like
---
```

```yaml
# 步骤 2: 通过 target:interaction 关系关联到目标（触发缓存更新 + 去重校验）
target_type: post
target_id: "post_codereview_copilot"
interaction_id: "iact_like_001"
```

### 发表评论与嵌套回复（target : interaction, type=comment）

```yaml
# 步骤 1: 创建顶层评论 interaction
---
type: comment
value: "方案很有创意！AST + LLM 的组合方式值得关注。请问支持哪些 CI/CD 集成？"
---
```

```yaml
# 步骤 2: 通过 target:interaction 关系关联到目标
target_type: post
target_id: "post_codereview_copilot"
interaction_id: "iact_comment_001"
```

```yaml
# 嵌套回复: 步骤 1 — 创建回复 interaction（parent_id 指向顶层评论）
---
type: comment
parent_id: "iact_comment_001"
value: "目前支持 GitHub Actions 和 GitLab CI，Jenkins 插件正在开发中。"
---
```

```yaml
# 嵌套回复: 步骤 2 — 通过 target:interaction 关系关联到同一目标
target_type: post
target_id: "post_codereview_copilot"
interaction_id: "iact_comment_002"
```

### 评委多维度评分（target : interaction, type=rating）

```yaml
# 步骤 1: 创建评分 interaction —— value 为多维度对象，Key 与 Rule.scoring_criteria.name 一一对应
# 每个维度统一 0-100 分
---
type: rating
value:
  创新性: 87                # 0-100，对应 Rule scoring_criteria weight=30
  技术实现: 82              # 0-100，对应 weight=30
  实用价值: 78              # 0-100，对应 weight=25
  演示效果: 91              # 0-100，对应 weight=15
  _comment: "架构设计清晰，建议完善错误处理"
---
```

```yaml
# 步骤 2: 通过 target:interaction 关系关联到参赛帖（触发 average_rating 重算）
target_type: post
target_id: "post_codereview_copilot"
interaction_id: "iact_rating_001"
```

```
# 系统按 weight 自动加权计算:
#   创新性:   87 × 30/100 = 26.10
#   技术实现: 82 × 30/100 = 24.60
#   实用价值: 78 × 25/100 = 19.50
#   演示效果: 91 × 15/100 = 13.65
#   ─────────────────────────────
#   加权总分: 83.85
#
# 此分数计入 post.average_rating 的均值计算
```

---

## 场景串联示例：从创建活动到互动评审

以下展示一个完整场景中涉及的数据操作序列：

```
=== 阶段一：组织者创建活动 ===
1.  Organizer: CREATE category           → 创建 "2025 AI Hackathon"
2.  Organizer: CREATE rule               → 创建提交规则（含多维度 scoring_criteria）
3.  Organizer: CREATE category:rule      → 将规则关联到活动
4.  Organizer: UPDATE category (status→published) → 发布活动

=== 阶段二：参赛者组队（含审批流程） ===
5.  Participant(Alice): READ category + READ rule → 浏览活动详情和规则
6.  Participant(Alice): CREATE group     → 创建团队（require_approval=true）
7.  Participant(Alice): CREATE group:user (role=owner, status=accepted) → 创建者自动成为组长
8.  Participant(Bob):   CREATE group:user (role=member, status=pending) → Bob 申请加入团队
9.  Participant(Alice): UPDATE group:user (status→accepted) → Alice 批准 Bob 加入
10. Participant(Carol): CREATE group:user (role=member, status=pending) → Carol 申请加入
11. Participant(Alice): UPDATE group:user (status→rejected) → Alice 拒绝 Carol

=== 阶段三：团队报名活动 ===
12. Participant(Alice): CREATE category:group → 团队报名活动（绑定 group 到 category）

=== 阶段四：参赛提交 ===
13. Participant(Alice): CREATE post (type=team)  → 创建团队介绍帖
14. Participant(Alice): CREATE post (type=for_category) → 创建参赛提交帖
15. Participant(Alice): CREATE post:post (embed) → 在参赛帖中嵌入团队卡片
16. Participant(Alice): CREATE resource  → 上传演示视频
17. Participant(Alice): CREATE post:resource → 关联视频到参赛帖
18. Participant(Alice): CREATE category:post (submission) → 将参赛帖关联到活动
19. Participant(Alice): UPDATE post (status→published) → 发布参赛帖

=== 阶段五：社区互动（两步创建：interaction + target:interaction） ===
20. Participant(Dave): CREATE interaction (type=like)    → 创建点赞记录
21. Participant(Dave): CREATE target:interaction         → 关联点赞到帖子
    [系统自动] 去重校验 + UPDATE post.like_count (+1)   → 校验 + 更新计数缓存
22. Participant(Eve):  CREATE interaction (type=comment) → 创建评论记录
23. Participant(Eve):  CREATE target:interaction         → 关联评论到帖子
    [系统自动] UPDATE post.comment_count (+1)           → 更新评论计数缓存
24. Participant(Alice): CREATE interaction (type=comment, parent_id=上一条) → 创建回复记录
25. Participant(Alice): CREATE target:interaction        → 关联回复到帖子
    [系统自动] UPDATE post.comment_count (+1)           → 更新评论计数缓存

=== 阶段六：评审多维度评分（两步创建） ===
26. Organizer(Judge): CREATE interaction (type=rating)  → 创建评分记录
    value: { 创新性: 87, 技术实现: 82, 实用价值: 78, 演示效果: 91 }
27. Organizer(Judge): CREATE target:interaction         → 关联评分到参赛帖
    [系统自动] UPDATE post.average_rating               → 重算加权总分均值（83.85）
```
