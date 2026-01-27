# 资源（Resource）模块

> **格式约定：** 每条用例仅描述「场景」与「预期结果」，不包含测试方法和执行过程。

---

## 6.1 创建资源

**TC-RES-001：最小字段创建资源**
仅提供 filename（如 "test-file.txt"）创建资源。创建完成后，id/created_by/created_at 自动生成，可通过读取获取信息。

**TC-RES-002：带完整元信息创建资源**
提供 filename、display_name、description 和 mime_type 创建资源（如演示视频 demo.mp4）。创建完成后，各字段值正确。

## 6.2 更新资源

**TC-RES-030：更新资源元信息**
更新资源的 display_name 和 description。更新完成后，读取资源返回新值，updated_at 变更。

## 6.3 删除资源

**TC-RES-031：删除资源后级联解除 post:resource**
删除一个已关联到帖子的资源。资源被物理删除后，post:resource 关系被解除。

## 6.4 间接可见性（Inherited Visibility）

> Resource 无独立 visibility 字段，其可见性完全继承自关联帖子（"关联帖子可见则可读"）。以下用例验证该继承行为在不同场景下的正确性。

**TC-RES-040：关联到 published + public 帖子的 resource 可被任何人读取**
创建 resource 并通过 post:resource 关联到一个 status=published、visibility=public 的帖子。访客和已登录用户均可读取该 resource。

**TC-RES-041：关联到 draft 帖子的 resource 对非作者不可读**
创建 resource 并通过 post:resource 关联到一个 status=draft 的帖子。非作者用户尝试读取该 resource，系统不返回或返回权限错误。作者和 Admin 可读取。

**TC-RES-042：关联到 private 帖子的 resource 对非作者不可读**
创建 resource 并通过 post:resource 关联到一个 visibility=private、status=published 的帖子。非作者用户尝试读取该 resource，系统不返回或返回权限错误。作者和 Admin 可读取。

**TC-RES-043：帖子从 public 改为 private 后，关联 resource 不可见性同步变更**
resource R 关联到一个 published + public 的帖子，此时任何人可读取 R。将帖子 visibility 更新为 private 后，非作者用户无法再读取 R。

**TC-RES-044：resource 同时关联到 public 和 private 帖子时的可见性**
resource R 同时通过 post:resource 关联到帖子 A（public + published）和帖子 B（private + published）。非作者用户通过帖子 A 的关联可读取 R（因为帖子 A 可见）。R 的可见性取决于其关联帖子中是否有至少一个可见帖子。

**TC-RES-045：帖子删除后 resource 的可访问性**
resource R 关联到帖子 P（published + public）。删除帖子 P 后，post:resource 关系被解除。R 成为孤立资源（不关联任何帖子）。非作者用户无法通过帖子路径读取 R。resource 实体本身未被删除（级联仅解除关系）。

## 6.5 负向/边界

**TC-RES-900：缺少 filename 被拒绝**
创建资源时不提供 filename。系统拒绝创建，返回缺少必填字段错误。

**TC-RES-901：未登录用户创建资源被拒绝**
未提供用户身份的情况下创建资源。系统拒绝操作。

**TC-RES-902：引用不存在的 post_id/resource_id 创建关系被拒绝**
使用不存在的 ID 创建 post:resource 关系。系统拒绝操作，返回对应 ID 不存在的错误。

**TC-RES-903：非法 display_type 枚举被拒绝**
创建 post:resource 关系时指定 display_type 为 "embedded"。系统拒绝操作，返回枚举值无效错误（合法值为 attachment | inline）。
