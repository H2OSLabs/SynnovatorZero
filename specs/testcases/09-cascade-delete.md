# 删除与级联

> **格式约定：** 每条用例仅描述「场景」与「预期结果」，不包含测试方法和执行过程。

> 所有删除均为硬删除（物理删除文件）。级联操作在删除父记录前执行，先清理关系和子记录，再删除父记录本身。

---

## 9.1 各内容类型删除

**TC-DEL-001：删除 event**
删除一个活动。活动文件被物理删除，读取返回 "not found"。

**TC-DEL-002：删除 rule**
删除一个规则。规则文件被物理删除，读取返回 "not found"。

**TC-DEL-003：删除 user**
删除一个用户。用户文件被物理删除，用户的所有 interaction 一并硬删除，group:user 关系被解除。

**TC-DEL-004：删除 group**
删除一个团队。团队文件被物理删除，group:user 关系被解除，event:group 关系被解除。

**TC-DEL-005：删除 interaction**
删除一条 like interaction。interaction 文件被物理删除，对应帖子的 like_count 递减。

## 9.2 级联删除

**TC-DEL-010：删除 event → 关联 interaction 级联硬删除**
删除一个有点赞和评论的活动。活动删除前，对该活动的 like 和 comment interaction 均被级联硬删除。

**TC-DEL-011：删除 user → interaction + group:user 级联处理**
删除一个有多条 interaction 和团队成员身份的用户。用户所有 interaction 被级联硬删除，帖子的 like_count/comment_count 相应递减，group:user 关系被解除。

**TC-DEL-012：删除 post → 完整级联链**
删除一个关联了 event:post、post:post、post:resource 和多条 interaction 的帖子。删除后：
- 帖子被物理删除
- event:post 关系解除
- post:post 关系解除
- post:resource 关系解除
- 所有关联 interaction 被级联硬删除

**TC-DEL-013：删除 rule → 级联 event:rule**
删除一个已关联到活动的规则。规则删除前，event:rule 关系被解除。

**TC-DEL-014：删除 group → 级联 event:group**
删除一个已注册活动的团队。团队删除前，event:group 关系被解除，group:user 关系被解除。

**TC-DEL-015：删除父评论 → 级联删除所有子评论**
删除一条有一级回复和二级回复的顶层评论。顶层评论和所有后代评论均被级联硬删除（物理删除）。

## 9.3 已删除记录的读取行为

**TC-DEL-020：读取已删除记录返回 not found**
对一个已删除的帖子执行读取。系统返回 "not found" 错误（文件已物理删除）。

**TC-DEL-021：已删除记录不可恢复**
硬删除后记录不可恢复。如需恢复，须重新创建。

**TC-DEL-022：已删除记录无法被更新**
对一个已删除的帖子尝试更新 title。系统返回 "not found" 错误。
