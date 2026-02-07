# 互动（Interaction）模块

> **格式约定：** 每条用例仅描述「场景」与「预期结果」，不包含测试方法和执行过程。

---

## 7.1 点赞（like）

**TC-IACT-001：对帖子点赞**
用户 Dave 对一个已发布帖子点赞。创建 like interaction 成功，帖子的 like_count 从 0 变为 1。

**TC-IACT-002：重复点赞被拒绝**
同一用户对同一帖子再次点赞。系统拒绝操作，返回"已点赞"错误。

**TC-IACT-003：取消点赞后 like_count 递减**
删除一条 like interaction。帖子的 like_count 相应递减。

## 7.2 评论（comment）

**TC-IACT-010：创建顶层评论**
用户 Bob 对帖子发表评论。创建 comment interaction 成功，帖子的 comment_count +1。

**TC-IACT-011：创建嵌套回复（一级回复）**
用户 Alice 回复 Bob 的评论（指定 parent_id）。创建成功，帖子的 comment_count 再 +1。

**TC-IACT-012：创建二级回复（回复的回复）**
用户 Bob 回复 Alice 的回复（parent_id 指向一级回复）。创建成功，parent_id 正确指向一级回复 ID。

**TC-IACT-013：comment_count 包含所有层级**
读取帖子，comment_count 包含顶层评论和所有嵌套回复的总数。

**TC-IACT-014：删除父评论级联删除子回复**
删除顶层评论。顶层评论和所有嵌套回复（一级、二级）均被级联硬删除（物理删除）。

## 7.3 评分（rating）

**TC-IACT-020：创建多维度评分**
评委对帖子提交多维度评分（创新性 87、技术实现 82、实用价值 78、演示效果 91），附带评语。创建成功后，帖子的 average_rating 按权重计算为 83.85（87x0.30 + 82x0.30 + 78x0.25 + 91x0.15）。

**TC-IACT-021：多个评分的均值计算**
第二个评委提交不同分数（75、90、85、70）。该评委加权分为 81.25。帖子的 average_rating 更新为两个评分的均值 82.55。

## 7.4 更新互动

**TC-IACT-050：修改评论文本**
评论发起人修改自己评论的 value 文本。更新成功，value 为新文本，updated_at 变更，comment_count 不变。

**TC-IACT-051：修改评分重新打分**
评委修改已提交的评分分值。更新成功，帖子的 average_rating 按新分值重新计算。

## 7.5 非 post 目标的互动

**TC-IACT-060：对 event（活动）点赞**
用户对一个 published 状态的 event 点赞。创建成功，target_type 为 event。

**TC-IACT-061：对 event 发表评论**
用户对一个 event 发表评论。创建成功。

**TC-IACT-062：对 resource（资源）点赞**
用户对一个 resource 点赞。创建成功，target_type 为 resource。

**TC-IACT-063：对 resource 发表评论**
用户对一个 resource 发表评论。创建成功。

## 7.6 负向/边界

**TC-IACT-900：非法 interaction type 被拒绝**
创建 interaction 时指定 type 为 "bookmark"。系统拒绝操作，返回枚举值无效错误（合法值为 like | comment | rating）。

**TC-IACT-901：非法 target_type 被拒绝**
创建 interaction 时指定 target_type 为 "user"。系统拒绝操作，返回枚举值无效错误。

**TC-IACT-902：target_id 不存在被拒绝**
对一个不存在的帖子 ID 点赞。系统拒绝操作，返回目标对象不存在错误。

**TC-IACT-903：对已删除的帖子点赞被拒绝**
对一个已删除的帖子点赞。系统拒绝操作，返回 "not found" 错误（帖子已物理删除）。

**TC-IACT-904：缺少 target_id 被拒绝**
创建 interaction 时不提供 target_id。系统拒绝操作，返回缺少必填字段错误。

**TC-IACT-905：非本人修改 interaction 被拒绝**
用户 Alice 尝试修改用户 Bob 的评论。系统拒绝操作，返回权限不足错误。
