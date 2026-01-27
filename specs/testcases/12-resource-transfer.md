# 资产转移（Resource Transfer）

> **格式约定：** 每条用例仅描述「场景」与「预期结果」，不包含测试方法和执行过程。

> 资产转移基于现有 `post:resource` 和 `post:post` 关系实现，不需要 Schema 变更。核心操作为：解除旧 post:resource 关系 → 创建新 post:resource 关系，可选通过 post:post reference 记录溯源。

---

## 12.1 基础转移

**TC-TRANSFER-001：证书资源从组织者帖子转移到参赛帖**
组织者创建 resource（证书 PDF），先通过 post:resource 关联到自己的管理帖子。然后解除旧 post:resource 关系（DELETE），再创建新 post:resource 关系将该 resource 关联到参赛者的帖子。转移完成后：
- 旧帖子的 post:resource 列表不再包含该资源
- 新帖子的 post:resource 列表包含该资源
- resource 实体本身未被修改或删除

**TC-TRANSFER-002：提案间文件转移**
Post A 关联了 resource R（post:resource，display_type=attachment）。创建 Post B 后，将 R 关联到 Post B（CREATE post:resource），然后解除 Post A 与 R 的关联（DELETE post:resource）。转移完成后：
- Post A 的 post:resource 列表不含 R
- Post B 的 post:resource 列表包含 R
- R 可通过 Post B 正常读取

## 12.2 共享与溯源

**TC-TRANSFER-003：资源同时关联多个 post（共享模式）**
Post A 和 Post B 同时通过 post:resource 关联到同一 resource R。验证：
- 两条 post:resource 关系共存
- 两个帖子均可正常读取 R
- 删除其中一条 post:resource 关系不影响另一条

**TC-TRANSFER-004：转移溯源（通过 post:post reference 记录来源）**
Post A 持有 resource R。创建 Post B，通过 post:post（source=B, target=A, relation_type=reference）记录来源关系，再将 R 从 A 转移到 B（DELETE A 的 post:resource，CREATE B 的 post:resource）。转移完成后：
- 通过 Post B 的 post:post reference 关系可追溯到 Post A（R 的原始来源）
- Post A 不再关联 R，Post B 持有 R
