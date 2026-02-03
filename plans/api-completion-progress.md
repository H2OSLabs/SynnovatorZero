# API 补全进度跟踪

> 对应计划文档: `plans/api-completion-plan.md`
>
> 创建时间: 2025-02-03
> 更新时间: 2026-02-03

## 当前状态总览

| 模块 | 状态 | 说明 |
|------|------|------|
| **OpenAPI 规范** | ✅ 完成 | Auth、User Relations、Category Association、Notifications 已添加 |
| **数据模型** | ✅ 完成 | notifications 模型已创建 |
| **缓存字段** | ✅ 完成 | User/Category 缓存字段已添加 |
| **权限校验** | ✅ 完成 | DELETE/PATCH 端点权限检查已实现 |
| **数据库迁移** | ✅ 完成 | 初始迁移已生成并执行 |
| **前端组件** | ✅ 完成 | P0/P1/P2 组件全部完成 |

## 当前阶段

**All Phases Complete** - ✅ 完成

## 进度总览

| Phase | 状态 | 完成度 |
|-------|------|--------|
| Phase 0: shadcn/ui 组件安装 | ✅ 完成 | 100% |
| Phase 1: OpenAPI 规范补全 | ✅ 完成 | 100% |
| Phase 2: 数据模型补全 | ✅ 完成 | 100% |
| Phase 3: 缓存策略实现 | ✅ 完成 | 100% |
| Phase 4: 权限校验修复 | ✅ 完成 | 100% |
| Phase 5: 数据库迁移 | ✅ 完成 | 100% |
| Phase 6: 业务逻辑实现 | ✅ 完成 | 100% |
| Phase 7: 前端组件实现 | ✅ 完成 | 100% |
| Phase 8: 测试与文档 | ✅ 完成 | 100% |
| Phase 9: OAuth Mock Switch | ✅ 完成 | 100% |
| Phase 10: Notification Event System | ✅ 完成 | 100% |
| Phase 11: E2E Testing (Playwright) | ✅ 完成 | 100% |
| Phase 12: P2 Frontend Components | ✅ 完成 | 100% |
| Phase 13: Admin Batch Operations | ✅ 完成 | 100% |

---

## Phase 0: shadcn/ui 组件安装与配置 ✅

### 0.1 初始化
- [x] `npx shadcn@latest init` 完成 (New York style, neutral, CSS variables)
- [x] 选择 style、base color、CSS variables

### 0.2 安装核心组件
- [x] 布局导航: sidebar, sheet, navigation-menu, breadcrumb, pagination, tabs
- [x] 按钮表单: button, input, textarea, select, checkbox, radio-group
- [x] 卡片展示: card, avatar, badge, skeleton, separator, scroll-area
- [x] 交互反馈: dialog, alert-dialog, dropdown-menu, popover, command, tooltip, sonner

### 0.3 主题配置
- [x] Neon Forge CSS 变量添加到 globals.css
- [x] shadcn dark mode 变量映射

### 0.4 验证
- [x] `npm run build` 无报错
- [x] 组件正常渲染 (25 个 UI 组件已安装)

---

## Phase 1: OpenAPI 规范补全 ✅

### 1.1 Auth 端点
- [x] `/auth/login` POST
- [x] `/auth/logout` POST
- [x] `/auth/refresh` POST
- [ ] OAuth 端点 (P1 - deferred)

### 1.2 User Relations 端点
- [x] `/users/{user_id}/follow` POST
- [x] `/users/{user_id}/follow` DELETE
- [x] `/users/{user_id}/followers` GET
- [x] `/users/{user_id}/following` GET
- [ ] `/users/{user_id}/block` POST (P2 - deferred)
- [ ] `/users/{user_id}/block` DELETE (P2 - deferred)

### 1.3 Category Association 端点
- [x] `/categories/{category_id}/categories` GET
- [x] `/categories/{category_id}/categories` POST
- [x] `/categories/{category_id}/categories/{target_id}` DELETE

### 1.4 Notifications 端点
- [x] `/notifications` GET
- [x] `/notifications/{id}` PATCH
- [x] `/notifications/read-all` POST

### 1.5 Schema 定义
- [x] LoginRequest / LoginResponse / RefreshRequest
- [x] CategoryAssociationType / CategoryAssociationCreate / CategoryAssociation
- [x] NotificationType / Notification / NotificationUpdate / PaginatedNotificationList
- [ ] PlatformStats (P2 - deferred)

---

## Phase 2: 数据模型补全 ✅

### 2.1 新增模型
- [x] `app/models/notification.py` - Notification 模型

### 2.2 User 模型缓存字段
- [x] 添加 `follower_count` 字段
- [x] 添加 `following_count` 字段
- [x] 添加 `notifications` 关系

### 2.3 Category 模型缓存字段
- [x] 添加 `participant_count` 字段

### 2.4 Schema 更新
- [x] 创建 `app/schemas/notification.py`
- [x] 更新 `app/schemas/user.py`
- [x] 更新 `app/schemas/category.py`
- [x] 更新 `app/models/__init__.py`

---

## Phase 3: 缓存策略实现 ✅

### 3.1 缓存更新函数
- [x] 创建 `app/services/cache_update.py`
- [x] 实现 `update_user_follow_cache()`
- [x] 实现 `update_category_participant_cache()`

### 3.2 CRUD 补充
- [x] `app/crud/user_users.py` - 添加 `count_followers()`, `count_following()`
- [x] `app/crud/category_groups.py` - 添加 `count_by_category()`

### 3.3 集成
- [ ] 在关注/取关路由中调用缓存更新 (Phase 6 实现)
- [ ] 在团队报名路由中调用缓存更新 (Phase 6 实现)
- [ ] 更新 `cascade_delete.py` 添加缓存清理 (Phase 6 实现)

---

## Phase 4: 权限校验修复 ✅

### 4.1 DELETE 端点所有权检查
- [x] `DELETE /posts/{id}` - 作者 or Admin
- [x] `DELETE /groups/{id}` - Owner or Admin
- [x] `DELETE /resources/{id}` - 创建者 or Admin
- [x] `DELETE /users/{id}` - 本人 or Admin
- [x] `DELETE /rules/{id}` - 创建者 or Admin
- [x] `DELETE /categories/{id}` - 创建者 or Admin

### 4.2 PATCH 端点所有权检查
- [x] `PATCH /posts/{id}` - 作者 or Admin
- [x] `PATCH /groups/{id}` - Owner/Admin member or Admin
- [x] `PATCH /resources/{id}` - 创建者 or Admin
- [x] `PATCH /users/{id}` - 本人 or Admin
- [x] `PATCH /rules/{id}` - 创建者 or Admin

### 4.3 Admin 批操作 ✅ (Phase 13)
- [x] 实现 `batch_delete_posts` + 权限检查
- [x] 实现 `batch_update_post_status` + 权限检查
- [x] 实现 `batch_update_user_roles` + 权限检查

### 4.4 JWT 认证 (P1 - 延期)
- [ ] 创建 `app/core/security.py`
- [ ] 更新 `app/deps.py` 替换 Header 认证
- [ ] 添加 Token 黑名单支持

### 4.5 测试更新
- [x] 更新 `app/tests/conftest.py` 添加 auth_headers fixture
- [x] 更新所有测试文件添加必要的认证头

---

## Phase 5: 数据库迁移 ✅

- [x] 确保所有模型已导入到 `__init__.py`
- [x] 初始化 alembic: `alembic init alembic`
- [x] 配置 `alembic/env.py` 导入模型和数据库 URL
- [x] 生成迁移: `alembic revision --autogenerate -m "initial_schema"`
- [x] 检查迁移脚本正确性 (添加 server_default 处理现有数据)
- [x] 执行迁移: `alembic upgrade head`
- [x] 验证测试通过 (293 passed)

---

## Phase 6: 业务逻辑实现 ✅

### 6.1 Auth 模块 (P0)
- [x] 创建 `app/routers/auth.py` (临时 header-based 实现)
- [x] `/auth/login` 实现 (验证用户名存在，返回 user_id)
- [x] `/auth/logout` 实现 (placeholder)
- [x] `/auth/refresh` 实现 (placeholder, 返回 501)
- [ ] 密码哈希和验证 (passlib + bcrypt) - P1 延期
- [ ] JWT Token 生成和验证 (python-jose) - P1 延期
- [ ] OAuth 集成 (P1) - 延期

### 6.2 User Relations 模块 (P0)
- [x] 关注功能 (`POST /users/{id}/follow`) - 已存在
- [x] 取关功能 (`DELETE /users/{id}/follow`) - 已存在
- [x] 关注列表查询 (`GET /users/{id}/following`) - 已存在
- [x] 粉丝列表查询 (`GET /users/{id}/followers`) - 已存在
- [x] 缓存更新集成 (follow/unfollow 时更新 follower_count/following_count)

### 6.3 Category Association 模块 (P0)
- [x] 创建关联 + 自引用检查 + 重复检查 + 循环依赖检测 - 已存在
- [x] 查询关联 (支持按 relation_type 筛选) - 已存在
- [x] 删除关联 - 已存在
- [x] 前置条件校验集成 - 已存在

### 6.4 Notifications 模块 (P1)
- [x] 创建 `app/crud/notifications.py`
- [x] 创建 `app/routers/notifications.py`
- [x] 通知 CRUD (list, get, update)
- [x] 未读计数 (`GET /notifications/unread-count`)
- [x] 全部标记已读 (`POST /notifications/read-all`)
- [ ] 通知触发器 (评论/点赞/关注/团队申请/获奖) - P2 延期

---

## Phase 7: 前端组件实现

### 7.1 P0 组件
- [x] `frontend/components/auth/LoginForm.tsx`
- [x] `frontend/components/auth/RegisterForm.tsx`
- [x] `frontend/components/user/UserFollowButton.tsx`
- [x] `frontend/components/category/CategoryStageView.tsx`

### 7.2 P1 组件
- [x] `frontend/components/notification/NotificationDropdown.tsx`
- [x] `frontend/components/user/FollowersList.tsx`
- [x] `frontend/components/user/FollowingList.tsx`
- [x] `frontend/components/category/CategoryTrackView.tsx`

### 7.3 支持文件
- [x] `frontend/lib/types.ts` - TypeScript 类型定义
- [x] `frontend/lib/api-client.ts` - API 客户端
- [x] `frontend/app/demo/page.tsx` - 组件演示页面

### 7.4 P2 组件
- [x] `frontend/components/search/SearchModal.tsx` (Phase 12)
- [x] `frontend/components/home/PlatformStats.tsx` (Phase 12)

---

## Phase 8: 测试与文档

### 8.1 单元测试
- [x] Auth 测试 (登录/Token验证/刷新/登出) - `app/tests/test_auth.py` (12 tests)
- [x] User Relations 测试 (参考 13-user-follow.md) - `app/tests/test_user_follow.py` (已存在)
- [x] Category Association 测试 (参考 14-category-association.md) - `app/tests/test_category_associations.py` (已存在)
- [x] Notifications 测试 - `app/tests/test_notifications.py` (22 tests)
- [x] 权限检查测试 - `app/tests/test_permissions.py` (已存在)

### 8.2 集成测试 (P2 - 延期)
- [ ] 登录流程 E2E
- [ ] OAuth E2E (需要先实现 OAuth)
- [ ] 多阶段活动报名 E2E
- [ ] 通知触发 E2E (需要先实现通知触发器)

### 8.3 文档
- [x] Swagger UI 更新 - FastAPI 自动生成 `/docs` 和 `/redoc`
- [x] TypeScript 客户端生成 - `frontend/lib/api-client.ts` 和 `frontend/lib/types.ts`
- [x] README 更新 - 完整 API 文档和开发指南

---

## 问题记录

| 日期 | 问题 | 解决方案 | 状态 |
|------|------|---------|------|
| 2025-02-03 | DELETE 端点无权限检查 | Phase 4 修复 | ⏳ 待处理 |
| 2025-02-03 | PATCH 端点大多无权限检查 | Phase 4 修复 | ⏳ 待处理 |
| 2025-02-03 | Admin 批操作未实现 | Phase 4 实现 | ⏳ 待处理 |
| 2025-02-03 | 使用 Header 认证而非 JWT | Phase 4.4 升级 | ⏳ 待处理 |
| 2025-02-03 | alembic/versions/ 为空 | Phase 5 生成迁移 | ⏳ 待处理 |

---

## Phase 9: OAuth Mock Switch ✅

> 目标: 添加 Mock 认证开关，便于开发测试，未来上线 OAuth 服务后可关闭

### 9.1 环境配置
- [x] 在 `app/core/config.py` 添加 `MOCK_AUTH` 环境变量
- [x] 添加 `MOCK_USER_ID` 和 `MOCK_USER_ROLE` 配置
- [x] 在 `.env.example` 添加配置说明

### 9.2 Mock 认证实现
- [x] 更新 `app/deps.py` 支持 mock 模式
- [x] Mock 模式下自动创建测试用户 (`_get_or_create_mock_user()`)
- [x] Mock 模式下验证 X-User-Id header (用户存在则通过)
- [x] 无 header 时自动创建 mock 用户

### 9.3 单元测试
- [x] 创建 `app/tests/test_mock_auth.py` (14 tests)
- [x] 测试 mock 模式开启/关闭切换
- [x] 测试 mock 用户自动创建
- [x] 测试角色检查 (`require_role`)
- [x] 更新 16 个现有测试适配 mock 模式行为

### 9.4 总测试结果
- 341 tests passed, 4 warnings

---

## Phase 10: Notification Event System ✅

> 目标: 实现通知触发器，在用户操作时自动创建通知

### 10.1 事件服务基础
- [x] 创建 `app/services/notification_events.py`
- [x] 实现事件函数: `notify_follow`, `notify_comment`, `notify_mentions`, `notify_team_request`, `notify_award`, `notify_system`
- [x] 实现 `parse_mentions()` 解析 @username

### 10.2 关注事件集成
- [x] 在 `POST /users/{id}/follow` 触发 follow 通知
- [x] 通知内容: "{username} 关注了你"
- [x] 包含 related_url 指向关注者的个人页面

### 10.3 评论事件集成
- [x] 在 `POST /posts/{id}/comments` 触发 comment 通知
- [x] 通知内容: "{username} 评论了你的作品「{post_title}」"
- [x] 自己评论自己的帖子不产生通知
- [x] 包含 related_url 指向被评论的帖子

### 10.4 提及事件集成
- [x] 解析评论内容中的 @username (支持字母、数字、下划线、连字符)
- [x] 触发 mention 通知: "{username} 在评论中提到了你"
- [x] 自己提及自己不产生通知
- [x] 提及不存在的用户不产生通知
- [x] 支持同一评论中多个 @mention

### 10.5 单元测试
- [x] 创建 `app/tests/test_notification_events.py` (20 tests)
- [x] 测试 follow 事件通知创建 (3 tests)
- [x] 测试 comment 事件通知创建 (3 tests)
- [x] 测试 @mention 解析 (7 tests)
- [x] 测试 mention 通知创建 (4 tests)
- [x] 测试集成场景 (3 tests)

### 10.6 总测试结果
- 361 tests passed (原有 341 + 新增 20)

---

## Phase 11: E2E Testing (Playwright) ✅

> 目标: 使用 Playwright 进行端到端测试，验证完整用户流程
> 工具: document-skills:webapp-testing skill + Python Playwright

### 11.1 Playwright 配置
- [x] 安装 Python Playwright: `uv add --dev playwright`
- [x] 安装 Chromium: `uv run playwright install chromium`
- [x] 创建 `e2e/` 测试目录
- [x] 创建 `e2e/conftest.py` - 测试配置和 fixtures
- [x] 创建 `e2e/run_e2e.py` - 使用 with_server.py 管理服务器
- [x] 更新 `Makefile` 添加 `test-e2e` target

### 11.2 首页 E2E (`e2e/test_home.py`)
- [x] 页面加载测试
- [x] 标题和副标题显示
- [x] Demo 链接存在和导航
- [x] 深色主题验证

### 11.3 组件演示页 E2E (`e2e/test_demo.py`)
- [x] 页面布局和分区显示
- [x] 认证组件 (登录表单显示、字段验证)
- [x] 活动阶段组件 (徽章、时间线、卡片)
- [x] 用户关系组件 (关注按钮、粉丝/关注 tabs)
- [x] 活动列表组件
- [x] 响应式布局 (mobile/tablet viewports)

### 11.4 测试结果
- 22 tests total (20 passed, 2 skipped)
- 跳过的测试: 表单切换在 headless 模式下有 React hydration 问题

---

## Phase 12: P2 Frontend Components ✅

> 目标: 完成剩余的 P2 前端组件
> 完成日期: 2026-02-03

### 12.1 SearchModal
- [x] 创建 `frontend/components/search/SearchModal.tsx`
- [x] 创建 `frontend/lib/search-api.ts` (客户端搜索)
- [x] 实现全局搜索 UI (用户/活动/作品)
- [x] 集成 Command 组件实现快捷键 (⌘K / Ctrl+K)
- [x] 添加 Jest 测试 `frontend/__tests__/SearchModal.test.tsx` (5 tests)

### 12.2 PlatformStats
- [x] 创建 `frontend/components/home/PlatformStats.tsx`
- [x] 显示平台统计数据 (用户数/活动数/作品数)
- [x] 添加 `GET /api/stats` 端点到 `app/main.py`
- [x] 添加 Jest 测试 `frontend/__tests__/PlatformStats.test.tsx` (5 tests)

### 12.3 Demo 页面更新
- [x] 更新 `frontend/app/demo/page.tsx` 集成新组件
- [x] 添加 "Phase 12 前端组件预览" 标识

### 12.4 Bug 修复
- [x] 修复 `CategoryStageView.tsx` config undefined 错误 (添加 fallback)
- [x] 添加 `ResizeObserver` mock 到 `jest.setup.ts` (cmdk 组件需要)

### 12.5 测试结果
- Frontend Jest: 11 tests passed (包括 5 SearchModal + 5 PlatformStats + 1 existing)
- E2E 验证: Demo 页面加载正常，PlatformStats 显示正确数据，⌘K 打开搜索弹窗

---

## Phase 13: Admin Batch Operations ✅

> 目标: 实现管理员批量操作功能
> 完成日期: 2026-02-03

### 13.1 批量删除作品
- [x] `POST /admin/posts/batch-delete`
- [x] 权限检查: admin only (403 for non-admin)
- [x] 支持软删除 (设置 deleted_at)
- [x] 返回 BatchResult (success_count, failed_count, failed_ids)

### 13.2 批量更新状态
- [x] `POST /admin/posts/batch-update-status`
- [x] 支持 draft/published/archived 状态切换
- [x] 无效状态返回 422 Validation Error

### 13.3 批量更新用户角色
- [x] `POST /admin/users/batch-update-roles`
- [x] 权限检查: admin only
- [x] 支持提升为 admin 角色
- [x] 无效角色返回 422 Validation Error

### 13.4 Schemas
- [x] `BatchDeleteRequest` (ids: list[int])
- [x] `BatchStatusUpdateRequest` (ids: list[int], status: str)
- [x] `BatchRoleUpdateRequest` (ids: list[int], role: str)
- [x] `BatchResult` (success_count, failed_count, failed_ids)

### 13.5 单元测试
- [x] 创建 `app/tests/test_admin_batch.py` (12 tests)
- [x] 测试批量删除成功/部分失败/非管理员禁止
- [x] 测试批量更新状态成功/无效状态/部分失败/非管理员禁止
- [x] 测试批量更新角色成功/无效角色/部分失败/非管理员禁止/提升管理员

### 13.6 测试结果
- Backend pytest: 373 tests passed (361 existing + 12 new admin batch tests)

---

## 决策记录

| 日期 | 决策 | 原因 |
|------|------|------|
| 2025-02-03 | 创建实现计划 | 基于 UI 设计规范和 OpenAPI 差距分析 |
| 2025-02-03 | 将权限修复设为 Phase 4 并标记优先 | 当前权限漏洞严重，可导致数据泄露/篡改 |
| 2025-02-03 | 新增 Phase 2 (数据模型) 和 Phase 3 (缓存策略) | 代码库检查发现缺失项 |
| 2025-02-03 | 新增 Phase 0 (shadcn/ui 组件安装) | 前端原型需要先配置组件库 |
| 2025-02-03 | Markdown 编辑器 → 简单 textarea | 用户确认，快速原型优先 |
| 2025-02-03 | 文件上传 → 原生 input[type=file] | 用户确认，快速原型优先 |
| 2025-02-03 | 标签输入 → Input + Badge 显示 | 用户确认，快速原型优先 |
| 2025-02-03 | 评论输入 → 简单 textarea | 用户确认，快速原型优先 |
| 2026-02-03 | 添加 OAuth Mock Switch | 便于开发测试，未来上线 OAuth 后可关闭 |
| 2026-02-03 | E2E 测试使用 Playwright | 通过 document-skills:webapp-testing skill 执行 |
| 2026-02-03 | 通知触发器分阶段实现 | 先实现 follow，再扩展到 comment/mention |
