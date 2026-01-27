# Synnovator Skill 补充测试指令集 (Fill-Gap)

> **目的：** 覆盖 `SynNovator-Skills-Test-Yuxin.md` 未测试的场景，包括缺失的 UPDATE/DELETE 操作、未覆盖的关系类型、用户旅程、枚举验证、边界条件等。
>
> **运行方式：** 按顺序执行每个 `bash` 代码块。测试数据存放在 `.synnovator_test/` 中。
>
> **前置条件：** 确保已安装 `pyyaml` (`uv add pyyaml`)
>
> **依赖：** 本测试在 `SynNovator-Skills-Test-Yuxin.md` 的 Section 0-2 执行完成后运行，或独立初始化。

---

## 0. 初始化测试环境与基础数据

```bash
rm -rf .synnovator_test && uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --init
```

```bash
# 创建基础用户
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create user --data '{"id":"user_alice","username":"alice","email":"alice@example.com","display_name":"Alice Chen","role":"organizer"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create user --data '{"id":"user_bob","username":"bob","email":"bob@example.com","display_name":"Bob Li","role":"participant"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create user --data '{"id":"user_carol","username":"carol","email":"carol@example.com","display_name":"Carol Zhang","role":"participant"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create user --data '{"id":"user_dave","username":"dave","email":"dave@example.com","display_name":"Dave Wu","role":"participant"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create user --data '{"id":"user_judge","username":"judge01","email":"judge@example.com","display_name":"Judge One","role":"organizer"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create user --data '{"id":"user_admin","username":"admin01","email":"admin@example.com","display_name":"Admin","role":"admin"}'
```

```bash
# 创建基础活动 + 规则 + 团队
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create category --data '{"id":"cat_hackathon","name":"2025 AI Hackathon","description":"Global AI competition","type":"competition","status":"published","start_date":"2025-03-01T00:00:00Z","end_date":"2025-03-15T23:59:59Z"}' --body '## About the Hackathon'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create rule --data '{"id":"rule_main","name":"Main Rule","description":"Submission requirements","allow_public":true,"require_review":true,"reviewers":["user_judge"],"scoring_criteria":[{"name":"Innovation","weight":30,"description":"Originality"},{"name":"Technical","weight":30,"description":"Code quality"},{"name":"Practical","weight":25,"description":"Practical value"},{"name":"Demo","weight":15,"description":"Demo quality"}]}' --body '## Rules'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create category_rule --data '{"category_id":"cat_hackathon","rule_id":"rule_main","priority":1}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create group --data '{"id":"grp_alpha","name":"Team Alpha","description":"First team","visibility":"public","max_members":5,"require_approval":true}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create group_user --data '{"group_id":"grp_alpha","user_id":"user_alice","role":"owner"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create group --data '{"id":"grp_beta","name":"Team Beta","description":"Second team","visibility":"private","require_approval":false}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create group_user --data '{"group_id":"grp_beta","user_id":"user_bob","role":"owner"}'
```

```bash
# 创建基础帖子
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create post --data '{"id":"post_sub_01","title":"AI Copilot Project","type":"for_category","status":"published","tags":["AI"]}' --body '## Project Description'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create category_post --data '{"category_id":"cat_hackathon","post_id":"post_sub_01","relation_type":"submission"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_bob create post --data '{"id":"post_general_01","title":"General Discussion","type":"general","status":"published"}' --body '## Discussion'
```

**预期：** 所有基础数据创建成功，为后续补充测试提供上下文。

---

## 1. UPDATE 操作补充测试

### 1.1 UPDATE category（活动字段修改）

```bash
# 修改活动名称和描述
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update category --id cat_hackathon --data '{"name":"2025 AI Hackathon - Updated","description":"Updated global AI competition"}'
```

**验证：** `name` = `2025 AI Hackathon - Updated`，`updated_at` 已更新。

```bash
# 修改活动状态：published → closed
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update category --id cat_hackathon --data '{"status":"closed"}'
```

**验证：** `status` = `closed`。

```bash
# 恢复为 published（用于后续测试）
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update category --id cat_hackathon --data '{"status":"published"}'
```

### 1.2 UPDATE rule（规则字段修改）

```bash
# 修改规则字段
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update rule --id rule_main --data '{"allow_public":false,"max_submissions":5}'
```

**验证：** `allow_public` = `false`，`max_submissions` = `5`。

```bash
# 读取验证
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read rule --id rule_main
```

```bash
# 恢复 allow_public
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update rule --id rule_main --data '{"allow_public":true}'
```

### 1.3 UPDATE user（用户信息修改）

```bash
# 修改用户显示名和简介
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update user --id user_bob --data '{"display_name":"Bob Li (Updated)","bio":"Full-stack developer"}'
```

**验证：** `display_name` = `Bob Li (Updated)`，`bio` = `Full-stack developer`。

```bash
# 读取验证
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read user --id user_bob
```

### 1.4 UPDATE group（团队信息修改）

```bash
# 修改团队 visibility 和 require_approval
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update group --id grp_alpha --data '{"visibility":"private","description":"Updated team description"}'
```

**验证：** `visibility` = `private`，`description` 已更新。

```bash
# 恢复 visibility
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update group --id grp_alpha --data '{"visibility":"public"}'
```

### 1.5 UPDATE resource（资源元数据修改）

```bash
# 创建资源用于更新测试
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create resource --data '{"id":"res_update_test","filename":"doc.pdf","display_name":"Original Name"}'
```

```bash
# 更新 display_name 和 description
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update resource --id res_update_test --data '{"display_name":"Updated Name","description":"Added description"}'
```

**验证：** `display_name` = `Updated Name`，`description` = `Added description`。

### 1.6 UPDATE interaction（修改评论内容）

```bash
# 创建评论
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_bob create interaction --data '{"id":"iact_edit_comment","type":"comment","target_type":"post","target_id":"post_sub_01","value":"Original comment"}'
```

```bash
# 修改评论内容
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update interaction --id iact_edit_comment --data '{"value":"Edited comment content"}'
```

**验证：** `value` = `Edited comment content`，`updated_at` 已更新。

```bash
# 读取验证
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read interaction --id iact_edit_comment
```

### 1.7 UPDATE post（标签移除 -tag 语法）

```bash
# 先添加多个标签
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update post --id post_general_01 --data '{"tags":"+devlog"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update post --id post_general_01 --data '{"tags":"+update"}'
```

```bash
# 移除标签
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update post --id post_general_01 --data '{"tags":"-devlog"}'
```

**验证：** `tags` 不再包含 `devlog`，但仍包含 `update`。

```bash
# 读取验证
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read post --id post_general_01
```

### 1.8 UPDATE post body（直接修改 Markdown 内容）

```bash
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update post --id post_general_01 --data '{"title":"General Discussion - Revised"}' --body '## Revised Discussion

New markdown content here.'
```

**验证：** `title` = `General Discussion - Revised`，`has_body` = `true`。

---

## 2. DELETE 操作补充测试（非 Post 类型）

### 2.1 DELETE rule（规则软删除 + 级联）

```bash
# 创建临时规则并关联
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create rule --data '{"id":"rule_temp","name":"Temp Rule","description":"Will be deleted"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create category_rule --data '{"category_id":"cat_hackathon","rule_id":"rule_temp","priority":2}'
```

```bash
# 软删除规则
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test delete rule --id rule_temp
```

**验证：** `mode` = `soft`。

```bash
# 验证级联：category_rule 关系已被删除
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read category_rule --filters '{"rule_id":"rule_temp"}'
```

**验证：** 返回空列表 `[]`。

```bash
# 验证规则本身不可读
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read rule --id rule_temp 2>&1; echo "EXIT=$?"
```

**验证：** 错误信息包含 `soft-deleted`，EXIT=1。

### 2.2 DELETE user（用户软删除 + 交互级联）

```bash
# 先为 Dave 创建一些交互数据
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_dave create interaction --data '{"id":"iact_dave_like","type":"like","target_type":"post","target_id":"post_sub_01"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_dave create interaction --data '{"id":"iact_dave_comment","type":"comment","target_type":"post","target_id":"post_sub_01","value":"Nice work"}'
```

```bash
# 软删除用户
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test delete user --id user_dave
```

**验证：** `mode` = `soft`。

```bash
# 验证级联：Dave 的交互已软删除
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read interaction --id iact_dave_like --include-deleted
```

**验证：** `deleted_at` 非空。

```bash
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read interaction --id iact_dave_comment --include-deleted
```

**验证：** `deleted_at` 非空。

```bash
# 验证用户本身不可读
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read user --id user_dave 2>&1; echo "EXIT=$?"
```

**验证：** 错误信息包含 `soft-deleted`，EXIT=1。

### 2.3 DELETE group（团队软删除 + 关系级联）

```bash
# 先让 Carol 加入 Beta 团队并注册活动
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create group_user --data '{"group_id":"grp_beta","user_id":"user_carol","role":"member"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create category_group --data '{"category_id":"cat_hackathon","group_id":"grp_beta"}'
```

```bash
# 软删除团队
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test delete group --id grp_beta
```

**验证：** `mode` = `soft`。

```bash
# 验证级联：category_group 关系已删除
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read category_group --filters '{"group_id":"grp_beta"}'
```

**验证：** 返回空列表 `[]`。

```bash
# 验证团队本身不可读
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read group --id grp_beta 2>&1; echo "EXIT=$?"
```

**验证：** 错误信息包含 `soft-deleted`，EXIT=1。

### 2.4 DELETE category（活动软删除 + 多级联）

```bash
# 创建临时活动及完整关联数据
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create category --data '{"id":"cat_temp","name":"Temp Event","description":"Will be deleted","type":"operation","status":"published"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create rule --data '{"id":"rule_temp2","name":"Temp Rule 2","description":"For temp event"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create category_rule --data '{"category_id":"cat_temp","rule_id":"rule_temp2","priority":1}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_bob create post --data '{"id":"post_temp","title":"Temp Post","type":"for_category","status":"published"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create category_post --data '{"category_id":"cat_temp","post_id":"post_temp","relation_type":"submission"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create group --data '{"id":"grp_temp","name":"Temp Team","description":"Temp","require_approval":false}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create group_user --data '{"group_id":"grp_temp","user_id":"user_alice","role":"owner"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create category_group --data '{"category_id":"cat_temp","group_id":"grp_temp"}'
```

```bash
# 软删除活动
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test delete category --id cat_temp
```

**验证：** `mode` = `soft`。

```bash
# 验证级联：所有关联关系已删除
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read category_rule --filters '{"category_id":"cat_temp"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read category_post --filters '{"category_id":"cat_temp"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read category_group --filters '{"category_id":"cat_temp"}'
```

**验证：** 三个查询均返回空列表 `[]`。

```bash
# 验证活动本身不可读
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read category --id cat_temp 2>&1; echo "EXIT=$?"
```

**验证：** 错误信息包含 `soft-deleted`，EXIT=1。

---

## 3. category:group 关系测试（Journey 7 团队报名）

### 3.1 团队注册活动

```bash
# Alpha 团队注册 Hackathon
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create category_group --data '{"category_id":"cat_hackathon","group_id":"grp_alpha"}'
```

**验证：** 关系创建成功，包含 `category_id` 和 `group_id`。

```bash
# 读取活动注册的团队列表
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read category_group --filters '{"category_id":"cat_hackathon"}'
```

**验证：** 包含 `grp_alpha`。

### 3.2 重复注册拦截

```bash
# 同一团队重复注册同一活动，应报错
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create category_group --data '{"category_id":"cat_hackathon","group_id":"grp_alpha"}' 2>&1; echo "EXIT=$?"
```

**验证：** 错误信息包含 `already registered`，EXIT=1。

### 3.3 DELETE category:group（退出活动）

```bash
# 创建另一个团队注册后退出
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_carol create group --data '{"id":"grp_gamma","name":"Team Gamma","description":"Third team","require_approval":false}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create group_user --data '{"group_id":"grp_gamma","user_id":"user_carol","role":"owner"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create category_group --data '{"category_id":"cat_hackathon","group_id":"grp_gamma"}'
```

```bash
# 退出活动
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test delete category_group --filters '{"category_id":"cat_hackathon","group_id":"grp_gamma"}'
```

```bash
# 验证已退出
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read category_group --filters '{"group_id":"grp_gamma"}'
```

**验证：** 返回空列表 `[]`。

---

## 4. Journey 10：获取证书流程

```bash
# Step 1: 关闭活动
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update category --id cat_hackathon --data '{"status":"closed"}'
```

**验证：** `status` = `closed`。

```bash
# Step 2: 创建证书资源
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create resource --data '{"id":"res_cert_alice","filename":"certificate_alice.pdf","display_name":"Participation Certificate","description":"AI Hackathon 2025"}'
```

```bash
# Step 3: 将证书关联到参赛帖子
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create post_resource --data '{"post_id":"post_sub_01","resource_id":"res_cert_alice","display_type":"attachment"}'
```

**验证：** `display_type` = `attachment`。

```bash
# Step 4: 创建证书分享帖子
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create post --data '{"id":"post_cert_share","title":"My Hackathon Certificate","type":"certificate","status":"published"}' --body '## Certificate

Proud to have participated in the AI Hackathon.'
```

**验证：** `type` = `certificate`，`status` = `published`。

```bash
# Step 5: 读取证书资源
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read resource --id res_cert_alice
```

**验证：** `filename` = `certificate_alice.pdf`，`display_name` = `Participation Certificate`。

```bash
# 恢复活动状态用于后续测试
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update category --id cat_hackathon --data '{"status":"published"}'
```

---

## 5. 关系 UPDATE 和 DELETE 补充

### 5.1 UPDATE category_rule（修改优先级）

```bash
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update category_rule --filters '{"category_id":"cat_hackathon","rule_id":"rule_main"}' --data '{"priority":10}'
```

**验证：** `priority` = `10`。

```bash
# 读取验证
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read category_rule --filters '{"category_id":"cat_hackathon"}'
```

### 5.2 UPDATE category_post（修改关系类型）

```bash
# 创建一个 reference 类型的关联
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create category_post --data '{"category_id":"cat_hackathon","post_id":"post_general_01","relation_type":"reference"}'
```

```bash
# 读取验证包含两种 relation_type
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read category_post --filters '{"category_id":"cat_hackathon"}'
```

**验证：** 包含 `submission`（post_sub_01）和 `reference`（post_general_01）两种记录。

### 5.3 DELETE category_rule（移除规则关联）

```bash
# 创建临时规则关联后删除
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create rule --data '{"id":"rule_removable","name":"Removable Rule","description":"Will be unlinked"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create category_rule --data '{"category_id":"cat_hackathon","rule_id":"rule_removable","priority":99}'
```

```bash
# 删除关系（不删除规则本身）
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test delete category_rule --filters '{"category_id":"cat_hackathon","rule_id":"rule_removable"}'
```

```bash
# 验证关系已删除
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read category_rule --filters '{"rule_id":"rule_removable"}'
```

**验证：** 返回空列表 `[]`。

```bash
# 验证规则本身仍然存在
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read rule --id rule_removable
```

**验证：** 规则仍可读取。

### 5.4 DELETE group_user（移除团队成员）

```bash
# 先添加 Carol 到 Alpha 团队
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create group_user --data '{"group_id":"grp_alpha","user_id":"user_carol","role":"member"}'
```

```bash
# 审批通过
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update group_user --filters '{"group_id":"grp_alpha","user_id":"user_carol"}' --data '{"status":"accepted"}'
```

```bash
# 移除成员
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test delete group_user --filters '{"group_id":"grp_alpha","user_id":"user_carol"}'
```

```bash
# 验证成员已移除
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read group_user --filters '{"group_id":"grp_alpha","user_id":"user_carol"}'
```

**验证：** 返回空列表 `[]`。

### 5.5 DELETE post_post（移除帖子引用）

```bash
# 创建两个帖子并建立引用关系
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_bob create post --data '{"id":"post_ref_source","title":"Source Post","status":"published"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create post_post --data '{"source_post_id":"post_ref_source","target_post_id":"post_sub_01","relation_type":"reference"}'
```

```bash
# 删除引用关系
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test delete post_post --filters '{"source_post_id":"post_ref_source","target_post_id":"post_sub_01"}'
```

```bash
# 验证关系已删除
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read post_post --filters '{"source_post_id":"post_ref_source"}'
```

**验证：** 返回空列表 `[]`。

### 5.6 DELETE post_resource（移除资源关联）

```bash
# 创建资源并关联
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_bob create resource --data '{"id":"res_removable","filename":"temp.txt","display_name":"Temp File"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create post_resource --data '{"post_id":"post_ref_source","resource_id":"res_removable","display_type":"inline"}'
```

```bash
# 删除关联（不删除资源本身）
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test delete post_resource --filters '{"post_id":"post_ref_source","resource_id":"res_removable"}'
```

```bash
# 验证关系已删除，资源仍在
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read post_resource --filters '{"resource_id":"res_removable"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read resource --id res_removable
```

**验证：** 关系返回空列表 `[]`，资源仍可读取。

---

## 6. 枚举验证（无效值拦截）

### 6.1 无效 category.type

```bash
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create category --data '{"name":"Bad Event","description":"Invalid type","type":"invalid_type"}' 2>&1; echo "EXIT=$?"
```

**验证：** 错误信息包含 `Invalid value`，EXIT=1。

### 6.2 无效 post.status

```bash
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update post --id post_general_01 --data '{"status":"nonexistent_status"}' 2>&1; echo "EXIT=$?"
```

**验证：** 错误信息包含 `Invalid value`，EXIT=1。

### 6.3 无效 user.role

```bash
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create user --data '{"username":"bad_role","email":"bad@example.com","role":"superuser"}' 2>&1; echo "EXIT=$?"
```

**验证：** 错误信息包含 `Invalid value`，EXIT=1。

### 6.4 无效 group.visibility

```bash
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create group --data '{"name":"Bad Group","visibility":"hidden"}' 2>&1; echo "EXIT=$?"
```

**验证：** 错误信息包含 `Invalid value`，EXIT=1。

### 6.5 无效 interaction.type

```bash
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_bob create interaction --data '{"type":"bookmark","target_type":"post","target_id":"post_sub_01"}' 2>&1; echo "EXIT=$?"
```

**验证：** 错误信息包含 `Invalid value`，EXIT=1。

### 6.6 无效 group_user.role

```bash
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create group_user --data '{"group_id":"grp_alpha","user_id":"user_bob","role":"superadmin"}' 2>&1; echo "EXIT=$?"
```

**验证：** 错误信息包含 `Invalid value`，EXIT=1。

---

## 7. 唯一性约束补充

### 7.1 重复 category_rule

```bash
# 同一规则重复关联到同一活动
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create category_rule --data '{"category_id":"cat_hackathon","rule_id":"rule_main","priority":1}' 2>&1; echo "EXIT=$?"
```

**验证：** 错误信息包含 `already linked`，EXIT=1。

### 7.2 重复 group_user（已 accepted 的成员再次加入）

```bash
# Alice 已是 owner，重复加入应报错
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create group_user --data '{"group_id":"grp_alpha","user_id":"user_alice","role":"member"}' 2>&1; echo "EXIT=$?"
```

**验证：** 错误信息包含 `already in this group`，EXIT=1。

### 7.3 重复 email

```bash
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create user --data '{"username":"alice_clone","email":"alice@example.com","display_name":"Fake Alice"}' 2>&1; echo "EXIT=$?"
```

**验证：** 错误信息包含 `already exists`，EXIT=1。

---

## 8. 边界条件与错误路径

### 8.1 对已删除目标创建交互

```bash
# 创建并删除一个帖子
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_bob create post --data '{"id":"post_deleted_target","title":"Will Delete","status":"published"}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test delete post --id post_deleted_target
```

```bash
# 尝试对已删除帖子点赞
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_carol create interaction --data '{"type":"like","target_type":"post","target_id":"post_deleted_target"}' 2>&1; echo "EXIT=$?"
```

**验证：** 错误信息包含 `soft-deleted`，EXIT=1。

### 8.2 对不存在的目标创建交互

```bash
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_bob create interaction --data '{"type":"comment","target_type":"post","target_id":"post_nonexistent","value":"ghost comment"}' 2>&1; echo "EXIT=$?"
```

**验证：** 错误信息包含 `not found`，EXIT=1。

### 8.3 更新已软删除的内容

```bash
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test update post --id post_deleted_target --data '{"title":"Should Fail"}' 2>&1; echo "EXIT=$?"
```

**验证：** 错误信息包含 `soft-deleted`，EXIT=1。

### 8.4 读取不存在的记录

```bash
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read user --id user_nonexistent 2>&1; echo "EXIT=$?"
```

**验证：** 错误信息包含 `not found`，EXIT=1。

### 8.5 缺少必填字段

```bash
# 创建 user 缺少 email
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create user --data '{"username":"no_email"}' 2>&1; echo "EXIT=$?"
```

**验证：** 错误信息包含 `Missing required field`，EXIT=1。

```bash
# 创建 interaction 缺少 target_id
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_bob create interaction --data '{"type":"like","target_type":"post"}' 2>&1; echo "EXIT=$?"
```

**验证：** 错误信息包含 `Missing required field`，EXIT=1。

### 8.6 嵌套评论（二级回复）

```bash
# 创建顶层评论
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_bob create interaction --data '{"id":"iact_top_comment","type":"comment","target_type":"post","target_id":"post_sub_01","value":"Top-level comment"}'
```

```bash
# 创建一级回复
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create interaction --data '{"id":"iact_reply_l1","type":"comment","target_type":"post","target_id":"post_sub_01","parent_id":"iact_top_comment","value":"Level 1 reply"}'
```

```bash
# 创建二级回复（回复的回复）
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_bob create interaction --data '{"id":"iact_reply_l2","type":"comment","target_type":"post","target_id":"post_sub_01","parent_id":"iact_reply_l1","value":"Level 2 reply"}'
```

**验证：** `iact_reply_l2` 的 `parent_id` = `iact_reply_l1`。

```bash
# 验证 comment_count 包括所有层级
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read post --id post_sub_01
```

**验证：** `comment_count` >= 4（包含之前的评论和此处3条新评论）。

### 8.7 删除父评论时级联删除子评论

```bash
# 删除顶层评论
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test delete interaction --id iact_top_comment
```

```bash
# 验证子评论也被级联软删除
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read interaction --id iact_reply_l1 --include-deleted
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read interaction --id iact_reply_l2 --include-deleted
```

**验证：** `iact_reply_l1` 和 `iact_reply_l2` 的 `deleted_at` 均非空。

---

## 9. 私有团队 (visibility: private) 与无需审批团队

### 9.1 创建 private 团队

```bash
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create group --data '{"id":"grp_private","name":"Private Team","description":"Invitation only","visibility":"private","require_approval":true}'
```

**验证：** `visibility` = `private`。

### 9.2 无需审批的团队直接 accepted

```bash
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create group --data '{"id":"grp_open","name":"Open Team","description":"No approval needed","visibility":"public","require_approval":false}'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create group_user --data '{"group_id":"grp_open","user_id":"user_alice","role":"owner"}'
```

```bash
# Bob 加入无需审批的团队
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create group_user --data '{"group_id":"grp_open","user_id":"user_bob","role":"member"}'
```

**验证：** `status` = `accepted`（无需审批直接通过），`joined_at` 已赋值。

---

## 10. 交互目标类型扩展（非 post 目标）

### 10.1 对 category 点赞

```bash
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_bob create interaction --data '{"id":"iact_like_cat","type":"like","target_type":"category","target_id":"cat_hackathon"}'
```

**验证：** `target_type` = `category`，创建成功。

### 10.2 对 resource 评论

```bash
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_bob create interaction --data '{"id":"iact_comment_res","type":"comment","target_type":"resource","target_id":"res_cert_alice","value":"Nice certificate"}'
```

**验证：** `target_type` = `resource`，创建成功。

---

## 11. admin 角色用户测试

```bash
# 读取 admin 用户
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read user --id user_admin
```

**验证：** `role` = `admin`。

```bash
# admin 创建活动
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_admin create category --data '{"id":"cat_admin_event","name":"Admin Event","description":"Created by admin","type":"operation","status":"draft"}'
```

**验证：** `type` = `operation`（非 competition），`status` = `draft`，`created_by` = `user_admin`。

---

## 12. post_post 关系类型：reply 和 embed

### 12.1 reply 关系

```bash
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_carol create post --data '{"id":"post_reply","title":"Reply to Copilot","type":"general","status":"published"}' --body 'This is a reply.'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create post_post --data '{"source_post_id":"post_reply","target_post_id":"post_sub_01","relation_type":"reply"}'
```

**验证：** `relation_type` = `reply`。

### 12.2 embed 关系（嵌入团队卡片）

```bash
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create post --data '{"id":"post_team_intro","title":"Team Alpha Intro","type":"team","status":"published"}' --body '## Team Alpha'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_alice create post --data '{"id":"post_with_embed","title":"Looking for Teammates","type":"general","status":"published"}' --body '## Proposal'
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test create post_post --data '{"source_post_id":"post_with_embed","target_post_id":"post_team_intro","relation_type":"embed","position":1}'
```

**验证：** `relation_type` = `embed`，`position` = `1`。

```bash
# 读取嵌入关系
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read post_post --filters '{"source_post_id":"post_with_embed"}'
```

---

## 13. 评分后修改评分值并验证缓存重算

```bash
# 创建评分
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test --user user_judge create interaction --data '{"id":"iact_rating_main","type":"rating","target_type":"post","target_id":"post_sub_01","value":{"Innovation":90,"Technical":80,"Practical":70,"Demo":60}}'
```

```bash
# 读取当前 average_rating
uv run python .claude/skills/synnovator/scripts/engine.py --data-dir .synnovator_test read post --id post_sub_01
```

**验证：** `average_rating` 已计算（基于 scoring_criteria 权重）。

---

## 14. 清理测试环境

```bash
rm -rf .synnovator_test
```
