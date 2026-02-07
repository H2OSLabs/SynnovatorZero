# Synnovator 开发工作流

从需求设计到前后端实现和测试的完整开发流程。

## 快速导航

| 阶段 | 文档 | 描述 |
|------|------|------|
| 0 | [00-project-init.md](00-project-init.md) | 项目初始化、环境配置 |
| 0.5 | [01-domain-modeling.md](01-domain-modeling.md) | 领域建模与数据架构 |
| 1 | [02-api-design.md](02-api-design.md) | OpenAPI 规范生成 |
| 2 | [03-backend-generation.md](03-backend-generation.md) | FastAPI 后端代码生成 |
| 2.5-3 | [04-seed-data.md](04-seed-data.md) | 种子数据设计与注入 |
| 4 | [05-ui-design.md](05-ui-design.md) | UI 设计文档生成 |
| 5-6 | [06-frontend-setup.md](06-frontend-setup.md) | 前端框架配置、API 客户端 |
| 7 | [07-frontend-components.md](07-frontend-components.md) | 前端组件开发 |
| 8 | [08-e2e-testing.md](08-e2e-testing.md) | E2E 测试 |
| 9 | [09-integration.md](09-integration.md) | 最终集成验证 |

## 附录

| 文档 | 描述 |
|------|------|
| [appendix-a-dependency-graph.md](appendix-a-dependency-graph.md) | 模块依赖图与开发顺序 |
| [appendix-b-update-flows.md](appendix-b-update-flows.md) | 数据模型更新流程 |
| [appendix-c-skills.md](appendix-c-skills.md) | Skills 参考 |

## 重要约定

- **后端包名**：`app/`（与 api-builder 模板一致，标准 FastAPI 项目结构）
- **Python 命令**：使用 `uv run python` 执行
- **进度追踪**：使用 **planning-with-files** skill 防止上下文丢失
- **增量测试**：每阶段完成后使用 **tests-kit** skill 测试
- **前端认证**：默认使用 Mock 登录（X-User-Id header）
- **前端 API 代理**：`next.config.js` 配置 rewrites（见 [06-frontend-setup.md](06-frontend-setup.md)）

## 本地开发

```bash
# 同步依赖
uv sync
cd frontend && npm install

# 重置数据库并注入种子数据
make resetdb && make seed

# 启动服务
make start  # 后端 8000 + 前端 3000
```

## 常见问题

### Hydration mismatch（开发环境）

如果浏览器控制台出现 “A tree hydrated but some attributes… didn’t match” 且差异类似 `data-gr-ext-installed`、`data-new-gr-c-s-check-loaded`，通常是 Grammarly 等浏览器扩展在 React 加载前向 `<body>` 注入了属性导致的，并不一定是业务代码问题。

### ENOENT: pages/_document.js（开发/构建产物）

如果出现 `ENOENT: no such file or directory, open .../.next/server/pages/_document.js`，通常是 `.next` 构建缓存残缺或历史构建产物引用不一致导致。解决方式：

- 删除 `frontend/.next` 后重启前端开发服务

## 完整工作流图

```
┌─────────────────────────────────────────────────────────────────┐
│ 贯穿全流程: planning-with-files skill                            │
│  - task_plan.md (规划) / progress.md (进度) / findings.md (发现) │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 阶段 0: 项目初始化                                               │
│  - 定义技术栈、创建项目结构、配置开发环境                          │
└───────────────────────────────┬─────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│ 阶段 0.5: 领域建模 [domain-modeler]                              │
│  - 从 user-journeys 提取实体、关系、约束                          │
│  - 输出: data-types.md, relationships.md, crud-operations.md    │
└───────────────────────────────┬─────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│ 阶段 1: API 设计 [schema-to-openapi]                             │
│  - 从 docs/ + specs/ 生成 OpenAPI 3.x 规范                       │
└───────────────────────────────┬─────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│ 阶段 2: 后端代码生成 [api-builder]                                │
│  - FastAPI 后端 + SQLAlchemy + Alembic 迁移                      │
└───────────────────────────────┬─────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│ 阶段 2.5-3: 种子数据 [seed-designer]                             │
│  - 从测试用例推导种子数据需求 → 注入数据库                         │
└───────────────────────────────┬─────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│ 阶段 4: UI 设计文档                                              │
│  - 参考 user-journeys 生成 UI 规范                               │
└───────────────────────────────┬─────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│ 阶段 5-6: 前端配置 [api-builder --generate-client]               │
│  - shadcn/ui + Neon Forge 主题                                   │
│  - TypeScript API 客户端 + Next.js rewrites 代理                 │
└───────────────────────────────┬─────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│ 阶段 7: 前端组件开发                                             │
│  - shadcn 组件优先 → 页面组件                                    │
│  - Mock 数据 → API 调用替换                                      │
└───────────────────────────────┬─────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│ 阶段 8: E2E 测试 [Playwright]                                    │
│  - 用户旅程端到端测试                                            │
└───────────────────────────────┬─────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│ 阶段 9: 最终集成验证                                             │
│  - 前端-后端连通性 → 全栈测试 → 测试汇总                          │
└─────────────────────────────────────────────────────────────────┘
```

## 测试结果预期

| 测试层 | 命令 | 预期 |
|-------|------|------|
| 后端单元测试 | `uv run pytest app/tests/` | 390+ passed |
| 前端单元测试 | `cd frontend && npm test` | 43+ passed |
| E2E 测试 | `npx playwright test` | 核心流程通过 |
