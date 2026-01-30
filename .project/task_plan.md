# Task Plan: 前端原型完整验证

## Goal
验证前端原型所有功能正常，确保从阶段 4a 到阶段 6 的所有成功标准都满足。

## Current Phase
**Phase 17: 最终验证与 CI/CD 配置**

## Phases

### Phase 1-13: 已完成
- [x] 后端开发 (293 tests), API mapping, 组件 API 数据获取, 测试, E2E 截图
- **Status:** complete

### Phase 14: 前端事件对接 — 导航 + 写操作
按组件逐个对接，优先级：高频交互 > 低频操作

**14a. 全局导航 (所有页面共用 header/sidebar)**
- [x] Header: 品牌名 → `/` (所有 10 个页面)
- [x] Sidebar: 探索→`/` / 星球→`/categories/1` / 营地→`/team` (所有页面)
- [x] Card 点击 → 跳转到详情页

**14b. PostDetail — 点赞/评论 (Journey 13: 社区互动)**
- [x] 点赞按钮: onClick → POST /api/posts/{id}/like, 更新 like_count
- [x] 评论输入框 + 提交: POST /api/posts/{id}/comments
- [x] 评论列表: GET /api/posts/{id}/comments 渲染

**14c. ProposalDetail — 点赞/评论/Tab 切换**
- [x] 同 PostDetail 点赞/评论逻辑
- [x] Tab 切换: 提案详情/团队信息/评论区/版本历史
- [x] 返回提案广场导航

**14d. CategoryDetail — Tab 切换 + 数据加载**
- [x] Tab 切换: 详情/排榜/讨论区/成员/赛程安排/关联活动

**14e. UserProfile — 关注/取关 (Journey: 好友)**
- [x] 关注按钮: POST /api/users/{id}/follow
- [x] 取关按钮: DELETE /api/users/{id}/follow
- [x] Tab 切换: 帖子/提案/收藏

**14f. Team — 成员管理**
- [x] Tab 切换: 提案/帖子/收藏
- [x] Sidebar 导航

**14g. FollowingList — Tab 过滤**
- [x] 已有 activeTab 切换 (全部好友/我关注的)
- [x] Sidebar 导航

**14h. Home/PostList/ProposalList — 卡片点击导航**
- [x] 帖子卡片 → /posts/{id}
- [x] 提案卡片 → /proposals/{id}
- [x] 队伍卡片 → /team (使用 fallback)
- [x] "查看更多" → /proposals
- [x] "找队友" → /posts

- **Status:** complete

### Phase 15: 更新前端测试
- [x] 添加 next/navigation mock 到 jest.setup.ts
- [x] 验证: npx jest 通过 (64 tests, 11 suites, 0 failures)
- **Status:** complete

### Phase 16: E2E 浏览器测试
- [x] 确保后端和前端服务运行
- [x] 用 API 创建种子数据 (3 users, 1 category, 3 posts, 1 group, 1 follow)
- [x] agent-browser 测试核心旅程 (10/10 PASS):
  - TC-JOUR-002: 匿名浏览 — 首页显示种子数据内容卡片 ✅
  - TC-JOUR-013: 社区互动 — 帖子点赞 (红心+计数) + 评论 (保存+渲染) ✅
  - TC-JOUR-013: 提案互动 — 提案点赞 + Tab切换评论区 + 评论 ✅
  - TC-FRIEND-001: 关注用户 — 按钮"关注"→"取消关注" ✅
  - 导航: 品牌名→首页, 侧边栏→活动详情, 卡片→帖子详情 ✅
- [x] 记录结果到 plans/e2e_test.md (含 10 张截图)
- **Status:** complete

### Bug Fixes During E2E (Phase 16)
- [x] api-client.ts: addComment/addRating 缺少 type 字段 → 添加 `type: "comment"` / `type: "rating"`
- [x] post-detail.tsx + proposal-detail.tsx: addComment 参数双重嵌套 value → 改为 `{ text: commentText }`
- [x] 创建 /profile/[id] 动态路由支持查看其他用户资料

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| 不新建"发帖"页面 | 当前原型无创建表单 UI, 通过 API 创建种子数据 |
| 使用 useRouter 导航 | Next.js App Router 标准做法 |
| 点赞/评论/关注用 API client 函数 | 已在 api-client.ts 中定义好 |
| useRouter mock 在 jest.setup.ts | 所有 10 个页面都用了 useRouter, 全局 mock 最简洁 |
| 顺序而非并行执行子 agent | 上一次 5 个并行子 agent 导致上下文耗尽，改为顺序执行 |
| addComment 添加 type 字段 | InteractionCreate schema 要求 type 字段 |
| 创建 /profile/[id] 动态路由 | 支持查看非当前用户的资料页 |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| Jest tests fail: useRouter not a function | 1 | 添加 next/navigation mock 到 jest.setup.ts |
| 5 并行子 agent 上下文耗尽 | 1 | 改为顺序单 agent 执行，减少上下文消耗 |
| addComment 422: missing type field | 1 | api-client.ts 添加 type: "comment" |
| addComment 422: double-nested value | 1 | 组件调用改为 { text: commentText } |
| Follow self 422 | 1 | 测试改为访问 /profile/3 (非当前用户) |
| Backend: email-validator not installed | 1 | 在父项目 SynnovatorZero/.venv 中安装 email-validator |

### Phase 17: 最终验证与 CI/CD 配置
- [x] 修复 frontend tsconfig.json (排除 jest 测试文件)
- [x] 修复 backend 依赖 (email-validator 安装到正确的 venv)
- [x] 验证 `npm run build` 成功 (10 pages built)
- [x] 验证 backend health: `GET /health` → `{"status":"ok"}`
- [x] 验证 API 数据: 4 users, 4 posts, 4 categories
- [x] 验证 frontend 启动: `localhost:3000` 响应 200
- [x] CI/CD 配置: `.github/workflows/ci.yml` 已创建
- [x] 环境变量模板: `.env.example` 已创建
- **Status:** complete

## Final Verification Summary
| Check | Status | Details |
|-------|--------|---------|
| Backend health | ✅ | `{"status":"ok"}` on port 8000 |
| API endpoints | ✅ | /api/users, /api/posts, /api/categories 返回数据 |
| Frontend build | ✅ | 10 pages, 0 errors |
| Frontend dev | ✅ | localhost:3000 正常响应 |
| Jest tests | ✅ | 64 tests passed (Phase 15) |
| E2E tests | ✅ | 10/10 scenarios passed (Phase 16) |
| CI/CD config | ✅ | GitHub Actions workflow created |
