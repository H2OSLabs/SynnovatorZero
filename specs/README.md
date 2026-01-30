# Spec Directory

本文件夹用于放置项目的技术规格说明。项目文档请参考 [docs文件夹](../docs/README.md)。

## Table of Content

### 数据模型规格 (`data/`)

- [data/types.md](./data/types.md) — 内容类型 Schema（category, post, resource, rule, user, group, interaction）、枚举值汇总、角色定义
- [data/relationships.md](./data/relationships.md) — 关系 Schema（9种关系类型）
- [data/crud-operations.md](./data/crud-operations.md) — 所有内容类型和关系的 CRUD 操作定义及权限要求
- [data/integrity.md](./data/integrity.md) — 数据完整性约束（唯一性约束、软删除策略、级联策略、恢复机制、引用完整性）
- [data/indexing.md](./data/indexing.md) — 建议索引
- [data/normalization.md](./data/normalization.md) — 规范化建议（反范式字段说明、拆分时机）
- [data/cache-strategy.md](./data/cache-strategy.md) — 缓存统计字段规范（维护策略、一致性模型）

### UI/UX 设计规格 (`design/`)

- [design/style.pen](./design/style.pen) — 样式指南（Neon Forge 主题）
- [design/basic.pen](./design/basic.pen) — 基础组件库
- [design/pages.yaml](./design/pages.yaml) — **页面规格唯一来源**（由 ui-spec-generator 生成）
- [design/pages.md](./design/pages.md) — Figma 链接快速参考索引
- [design/components/](./design/components/) — UI 组件 .pen 文件
- [design/figma/](./design/figma/) — Figma 设计资源文档（由 figma-resource-extractor 生成）

### UX 交互规格 (`ux/`)

- [ux/README.md](./ux/README.md) — 交互规格总览（由 ux-spec-generator 生成）

### 测试用例 (`testcases/`)

- [testcases/](./testcases/) — 17个测试用例文件（涵盖 CRUD、关系、权限、用户旅程等）

### 开发指南 (`guidelines/`)

- [guidelines/spec-guideline.md](./guidelines/spec-guideline.md) — AI Agent 规范写作指南
