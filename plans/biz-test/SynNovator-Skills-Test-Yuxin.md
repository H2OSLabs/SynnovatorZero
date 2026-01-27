# Synnovator Skill 自动化测试指令集 (可执行版)

> **运行方式：** 按顺序执行每个 `bash` 代码块。所有命令使用 `engine.py` CLI，测试数据存放在 `.synnovator_test/` 中，与生产数据隔离。
>
> **前置条件：** 确保已安装 `pyyaml` (`uv add pyyaml`)

## 变量定义

以下固定 ID 在整个测试中保持一致：

```
ENGINE=.claude/skills/synnovator/scripts/engine.py
DATA_DIR=.synnovator_test
```

---

## 0. 准备工作：初始化测试环境

```bash
# 清除旧测试数据并初始化目录结构
rm -rf .synnovator_test && uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --init
```

**预期输出：** `{"status": "ok", "data_dir": ".../.synnovator_test"}`

---

## 1. 基础数据模型测试 (CRUD)

### 1.1 创建用户 (user)

```bash
# 创建组织者 Alice
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create user --data '{"id":"user_alice","username":"alice","email":"alice@example.com","display_name":"Alice Chen","role":"organizer"}'
```

**验证：** 返回 JSON 中 `id` = `user_alice`，`role` = `organizer`，自动生成 `created_at`。

```bash
# 创建参赛者 Bob
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create user --data '{"id":"user_bob","username":"bob","email":"bob@example.com","display_name":"Bob Li","role":"participant"}'
```

```bash
# 创建参赛者 Carol
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create user --data '{"id":"user_carol","username":"carol","email":"carol@example.com","display_name":"Carol Zhang","role":"participant"}'
```

```bash
# 创建参赛者 Dave
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create user --data '{"id":"user_dave","username":"dave","email":"dave@example.com","display_name":"Dave Wu","role":"participant"}'
```

```bash
# 创建评委 Judge
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create user --data '{"id":"user_judge","username":"judge01","email":"judge@example.com","display_name":"Judge One","role":"organizer"}'
```

### 1.2 创建活动 (category)

```bash
# 创建一个 type: competition 的 category，状态设为 published
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create category --data '{"id":"cat_hackathon_2025","name":"2025 AI Hackathon","description":"Global AI innovation competition","type":"competition","status":"published","start_date":"2025-03-01T00:00:00Z","end_date":"2025-03-15T23:59:59Z"}' --body '## About

AI Hackathon for developers worldwide.'
```

**验证：**
- 返回 JSON 中 `id` = `cat_hackathon_2025`
- `type` = `competition`，`status` = `published`
- 包含 `name`, `description`, `start_date` 字段
- `has_body` = `true`

```bash
# 读取验证：确认活动已创建
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read category --id cat_hackathon_2025
```

### 1.3 创建团队 (group) 并验证关系

```bash
# 以 Alice 身份创建一个 group，设置 require_approval: true
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create group --data '{"id":"grp_team_synnovator","name":"Team Synnovator","description":"AI Hackathon team","visibility":"public","max_members":5,"require_approval":true}'
```

```bash
# 将 Alice 设为 group owner
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create group_user --data '{"group_id":"grp_team_synnovator","user_id":"user_alice","role":"owner"}'
```

**验证：** `role` = `owner`，`status` = `accepted`（owner 自动 accepted）。

```bash
# 读取验证：group:user 关系
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read group_user --filters '{"group_id":"grp_team_synnovator","user_id":"user_alice"}'
```

### 1.4 创建资源 (resource)

```bash
# 创建一个 resource 实体
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create resource --data '{"id":"res_demo_video","filename":"demo.mp4","display_name":"Demo Video","mime_type":"video/mp4","url":"https://storage.example.com/demo.mp4"}'
```

**验证：** `filename` = `demo.mp4`，`mime_type` = `video/mp4`，`url` 字段非空。

```bash
# 读取验证
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read resource --id res_demo_video
```

---

## 2. 核心业务逻辑测试 (Logic & Rules)

### 2.1 创建规则 (rule) 并关联活动

```bash
# 创建评审规则
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create rule --data '{"id":"rule_submission_01","name":"AI Hackathon Submission Rule","description":"2025 AI Hackathon submission requirements","allow_public":true,"require_review":true,"reviewers":["user_judge"],"submission_start":"2025-03-01T00:00:00Z","submission_deadline":"2025-03-14T23:59:59Z","submission_format":["markdown","pdf","zip"],"max_submissions":3,"min_team_size":1,"max_team_size":5,"scoring_criteria":[{"name":"创新性","weight":30,"description":"Originality"},{"name":"技术实现","weight":30,"description":"Code quality"},{"name":"实用价值","weight":25,"description":"Practical value"},{"name":"演示效果","weight":15,"description":"Demo quality"}]}' --body '## Rules

1. Submit project docs, source code, demo video.'
```

```bash
# 将 Rule 关联至活动
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create category_rule --data '{"category_id":"cat_hackathon_2025","rule_id":"rule_submission_01","priority":1}'
```

**验证：** category_rule 关系已创建。

```bash
# 读取验证：活动关联的规则
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read category_rule --filters '{"category_id":"cat_hackathon_2025"}'
```

### 2.2 创建 "Not Create Only Select" 规则

```bash
# 创建 select-only 规则（不允许新建 Post，只能选择已有）
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create rule --data '{"id":"rule_select_only","name":"Select Only Rule","description":"Only allow selecting existing posts, not creating new ones","allow_public":false,"require_review":true}'
```

**验证：** `allow_public` = `false`，`require_review` = `true`。

```bash
# 读取验证
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read rule --id rule_select_only
```

### 2.3 创建参赛提案 (post type=for_category)

```bash
# 先创建 Alice 的个人简介 Post（后续测试需要）
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create post --data '{"id":"post_profile_alice","title":"About Alice","type":"profile","status":"published","tags":["backend","AI"]}' --body '## About Me

Full-stack developer with AI focus.'
```

```bash
# 为活动创建参赛提案
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create post --data '{"id":"post_submission_01","title":"AI Code Review Copilot","type":"for_category","tags":["AI","Developer Tools"]}' --body '## Project

CodeReview Copilot is an AI-powered code review tool.'
```

**验证：** `type` = `for_category`，`status` 初始值为 `draft`（默认值）。

```bash
# 将提案关联到活动（submission 类型）
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create category_post --data '{"category_id":"cat_hackathon_2025","post_id":"post_submission_01","relation_type":"submission"}'
```

### 2.4 编辑逻辑与版本管理

```bash
# 创建新版本的提案（模拟编辑 = 创建新版本）
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create post --data '{"id":"post_submission_v2","title":"AI Code Review Copilot v2","type":"for_category","tags":["AI","Developer Tools"]}' --body '## Updated Project

Now with better error handling and CI/CD support.'
```

```bash
# 通过 post_post 关系链接新旧版本
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create post_post --data '{"source_post_id":"post_submission_v2","target_post_id":"post_submission_01","relation_type":"reference"}'
```

**验证：** 新 Post 有独立的 `id`（`post_submission_v2`），通过 `post_post` 关系保留与原版本的关联。

```bash
# 发布新版本（rule.allow_public=true 允许直接发布）
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update post --id post_submission_v2 --data '{"status":"published"}'
```

**验证：** `status` = `published`。

### 2.5 测试审核流程 (pending_review → published / rejected)

```bash
# 创建需要审核的 Post
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_bob create post --data '{"id":"post_needs_review","title":"Needs Review Post","type":"for_category"}'
```

```bash
# 提交审核
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update post --id post_needs_review --data '{"status":"pending_review"}'
```

**验证：** `status` = `pending_review`。

```bash
# 审核通过
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update post --id post_needs_review --data '{"status":"published"}'
```

```bash
# 创建另一个 Post 测试拒绝流程
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_bob create post --data '{"id":"post_will_reject","title":"Will Be Rejected","type":"for_category"}'
```

```bash
# 提交审核 → 拒绝
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update post --id post_will_reject --data '{"status":"pending_review"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update post --id post_will_reject --data '{"status":"rejected"}'
```

**验证：** `status` = `rejected`。

```bash
# 读取验证
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read post --id post_will_reject
```

---

## 3. 关系与统计验证

### 3.1 列出某活动的提案

```bash
# READ category_post，过滤 relation_type: submission
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read category_post --filters '{"category_id":"cat_hackathon_2025","relation_type":"submission"}'
```

**验证：** 输出列表仅包含 `relation_type` = `submission` 的记录，包含 `post_submission_01`。

### 3.2 社区互动与缓存更新

```bash
# 发布 submission_01 以便进行互动
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update post --id post_submission_01 --data '{"status":"published"}'
```

```bash
# 3.2.1 点赞 (like)
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_dave create interaction --data '{"id":"iact_like_01","type":"like","target_type":"post","target_id":"post_submission_01"}'
```

```bash
# 3.2.2 创建 target_interaction 关系
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create target_interaction --data '{"target_type":"post","target_id":"post_submission_01","interaction_id":"iact_like_01"}'
```

```bash
# 3.2.3 评论 (comment)
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_bob create interaction --data '{"id":"iact_comment_01","type":"comment","target_type":"post","target_id":"post_submission_01","value":"Great project! How does the AST parsing work?"}'
```

```bash
# 3.2.4 检查缓存计数是否自动更新
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read post --id post_submission_01
```

**验证：**
- `like_count` >= 1
- `comment_count` >= 1

### 3.3 评分 (rating) 与加权平均

```bash
# 创建多维度评分
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_judge create interaction --data '{"id":"iact_rating_01","type":"rating","target_type":"post","target_id":"post_submission_01","value":{"创新性":87,"技术实现":82,"实用价值":78,"演示效果":91,"_comment":"Well-designed architecture"}}'
```

```bash
# 检查 average_rating 是否已自动计算
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read post --id post_submission_01
```

**验证：**
- `average_rating` ≈ 83.85（计算：87×0.30 + 82×0.30 + 78×0.25 + 91×0.15 = 83.85）
- `like_count` >= 1
- `comment_count` >= 1

### 3.4 重复点赞拦截

```bash
# Dave 重复点赞同一目标，应该报错
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_dave create interaction --data '{"type":"like","target_type":"post","target_id":"post_submission_01"}'
```

**验证：** 返回 `stderr` 错误信息包含 `already liked`，退出码非 0。

---

## 4. 团队审批工作流

### 4.1 加入需要审批的团队

```bash
# Carol 申请加入团队（require_approval=true → status=pending）
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create group_user --data '{"group_id":"grp_team_synnovator","user_id":"user_carol","role":"member"}'
```

**验证：** `status` = `pending`（因为团队设置了 `require_approval: true`）。

```bash
# Alice 批准 Carol
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update group_user --filters '{"group_id":"grp_team_synnovator","user_id":"user_carol"}' --data '{"status":"accepted"}'
```

**验证：** `status` = `accepted`，`joined_at` 字段已赋值。

### 4.2 拒绝与重新申请

```bash
# Bob 申请加入
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create group_user --data '{"group_id":"grp_team_synnovator","user_id":"user_bob","role":"member"}'
```

```bash
# 拒绝 Bob
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update group_user --filters '{"group_id":"grp_team_synnovator","user_id":"user_bob"}' --data '{"status":"rejected"}'
```

```bash
# Bob 重新申请（被拒绝后应可以重新申请）
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create group_user --data '{"group_id":"grp_team_synnovator","user_id":"user_bob","role":"member"}'
```

**验证：** 重新申请成功，`status` = `pending`。

```bash
# 读取全部成员
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read group_user --filters '{"group_id":"grp_team_synnovator"}'
```

---

## 5. "Not Create Only Select" 规则模拟

```bash
# Bob 创建一个日常 Post
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_bob create post --data '{"id":"post_daily_bob","title":"My Daily Update","tags":["diary"],"status":"published"}' --body '## Today

Worked on the project.'
```

```bash
# 模拟 "选择已有 Post" 报名：给已有 Post 打上活动标签
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update post --id post_daily_bob --data '{"tags":"+for_ai_hackathon"}'
```

**验证：** `tags` 列表中包含 `for_ai_hackathon`。

```bash
# 读取验证
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read post --id post_daily_bob
```

---

## 6. 删除功能与级联验证

### 6.1 创建测试用 Post 及关联数据

```bash
# 创建待删除的 Post
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create post --data '{"id":"post_to_delete","title":"To Be Deleted","status":"published"}' --body 'This will be deleted.'
```

```bash
# 为该 Post 创建关联关系
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create category_post --data '{"category_id":"cat_hackathon_2025","post_id":"post_to_delete","relation_type":"reference"}'
```

```bash
# 为该 Post 创建互动（点赞）
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_bob create interaction --data '{"id":"iact_like_del","type":"like","target_type":"post","target_id":"post_to_delete"}'
```

### 6.2 执行软删除

```bash
# 删除 Post（软删除）
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test delete post --id post_to_delete
```

**验证：** `mode` = `soft`。

### 6.3 验证级联效果

```bash
# 验证：关联的 category_post 关系已被级联删除
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read category_post --filters '{"post_id":"post_to_delete"}'
```

**验证：** 返回空列表 `[]`。

```bash
# 验证：关联的 interaction 已被软删除（需要 --include-deleted 才能看到）
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read interaction --id iact_like_del --include-deleted
```

**验证：** `deleted_at` 字段非空。

```bash
# 验证：Post 本身已无法被普通 READ 检索（应报错 soft-deleted）
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read post --id post_to_delete
```

**验证：** 返回 `stderr` 错误信息包含 `soft-deleted`，退出码非 0。

---

## 7. 清理测试环境

```bash
# 清除测试数据
rm -rf .synnovator_test
```

---

## 快速全量执行（一键运行）

将以上所有命令整合为一个脚本，可直接执行：

```bash
uv run python .claude/skills/synnovator/scripts/test_journeys.py
```

此脚本执行所有 13 个用户旅程的自动化测试，包含 60+ 断言，使用独立的 `.synnovator_test/` 目录，运行后自动清理。
