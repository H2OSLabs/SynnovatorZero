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
| `UPDATE category` | 更新活动信息或状态变更（draft→published→closed） | 创建者, Admin |
| `UPDATE post` | 更新帖子内容、添加/修改 tag、状态变更、visibility 变更（private 帖子发布时跳过 pending_review 流程） | 作者（编辑他人帖子需 Rule 允许或副本机制） |
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

> **默认软删除：** 内容类型的 DELETE 操作默认执行**软删除**（设置 `deleted_at`），详见 [specs/data-integrity.md](../specs/data-integrity.md)。

| 操作 | 说明 | 权限 | 级联影响 |
|------|------|------|----------|
| `DELETE category` | 删除活动 | 创建者, Admin | 解除所有 category:rule、category:post、category:group、category:category 关系，删除关联 interaction |
| `DELETE post` | 删除帖子 | 作者, Admin | 解除所有 post:post、post:resource、category:post 关系，删除关联 interaction |
| `DELETE resource` | 删除文件资源 | 上传者, Admin | 解除所有 post:resource 关系，删除关联 interaction |
| `DELETE rule` | 删除规则 | 创建者, Admin | 解除所有 category:rule 关系 |
| `DELETE user` | 删除/注销用户 | 本人, Admin | 解除所有 group:user、user:user 关系，删除所有该用户的 interaction |
| `DELETE group` | 删除分组 | Owner, Admin | 解除所有 group:user、category:group 关系 |
| `DELETE interaction` | 删除交互记录 | 交互发起人, Admin | 若为父评论，级联删除所有子回复 |

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
