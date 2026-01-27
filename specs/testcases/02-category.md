# 活动（Category）模块

> **格式约定：** 每条用例仅描述「场景」与「预期结果」，不包含测试方法和执行过程。

---

## 2.1 创建活动

**TC-CAT-001：创建 competition 类型活动**
组织者 Alice 创建一个比赛活动（type=competition），设置名称、描述、起止日期，附带 Markdown 正文。创建完成后，系统返回记录，id 自动生成，type 为 competition，has_body 为 true，created_by 为 Alice。

**TC-CAT-002：创建 operation 类型活动**
组织者创建一个运营活动（type=operation）。创建完成后，type 为 operation。

## 2.2 读取活动

**TC-CAT-003：读取已创建的活动**
读取上述创建的活动，返回完整的活动信息，包括 name、description、type、status、start_date、end_date 等字段。

## 2.3 更新活动

**TC-CAT-010：活动状态流转 draft → published → closed**
将一个 draft 状态的活动依次更新为 published，再更新为 closed。每步更新成功后，status 变为对应值，updated_at 逐步递增。

**TC-CAT-011：修改活动名称和描述**
更新活动的 name 和 description 字段。更新完成后，读取活动返回新值。

## 2.4 删除活动

**TC-CAT-020：删除活动及级联影响**
删除一个已关联 rule（category:rule）、post（category:post）、group（category:group）和 interaction 的活动。删除完成后：
- 活动记录被物理删除
- category:rule、category:post、category:group 关系均被解除
- 关联的 interaction（如对该活动的点赞）一并硬删除

## 2.5 负向/边界

**TC-CAT-900：非法 type 枚举被拒绝**
创建活动时指定 type 为 "workshop"（不在合法枚举范围内）。系统拒绝创建，返回枚举值无效错误。

**TC-CAT-901：非法 status 枚举被拒绝**
创建或更新活动时指定 status 为 "archived"。系统拒绝操作，返回枚举值无效错误。

**TC-CAT-902：participant 创建活动被拒绝**
一个 participant 角色的用户尝试创建活动。系统拒绝操作，返回权限不足错误（CREATE category 仅限 Organizer/Admin）。
