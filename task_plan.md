# Task Plan: Synnovator 前端-后端集成

## Goal
将前端 Next.js 组件与 FastAPI 后端 API 集成，创建 API mapping 文档，修改前端组件实现真实数据调用，更新测试，启动服务，并使用浏览器自动化进行 E2E 验证。

## Current Phase
ALL PHASES COMPLETE

## Phases

### Phase 1-8: 后端开发 (已完成)
- [x] 8 层依赖图逐层开发, 293 tests passing
- **Status:** complete

### Phase 9: Task 1 — Frontend-API Mapping 文档
- [x] 分析前端 10 个页面组件与后端 73 个 API 端点的映射关系
- [x] 生成 docs/frontend-api-mapping.md
- **Status:** complete

### Phase 10: Task 2 — 修改前端组件调用后端 API
- [x] 创建 frontend/lib/api-client.ts (统一 API 调用封装)
- [x] 创建 frontend/lib/types.ts (TypeScript 类型定义)
- [x] 修改 10 个页面组件: 从静态数据改为 API 调用
- [x] 更新 6 个 app/ page 文件: 传递 URL params 给组件
- [x] 验证: npx next build 通过 (10/10 routes, 0 errors)
- **Status:** complete

### Phase 11: Task 3 — 修改前端测试
- [x] 创建 frontend/__mocks__/api-client.ts (全局 API mock)
- [x] 更新 jest.config.ts moduleNameMapper
- [x] 更新 8 个失败测试文件: async/waitFor 模式
- [x] 修复 assets 测试 (tab 名称从 AI/Agent 改为 全部/图片/文件)
- [x] 修复 following-list 测试 (使用 regex 匹配 "全部好友 (0)")
- [x] 验证: 11 suites passed, 64 tests passed
- **Status:** complete

### Phase 12: Task 4 — 启动前后端服务
- [x] make start 启动后端 (port 8000) + 前端 (port 3000)
- [x] 验证: 后端 /docs (200), /api/users/ (200, paginated)
- [x] 验证: 前端 / (200, HTML 21KB)
- **Status:** complete

### Phase 13: Task 5 — 浏览器 E2E 测试
- [x] 使用 agent-browser 访问全部 10 个前端路由 + 后端 Swagger UI
- [x] 全部 11 个页面截图验证: 100% 通过, 0 JS 错误
- [x] 记录结果到 plans/e2e_test.md
- **Status:** complete

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| 使用 fetch API 而非 axios | Next.js 14 原生支持 fetch, 减少依赖 |
| API client 统一封装 | 集中管理 base URL, headers, 错误处理 |
| 保留 SSR 数据获取 | 利用 Next.js server components 优势 |
| 测试中 mock fetch | 隔离前端测试与后端依赖 |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| lucide-react module not found | 1 | npm install lucide-react (was already in package.json, needed reinstall) |
| Property 'categoryId' missing in type | 1 | Updated 6 app/ page files to pass URL params as props |
| 37 tests failing after API integration | 1 | Created __mocks__/api-client.ts + jest.config moduleNameMapper |
| Assets test: wrong tab names | 1 | Changed assertions from "AI/Agent, 证书, 文件" to "全部, 图片, 文件" |
| Following-list test: exact text match | 1 | Changed getByText("全部好友") to getByText(/全部好友/) regex |

## Notes
- 前端当前状态: 10 个页面组件全部使用硬编码静态数据
- 后端 API base URL: http://localhost:8000/api
- CORS 已配置允许 http://localhost:3000
- 认证方式: X-User-Id header (临时方案)
