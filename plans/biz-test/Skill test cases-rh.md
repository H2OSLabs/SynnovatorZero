# Synnovator Skill 测试用例库（完整版）

> 本文档整合了原有测试用例与 `test-gap.md` 覆盖分析中发现的所有缺口，按模块分类。
> 格式统一为：【用例描述】、【前置条件】、【Mock Data】、【预期结果】。
> 标注 `[GAP]` 的用例为从 test-gap.md 合并的新增场景。

---

## 目录

1. [Post 模块](#1-post-模块)
2. [Resource 模块](#2-resource-模块)
3. [List 模块（category:post 列表查询）](#3-list-模块categorypost-列表查询)
4. [Interaction 模块](#4-interaction-模块)
5. [Category 模块 [GAP]](#5-category-模块-gap)
6. [Rule 模块 [GAP]](#6-rule-模块-gap)
7. [User 模块 [GAP]](#7-user-模块-gap)
8. [Group 模块 [GAP]](#8-group-模块-gap)
9. [Category:Group 关系 [GAP]](#9-categorygroup-关系-gap)
10. [关系 UPDATE/DELETE [GAP]](#10-关系-updatedelete-gap)
11. [软删除与恢复 [GAP]](#11-软删除与恢复-gap)
12. [权限边界 [GAP]](#12-权限边界-gap)
13. [用户旅程集成 [GAP]](#13-用户旅程集成-gap)
14. [通用 Mock Data 基座](#14-通用-mock-data-基座)

---

## 1. Post 模块

### 1.1 A1. 基础可用性

**TC-POST-001：最小字段创建（general, draft）**

- 【用例描述】仅提供 title + 正文创建帖子，验证默认值
- 【前置条件】已登录用户（participant）
- 【Mock Data】
```yaml
---
title: "测试最小字段帖子"
---
这是一篇最小字段帖子的正文。
```
- 【预期结果】
  - 创建成功；type 默认 general；status 默认 draft
  - 缓存统计字段初始化：`like_count=0`, `comment_count=0`, `average_rating=null`
  - READ post 能查到该帖

**TC-POST-002：显式发布（general, published）**

- 【用例描述】创建时指定 status=published，验证公开可读
- 【前置条件】已登录用户
- 【Mock Data】
```yaml
---
title: "测试显式发布帖子"
status: published
---
这是一篇已发布帖子。
```
- 【预期结果】创建成功；READ post（公开视角）可读到已发布帖

**TC-POST-003：带 tags 创建**

- 【用例描述】创建带 tags 的帖子，验证按 tag 筛选
- 【前置条件】已登录用户
- 【Mock Data】
```yaml
---
title: "【找队友】AI Hackathon 2025 一起组队做开发者工具"
type: general
tags: ["找队友", "提案"]
status: published
---
我们计划做一个"AI 代码审查助手"，欢迎前端/后端/LLM 应用同学加入。
```
- 【预期结果】READ post 支持按 tag 筛选命中；验证引擎 tag 过滤参数语法

**TC-POST-004：按 type 筛选**

- 【用例描述】创建不同 type 帖子后按 type 筛选
- 【前置条件】已创建多种 type 的 post
- 【Mock Data】使用 B4 帖子样本（general + team + for_category + certificate）
- 【预期结果】`READ post --filters '{"type": "for_category"}'` 仅返回 type=for_category 的帖子

---

### 1.2 A2. type 语义覆盖

**TC-POST-010：type=team（团队卡片内容）**

- 【用例描述】创建 team 类型帖子
- 【前置条件】已登录用户
- 【Mock Data】
```yaml
---
title: "Team Synnovator"
type: team
tags: ["全栈", "AI"]
status: published
---
## 团队介绍
我们是一支专注于 AI 应用开发的全栈团队。

## 成员
- Alice — 后端 / 分布式
- Bob — 前端 / React
- Carol — AI / LLM 应用
```
- 【预期结果】创建成功；后续可被嵌入到其它帖子（post:post embed）

**TC-POST-011：type=profile（个人资料卡片）**

- 【用例描述】创建 profile 类型帖子
- 【前置条件】已登录用户
- 【Mock Data】
```yaml
---
title: "关于我"
type: profile
tags: ["后端", "AI", "开源"]
status: published
---
## 自我介绍
全栈开发者，3 年 AI 应用开发经验。
```
- 【预期结果】创建成功；能作为用户主页/卡片渲染的数据源

**TC-POST-012：type=for_category（参赛提交/提案）**

- 【用例描述】创建 for_category 类型帖子
- 【前置条件】已登录用户
- 【Mock Data】
```yaml
---
title: "AI 代码审查助手 — CodeReview Copilot"
type: for_category
tags: ["AI", "开发者工具", "代码审查"]
status: published
---
## 项目简介
CodeReview Copilot 是一款基于大语言模型的智能代码审查工具。

## 技术方案
- AST 解析 + LLM 理解的双层分析
- 支持 Python / JavaScript / Go

## 演示
[Demo 视频](https://example.com/demo.mp4)
```
- 【预期结果】创建成功；能被关联到某个活动（category:post relation_type=submission）

**TC-POST-013：type=certificate（证书分享帖）**

- 【用例描述】创建 certificate 类型帖子
- 【前置条件】已登录用户
- 【Mock Data】
```yaml
---
title: "2025 AI Hackathon 一等奖证书"
type: certificate
tags: ["证书", "AI Hackathon"]
status: published
---
## 获奖信息
- 活动: 2025 AI Hackathon
- 奖项: 一等奖
- 团队: Team Synnovator
```
- 【预期结果】创建成功；后续能挂 resource（证书文件）作为附件/内联

---

### 1.3 A3. 关系驱动的可用性

**TC-POST-020：提案帖嵌入团队卡片（post:post embed）**

- 【用例描述】创建 embed 类型的 post:post 关系
- 【前置条件】已存在 team post 和 for_category post
- 【Mock Data】
```yaml
source_post_id: "post_codereview_copilot"
target_post_id: "post_team_synnovator"
relation_type: embed
position: 1
```
- 【预期结果】READ post:post 能查询到 embed 关系；position 正确

**TC-POST-021：提案帖引用另一帖（post:post reference）**

- 【用例描述】创建 reference 类型的 post:post 关系
- 【前置条件】已存在两个 post
- 【Mock Data】
```yaml
source_post_id: "post_looking_for_teammates"
target_post_id: "post_codereview_copilot"
relation_type: reference
position: 0
```
- 【预期结果】引用关系可查询；用于"证据链/关联阅读"

**TC-POST-022：帖子回复另一帖（post:post reply）**

- 【用例描述】创建 reply 类型的 post:post 关系
- 【前置条件】已存在两个 post
- 【Mock Data】
```yaml
source_post_id: "post_reply_to_copilot"
target_post_id: "post_codereview_copilot"
relation_type: reply
position: 0
```
- 【预期结果】READ post:post 可按 `relation_type=reply` 筛选；position 正确

---

### 1.4 A4. 状态流转

**TC-POST-030：status=pending_review**

- 【用例描述】创建 pending_review 状态的帖子
- 【前置条件】已登录用户
- 【Mock Data】
```yaml
---
title: "待审核提案"
type: for_category
status: pending_review
---
此帖因 Rule 要求需审核后才能发布。
```
- 【预期结果】创建成功；此状态用于"Rule 不允许直接发布时"

**TC-POST-031：status=rejected**

- 【用例描述】创建 rejected 状态的帖子
- 【前置条件】已登录用户
- 【Mock Data】
```yaml
---
title: "被驳回的提案"
type: for_category
status: rejected
---
审核未通过。
```
- 【预期结果】创建成功；引擎应接受直接创建

**TC-POST-032：UPDATE post 状态变更（draft→published）**

- 【用例描述】更新帖子状态从 draft 到 published
- 【前置条件】已存在一个 draft 帖子
- 【Mock Data】
```yaml
# 原始帖子
---
title: "草稿帖子"
status: draft
---
# UPDATE 操作
status: published
```
- 【预期结果】更新成功；updated_at 变更

---

### 1.5 A5. 负向/边界

**TC-POST-900：缺少 title**

- 【用例描述】创建帖子时不提供 title
- 【前置条件】已登录用户
- 【Mock Data】
```yaml
---
type: general
status: draft
---
没有标题的帖子。
```
- 【预期结果】创建失败；错误明确指出必填字段缺失（title）

**TC-POST-901：非法 type / status**

- 【用例描述】使用非法枚举值创建帖子
- 【前置条件】已登录用户
- 【Mock Data】
```yaml
---
title: "非法类型帖子"
type: foo
status: archived
---
```
- 【预期结果】创建失败；错误明确指出枚举可选范围

**TC-POST-902：未登录用户创建 post**

- 【用例描述】无认证状态下创建帖子
- 【前置条件】未登录
- 【Mock Data】同 TC-POST-001
- 【预期结果】拒绝；错误说明需要认证

**TC-POST-903：用户唯一性约束（username/email）**

- 【用例描述】创建重复 username 或 email 的用户
- 【前置条件】已存在 user_alice
- 【Mock Data】
```yaml
---
username: "alice"
email: "alice-dup@example.com"
display_name: "Alice Duplicate"
role: participant
---
```
- 【预期结果】创建失败；错误指出唯一性冲突

---

## 2. Resource 模块

### 2.1 A1. 基础可用性

**TC-RES-001：最小字段上传（只带 filename）**

- 【用例描述】仅提供 filename 创建资源
- 【前置条件】已登录用户（任意角色）
- 【Mock Data】
```yaml
---
filename: "test-file.txt"
---
```
- 【预期结果】
  - 创建成功；自动生成 id/created_by/created_at
  - 验证 mime_type, size, url 是否自动生成
  - READ resource 可获取信息

**TC-RES-002：带 display_name + description 上传**

- 【用例描述】提供完整元信息创建资源
- 【前置条件】已登录用户
- 【Mock Data】
```yaml
---
filename: "project-demo.mp4"
display_name: "项目演示视频"
description: "3 分钟 demo，用于提案展示"
---
```
- 【预期结果】创建成功；display_name 覆盖默认展示名

---

### 2.2 A2. 与帖子关联的可用性

**TC-RES-010：资源作为"附件 attachment"挂到帖子**

- 【用例描述】创建 post:resource 关系，display_type=attachment
- 【前置条件】已存在一个 post 和一个 resource
- 【Mock Data】
```yaml
post_id: "post_codereview_copilot"
resource_id: "res_project_demo_mp4"
display_type: attachment
position: 0
```
- 【预期结果】READ post:resource 可查到；display_type=attachment，position 正确

**TC-RES-011：资源作为"内联 inline"挂到帖子**

- 【用例描述】创建 post:resource 关系，display_type=inline
- 【前置条件】已存在一个 post 和一个 resource
- 【Mock Data】
```yaml
post_id: "post_codereview_copilot"
resource_id: "res_project_demo_mp4"
display_type: inline
position: 0
```
- 【预期结果】READ post:resource 返回 display_type=inline；position 可用于排序

**TC-RES-012：同一帖子挂多个资源，position 排序生效**

- 【用例描述】同一 post 关联多个 resource，验证 position 排序
- 【前置条件】已存在一个 post 和两个 resource
- 【Mock Data】
```yaml
# 资源1: 内联视频
post_id: "post_codereview_copilot"
resource_id: "res_project_demo_mp4"
display_type: inline
position: 0
```
```yaml
# 资源2: 附件zip
post_id: "post_codereview_copilot"
resource_id: "res_source_code_zip"
display_type: attachment
position: 1
```
- 【预期结果】READ post:resource 返回结果可排序且 position 信息完整

---

### 2.3 A3. 权限与可见性

**TC-RES-020：资源可读性继承帖子可见性**

- 【用例描述】验证资源的可读性取决于关联帖子的可见性
- 【前置条件】
  - post A：published（任何人可读）
  - post B：draft（只有作者/Admin 可读）
  - 同一 resource 分别关联到 A 和 B
- 【Mock Data】
```yaml
# post A (published)
---
title: "公开帖子"
status: published
---
```
```yaml
# post B (draft)
---
title: "草稿帖子"
status: draft
---
```
```yaml
# resource
---
filename: "shared-file.pdf"
display_name: "共享文件"
---
```
- 【预期结果】
  - 关联到 published post 的资源：访客可读
  - 关联到 draft post 的资源：访客不可读

---

### 2.4 A4. 更新与删除

**TC-RES-030：UPDATE resource 元信息**

- 【用例描述】更新资源的 display_name 和 description
- 【前置条件】已存在资源，操作者为上传者或 Admin
- 【Mock Data】
```yaml
# UPDATE 操作
display_name: "更新后的名称"
description: "更新后的描述"
```
- 【预期结果】更新成功；READ resource 返回新元信息；updated_at 变更

**TC-RES-031：DELETE resource 级联解除 post:resource**

- 【用例描述】删除资源后验证 post:resource 关系解除
- 【前置条件】已创建 resource 并关联到 post
- 【Mock Data】使用 RES-MOCK-001 + REL-MOCK-001
- 【预期结果】资源被软删除；post:resource 关系解除

---

### 2.5 A5. 负向/边界

**TC-RES-900：缺少 filename**

- 【用例描述】创建资源时不提供 filename
- 【前置条件】已登录用户
- 【Mock Data】
```yaml
---
display_name: "无文件名资源"
---
```
- 【预期结果】失败；错误指出必填字段 filename 缺失

**TC-RES-901：未登录用户 CREATE resource**

- 【用例描述】无认证状态下创建资源
- 【前置条件】未登录
- 【Mock Data】同 TC-RES-001
- 【预期结果】拒绝；错误提示需要认证

**TC-RES-902：创建 post:resource 时引用不存在的 post_id/resource_id**

- 【用例描述】使用不存在的 ID 创建 post:resource 关系
- 【前置条件】已登录用户
- 【Mock Data】
```yaml
post_id: "post_nonexistent_999"
resource_id: "res_nonexistent_999"
display_type: attachment
position: 0
```
- 【预期结果】失败；错误能明确是哪个 ID 不存在

**TC-RES-903：非法 display_type 枚举**

- 【用例描述】使用非法 display_type 创建 post:resource
- 【前置条件】已存在有效的 post 和 resource
- 【Mock Data】
```yaml
post_id: "post_codereview_copilot"
resource_id: "res_project_demo_mp4"
display_type: "embedded"
position: 0
```
- 【预期结果】失败；错误指出枚举可选范围（attachment | inline）

---

## 3. List 模块（category:post 列表查询）

### 3.1 A1. 基础可用性

**TC-LIST-001：活动下只列出 submission（单条）**

- 【用例描述】查询活动下的 submission 类型帖子（单条）
- 【前置条件】
  - 已发布活动 category
  - 存在 1 条 category:post 关系，relation_type=submission
- 【Mock Data】
```yaml
# category
---
name: "2025 AI Hackathon"
type: competition
status: published
---
```
```yaml
# relation
category_id: "cat_ai_hackathon_2025"
post_id: "post_codereview_copilot"
relation_type: submission
```
- 【预期结果】返回列表仅包含该提案帖，不含 reference 类型帖子

**TC-LIST-002：活动下 submission 多条，全部被列出**

- 【用例描述】查询活动下的多条 submission
- 【前置条件】同一活动下挂 3 条 submission
- 【Mock Data】使用 B2+B3 的 POST-SUB-001~003 + REL-CATPOST-001~002,004
- 【预期结果】返回 3 条且数量准确

---

### 3.2 A2. 过滤正确性

**TC-LIST-010：混合关联（submission + reference），过滤只出 submission**

- 【用例描述】同一 category 下有 submission 和 reference，验证过滤
- 【前置条件】同一 category 下同时存在 submission 和 reference 关系
- 【Mock Data】
```yaml
# submission 关系
category_id: "cat_ai_hackathon_2025"
post_id: "post_codereview_copilot"
relation_type: submission
```
```yaml
# reference 关系
category_id: "cat_ai_hackathon_2025"
post_id: "post_showcase_collection"
relation_type: reference
```
- 【预期结果】READ category:post (relation_type=submission) 结果集中完全不出现 reference 帖

**TC-LIST-011：不带 filter 读取 category:post**

- 【用例描述】不传 relation_type filter 读取所有 category:post
- 【前置条件】同 TC-LIST-010
- 【Mock Data】同 TC-LIST-010
- 【预期结果】结果包含 submission + reference 两类

---

### 3.3 A3. 权限与可见性

**TC-LIST-020：活动 published + submission post draft：列表安全性**

- 【用例描述】已发布活动下关联了一个 draft 帖子的 submission，验证访客视角
- 【前置条件】
  - category: published
  - submission 指向 draft post
- 【Mock Data】
```yaml
# draft submission post
---
title: "Stealth Project Draft"
type: for_category
tags: ["AI"]
status: draft
---
未发布草稿作品。
```
```yaml
# relation
category_id: "cat_ai_hackathon_2025"
post_id: "post_stealth_draft"
relation_type: submission
```
- 【预期结果】以未登录访客执行 READ category:post (submission) 时，该 draft submission 不出现在列表

---

### 3.4 A4. 一致性与健壮性

**TC-LIST-030：关联指向不存在的 post_id（脏数据）**

- 【用例描述】category:post 关系指向不存在的 post_id
- 【前置条件】手工造一条 category:post 关系，post_id 不存在
- 【Mock Data】
```yaml
category_id: "cat_ai_hackathon_2025"
post_id: "post_nonexistent_999"
relation_type: submission
```
- 【预期结果】不崩；返回结果跳过或明确标记 broken reference

**TC-LIST-031：同一 post 被重复 submission 关联**

- 【用例描述】同一 post_id 被同一 category 关联两次 submission
- 【前置条件】手工造两条同样的 category:post 关系
- 【Mock Data】
```yaml
# 第一条
category_id: "cat_ai_hackathon_2025"
post_id: "post_codereview_copilot"
relation_type: submission
```
```yaml
# 第二条（重复）
category_id: "cat_ai_hackathon_2025"
post_id: "post_codereview_copilot"
relation_type: submission
```
- 【预期结果】确认引擎行为：去重（产品语义）还是保留（数据库语义）

---

## 4. Interaction 模块

### 4.1 D1. 点赞（like）

**TC-IACT-001：创建 like interaction**

- 【用例描述】对已发布帖子点赞，验证 like_count 递增
- 【前置条件】已存在 published post + 已登录用户
- 【Mock Data】
```yaml
---
type: like
target_type: post
target_id: "post_codereview_copilot"
# created_by: user_bob (由 --user 传入)
---
```
- 【预期结果】interaction 创建成功；post 的 like_count 从 0 变为 1

**TC-IACT-002：like 唯一性约束（同一用户不能重复点赞）**

- 【用例描述】同一用户对同一 post 再次点赞
- 【前置条件】user_bob 已对 post_codereview_copilot 点过赞
- 【Mock Data】同 IACT-MOCK-001
- 【预期结果】创建失败；错误指出重复点赞

**TC-IACT-003：DELETE like → like_count 递减**

- 【用例描述】取消点赞后 like_count 递减
- 【前置条件】已存在 like interaction
- 【Mock Data】DELETE 对应的 like interaction
- 【预期结果】post 的 like_count 从 1 回到 0

---

### 4.2 D2. 评论（comment）

**TC-IACT-010：创建顶层评论**

- 【用例描述】发表顶层评论，验证 comment_count 递增
- 【前置条件】已存在 published post + 已登录用户
- 【Mock Data】
```yaml
---
type: comment
target_type: post
target_id: "post_codereview_copilot"
value: "方案很有创意！AST + LLM 的组合方式值得关注。请问支持哪些 CI/CD 集成？"
---
```
- 【预期结果】interaction 创建成功；post 的 comment_count +1

**TC-IACT-011：创建嵌套回复（parent_id）**

- 【用例描述】回复已有评论，验证 comment_count 继续递增
- 【前置条件】已存在顶层评论
- 【Mock Data】
```yaml
---
type: comment
target_type: post
target_id: "post_codereview_copilot"
parent_id: "<iact_comment_id>"
value: "目前支持 GitHub Actions 和 GitLab CI，Jenkins 插件正在开发中。"
---
```
- 【预期结果】parent_id 指向顶层评论；post 的 comment_count 再 +1

**TC-IACT-012：DELETE 父评论 → 级联删除子回复**

- 【用例描述】删除顶层评论后级联删除子回复
- 【前置条件】已存在顶层评论和嵌套回复
- 【Mock Data】DELETE 顶层评论
- 【预期结果】顶层评论和嵌套回复均被软删除；post 的 comment_count 归 0

---

### 4.3 D3. 评分（rating）

**TC-IACT-020：创建多维度评分**

- 【用例描述】提交多维度评分，验证加权计算
- 【前置条件】
  - 已存在 published post（关联了含 scoring_criteria 的 rule）
  - 已登录评委用户
- 【Mock Data】
```yaml
---
type: rating
target_type: post
target_id: "post_codereview_copilot"
value:
  创新性: 87
  技术实现: 82
  实用价值: 78
  演示效果: 91
  _comment: "架构设计清晰，建议完善错误处理"
---
# 加权计算: 87×0.30 + 82×0.30 + 78×0.25 + 91×0.15 = 83.85
```
- 【预期结果】interaction 创建成功；post 的 average_rating 更新为 83.85

**TC-IACT-021：多个 rating → average_rating 取均值**

- 【用例描述】第二个评委提交不同分数，验证均值计算
- 【前置条件】TC-IACT-020 已执行
- 【Mock Data】
```yaml
---
type: rating
target_type: post
target_id: "post_codereview_copilot"
value:
  创新性: 75
  技术实现: 90
  实用价值: 85
  演示效果: 70
  _comment: "技术实现扎实，但演示还需完善"
---
# 加权计算: 75×0.30 + 90×0.30 + 85×0.25 + 70×0.15 = 81.25
# 两次均值: (83.85 + 81.25) / 2 = 82.55
```
- 【预期结果】average_rating = 82.55

---

### 4.4 D4. 负向/边界

**TC-IACT-900：非法 interaction type**

- 【用例描述】使用非法 type 创建 interaction
- 【前置条件】已登录用户
- 【Mock Data】
```yaml
---
type: "bookmark"
target_type: post
target_id: "post_codereview_copilot"
---
```
- 【预期结果】失败；错误指出枚举范围 (like/comment/rating)

**TC-IACT-901：非法 target_type**

- 【用例描述】使用非法 target_type 创建 interaction
- 【前置条件】已登录用户
- 【Mock Data】
```yaml
---
type: like
target_type: "user"
target_id: "user_alice"
---
```
- 【预期结果】失败；错误指出 target_type 枚举范围 (post/category/resource)

**TC-IACT-902：target_id 不存在**

- 【用例描述】指向不存在的目标对象
- 【前置条件】已登录用户
- 【Mock Data】
```yaml
---
type: like
target_type: post
target_id: "post_nonexistent_999"
---
```
- 【预期结果】失败；错误指出目标对象不存在

### 4.5 [GAP] D5. UPDATE interaction（修改评论/评分）

> **来源：** test-gap.md — interaction UPDATE 完全缺失

**TC-IACT-050：UPDATE comment 文本**

- 【用例描述】修改已有评论的文本内容
- 【前置条件】已存在 comment interaction，操作者为评论发起人
- 【Mock Data】
```yaml
# 原始评论
---
type: comment
target_type: post
target_id: "post_codereview_copilot"
value: "方案很有创意！"
---
# UPDATE 操作
value: "方案很有创意！补充：能否支持 Rust？"
```
- 【预期结果】更新成功；value 更新为新文本；updated_at 变更；comment_count 不变

**TC-IACT-051：UPDATE rating 重新打分**

- 【用例描述】评委修改已提交的评分
- 【前置条件】已存在 rating interaction，操作者为评分发起人
- 【Mock Data】
```yaml
# 原始评分
---
type: rating
target_type: post
target_id: "post_codereview_copilot"
value:
  创新性: 87
  技术实现: 82
  实用价值: 78
  演示效果: 91
  _comment: "架构设计清晰"
---
# UPDATE 操作
value:
  创新性: 90
  技术实现: 85
  实用价值: 80
  演示效果: 88
  _comment: "架构设计清晰，补充演示后更完善"
# 新加权: 90×0.30 + 85×0.30 + 80×0.25 + 88×0.15 = 85.70
```
- 【预期结果】更新成功；post 的 average_rating 重新计算

**TC-IACT-052：非本人 UPDATE interaction 被拒绝**

- 【用例描述】其他用户尝试修改别人的评论
- 【前置条件】user_bob 的评论，user_alice 尝试修改
- 【Mock Data】同 TC-IACT-050，但操作者改为 user_alice
- 【预期结果】拒绝；错误指出权限不足（仅交互发起人本人可修改）

---

### 4.6 [GAP] D6. Interaction on 非 post 目标

> **来源：** test-gap.md — "所有测试使用 target_type=post，无 category/resource 目标测试"

**TC-IACT-060：对 category 点赞**

- 【用例描述】对活动（category）进行点赞
- 【前置条件】已存在 published category + 已登录用户
- 【Mock Data】
```yaml
---
type: like
target_type: category
target_id: "cat_ai_hackathon_2025"
---
```
- 【预期结果】interaction 创建成功；target_type=category 被正确存储和查询

**TC-IACT-061：对 category 发表评论**

- 【用例描述】对活动发表评论
- 【前置条件】已存在 published category + 已登录用户
- 【Mock Data】
```yaml
---
type: comment
target_type: category
target_id: "cat_ai_hackathon_2025"
value: "这个活动太棒了！期待参加。"
---
```
- 【预期结果】interaction 创建成功

**TC-IACT-062：对 resource 点赞**

- 【用例描述】对资源（resource）进行点赞
- 【前置条件】已存在可见 resource + 已登录用户
- 【Mock Data】
```yaml
---
type: like
target_type: resource
target_id: "res_project_demo_mp4"
---
```
- 【预期结果】interaction 创建成功；target_type=resource 被正确存储和查询

**TC-IACT-063：对 resource 发表评论**

- 【用例描述】对资源发表评论
- 【前置条件】已存在可见 resource + 已登录用户
- 【Mock Data】
```yaml
---
type: comment
target_type: resource
target_id: "res_project_demo_mp4"
value: "演示视频制作精良！"
---
```
- 【预期结果】interaction 创建成功

---

## 5. Category 模块 [GAP]

> **来源：** test-gap.md — category DELETE 缺失；状态流转 draft→published→closed 未覆盖

### 5.1 基础 CRUD

**TC-CAT-001：CREATE category（competition 类型）**

- 【用例描述】组织者创建比赛活动
- 【前置条件】已登录 organizer 用户
- 【Mock Data】
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
本次 Hackathon 面向全球 AI 开发者。
```
- 【预期结果】
  - 创建成功；id/created_by/created_at 自动生成
  - deleted_at=null
  - READ category 可查到

**TC-CAT-002：CREATE category（operation 类型）**

- 【用例描述】组织者创建运营活动
- 【前置条件】已登录 organizer 用户
- 【Mock Data】
```yaml
---
name: "每周创意分享"
description: "社区成员每周分享创意想法"
type: operation
status: draft
---
## 活动说明
每周五晚 8 点线上分享。
```
- 【预期结果】创建成功；type=operation

**TC-CAT-010：UPDATE category 状态流转 draft→published→closed**

- 【用例描述】验证 category 完整状态流转
- 【前置条件】已存在 draft category，操作者为创建者或 Admin
- 【Mock Data】
```yaml
# 步骤1: draft → published
status: published

# 步骤2: published → closed
status: closed
```
- 【预期结果】每步更新成功；updated_at 变更；READ category 返回最新状态

**TC-CAT-020：DELETE category 及级联影响**

- 【用例描述】删除活动后验证级联：解除关系 + 删除关联 interaction
- 【前置条件】
  - 已存在 published category
  - 关联了 rule（category:rule）、post（category:post）、group（category:group）
  - 存在 target_type=category 的 interaction
- 【Mock Data】
```yaml
# category
---
name: "待删除活动"
type: competition
status: published
---
```
```yaml
# 关联的 category:rule
category_id: "cat_to_delete"
rule_id: "rule_submission_01"
priority: 1
```
```yaml
# 关联的 category:post
category_id: "cat_to_delete"
post_id: "post_codereview_copilot"
relation_type: submission
```
```yaml
# 关联的 category:group
category_id: "cat_to_delete"
group_id: "grp_team_synnovator"
```
```yaml
# 关联的 interaction
---
type: like
target_type: category
target_id: "cat_to_delete"
---
```
- 【预期结果】
  - category 软删除（deleted_at 非 null）
  - category:rule、category:post、category:group 关系解除
  - 关联的 interaction 一并软删除

### 5.2 负向/边界

**TC-CAT-900：非法 type 枚举**

- 【用例描述】使用非法 type 创建 category
- 【前置条件】已登录 organizer
- 【Mock Data】
```yaml
---
name: "非法类型活动"
description: "测试"
type: "workshop"
---
```
- 【预期结果】失败；错误指出 type 枚举范围 (competition | operation)

**TC-CAT-901：非法 status 枚举**

- 【用例描述】使用非法 status 创建/更新 category
- 【前置条件】已登录 organizer
- 【Mock Data】
```yaml
---
name: "非法状态活动"
description: "测试"
type: competition
status: "archived"
---
```
- 【预期结果】失败；错误指出 status 枚举范围 (draft | published | closed)

**TC-CAT-902：participant 创建 category 被拒绝**

- 【用例描述】普通参赛者尝试创建活动
- 【前置条件】已登录 participant（非 organizer/admin）
- 【Mock Data】同 TC-CAT-001
- 【预期结果】拒绝；错误指出权限不足（CREATE category = Organizer/Admin）

---

## 6. Rule 模块 [GAP]

> **来源：** test-gap.md — rule UPDATE 和 DELETE 完全缺失

### 6.1 基础 CRUD

**TC-RULE-001：CREATE rule（含完整 scoring_criteria）**

- 【用例描述】创建包含多维度评分标准的活动规则
- 【前置条件】已登录 organizer 用户
- 【Mock Data】
```yaml
---
name: "AI Hackathon 提交规则"
description: "2025 AI Hackathon 参赛提交规范"
allow_public: true
require_review: true
reviewers: ["user_judge_01", "user_judge_02"]
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
1. 必须包含项目说明文档（Markdown）
2. 必须包含源代码（zip）
3. 所有提交内容必须为参赛期间原创
```
- 【预期结果】创建成功；scoring_criteria 被正确存储；权重总和=100

**TC-RULE-010：UPDATE rule 修改配置**

- 【用例描述】更新规则的截止时间和审核人列表
- 【前置条件】已存在 rule，操作者为创建者或 Admin
- 【Mock Data】
```yaml
# UPDATE 操作
submission_deadline: "2025-03-21T23:59:59Z"
reviewers: ["user_judge_01", "user_judge_02", "user_judge_03"]
max_team_size: 6
```
- 【预期结果】更新成功；READ rule 返回新值；updated_at 变更

**TC-RULE-011：UPDATE rule 修改 scoring_criteria**

- 【用例描述】修改评分标准的权重
- 【前置条件】已存在含 scoring_criteria 的 rule
- 【Mock Data】
```yaml
# UPDATE scoring_criteria
scoring_criteria:
  - name: "创新性"
    weight: 25
    description: "方案的原创性和创新程度"
  - name: "技术实现"
    weight: 25
    description: "代码质量、架构设计、技术深度"
  - name: "实用价值"
    weight: 25
    description: "解决实际问题的程度和商业潜力"
  - name: "演示效果"
    weight: 25
    description: "Demo 完成度和展示效果"
```
- 【预期结果】更新成功；后续 rating 按新权重计算

**TC-RULE-020：DELETE rule 及级联**

- 【用例描述】删除规则后验证 category:rule 关系解除
- 【前置条件】已存在 rule 且关联到 category
- 【Mock Data】
```yaml
# 已关联
category_id: "cat_ai_hackathon_2025"
rule_id: "rule_to_delete"
priority: 1
```
- 【预期结果】rule 被软删除；category:rule 关系解除

### 6.2 负向/边界

**TC-RULE-900：participant 创建 rule 被拒绝**

- 【用例描述】普通参赛者尝试创建规则
- 【前置条件】已登录 participant
- 【Mock Data】同 TC-RULE-001
- 【预期结果】拒绝；错误指出权限不足（CREATE rule = Organizer/Admin）

**TC-RULE-901：scoring_criteria 权重总和不等于 100**

- 【用例描述】验证评分维度权重之和的合法性
- 【前置条件】已登录 organizer
- 【Mock Data】
```yaml
---
name: "权重错误规则"
description: "测试"
scoring_criteria:
  - name: "创新性"
    weight: 50
  - name: "技术实现"
    weight: 60
---
# 权重总和 = 110，超过 100
```
- 【预期结果】失败或警告（取决于引擎验证策略）

---

## 7. User 模块 [GAP]

> **来源：** test-gap.md — user UPDATE 和 DELETE 完全缺失

### 7.1 基础 CRUD

**TC-USER-001：CREATE user（participant）**

- 【用例描述】注册新 participant 用户
- 【前置条件】无（任何人可注册）
- 【Mock Data】
```yaml
---
username: "charlie"
email: "charlie@example.com"
display_name: "Charlie Zhang"
avatar_url: "https://example.com/avatars/charlie.png"
bio: "UI 设计师，专注用户体验"
role: participant
---
```
- 【预期结果】创建成功；id/created_at/updated_at 自动生成；deleted_at=null

**TC-USER-010：UPDATE user 信息**

- 【用例描述】用户更新自己的个人信息
- 【前置条件】已登录用户 user_charlie，操作者为本人
- 【Mock Data】
```yaml
# UPDATE 操作
display_name: "Charlie Z."
bio: "UI 设计师 & 前端开发，专注用户体验和交互设计"
avatar_url: "https://example.com/avatars/charlie_v2.png"
```
- 【预期结果】更新成功；READ user 返回新值；updated_at 变更

**TC-USER-011：Admin UPDATE 其他用户角色**

- 【用例描述】管理员修改用户角色
- 【前置条件】已登录 admin 用户
- 【Mock Data】
```yaml
# 目标: user_charlie
# UPDATE 操作
role: organizer
```
- 【预期结果】更新成功；user_charlie 的 role 变为 organizer

**TC-USER-020：DELETE user 及级联**

- 【用例描述】删除用户后验证级联影响
- 【前置条件】
  - 已存在 user_charlie
  - user_charlie 是 group 成员（group:user 关系存在）
  - user_charlie 有若干 interaction 记录
- 【Mock Data】
```yaml
# user
---
username: "charlie"
email: "charlie@example.com"
display_name: "Charlie Zhang"
role: participant
---
```
```yaml
# group:user 关系
group_id: "grp_team_synnovator"
user_id: "user_charlie"
role: member
status: accepted
```
```yaml
# charlie 的 interaction
---
type: like
target_type: post
target_id: "post_codereview_copilot"
# created_by: user_charlie
---
```
- 【预期结果】
  - user 软删除（deleted_at 非 null）
  - 该用户的所有 interaction 一并软删除
  - group:user 关系保留（标记为离组）
  - 对应 post 的 like_count 递减

### 7.2 负向/边界

**TC-USER-900：重复 username**

- 【用例描述】创建与已有用户相同 username 的用户
- 【前置条件】已存在 user_alice (username="alice")
- 【Mock Data】
```yaml
---
username: "alice"
email: "another-alice@example.com"
display_name: "Another Alice"
---
```
- 【预期结果】失败；错误指出 username 唯一性冲突

**TC-USER-901：重复 email**

- 【用例描述】创建与已有用户相同 email 的用户
- 【前置条件】已存在 user_alice (email="alice@example.com")
- 【Mock Data】
```yaml
---
username: "alice2"
email: "alice@example.com"
display_name: "Alice Two"
---
```
- 【预期结果】失败；错误指出 email 唯一性冲突

**TC-USER-902：非本人/非 Admin 修改用户信息**

- 【用例描述】用户 A 尝试修改用户 B 的信息
- 【前置条件】user_bob 尝试 UPDATE user_alice 的 bio
- 【Mock Data】
```yaml
# 操作者: user_bob
# 目标: user_alice
bio: "被篡改的简介"
```
- 【预期结果】拒绝；错误指出权限不足（UPDATE user = 本人/Admin）

---

## 8. Group 模块 [GAP]

> **来源：** test-gap.md — group UPDATE 和 DELETE 完全缺失

### 8.1 基础 CRUD

**TC-GRP-001：CREATE group（public, require_approval=true）**

- 【用例描述】创建需要审批的公开团队
- 【前置条件】已登录用户
- 【Mock Data】
```yaml
---
name: "Team Synnovator"
description: "AI Hackathon 参赛团队"
visibility: public
max_members: 5
require_approval: true
---
```
- 【预期结果】
  - 创建成功；id/created_by/created_at 自动生成
  - deleted_at=null

**TC-GRP-002：CREATE group（private, require_approval=false）**

- 【用例描述】创建无需审批的私有团队
- 【前置条件】已登录用户
- 【Mock Data】
```yaml
---
name: "Internal Dev Team"
description: "内部开发团队"
visibility: private
max_members: 10
require_approval: false
---
```
- 【预期结果】创建成功；visibility=private；新成员加入时自动 accepted

**TC-GRP-010：UPDATE group 信息**

- 【用例描述】团队 Owner 更新团队信息
- 【前置条件】已登录 group owner
- 【Mock Data】
```yaml
# UPDATE 操作
description: "AI Hackathon 2025 参赛团队 — 更新描述"
max_members: 8
```
- 【预期结果】更新成功；READ group 返回新值；updated_at 变更

**TC-GRP-011：UPDATE group 变更 require_approval**

- 【用例描述】Owner 关闭审批要求
- 【前置条件】已存在 require_approval=true 的 group
- 【Mock Data】
```yaml
# UPDATE 操作
require_approval: false
```
- 【预期结果】更新成功；后续新成员加入时自动 accepted

**TC-GRP-020：DELETE group 及级联**

- 【用例描述】删除团队后验证级联影响
- 【前置条件】
  - 已存在 group（含 owner + member）
  - group 已关联到 category（category:group 关系）
- 【Mock Data】
```yaml
# group
---
name: "待删除团队"
visibility: public
---
```
```yaml
# group:user 关系
group_id: "grp_to_delete"
user_id: "user_alice"
role: owner
status: accepted
```
```yaml
# category:group 关系
category_id: "cat_ai_hackathon_2025"
group_id: "grp_to_delete"
```
- 【预期结果】
  - group 软删除
  - group:user 关系保留（成员可查询历史）
  - category:group 关系解除

### 8.2 负向/边界

**TC-GRP-900：非法 visibility 枚举**

- 【用例描述】使用非法 visibility 创建 group
- 【前置条件】已登录用户
- 【Mock Data】
```yaml
---
name: "非法可见性团队"
visibility: "restricted"
---
```
- 【预期结果】失败；错误指出枚举范围 (public | private)

**TC-GRP-901：非 Owner/Admin 修改 group**

- 【用例描述】普通 member 尝试更新 group 信息
- 【前置条件】user_bob 为 group member（非 owner/admin）
- 【Mock Data】
```yaml
# 操作者: user_bob (member)
description: "被普通成员修改的描述"
```
- 【预期结果】拒绝；错误指出权限不足

---

## 9. Category:Group 关系 [GAP]

> **来源：** test-gap.md — "category:group 关系完全缺失，阻塞 Journey 7（团队报名活动）"

### 9.1 基础 CRUD

**TC-CATGRP-001：CREATE category:group（团队报名活动）**

- 【用例描述】团队报名参加活动
- 【前置条件】
  - 已存在 published category
  - 已存在 group（team 人数符合 rule 要求）
  - 操作者为 Group Owner
- 【Mock Data】
```yaml
# category:group 关系
category_id: "cat_ai_hackathon_2025"
group_id: "grp_team_synnovator"
# registered_at 自动生成
```
- 【预期结果】
  - 关系创建成功
  - registered_at 自动生成
  - READ category:group 可查到该团队

**TC-CATGRP-002：READ category:group（查询活动报名团队列表）**

- 【用例描述】查询某活动下所有已报名团队
- 【前置条件】已有多个 group 报名同一 category
- 【Mock Data】
```yaml
# 团队1
category_id: "cat_ai_hackathon_2025"
group_id: "grp_team_synnovator"
```
```yaml
# 团队2
category_id: "cat_ai_hackathon_2025"
group_id: "grp_team_alpha"
```
```yaml
# 团队2 mock
---
name: "Team Alpha"
description: "另一支参赛团队"
visibility: public
max_members: 5
require_approval: true
---
```
- 【预期结果】返回该 category 下所有已报名的 group 列表

**TC-CATGRP-010：DELETE category:group（取消报名）**

- 【用例描述】团队取消活动报名
- 【前置条件】已存在 category:group 关系
- 【Mock Data】
```yaml
category_id: "cat_ai_hackathon_2025"
group_id: "grp_team_synnovator"
```
- 【预期结果】关系被物理删除（关系 DELETE 为硬删除）；READ category:group 不再返回该团队

### 9.2 唯一性约束

**TC-CATGRP-900：同一团队重复报名同一活动**

- 【用例描述】同一 group 对同一 category 创建两次 category:group
- 【前置条件】grp_team_synnovator 已报名 cat_ai_hackathon_2025
- 【Mock Data】
```yaml
# 第二次报名（重复）
category_id: "cat_ai_hackathon_2025"
group_id: "grp_team_synnovator"
```
- 【预期结果】失败；错误指出唯一性约束 (category_id, group_id)

**TC-CATGRP-901：同一用户在同一活动中属于多个团队**

- 【用例描述】用户通过不同 group 参加同一 category
- 【前置条件】
  - user_alice 已通过 grp_team_synnovator 报名 cat_ai_hackathon_2025
  - user_alice 同时属于 grp_team_alpha
- 【Mock Data】
```yaml
# grp_team_alpha 也报名同一活动
category_id: "cat_ai_hackathon_2025"
group_id: "grp_team_alpha"
```
```yaml
# user_alice 在 grp_team_alpha 中
group_id: "grp_team_alpha"
user_id: "user_alice"
role: member
status: accepted
```
- 【预期结果】失败；错误指出"同一用户在同一 category 中只能属于一个 group"（业务唯一性规则）

---

## 10. 关系 UPDATE/DELETE [GAP]

> **来源：** test-gap.md — 多个关系的 UPDATE/DELETE 缺失

### 10.1 category:rule 关系

**TC-REL-001：UPDATE category:rule priority**

- 【用例描述】修改规则在活动中的优先级
- 【前置条件】已存在 category:rule 关系
- 【Mock Data】
```yaml
category_id: "cat_ai_hackathon_2025"
rule_id: "rule_submission_01"
# UPDATE
priority: 2
```
- 【预期结果】更新成功；READ category:rule 返回新 priority

**TC-REL-002：DELETE category:rule**

- 【用例描述】解除活动与规则的关联
- 【前置条件】已存在 category:rule 关系
- 【Mock Data】
```yaml
category_id: "cat_ai_hackathon_2025"
rule_id: "rule_submission_01"
```
- 【预期结果】关系被物理删除

**TC-REL-003：category:rule 唯一性约束（重复关联）**

- 【用例描述】同一 rule 重复关联到同一 category
- 【前置条件】已存在 category:rule 关系
- 【Mock Data】
```yaml
# 第二次关联（重复）
category_id: "cat_ai_hackathon_2025"
rule_id: "rule_submission_01"
priority: 1
```
- 【预期结果】失败；错误指出唯一性约束

### 10.2 category:post 关系

**TC-REL-010：UPDATE category:post relation_type**

- 【用例描述】将 reference 关系修改为 submission
- 【前置条件】已存在 category:post 关系（relation_type=reference）
- 【Mock Data】
```yaml
category_id: "cat_ai_hackathon_2025"
post_id: "post_showcase_collection"
# UPDATE
relation_type: submission
```
- 【预期结果】更新成功

### 10.3 post:post 关系

**TC-REL-020：UPDATE post:post relation_type/position**

- 【用例描述】修改帖子间关系类型和位置
- 【前置条件】已存在 post:post embed 关系
- 【Mock Data】
```yaml
source_post_id: "post_codereview_copilot"
target_post_id: "post_team_synnovator"
# UPDATE
relation_type: reference
position: 0
```
- 【预期结果】更新成功

**TC-REL-021：DELETE post:post 关系**

- 【用例描述】解除帖子间关联
- 【前置条件】已存在 post:post 关系
- 【Mock Data】
```yaml
source_post_id: "post_codereview_copilot"
target_post_id: "post_team_synnovator"
```
- 【预期结果】关系被物理删除

### 10.4 post:resource 关系

**TC-REL-030：UPDATE post:resource display_type**

- 【用例描述】将资源展示方式从 attachment 改为 inline
- 【前置条件】已存在 post:resource 关系（display_type=attachment）
- 【Mock Data】
```yaml
post_id: "post_codereview_copilot"
resource_id: "res_project_demo_mp4"
# UPDATE
display_type: inline
position: 0
```
- 【预期结果】更新成功

**TC-REL-031：DELETE post:resource 关系**

- 【用例描述】解除帖子与资源的关联
- 【前置条件】已存在 post:resource 关系
- 【Mock Data】
```yaml
post_id: "post_codereview_copilot"
resource_id: "res_project_demo_mp4"
```
- 【预期结果】关系被物理删除

### 10.5 group:user 关系

**TC-REL-040：DELETE group:user（移出成员）**

- 【用例描述】Owner 将成员移出团队
- 【前置条件】已存在 group:user 关系（status=accepted）
- 【Mock Data】
```yaml
group_id: "grp_team_synnovator"
user_id: "user_bob"
```
- 【预期结果】关系被物理删除；READ group:user 不再返回该成员

**TC-REL-041：group:user 唯一性约束（重复加入）**

- 【用例描述】同一用户重复加入同一 group
- 【前置条件】user_bob 已是 grp_team_synnovator 成员
- 【Mock Data】
```yaml
group_id: "grp_team_synnovator"
user_id: "user_bob"
role: member
```
- 【预期结果】失败；错误指出唯一性约束 (group_id, user_id)

### 10.6 target:interaction 关系

**TC-REL-050：DELETE target:interaction 关系**

- 【用例描述】解除目标对象与交互记录的关联
- 【前置条件】已存在 target:interaction 关系
- 【Mock Data】
```yaml
target_type: post
target_id: "post_codereview_copilot"
interaction_id: "iact_like_001"
```
- 【预期结果】关系被物理删除

---

## 11. 软删除与恢复 [GAP]

> **来源：** test-gap.md — 仅 post 软删除被测试过，其他内容类型 + 恢复机制完全缺失

### 11.1 各内容类型软删除

**TC-DEL-001：软删除 category + 验证 deleted_at**

- 【用例描述】软删除 category 后验证 deleted_at 被设置
- 【前置条件】已存在 published category
- 【Mock Data】
```yaml
---
name: "待删除活动"
type: competition
status: published
---
```
- 【预期结果】
  - deleted_at 被设置为当前时间
  - 默认查询不再返回该 category
  - Admin 可通过特殊参数查询到

**TC-DEL-002：软删除 rule**

- 【用例描述】软删除 rule
- 【前置条件】已存在 rule
- 【Mock Data】使用 TC-RULE-001 的 mock
- 【预期结果】deleted_at 被设置；默认查询不返回

**TC-DEL-003：软删除 user**

- 【用例描述】软删除 user 及验证级联
- 【前置条件】user 有 interaction 记录和 group:user 关系
- 【Mock Data】使用 TC-USER-020 的 mock
- 【预期结果】
  - user 的 deleted_at 被设置
  - 该用户的所有 interaction 一并软删除
  - group:user 关系保留（标记为离组）

**TC-DEL-004：软删除 group**

- 【用例描述】软删除 group
- 【前置条件】group 含 owner + member
- 【Mock Data】使用 TC-GRP-020 的 mock
- 【预期结果】
  - group 的 deleted_at 被设置
  - group:user 关系保留（成员可查询历史）
  - category:group 关系解除

**TC-DEL-005：软删除 interaction**

- 【用例描述】软删除 interaction
- 【前置条件】已存在 like interaction
- 【Mock Data】
```yaml
---
type: like
target_type: post
target_id: "post_codereview_copilot"
---
```
- 【预期结果】deleted_at 被设置；对应 post 的 like_count 递减

### 11.2 级联软删除

**TC-DEL-010：软删除 category → 关联 interaction 级联软删除**

- 【用例描述】删除活动后验证关联的 interaction 也被软删除
- 【前置条件】
  - 已存在 category
  - 存在 target_type=category 的 interaction（like + comment）
- 【Mock Data】
```yaml
# category
---
name: "级联测试活动"
type: competition
status: published
---
```
```yaml
# interaction 1 (like on category)
---
type: like
target_type: category
target_id: "cat_cascade_test"
---
```
```yaml
# interaction 2 (comment on category)
---
type: comment
target_type: category
target_id: "cat_cascade_test"
value: "好活动！"
---
```
- 【预期结果】category 软删除后，两条 interaction 均被级联软删除

**TC-DEL-011：软删除 user → 用户的 interaction + group:user 级联处理**

- 【用例描述】删除用户后验证级联
- 【前置条件】
  - user_charlie 有多条 interaction
  - user_charlie 是某 group 的 member
- 【Mock Data】使用 TC-USER-020 的 mock（扩展多条 interaction）
```yaml
# interaction 1 (like)
---
type: like
target_type: post
target_id: "post_codereview_copilot"
# created_by: user_charlie
---
```
```yaml
# interaction 2 (comment)
---
type: comment
target_type: post
target_id: "post_codereview_copilot"
value: "不错的项目！"
# created_by: user_charlie
---
```
- 【预期结果】
  - 所有 charlie 的 interaction 被级联软删除
  - post 的 like_count 和 comment_count 相应递减
  - group:user 关系保留但标记为离组

### 11.3 恢复机制

**TC-DEL-020：恢复软删除的 post**

- 【用例描述】Admin 恢复被软删除的帖子
- 【前置条件】
  - 已存在软删除的 post（deleted_at 非 null）
  - 操作者为 Admin
- 【Mock Data】
```yaml
# 被软删除的 post
---
title: "恢复测试帖子"
status: published
deleted_at: "2025-06-01T12:00:00Z"
---
# RESTORE 操作
deleted_at: null
```
- 【预期结果】deleted_at 被清除为 null；默认查询重新返回该 post

**TC-DEL-021：级联恢复（恢复 post → 恢复因级联软删除的 interaction）**

- 【用例描述】恢复帖子后，因级联被软删除的 interaction 也恢复
- 【前置条件】
  - post 被软删除，其关联的 interaction 也被级联软删除
  - Admin 执行恢复操作
- 【Mock Data】
```yaml
# 被级联删除的 interaction
---
type: like
target_type: post
target_id: "post_restore_test"
deleted_at: "2025-06-01T12:00:00Z"
---
```
- 【预期结果】post 和 interaction 均恢复；post 的 like_count 恢复

**TC-DEL-022：恢复权限 — 非 Admin 被拒绝**

- 【用例描述】普通用户尝试恢复被软删除的内容
- 【前置条件】操作者为 participant（非 Admin）
- 【Mock Data】同 TC-DEL-020
- 【预期结果】拒绝；错误指出"仅 Admin 可执行恢复操作"

---

## 12. 权限边界 [GAP]

> **来源：** test-gap.md — "无系统化的角色权限边界测试"

### 12.1 Organizer 专属操作

**TC-PERM-001：participant 尝试 CREATE category → 拒绝**

- 【用例描述】参赛者尝试创建活动
- 【前置条件】已登录 participant
- 【Mock Data】同 TC-CAT-001
- 【预期结果】拒绝

**TC-PERM-002：participant 尝试 CREATE rule → 拒绝**

- 【用例描述】参赛者尝试创建规则
- 【前置条件】已登录 participant
- 【Mock Data】同 TC-RULE-001
- 【预期结果】拒绝

**TC-PERM-003：participant 尝试 UPDATE category → 拒绝**

- 【用例描述】参赛者尝试更新活动
- 【前置条件】已登录 participant（非活动创建者）
- 【Mock Data】`status: published`
- 【预期结果】拒绝

### 12.2 Admin 专属操作

**TC-PERM-010：Admin 恢复软删除内容 → 允许**

- 【用例描述】Admin 执行恢复操作
- 【前置条件】已登录 admin
- 【Mock Data】同 TC-DEL-020
- 【预期结果】允许

**TC-PERM-011：participant 恢复软删除内容 → 拒绝**

- 【用例描述】参赛者尝试恢复
- 【前置条件】已登录 participant
- 【Mock Data】同 TC-DEL-020
- 【预期结果】拒绝

### 12.3 跨用户可见性

**TC-PERM-020：访客 READ draft post → 不可见**

- 【用例描述】未登录访客访问 draft 帖子
- 【前置条件】已存在 draft post
- 【Mock Data】
```yaml
---
title: "草稿帖子"
status: draft
---
```
- 【预期结果】不可见或返回权限错误

**TC-PERM-021：访客 READ draft category → 不可见**

- 【用例描述】未登录访客访问 draft 活动
- 【前置条件】已存在 draft category
- 【Mock Data】
```yaml
---
name: "草稿活动"
type: competition
status: draft
---
```
- 【预期结果】不可见或返回权限错误

**TC-PERM-022：非成员 READ private group → 不可见**

- 【用例描述】非成员访问 private group
- 【前置条件】已存在 visibility=private 的 group，操作者非成员
- 【Mock Data】
```yaml
---
name: "Private Team"
visibility: private
---
```
- 【预期结果】不可见或返回权限错误

---

## 13. 用户旅程集成 [GAP]

> **来源：** test-gap.md — 多个 Journey 未覆盖

### 13.1 Journey 2：匿名浏览

**TC-JOUR-002：匿名访客浏览公开内容**

- 【用例描述】未登录访客能浏览 published 的 category 和 post
- 【前置条件】
  - 已存在 published category
  - 已存在 published post（多种 type）
- 【Mock Data】使用通用 Mock Data 基座
- 【预期结果】
  - READ category (published) 成功
  - READ post (published) 成功，支持按 tag/type 筛选
  - draft 内容不可见

### 13.2 Journey 7：团队报名活动

**TC-JOUR-007：完整团队报名流程**

- 【用例描述】团队从创建到报名活动的完整流程
- 【前置条件】已存在 published category（含 rule）
- 【Mock Data】
```yaml
# 步骤1: Alice 创建团队
---
name: "Team Synnovator"
visibility: public
max_members: 5
require_approval: true
---

# 步骤2: Alice 自动成为 owner
group_id: "grp_team_synnovator"
user_id: "user_alice"
role: owner
status: accepted

# 步骤3: Bob 申请加入
group_id: "grp_team_synnovator"
user_id: "user_bob"
role: member
# status 自动为 pending

# 步骤4: Alice 批准 Bob
group_id: "grp_team_synnovator"
user_id: "user_bob"
status: accepted

# 步骤5: 团队报名活动
category_id: "cat_ai_hackathon_2025"
group_id: "grp_team_synnovator"
```
- 【预期结果】
  - 每步操作成功
  - READ category:group 能查到该团队
  - READ group:user 能查到 Alice(owner) + Bob(member, accepted)

### 13.3 Journey 10：获取证书

**TC-JOUR-010：完整证书颁发流程**

- 【用例描述】活动结束后颁发证书的完整流程
- 【前置条件】
  - 已存在活动（closed 状态）
  - 已存在获奖团队/用户
- 【Mock Data】
```yaml
# 步骤1: 关闭活动
category_id: "cat_ai_hackathon_2025"
status: closed

# 步骤2: 创建证书资源
---
filename: "certificate-alice.pdf"
display_name: "一等奖证书 - Alice"
description: "2025 AI Hackathon 一等奖证书"
---

# 步骤3: 创建证书帖子
---
title: "2025 AI Hackathon 一等奖证书"
type: certificate
tags: ["证书", "AI Hackathon"]
status: published
---
## 获奖信息
- 活动: 2025 AI Hackathon
- 奖项: 一等奖
- 获奖者: Alice Chen

# 步骤4: 关联证书资源到帖子
post_id: "post_certificate_alice"
resource_id: "res_certificate_alice_pdf"
display_type: inline
position: 0
```
- 【预期结果】
  - 证书帖子创建成功，type=certificate
  - 资源关联成功
  - READ post 可查到证书帖子
  - READ post:resource 可获取证书文件

### 13.4 Journey 11.2：编辑他人帖子

**TC-JOUR-011-2：编辑他人帖子（副本机制）**

- 【用例描述】用户请求编辑他人的帖子（需权限请求 + 副本创建）
- 【前置条件】
  - user_alice 的 published post
  - user_bob 尝试编辑
- 【Mock Data】
```yaml
# Alice 的原始帖子
---
title: "CodeReview Copilot"
type: for_category
status: published
# created_by: user_alice
---

# Bob 的编辑副本
---
title: "CodeReview Copilot（编辑副本 by Bob）"
type: for_category
status: draft
# created_by: user_bob
---

# 副本与原帖的关系
source_post_id: "post_bob_edit_copy"
target_post_id: "post_codereview_copilot"
relation_type: reference
position: 0
```
- 【预期结果】
  - Bob 无法直接 UPDATE Alice 的帖子
  - 创建副本 post 成功
  - 副本与原帖通过 post:post reference 关联

### 13.5 Journey 12：完整删除级联链

**TC-JOUR-012：完整 post 删除级联验证**

- 【用例描述】删除帖子后验证所有关联关系和 interaction 的级联处理
- 【前置条件】
  - 已存在 post，关联了：
    - category:post (submission)
    - post:post (embed + reference)
    - post:resource (attachment + inline)
    - interaction (like + comment + rating)
- 【Mock Data】
```yaml
# post
---
title: "级联删除测试帖子"
type: for_category
status: published
like_count: 2
comment_count: 3
average_rating: 83.85
---

# category:post
category_id: "cat_ai_hackathon_2025"
post_id: "post_cascade_test"
relation_type: submission

# post:post (被引用)
source_post_id: "post_other"
target_post_id: "post_cascade_test"
relation_type: reference
position: 0

# post:resource
post_id: "post_cascade_test"
resource_id: "res_project_demo_mp4"
display_type: attachment
position: 0

# interactions
---
type: like
target_type: post
target_id: "post_cascade_test"
---
---
type: comment
target_type: post
target_id: "post_cascade_test"
value: "评论1"
---
---
type: rating
target_type: post
target_id: "post_cascade_test"
value:
  创新性: 87
  技术实现: 82
  实用价值: 78
  演示效果: 91
---
```
- 【预期结果】
  - post 被软删除
  - category:post 关系解除
  - post:post 关系解除
  - post:resource 关系解除
  - 所有关联 interaction 被级联软删除

---

## 14. 通用 Mock Data 基座

> 以下为所有测试共享的基础 Mock 数据，确保字段完整、符合 command.md Schema。

### 14.1 用户（user）

```yaml
# user_alice (participant，主测试用户)
---
username: "alice"
email: "alice@example.com"
display_name: "Alice Chen"
avatar_url: "https://example.com/avatars/alice.png"
bio: "全栈开发者，AI 爱好者"
role: participant
# 自动生成: id, created_at, updated_at, deleted_at(null)
---
```

```yaml
# user_bob (participant，队友/被邀请者)
---
username: "bob"
email: "bob@example.com"
display_name: "Bob Wang"
avatar_url: "https://example.com/avatars/bob.png"
bio: "前端开发，React 专家"
role: participant
---
```

```yaml
# user_charlie (participant，辅助测试用户)
---
username: "charlie"
email: "charlie@example.com"
display_name: "Charlie Zhang"
avatar_url: "https://example.com/avatars/charlie.png"
bio: "UI 设计师，专注用户体验"
role: participant
---
```

```yaml
# user_org_01 (organizer，活动/规则创建者)
---
username: "org_01"
email: "org01@example.com"
display_name: "Organizer One"
role: organizer
---
```

```yaml
# user_admin_01 (admin，管理员)
---
username: "admin_01"
email: "admin01@example.com"
display_name: "Admin One"
role: admin
---
```

```yaml
# user_judge_01 (organizer，评委)
---
username: "judge_01"
email: "judge01@example.com"
display_name: "Judge One"
role: organizer
---
```

```yaml
# user_judge_02 (organizer，评委)
---
username: "judge_02"
email: "judge02@example.com"
display_name: "Judge Two"
role: organizer
---
```

### 14.2 活动与规则（category + rule）

```yaml
# cat_ai_hackathon_2025 (competition, published)
---
name: "2025 AI Hackathon"
description: "面向全球开发者的 AI 创新大赛"
type: competition
status: published
cover_image: "https://example.com/cover.png"
start_date: "2025-03-01T00:00:00Z"
end_date: "2025-03-15T23:59:59Z"
# 自动生成: id, created_by(user_org_01), created_at, updated_at, deleted_at(null)
---
## 活动介绍
本次 Hackathon 面向全球 AI 开发者。
```

```yaml
# rule_submission_01 (含完整 scoring_criteria)
---
name: "AI Hackathon 提交规则"
description: "2025 AI Hackathon 参赛提交规范"
allow_public: true
require_review: true
reviewers: ["user_judge_01", "user_judge_02"]
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
# 自动生成: id, created_by(user_org_01), created_at, updated_at, deleted_at(null)
---
```

```yaml
# category:rule 关系
category_id: "cat_ai_hackathon_2025"
rule_id: "rule_submission_01"
priority: 1
```

### 14.3 团队（group）

```yaml
# grp_team_synnovator (public, require_approval=true)
---
name: "Team Synnovator"
description: "AI Hackathon 参赛团队"
visibility: public
max_members: 5
require_approval: true
# 自动生成: id, created_by(user_alice), created_at, updated_at, deleted_at(null)
---
```

```yaml
# grp_team_alpha (辅助测试团队)
---
name: "Team Alpha"
description: "另一支参赛团队"
visibility: public
max_members: 5
require_approval: true
---
```

```yaml
# group:user 关系
# Alice = owner（自动 accepted）
group_id: "grp_team_synnovator"
user_id: "user_alice"
role: owner
status: accepted
# joined_at: 自动记录
```

```yaml
# Bob = member（pending，因 require_approval=true）
group_id: "grp_team_synnovator"
user_id: "user_bob"
role: member
status: pending
# status_changed_at: 自动记录
```

### 14.4 category:group 关系

```yaml
# 团队报名活动
category_id: "cat_ai_hackathon_2025"
group_id: "grp_team_synnovator"
# registered_at: 自动生成
```

### 14.5 帖子（post）

```yaml
# post_looking_for_teammates (general, published)
---
title: "【找队友】AI Hackathon 2025 一起组队做开发者工具"
type: general
tags: ["找队友", "提案"]
status: published
like_count: 0
comment_count: 0
average_rating: null
# 自动生成: id, created_by(user_alice), created_at, updated_at, deleted_at(null)
---
我们计划做一个"AI 代码审查助手"，欢迎前端/后端/LLM 应用同学加入。
```

```yaml
# post_team_synnovator (team, published)
---
title: "Team Synnovator"
type: team
tags: ["全栈", "AI"]
status: published
like_count: 0
comment_count: 0
average_rating: null
---
## 团队介绍
我们是一支专注于 AI 应用开发的全栈团队。

## 成员
- Alice — 后端 / 分布式
- Bob — 前端 / React
- Carol — AI / LLM 应用
```

```yaml
# post_codereview_copilot (for_category, published)
---
title: "AI 代码审查助手 — CodeReview Copilot"
type: for_category
tags: ["AI", "开发者工具", "代码审查"]
status: published
like_count: 0
comment_count: 0
average_rating: null
---
## 项目简介
CodeReview Copilot 是一款基于大语言模型的智能代码审查工具。

## 技术方案
- AST 解析 + LLM 理解的双层分析
- 支持 Python / JavaScript / Go

## 演示
[Demo 视频](https://example.com/demo.mp4)
```

```yaml
# post_data_labeling_agent (for_category, published)
---
title: "Data Labeling Agent"
type: for_category
tags: ["AI", "数据"]
status: published
like_count: 0
comment_count: 0
average_rating: null
---
## 项目简介
智能数据标注代理。
```

```yaml
# post_showcase_collection (general, published, reference 用途)
---
title: "优秀作品展示合集"
type: general
tags: ["展示"]
status: published
like_count: 0
comment_count: 0
average_rating: null
---
这里引用了多个作品链接。
```

```yaml
# post_stealth_draft (for_category, draft, 权限测试用)
---
title: "Stealth Project Draft"
type: for_category
tags: ["AI"]
status: draft
like_count: 0
comment_count: 0
average_rating: null
---
未发布草稿作品。
```

```yaml
# post_certificate_alice (certificate, published)
---
title: "2025 AI Hackathon 一等奖证书"
type: certificate
tags: ["证书", "AI Hackathon"]
status: published
like_count: 0
comment_count: 0
average_rating: null
---
## 获奖信息
- 活动: 2025 AI Hackathon
- 奖项: 一等奖
- 获奖者: Alice Chen
```

### 14.6 资源（resource）

```yaml
# res_project_demo_mp4
---
filename: "project-demo.mp4"
display_name: "项目演示视频"
description: "3 分钟 demo，用于提案展示"
# 自动生成: id, mime_type(video/mp4), size, url, created_by, created_at, updated_at, deleted_at(null)
---
```

```yaml
# res_source_code_zip
---
filename: "source-code.zip"
display_name: "源代码提交包"
description: "包含核心代码与README"
---
```

```yaml
# res_project_report_pdf
---
filename: "project-report.pdf"
display_name: "项目说明书"
description: "PDF 版技术报告"
---
```

```yaml
# res_cover_png
---
filename: "cover.png"
display_name: "封面图"
description: "活动/提案用封面"
---
```

```yaml
# res_certificate_alice_pdf
---
filename: "certificate-alice.pdf"
display_name: "一等奖证书 - Alice"
description: "2025 AI Hackathon 一等奖证书"
---
```

### 14.7 关系样本

```yaml
# post:post — embed 团队卡片到提案贴
source_post_id: "post_codereview_copilot"
target_post_id: "post_team_synnovator"
relation_type: embed
position: 1
```

```yaml
# post:post — reference 找队友贴引用提案贴
source_post_id: "post_looking_for_teammates"
target_post_id: "post_codereview_copilot"
relation_type: reference
position: 0
```

```yaml
# post:resource — 附件
post_id: "post_codereview_copilot"
resource_id: "res_project_demo_mp4"
display_type: attachment
position: 0
```

```yaml
# post:resource — 内联
post_id: "post_codereview_copilot"
resource_id: "res_source_code_zip"
display_type: inline
position: 1
```

```yaml
# category:post — submission
category_id: "cat_ai_hackathon_2025"
post_id: "post_codereview_copilot"
relation_type: submission
```

```yaml
# category:post — submission (第二个)
category_id: "cat_ai_hackathon_2025"
post_id: "post_data_labeling_agent"
relation_type: submission
```

```yaml
# category:post — reference
category_id: "cat_ai_hackathon_2025"
post_id: "post_showcase_collection"
relation_type: reference
```

### 14.8 Interaction 样本

```yaml
# iact_like_bob (点赞)
---
type: like
target_type: post
target_id: "post_codereview_copilot"
# created_by: user_bob
---
```

```yaml
# iact_comment_top (顶层评论)
---
type: comment
target_type: post
target_id: "post_codereview_copilot"
value: "方案很有创意！AST + LLM 的组合方式值得关注。请问支持哪些 CI/CD 集成？"
# created_by: user_bob
---
```

```yaml
# iact_comment_reply (嵌套回复)
---
type: comment
target_type: post
target_id: "post_codereview_copilot"
parent_id: "<iact_comment_top_id>"
value: "目前支持 GitHub Actions 和 GitLab CI，Jenkins 插件正在开发中。"
# created_by: user_alice
---
```

```yaml
# iact_rating_judge01 (评委1多维度评分)
---
type: rating
target_type: post
target_id: "post_codereview_copilot"
value:
  创新性: 87
  技术实现: 82
  实用价值: 78
  演示效果: 91
  _comment: "架构设计清晰，建议完善错误处理"
# created_by: user_judge_01
# 加权计算: 87×0.30 + 82×0.30 + 78×0.25 + 91×0.15 = 83.85
---
```

```yaml
# iact_rating_judge02 (评委2多维度评分，用于均值测试)
---
type: rating
target_type: post
target_id: "post_codereview_copilot"
value:
  创新性: 75
  技术实现: 90
  实用价值: 85
  演示效果: 70
  _comment: "技术实现扎实，但演示还需完善"
# created_by: user_judge_02
# 加权计算: 75×0.30 + 90×0.30 + 85×0.25 + 70×0.15 = 81.25
# 两次均值: (83.85 + 81.25) / 2 = 82.55
---
```

```yaml
# iact_like_on_category (对活动点赞，用于非 post 目标测试)
---
type: like
target_type: category
target_id: "cat_ai_hackathon_2025"
# created_by: user_bob
---
```

```yaml
# iact_comment_on_category (对活动评论)
---
type: comment
target_type: category
target_id: "cat_ai_hackathon_2025"
value: "这个活动太棒了！期待参加。"
# created_by: user_charlie
---
```

```yaml
# iact_like_on_resource (对资源点赞)
---
type: like
target_type: resource
target_id: "res_project_demo_mp4"
# created_by: user_charlie
---
```
