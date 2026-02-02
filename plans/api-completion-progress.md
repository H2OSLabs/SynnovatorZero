# API 补全进度跟踪

> 对应计划文档: `plans/api-completion-plan.md`
>
> 创建时间: 2025-02-03
> 更新时间: 2025-02-03

## 当前状态总览

| 模块 | 状态 | 说明 |
|------|------|------|
| **OpenAPI 规范** | ⚠️ 部分完成 | 缺失 Auth、User Relations、Category Association、Notifications |
| **数据模型** | ⚠️ 部分完成 | user_user/category_category 已有，notifications 缺失 |
| **缓存字段** | ⚠️ 部分完成 | Post 缓存完整，User/Category 缓存字段缺失 |
| **权限校验** | 🔴 严重不足 | DELETE 端点无权限检查，Admin 端点未实现 |
| **数据库迁移** | 🔴 未执行 | alembic/versions/ 为空 |
| **前端组件** | 🔴 未开始 | 仅有占位符 |

## 当前阶段

**Phase 0: shadcn/ui 组件安装与配置** - ⏳ 待开始

## 进度总览

| Phase | 状态 | 完成度 |
|-------|------|--------|
| Phase 0: shadcn/ui 组件安装 | ⏳ 待开始 | 0% |
| Phase 1: OpenAPI 规范补全 | ⏳ 待开始 | 0% |
| Phase 2: 数据模型补全 | ⏳ 待开始 | 0% |
| Phase 3: 缓存策略实现 | ⏳ 待开始 | 0% |
| Phase 4: 权限校验修复 | ⏳ 待开始 | 0% |
| Phase 5: 数据库迁移 | ⏳ 待开始 | 0% |
| Phase 6: 业务逻辑实现 | ⏳ 待开始 | 0% |
| Phase 7: 前端组件实现 | ⏳ 待开始 | 0% |
| Phase 8: 测试与文档 | ⏳ 待开始 | 0% |

---

## Phase 0: shadcn/ui 组件安装与配置

### 0.1 初始化
- [ ] `npx shadcn@latest init` 完成
- [ ] 选择 style、base color、CSS variables

### 0.2 安装核心组件
- [ ] 布局导航: sidebar, sheet, navigation-menu, breadcrumb, pagination, tabs
- [ ] 按钮表单: button, input, textarea, select, checkbox, radio-group
- [ ] 卡片展示: card, avatar, badge, skeleton, separator, scroll-area
- [ ] 交互反馈: dialog, alert-dialog, dropdown-menu, popover, command, tooltip, sonner

### 0.3 主题配置
- [ ] Neon Forge CSS 变量添加到 globals.css
- [ ] shadcn dark mode 变量映射

### 0.4 验证
- [ ] `npm run build` 无报错
- [ ] 组件正常渲染

---

## Phase 1: OpenAPI 规范补全

### 1.1 Auth 端点
- [ ] `/auth/login` POST
- [ ] `/auth/logout` POST
- [ ] `/auth/refresh` POST
- [ ] OAuth 端点 (P1)

### 1.2 User Relations 端点
- [ ] `/users/{user_id}/follow` POST
- [ ] `/users/{user_id}/follow` DELETE
- [ ] `/users/{user_id}/followers` GET
- [ ] `/users/{user_id}/following` GET
- [ ] `/users/{user_id}/block` POST (P2)
- [ ] `/users/{user_id}/block` DELETE (P2)

### 1.3 Category Association 端点
- [ ] `/categories/{category_id}/categories` GET
- [ ] `/categories/{category_id}/categories` POST
- [ ] `/categories/{category_id}/categories/{target_id}` DELETE

### 1.4 Notifications 端点
- [ ] `/notifications` GET
- [ ] `/notifications/{id}` PATCH
- [ ] `/notifications/read-all` POST

### 1.5 Schema 定义
- [ ] LoginRequest / LoginResponse / RefreshRequest
- [ ] CategoryAssociationType / CategoryAssociationCreate / CategoryAssociation
- [ ] NotificationType / Notification / NotificationUpdate / PaginatedNotificationList
- [ ] PlatformStats

---

## Phase 2: 数据模型补全

### 2.1 新增模型
- [ ] `app/models/notification.py` - Notification 模型

### 2.2 User 模型缓存字段
- [ ] 添加 `follower_count` 字段
- [ ] 添加 `following_count` 字段
- [ ] 添加 `notifications` 关系

### 2.3 Category 模型缓存字段
- [ ] 添加 `participant_count` 字段

### 2.4 Schema 更新
- [ ] 创建 `app/schemas/notification.py`
- [ ] 更新 `app/schemas/user.py`
- [ ] 更新 `app/schemas/category.py`
- [ ] 更新 `app/models/__init__.py`

---

## Phase 3: 缓存策略实现

### 3.1 缓存更新函数
- [ ] 创建 `app/services/cache_update.py`
- [ ] 实现 `_update_user_follow_cache()`
- [ ] 实现 `_update_category_participant_cache()`

### 3.2 CRUD 补充
- [ ] `app/crud/user_users.py` - 添加 `count_followers()`, `count_following()`
- [ ] `app/crud/category_groups.py` - 添加 `count_by_category()`

### 3.3 集成
- [ ] 在关注/取关路由中调用缓存更新
- [ ] 在团队报名路由中调用缓存更新
- [ ] 更新 `cascade_delete.py` 添加缓存清理

---

## Phase 4: 权限校验修复 (🔴 优先)

### 4.1 DELETE 端点所有权检查
- [ ] `DELETE /posts/{id}` - 作者 or Admin
- [ ] `DELETE /groups/{id}` - Owner or Admin
- [ ] `DELETE /resources/{id}` - 创建者 or Admin
- [ ] `DELETE /users/{id}` - 本人 or Admin
- [ ] `DELETE /rules/{id}` - 创建者 or Admin
- [ ] `DELETE /categories/{id}` - 创建者 or Admin

### 4.2 PATCH 端点所有权检查
- [ ] `PATCH /posts/{id}` - 作者 or Admin
- [ ] `PATCH /groups/{id}` - Owner/Admin member or Admin
- [ ] `PATCH /resources/{id}` - 创建者 or Admin
- [ ] `PATCH /users/{id}` - 本人 or Admin
- [ ] `PATCH /rules/{id}` - 创建者 or Admin

### 4.3 Admin 批操作
- [ ] 实现 `batch_delete_posts` + 权限检查
- [ ] 实现 `batch_update_post_status` + 权限检查
- [ ] 实现 `batch_update_user_roles` + 权限检查

### 4.4 JWT 认证 (P1)
- [ ] 创建 `app/core/security.py`
- [ ] 更新 `app/deps.py` 替换 Header 认证
- [ ] 添加 Token 黑名单支持

---

## Phase 5: 数据库迁移

- [ ] 确保所有模型已导入到 `__init__.py`
- [ ] 生成初始迁移: `alembic revision --autogenerate -m "initial_schema"`
- [ ] 检查迁移脚本正确性
- [ ] 执行迁移: `alembic upgrade head`
- [ ] 验证表结构

---

## Phase 6: 业务逻辑实现

### 6.1 Auth 模块 (P0)
- [ ] 密码哈希和验证 (passlib + bcrypt)
- [ ] JWT Token 生成和验证 (python-jose)
- [ ] `/auth/login` 实现
- [ ] `/auth/logout` 实现
- [ ] `/auth/refresh` 实现
- [ ] OAuth 集成 (P1)

### 6.2 User Relations 模块 (P0)
- [ ] 关注功能 (`POST /users/{id}/follow`)
- [ ] 取关功能 (`DELETE /users/{id}/follow`)
- [ ] 关注列表查询 (`GET /users/{id}/following`)
- [ ] 粉丝列表查询 (`GET /users/{id}/followers`)

### 6.3 Category Association 模块 (P0)
- [ ] 创建关联 + 自引用检查 + 重复检查 + 循环依赖检测
- [ ] 查询关联 (支持按 relation_type 筛选)
- [ ] 删除关联
- [ ] 前置条件校验集成

### 6.4 Notifications 模块 (P1)
- [ ] 通知 CRUD
- [ ] 通知触发器 (评论/点赞/关注/团队申请/获奖)
- [ ] 未读计数

---

## Phase 7: 前端组件实现

### 7.1 P0 组件
- [ ] `frontend/components/auth/LoginForm.tsx`
- [ ] `frontend/components/auth/RegisterForm.tsx`
- [ ] `frontend/components/user/UserFollowButton.tsx`
- [ ] `frontend/components/category/CategoryStageView.tsx`

### 7.2 P1 组件
- [ ] `frontend/components/notification/NotificationDropdown.tsx`
- [ ] `frontend/components/user/FollowersList.tsx`
- [ ] `frontend/components/user/FollowingList.tsx`
- [ ] `frontend/components/category/CategoryTrackView.tsx`

### 7.3 P2 组件
- [ ] `frontend/components/search/SearchModal.tsx`
- [ ] `frontend/components/home/PlatformStats.tsx`

---

## Phase 8: 测试与文档

### 8.1 单元测试
- [ ] Auth 测试 (登录/Token验证/刷新/登出)
- [ ] User Relations 测试 (参考 13-user-follow.md)
- [ ] Category Association 测试 (参考 14-category-association.md)
- [ ] Notifications 测试
- [ ] 权限检查测试

### 8.2 集成测试
- [ ] 登录流程 E2E
- [ ] OAuth E2E
- [ ] 多阶段活动报名 E2E
- [ ] 通知触发 E2E

### 8.3 文档
- [ ] Swagger UI 更新
- [ ] TypeScript 客户端生成
- [ ] README 更新

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
