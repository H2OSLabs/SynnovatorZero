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
| **前端组件** | ✅ 完成 | P0/P1 组件完成 (SearchModal/PlatformStats P2 延期) |

## 当前阶段

**Phase 8: 测试与文档** - ✅ 完成 (E2E 测试延期至 P2)

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

### 4.3 Admin 批操作 (P2 - 延期)
- [ ] 实现 `batch_delete_posts` + 权限检查
- [ ] 实现 `batch_update_post_status` + 权限检查
- [ ] 实现 `batch_update_user_roles` + 权限检查

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
- [ ] `frontend/components/search/SearchModal.tsx`
- [ ] `frontend/components/home/PlatformStats.tsx`

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
