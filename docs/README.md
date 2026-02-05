# Documents Directory

本文件夹用于放置项目的功能说明文档。开发规范请参考 [specs文件夹](../specs/README.md)。

## Table of Content

### 数据模型

- [data-types.md](./data-types.md) — 内容类型 Schema（category, post, resource, rule, user, group, interaction）、枚举值汇总、角色定义
- [relationships.md](./relationships.md) — 关系 Schema（category:rule, category:post, category:group, category:category, post:post, post:resource, group:user, user:user, target:interaction）

### 操作规范

- [crud-operations.md](./crud-operations.md) — 所有内容类型和关系的 CRUD 操作定义及权限要求

### 用户旅程

- [user-journeys.md](./user-journeys.md) — 13 个核心用户流程（浏览、注册、登录、组队、创建活动、报名、发帖、编辑、删除、社区互动等）

### 规则引擎

- [rule-engine.md](./rule-engine.md) — 声明式规则引擎规范（条件类型、触发点、执行阶段）

### 开发流程

- [development-workflow.md](./development-workflow.md) — 完整开发流程（12 个阶段）
