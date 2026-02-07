# 团队（Group）模块

> **格式约定：** 每条用例仅描述「场景」与「预期结果」，不包含测试方法和执行过程。

---

## 4.1 创建团队

**TC-GRP-001：创建需审批的公开团队**
创建一个团队，设置 visibility=public、require_approval=true、max_members=5。创建完成后，系统返回记录，id 自动生成。

**TC-GRP-002：创建无需审批的私有团队**
创建一个团队，设置 visibility=private、require_approval=false。创建完成后，visibility 为 private，新成员加入时自动变为 accepted 状态。

## 4.2 团队成员管理

**TC-GRP-003：Owner 自动加入**
将用户设为团队 owner。该 group_user 记录的 status 自动为 accepted，joined_at 已赋值。

**TC-GRP-004：需审批团队 — 成员申请加入为 pending**
用户 Carol 申请加入一个 require_approval=true 的团队。创建的 group_user 记录 status 为 pending。

**TC-GRP-005：Owner 批准成员申请**
Alice（Owner）批准 Carol 的加入申请。更新后 status 变为 accepted，joined_at 被赋值。

**TC-GRP-006：Owner 拒绝成员申请**
Alice 拒绝 Bob 的加入申请。更新后 status 变为 rejected。

**TC-GRP-007：被拒绝后重新申请**
Bob 被拒绝后重新申请加入团队。重新申请成功，新的 group_user 记录 status 为 pending。

**TC-GRP-008：无需审批团队 — 成员直接 accepted**
Bob 加入一个 require_approval=false 的团队。创建的 group_user 记录 status 自动为 accepted，joined_at 已赋值。

## 4.3 更新团队

**TC-GRP-010：Owner 更新团队信息**
团队 Owner 更新团队的 description 和 max_members。更新完成后，读取团队返回新值，updated_at 变更。

**TC-GRP-011：变更审批设置**
将 require_approval 从 true 改为 false。更新成功后，后续新成员加入时自动 accepted。

**TC-GRP-012：变更可见性**
将团队 visibility 从 public 改为 private。更新成功后，读取团队返回 visibility=private。

## 4.4 删除团队

**TC-GRP-020：删除团队及级联**
删除一个已注册活动（event:group 关系存在）的团队。删除完成后：
- 团队记录被物理删除
- group:user 关系被解除
- event:group 关系被解除

## 4.5 负向/边界

**TC-GRP-900：非法 visibility 枚举被拒绝**
创建团队时指定 visibility 为 "restricted"。系统拒绝创建，返回枚举值无效错误。

**TC-GRP-901：非 Owner/Admin 修改团队信息被拒绝**
普通 member 用户 Bob 尝试更新团队信息。系统拒绝操作，返回权限不足错误。
