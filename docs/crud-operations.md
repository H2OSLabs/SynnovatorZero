# CRUD 操作

本文档定义 Synnovator 平台所有内容类型和关系的 CRUD（创建、读取、更新、删除）操作规范及权限要求。

> 数据类型 Schema 详见 [data-types.md](./data-types.md)，关系 Schema 详见 [relationships.md](./relationships.md)。

---

## Create

### 创建内容

| 操作 | 说明 | 权限 |
|------|------|------|
| `CREATE category` | 创建活动，填写 YAML + Markdown | Organizer, Admin |
| `CREATE post` | 创建帖子，编写 Markdown 内容 | 已登录用户 |
| `CREATE resource` | 上传文件资源 | 已登录用户 |
| `CREATE rule` | 创建活动规则 | Organizer, Admin |
| `CREATE user` | 注册新用户 | 任何人 |
| `CREATE group` | 创建团队/分组 | 已登录用户 |
| `CREATE interaction` | 创建交互记录（点赞/评论/评分），需配合 `CREATE target:interaction` 关联到目标 | 已登录用户 |

### 创建关系

| 操作 | 说明 | 权限 |
|------|------|------|
| `CREATE category:rule` | 将 Rule 关联到活动 | Category 创建者, Admin |
| `CREATE category:post` | 将 Post 关联到活动（报名/提交） | Post 作者（需符合 Rule） |
| `CREATE category:group` | 团队报名活动（建立团队与活动的绑定） | Group Owner（需符合 Rule 的团队人数要求） |
| `CREATE post:post` | 帖子间建立关联（引用/回复/嵌入） | 发起方 Post 作者 |
| `CREATE post:resource` | 将资源关联到帖子 | Post 作者 |
| `CREATE group:user` | 将用户加入分组（require_approval=true 时 status 初始为 pending） | Group owner/admin, 或自助申请 |
| `CREATE target:interaction` | 将交互记录关联到目标对象（触发目标验证、去重校验、缓存更新） | 交互发起人（目标对象须可见） |
| `CREATE user:user` | 关注或拉黑用户（禁止自引用，拉黑方阻止被拉黑方创建 follow） | 已登录用户 |
| `CREATE category:category` | 创建活动间关联（赛段/赛道/前置条件，禁止自引用和循环依赖） | Category 创建者, Admin |

---

## Read

### 读取内容

| 操作 | 说明 | 权限 |
|------|------|------|
| `READ category` | 读取活动列表或详情 | 公开活动: 任何人；草稿: 创建者/Admin |
| `READ post` | 读取帖子列表或详情，支持按 tag/type/visibility 筛选 | 已发布且 visibility=public: 任何人；visibility=private: 作者/Admin；草稿: 作者/Admin |
| `READ resource` | 读取/下载文件资源 | 关联帖子可见则可读 |
| `READ rule` | 读取活动规则 | 关联活动可见则可读 |
| `READ user` | 读取用户信息 | 公开信息: 任何人；完整信息: 本人/Admin |
| `READ group` | 读取分组信息及成员列表 | public: 任何人；private: 成员/Admin |
| `READ interaction` | 读取交互记录（支持按 type 筛选） | 目标对象可见则可读 |

### 读取关系

| 操作 | 说明 |
|------|------|
| `READ category:rule` | 查询活动关联的所有规则 |
| `READ category:post` | 查询活动关联的所有帖子（可按 relation_type 筛选） |
| `READ category:group` | 查询活动的报名团队列表 |
| `READ post:post` | 查询帖子的关联帖子（可按 relation_type 筛选） |
| `READ post:resource` | 查询帖子的关联资源 |
| `READ group:user` | 查询分组的成员列表（含角色和状态信息，可按 status 筛选） |
| `READ target:interaction` | 查询目标对象的交互记录（可按 interaction.type 筛选） |
| `READ user:user` | 查询用户的关注/粉丝/好友列表（可按 relation_type 筛选） |
| `READ category:category` | 查询活动的赛段链、赛道列表、前置条件（可按 relation_type 筛选） |

---

## Update

### 更新内容

| 操作 | 说明 | 权限 |
|------|------|------|
| `UPDATE category` | 更新活动信息或状态变更（**严格单向**: draft→published→closed，不可逆转；如需修改已发布/已关闭活动，创建新版本） | 创建者, Admin |
| `UPDATE post` | 更新帖子内容、添加/修改 tag、状态变更（**严格单向**: draft→pending_review→published\|rejected; rejected→draft 允许修订；published 为终态，如需修改创建新版本）、visibility 变更（private 帖子发布时跳过 pending_review 流程） | 作者（编辑他人帖子需 Rule 允许或副本机制） |
| `UPDATE resource` | 更新资源元信息（display_name, description） | 上传者, Admin |
| `UPDATE rule` | 更新规则配置 | 创建者, Admin |
| `UPDATE user` | 更新用户信息 | 本人, Admin |
| `UPDATE group` | 更新分组信息和设置 | Owner, Admin |
| `UPDATE interaction` | 更新交互内容（如修改评论文本、修改评分） | 交互发起人本人 |

### 更新关系属性

| 操作 | 说明 |
|------|------|
| `UPDATE category:rule` | 修改规则优先级等属性 |
| `UPDATE category:post` | 修改关联类型（如 reference→submission） |
| `UPDATE post:post` | 修改关联类型或排序位置 |
| `UPDATE post:resource` | 修改展示方式或排序位置 |
| `UPDATE group:user` | 修改成员角色（如 member→admin）或审批状态（pending→accepted/rejected） |
| `UPDATE category:category` | 修改赛段序号或关联类型 |

### 状态机约束

引擎层（`content.py`）在执行 UPDATE 操作时强制校验状态转换方向。不允许逆向变更。

**category.status 状态机（严格单向）：**

```
draft → published → closed
```

- `closed` 是终态，不可变更。
- 如需修改已发布或已关闭的活动，应创建新的 category 版本（重置为 `draft`）。

**post.status 状态机：**

```
draft → pending_review → published
                       → rejected → draft（修订后重提）
draft → published（仅 visibility=private 帖子可跳过审核）
```

- `published` 是终态，不可变更。
- `rejected` 帖子可修订后重置为 `draft`。
- 如需修改已发布帖子，应创建新版本（重置为 `draft`）。

**校验位置：** `content.py::update_content()` → `core.py::validate_state_transition()`

---

### 组队审批操作规范

| 场景 | 操作 | 权限 | status 变更 |
|------|------|------|------------|
| 申请加入 | `CREATE group:user` | 申请人自身 | → `pending`（require_approval=true 时） |
| 批准加入 | `UPDATE group:user` | Group Owner/Admin | `pending` → `accepted` |
| 拒绝加入 | `UPDATE group:user` | Group Owner/Admin | `pending` → `rejected` |
| 直接加入 | `CREATE group:user` | 申请人自身 | → `accepted`（require_approval=false 时） |
| 重新申请 | `CREATE group:user` | 申请人自身 | 删除旧 rejected 记录，新建 `pending` |

---

## Delete

### 删除内容

> **硬删除：** 内容类型的 DELETE 操作执行**硬删除**（物理移除文件），不设 `deleted_at` 字段。如需恢复，应创建新记录。

| 操作 | 说明 | 权限 | 级联影响 |
|------|------|------|----------|
| `DELETE category` | 删除活动 | 创建者, Admin | **级联删除** target:interaction 关系及关联 interaction 记录；解除所有 category:rule、category:post、category:group、category:category 关系 |
| `DELETE post` | 删除帖子 | 作者, Admin | **级联删除** target:interaction 关系及关联 interaction 记录；解除所有 post:post、post:resource、category:post 关系 |
| `DELETE resource` | 删除文件资源 | 上传者, Admin | **级联删除** target:interaction 关系及关联 interaction 记录；解除所有 post:resource 关系 |
| `DELETE rule` | 删除规则 | 创建者, Admin | 解除所有 category:rule 关系 |
| `DELETE user` | 删除/注销用户 | 本人, Admin | 解除所有 group:user、user:user 关系；**级联删除**该用户创建的所有 interaction 及其 target:interaction 关系，并更新受影响目标的缓存计数 |
| `DELETE group` | 删除分组 | Owner, Admin | 解除所有 group:user、category:group 关系 |
| `DELETE interaction` | 删除交互记录 | 交互发起人, Admin | **级联删除** target:interaction 关系；若为父评论，递归级联删除所有子回复及其 target:interaction 关系；更新受影响目标的缓存计数 |

### target:interaction 级联删除策略

> **统一策略：** 当内容类型（作为 interaction 目标）被删除时，所有指向该内容的 `target:interaction` 关系和对应的 `interaction` 记录一并**级联硬删除**。

| 被删除的目标类型 | 级联行为 | 实现位置 |
|-----------------|---------|---------|
| `category` | 删除所有 `target_type=category` 的 target:interaction 关系 + 关联 interaction 记录 | `endpoints/category.py` → `cascade._cascade_hard_delete_interactions()` |
| `post` | 删除所有 `target_type=post` 的 target:interaction 关系 + 关联 interaction 记录 | `endpoints/post.py` → `cascade._cascade_hard_delete_interactions()` |
| `resource` | 删除所有 `target_type=resource` 的 target:interaction 关系 + 关联 interaction 记录 | `endpoints/resource.py` → `cascade._cascade_hard_delete_interactions()` |
| `user`（非目标类型） | 删除该用户**创建的**所有 interaction + 对应 target:interaction 关系，并更新受影响目标的缓存计数 | `endpoints/user.py` → `cascade._cascade_hard_delete_user_interactions()` |

> **注意：** `group` 和 `rule` 不是有效的 `target_interaction.target_type`（枚举值仅含 post、category、resource），因此删除 group/rule 时无需级联 interaction。

### 删除关系

> **硬删除：** 关系的 DELETE 操作执行**物理删除**，直接移除关联记录。关系不设 `deleted_at` 字段。

| 操作 | 说明 |
|------|------|
| `DELETE category:rule` | 解除活动与规则的关联 |
| `DELETE category:post` | 解除活动与帖子的关联 |
| `DELETE category:group` | 解除团队与活动的报名绑定 |
| `DELETE post:post` | 解除帖子间的关联 |
| `DELETE post:resource` | 解除帖子与资源的关联 |
| `DELETE group:user` | 将成员移出分组（或撤回申请） |
| `DELETE target:interaction` | 解除目标对象与交互记录的关联 |
| `DELETE user:user` | 取消关注或解除拉黑 |
| `DELETE category:category` | 解除活动间的赛段/赛道/前置条件关联 |

---

## 权限执行层（RBAC）

> **决策：** 权限检查是**引擎层**的责任，在 CRUD 操作执行前由引擎自动校验。上层应用不需要重复校验。
>
> **实现状态：** 已实现（FIX-11, 简化版 RBAC）。角色门控 CREATE + 所有权门控 UPDATE/DELETE，admin 跳过所有检查。

### 架构位置

引擎已从 `engine.py` 拆分为多个模块。RBAC 权限检查的实现位置如下：

| 模块 | 职责 | RBAC 切入点 |
|------|------|------------|
| `core.py` | 共享基础设施 | 新增 `check_permission(data_dir, current_user, operation, target_type, record=None)` 函数，封装权限矩阵查询逻辑 |
| `content.py` | 内容 CRUD 分发 | 在 `create_content()`、`read_content()`、`update_content()`、`delete_content()` 入口处调用 `check_permission()` |
| `relations.py` | 关系 CRUD | 在 `create_relation()`、`update_relation()`、`delete_relation()` 入口处调用 `check_permission()` |
| `endpoints/*.py` | 类型特定钩子 | 不负责通用权限检查；仅处理业务规则级约束（如 Rule 校验） |

### 权限矩阵

权限矩阵定义在 `core.py` 中，基于 `user.role` 和操作类型进行门控：

| 操作 | participant | organizer | admin |
|------|------------|-----------|-------|
| CREATE category | - | Y | Y |
| CREATE post | Y | Y | Y |
| CREATE resource | Y | Y | Y |
| CREATE rule | - | Y | Y |
| CREATE interaction | Y | Y | Y |
| UPDATE (own content) | Y | Y | Y |
| UPDATE (others' content) | - | - | Y |
| DELETE (own content) | Y | Y | Y |
| DELETE (others' content) | - | - | Y |

### 所有权检查

对 UPDATE 和 DELETE 操作，除权限矩阵外还需检查 `created_by` 所有权：
- **本人操作：** `record.created_by == current_user` → 允许
- **Admin 覆写：** `user.role == "admin"` → 允许
- **其他情况：** 拒绝

### current_user 参数传递

当前 `current_user` 参数已在部分函数中存在（`create_content`、`read_content`），需扩展到：
- `update_content(data_dir, content_type, record_id, updates, current_user=None)`
- `delete_content(data_dir, content_type, record_id, current_user=None)`
- `create_relation(data_dir, relation_type, data, current_user=None)`
- `update_relation(data_dir, relation_type, filters, updates, current_user=None)`
- `delete_relation(data_dir, relation_type, filters, current_user=None)`

CLI 入口（`engine.py`）已接受 `--user` 参数，负责将其传递给所有 CRUD 调用。

---

## Rule Engine Hook Points

> 规则引擎通过 Hook 机制在 CRUD 操作的关键节点自动执行约束校验和后续动作。详细规范见 [rule-engine.md](./rule-engine.md)。

### Hook 执行阶段

| 阶段 | 执行时机 | 失败行为 |
|------|---------|---------|
| **pre** | 操作执行前 | 根据 `on_fail` 决定：`deny`（拒绝操作）、`warn`（警告但允许）、`flag`（标记但允许） |
| **post** | 操作执行成功后 | 不回滚已完成的操作，仅执行后续动作（标记、计算排名、颁奖等） |

### Hook 操作点

| 操作 | Phase | 说明 | 来源 |
|------|-------|------|------|
| `CREATE category:post` | pre | 提交帖子到活动前校验（时间窗口、提交次数、格式、团队人数、必要 resource） | 现有 + 扩展 |
| `CREATE category:post` | post | 提交成功后触发动作（通知等） | 新增 |
| `CREATE group:user` | pre | 成员加入团队前校验（团队人数上限） | 现有 |
| `CREATE group:user` | post | 成员加入成功后触发动作 | 新增 |
| `CREATE category:group` | pre | 团队报名活动前校验（前置条件、入场条件） | 现有 + 扩展 |
| `CREATE category:group` | post | 团队报名成功后触发动作 | 新增 |
| `UPDATE post.status` | pre | 帖子状态变更前校验（发布路径、审核流程） | 现有 |
| `UPDATE post.status` | post | 帖子状态变更后触发动作 | 新增 |
| `UPDATE category.status` | pre | 活动状态变更前校验 | **新增** |
| `UPDATE category.status` | post | 活动关闭时触发终审校验、排名计算、奖励发放 | **新增** |

### 校验链

引擎根据操作类型，沿关系链定位关联的 Rule，然后执行匹配 trigger + phase 的所有 checks：

```
CREATE category_post:
  post → category_post.category_id → category_rule → rule.checks[trigger=create_relation(category_post)]

CREATE group_user:
  group → category_group → category → category_rule → rule.checks[trigger=create_relation(group_user)]

CREATE category_group:
  category → category_category(prerequisite) → prerequisite 检查
  category → category_rule → rule.checks[trigger=create_relation(category_group)]

UPDATE post.status:
  post → category_post → category → category_rule → rule.checks[trigger=update_content(post.status)]

UPDATE category.status:
  category → category_rule → rule.checks[trigger=update_content(category.status)]
```

### AND 逻辑

- 同一操作点的所有 checks 必须全部通过（AND 逻辑）。
- 一个活动可关联多条 Rule，所有 Rule 的 checks 合并后按 AND 逻辑执行。
- 任一 check 的 `on_fail: deny` 失败即拒绝操作。
