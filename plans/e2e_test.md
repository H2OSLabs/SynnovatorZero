# E2E 测试报告

**日期:** 2026-01-28
**环境:** macOS Darwin 25.2.0
**后端:** FastAPI @ http://localhost:8000 (uvicorn --reload)
**前端:** Next.js 14 @ http://localhost:3000 (next dev)
**浏览器:** Playwright (headless Chromium, via agent-browser)
**分支:** feat/prototype-v1

---

## 第一轮: 页面路由渲染测试 (Phase 13)

| # | 页面 | URL | 状态 | 备注 |
|---|------|-----|------|------|
| 1 | Home | / | PASS | 品牌标识、导航、卡片渲染 |
| 2 | PostList | /posts | PASS | 找队友/找点子区域 |
| 3 | PostDetail | /posts/1 | PASS | 帖子标题、标签、侧边栏 |
| 4 | ProposalList | /proposals | PASS | 提案广场、筛选 tabs |
| 5 | ProposalDetail | /proposals/1 | PASS | 提案详情、团队信息、tabs |
| 6 | CategoryDetail | /categories/1 | PASS | 活动信息、6 个 tabs |
| 7 | UserProfile | /profile | PASS | 用户统计、关注按钮、tabs |
| 8 | Team | /team | PASS | 团队成员、管理面板 |
| 9 | FollowingList | /following | PASS | 好友/关注 tabs |
| 10 | Assets | /assets | PASS | 资产列表、筛选 |
| 11 | Swagger UI | :8000/docs | PASS | API 文档完整 |

---

## 第二轮: 前端事件对接 E2E 测试 (Phase 16)

### 种子数据

通过 API 创建的测试数据:
- **Users:** Alice 创客 (id=1), Bob 开发者 (id=2), Charlie 组织者 (id=3)
- **Category:** 上海AI创业大赛2026 (id=1)
- **Posts:** 基于大模型的智能教育平台 (id=1), 绿色能源监测系统 (id=2), 社区互助配送网络 (id=3)
- **Group:** AI创新实验室 (id=1), Bob 为成员
- **Follow:** Alice follows Bob

### 测试结果

| # | 测试用例 | 页面 | 操作 | 预期结果 | 实际结果 | 状态 | 截图 |
|---|---------|------|------|---------|---------|------|------|
| 1 | TC-JOUR-002 匿名浏览 | / | 访问首页 | 看到品牌名和内容卡片 | "协创者"可见, 3 篇种子帖子卡片渲染 | **PASS** | e2e-01-home.png |
| 2 | 品牌名导航 | / | 点击"协创者" | URL 为 / | URL: http://localhost:3000/ | **PASS** | e2e-02-brand-nav.png |
| 3 | 侧边栏导航 | / → /categories/1 | 点击"星球" | 跳转到 /categories/1 | 显示"上海AI创业大赛2026" | **PASS** | e2e-03-category-nav.png |
| 4 | 帖子详情 API 数据 | /posts/1 | 访问帖子 | 显示种子数据标题和标签 | "基于大模型的智能教育平台", 标签: AI教育/大模型/个性化学习, 作者: Alice 创客 | **PASS** | e2e-04-post-detail.png |
| 5 | TC-JOUR-013 点赞 | /posts/1 | 点击心形图标 | 图标变红, count+1 | Heart SVG: text-red-500 fill-red-500, count: 0→1 | **PASS** | e2e-05-post-like.png |
| 6 | TC-JOUR-013 评论 | /posts/1 | 输入+发送评论 | 评论保存并显示 | API 返回 201, 评论 "这是一条测试评论！" 渲染在列表中, 评论数 (1) | **PASS** | e2e-06-post-comment.png |
| 7 | 提案详情 API 数据 | /proposals/2 | 访问提案 | 显示种子数据 | "绿色能源监测系统", 标签: 清洁能源/IoT/碳中和, 作者: Bob 开发者 | **PASS** | e2e-07-proposal-detail.png |
| 8 | 提案点赞+评论 | /proposals/2 | 点赞+切Tab+评论 | Like API + comment 保存 | Tab 切换到评论区, 评论 "提案评论测试" 成功保存并渲染 | **PASS** | e2e-08-proposal-comment.png |
| 9 | TC-FRIEND-001 关注 | /profile/3 | 点击关注按钮 | 按钮变为"取消关注" | 按钮文本: "关注" → "取消关注", API 201 成功 | **PASS** | e2e-09-follow.png |
| 10 | 卡片点击导航 | / → /posts/1 | 点击帖子卡片 | 跳转到帖子详情页 | URL: /posts/1, 帖子详情正确渲染 | **PASS** | e2e-10-card-nav.png |

### 测试总结

| 指标 | 结果 |
|------|------|
| 总测试数 | 10 |
| 通过 | 10 |
| 失败 | 0 |
| 通过率 | **100%** |

### 发现并修复的 Bug

| Bug | 原因 | 修复 |
|-----|------|------|
| 评论提交 422 (缺少 type 字段) | api-client `addComment` 未发送 `type: "comment"` | 在 api-client.ts 的 addComment/addRating 中添加 type 字段 |
| 评论提交 422 (双重嵌套 value) | 组件调用 `addComment(id, { value: { text } })` 导致 body 变为 `{value:{value:{text}}}` | 改为 `addComment(id, { text })` |
| 关注自己 422 | /profile 页面 userId=1, currentUser 也是 1 | 创建 /profile/[id] 动态路由, 测试 user 3 (未关注) |

### 已知限制

| 限制 | 说明 |
|------|------|
| currentUser 硬编码为 1 | 所有写操作 (like/comment/follow) 以 userId=1 (Alice) 身份执行 |
| 关注状态未初始化 | UserProfile 不检查当前用户是否已关注, 按钮初始总是"关注" |
| 无登录流程 | 使用 X-User-Id header 简化认证 |
| 无创建表单 | 帖子/提案通过 API 种子数据创建, 前端无创建 UI |

### 覆盖的用户旅程

| Journey | 描述 | 测试覆盖 |
|---------|------|---------|
| TC-JOUR-002 | 匿名浏览 | Test 1: 首页内容卡片可见 |
| TC-JOUR-013 | 社区互动 | Test 5-6: 点赞 + 评论帖子; Test 8: 提案评论 |
| TC-FRIEND-001 | 关注用户 | Test 9: 点击关注按钮, 状态切换 |
| Navigation | 页面导航 | Test 2-3: 品牌名/侧边栏; Test 10: 卡片点击跳转 |

---

## 截图清单

| 文件 | 内容 |
|------|------|
| plans/screenshots/e2e-01-home.png | 首页 (种子数据) |
| plans/screenshots/e2e-02-brand-nav.png | 品牌名点击后 |
| plans/screenshots/e2e-03-category-nav.png | 侧边栏导航到活动详情 |
| plans/screenshots/e2e-04-post-detail.png | 帖子详情 (API 数据) |
| plans/screenshots/e2e-05-post-like.png | 帖子点赞 (红心) |
| plans/screenshots/e2e-06-post-comment.png | 帖子评论 |
| plans/screenshots/e2e-07-proposal-detail.png | 提案详情 (API 数据) |
| plans/screenshots/e2e-08-proposal-comment.png | 提案评论区 |
| plans/screenshots/e2e-09-follow.png | 关注按钮 (取消关注) |
| plans/screenshots/e2e-10-card-nav.png | 卡片点击导航到详情 |

---

## 第三轮: Phase 12 & 13 组件测试

**日期:** 2026-02-03
**环境:** 同上

### Phase 12: P2 Frontend Components

#### 12.1 Demo Page Loading ✅

| 测试项 | 期望结果 | 实际结果 | 状态 |
|--------|----------|----------|------|
| 页面加载 | "协创者 组件演示" 显示 | 正确显示 | PASS |
| Phase 文本 | "Phase 12 前端组件预览" | 正确显示 | PASS |
| 快捷键提示 | "⌘K 搜索" 显示 | 正确显示 | PASS |

**截图**: `plans/e2e_demo_page_2.png`

#### 12.2 PlatformStats Component ✅

| 测试项 | 期望结果 | 实际结果 | 状态 |
|--------|----------|----------|------|
| 组件渲染 | "平台统计" 标题显示 | 正确显示 | PASS |
| 用户统计 | "注册用户" 显示数量 | 显示 "3" | PASS |
| 活动统计 | "活动数量" 显示数量 | 显示 "1" | PASS |
| 作品统计 | "作品数量" 显示数量 | 显示 "3" | PASS |
| API 调用 | GET /api/stats 返回数据 | 正常返回 | PASS |

**截图**: `plans/e2e_demo_stats.png`

#### 12.3 SearchModal Component ✅

| 测试项 | 期望结果 | 实际结果 | 状态 |
|--------|----------|----------|------|
| ⌘K 打开 | 按下 ⌘K 打开搜索弹窗 | 弹窗正常打开 | PASS |
| 搜索框显示 | "搜索用户、活动、作品..." | 正确显示 | PASS |
| 空状态提示 | "输入关键词搜索..." | 正确显示 | PASS |
| 搜索功能 | 输入查询后显示结果 | 正常搜索 | PASS |
| 无结果提示 | "未找到相关结果" | 正确显示 | PASS |

**截图**:
- `plans/e2e_search_modal.png` (弹窗打开)
- `plans/e2e_search_results.png` (搜索结果)

### Phase 13: Admin Batch Operations ✅

#### 13.1 Backend Unit Tests

| 端点 | 测试用例 | 状态 |
|------|----------|------|
| POST /admin/posts/batch-delete | 批量删除成功 | PASS |
| POST /admin/posts/batch-delete | 部分失败(无效ID) | PASS |
| POST /admin/posts/batch-delete | 非管理员禁止(403) | PASS |
| POST /admin/posts/batch-update-status | 批量更新状态成功 | PASS |
| POST /admin/posts/batch-update-status | 无效状态拒绝(422) | PASS |
| POST /admin/posts/batch-update-status | 部分失败(无效ID) | PASS |
| POST /admin/posts/batch-update-status | 非管理员禁止(403) | PASS |
| POST /admin/users/batch-update-roles | 批量更新角色成功 | PASS |
| POST /admin/users/batch-update-roles | 无效角色拒绝(422) | PASS |
| POST /admin/users/batch-update-roles | 部分失败(无效ID) | PASS |
| POST /admin/users/batch-update-roles | 非管理员禁止(403) | PASS |
| POST /admin/users/batch-update-roles | 提升为管理员 | PASS |

**测试结果**: 12 tests passed

### Phase 12 & 13 测试总结

| Phase | 组件/功能 | 测试数 | 通过 | 失败 |
|-------|-----------|--------|------|------|
| 12 | SearchModal | 5 | 5 | 0 |
| 12 | PlatformStats | 5 | 5 | 0 |
| 12 | Demo Page | 3 | 3 | 0 |
| 13 | Admin Batch Operations | 12 | 12 | 0 |
| **总计** | | **25** | **25** | **0** |

### 发现并修复的问题

| 问题 | 修复 |
|------|------|
| CategoryStageView config undefined | 添加 `\|\| STAGE_CONFIGS.draft` 默认值 |
| test_mock_auth.py endpoint path | 更新为新的 POST /admin/posts/batch-update-status |

### Phase 12 & 13 新增截图

| 文件名 | 描述 |
|--------|------|
| plans/e2e_demo_page_2.png | Demo 页面 Phase 12 |
| plans/e2e_demo_stats.png | 平台统计组件 |
| plans/e2e_search_modal.png | 搜索弹窗打开 |
| plans/e2e_search_results.png | 搜索结果显示 |
