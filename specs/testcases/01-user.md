# 用户（User）模块

> **格式约定：** 每条用例仅描述「场景」与「预期结果」，不包含测试方法和执行过程。

---

## 1.1 创建用户

**TC-USER-001：创建 participant 用户**
创建一个用户 Alice，角色为 participant，提供用户名、邮箱、显示名等信息。创建完成后，系统返回该用户记录，包含自动生成的 id、created_at、updated_at。

**TC-USER-002：创建 organizer 用户**
创建一个用户 Judge，角色为 organizer。创建完成后，role 字段为 organizer。

**TC-USER-003：创建 admin 用户**
创建一个管理员用户，角色为 admin。创建完成后，role 字段为 admin，可通过读取验证。

## 1.2 读取用户

**TC-USER-004：读取已创建的用户**
读取上述创建的用户记录，返回完整的用户信息，包括 username、email、display_name、role 等字段。

## 1.3 更新用户

**TC-USER-010：用户修改自己的个人信息**
用户 Bob 更新自己的 display_name 和 bio 字段。更新完成后，读取该用户可看到新的 display_name 和 bio 值，updated_at 已变更。

**TC-USER-011：Admin 修改其他用户的角色**
管理员将某个 participant 用户的角色修改为 organizer。更新完成后，该用户的 role 变为 organizer。

## 1.4 删除用户

**TC-USER-020：删除用户及级联影响**
删除用户 Charlie（该用户已加入团队、有点赞和评论记录）。删除完成后：
- 用户记录被物理删除
- 该用户的所有 interaction（点赞、评论）一并硬删除
- group:user 关系被解除（硬删除）
- 对应帖子的 like_count 和 comment_count 相应递减

## 1.5 负向/边界

**TC-USER-900：重复 username 被拒绝**
创建一个与已有用户相同 username（"alice"）的新用户。系统拒绝创建，返回 username 唯一性冲突错误。

**TC-USER-901：重复 email 被拒绝**
创建一个与已有用户相同 email（"alice@example.com"）的新用户。系统拒绝创建，返回 email 唯一性冲突错误。

**TC-USER-902：非本人/非 Admin 修改用户信息被拒绝**
用户 Bob 尝试修改用户 Alice 的个人信息。系统拒绝操作，返回权限不足错误。

**TC-USER-903：缺少必填字段 email**
创建用户时只提供 username，不提供 email。系统拒绝创建，返回缺少必填字段错误。
