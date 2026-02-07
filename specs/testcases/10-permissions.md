# 权限与可见性

> **格式约定：** 每条用例仅描述「场景」与「预期结果」，不包含测试方法和执行过程。

---

## 10.1 角色权限

**TC-PERM-001：participant 创建 event 被拒绝**
participant 尝试创建活动。系统拒绝。

**TC-PERM-002：participant 创建 rule 被拒绝**
participant 尝试创建规则。系统拒绝。

**TC-PERM-003：participant 更新 event 被拒绝**
participant（非活动创建者）尝试更新活动。系统拒绝。

## 10.2 所有权检查

**TC-PERM-012：非本人修改用户信息被拒绝**
用户 Bob 尝试修改用户 Alice 的 bio。系统拒绝。

**TC-PERM-013：非 Owner 修改团队信息被拒绝**
团队普通成员 Bob 尝试更新团队 description。系统拒绝。

**TC-PERM-014：非本人修改评论被拒绝**
用户 Bob 尝试修改用户 Alice 发表的评论。系统拒绝。

## 10.3 可见性过滤

**TC-PERM-020：访客读取 draft 帖子不可见**
未登录访客尝试读取一个 status=draft 的帖子。系统不返回该帖子或返回权限错误。

**TC-PERM-021：访客读取 draft 活动不可见**
未登录访客尝试读取一个 status=draft 的活动。系统不返回该活动。

**TC-PERM-022：非成员读取 private 团队不可见**
非团队成员尝试读取一个 visibility=private 的团队。系统不返回该团队或返回权限错误。

**TC-PERM-023：已发布活动下的 draft 帖子在列表中不可见**
一个 published 活动关联了一个 draft 帖子（event:post submission）。访客查询活动的 submission 列表时，该 draft 帖子不出现在结果中。

**TC-PERM-024：已发布活动下的 private 帖子在列表中不可见**
一个 published 活动关联了一个 visibility=private、status=published 的帖子（event:post submission）。非作者访客查询活动的 submission 列表时，该 private 帖子不出现在结果中。作者本人查询时可见。

**TC-PERM-025：private 帖子的关联 resource 在活动资源列表中不可见**
活动关联了一个 visibility=private 的帖子，该帖子挂载了 resource。非作者用户查询该活动下的资源列表时，该 resource 不出现在结果中（因关联帖子不可见）。
