# 好友（User Follow / Friend）

> **格式约定：** 每条用例仅描述「场景」与「预期结果」，不包含测试方法和执行过程。

> 好友功能基于新增的第 8 种关系 `user:user`（也称 `user_user`）实现。关注为单向关系，互关即好友。

---

## 13.1 关注

**TC-FRIEND-001：用户 A 关注用户 B**
创建 user:user 关系（source_user_id=A, target_user_id=B, relation_type=follow）。创建成功后，读取 A 的关注列表包含 B。

**TC-FRIEND-002：用户 B 回关用户 A，双方成为好友**
在 TC-FRIEND-001 基础上，创建 user:user（source_user_id=B, target_user_id=A, relation_type=follow）。查询 A 和 B 的互关状态 = true（好友）。

**TC-FRIEND-003：单向关注不构成好友**
仅 A 关注了 B（只有一条 A→B follow 记录）。查询 A 和 B 的好友状态 = false。

## 13.2 取关与拉黑

**TC-FRIEND-004：取消关注**
删除 user:user 关系（source_user_id=A, target_user_id=B, relation_type=follow）。删除后 A 的关注列表不再包含 B，好友关系解除。

**TC-FRIEND-005：拉黑用户**
A 创建 user:user（source_user_id=A, target_user_id=B, relation_type=block）。即使 B 已关注 A，A 的好友列表不含 B（block 优先级高于 follow）。

**TC-FRIEND-006：被拉黑用户无法关注**
A 已 block B。B 尝试创建 follow 关系指向 A（source_user_id=B, target_user_id=A, relation_type=follow）。系统拒绝操作，返回 "blocked" 错误。

## 13.3 级联与删除

**TC-FRIEND-007：删除用户后级联解除 user:user**
用户 A 被删除。A 的所有 user:user 关系（作为 source 或 target）被解除。

## 13.4 负向/边界

**TC-FRIEND-900：自己关注自己被拒绝**
用户 A 创建 user:user（source_user_id=A, target_user_id=A, relation_type=follow）。系统拒绝操作，返回 "cannot follow self" 错误。

**TC-FRIEND-901：重复关注被拒绝**
A 已关注 B，再次创建相同的 follow 关系。系统拒绝操作，返回唯一性冲突错误。唯一性约束：(source_user_id, target_user_id, relation_type)。

**TC-FRIEND-902：非法 relation_type 被拒绝**
创建 user:user 时 relation_type 为 "mute"。系统拒绝操作，返回枚举值无效错误（合法值为 follow | block）。
