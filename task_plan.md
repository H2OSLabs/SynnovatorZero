# Task Plan: 简单用户认证系统

> **目标**: 实现简单的用户名密码认证，区分参赛者(participant)和组织者(organizer)权限
> **创建时间**: 2026-02-04
> **状态**: ✅ 完成

## 设计决策

| 决策项 | 选择 | 原因 |
|--------|------|------|
| 密码方案 | 明文存储比对 | 开发/演示用，快速实现 |
| 角色选择 | 注册时用户自选 | 简单直接，适合原型 |
| 页面权限 | 混合方式 | 核心页面共用，管理功能用 `/manage/*` |
| 会话管理 | X-User-Id header + localStorage | 当前代码已有，改动最小 |
| 种子密码 | 密码 = 用户名 | 方便记忆和演示 |

## 阶段列表

| Phase | 描述 | 状态 | 完成度 |
|-------|------|------|--------|
| Phase 1 | 后端 - 数据模型 | `complete` | 100% |
| Phase 2 | 后端 - API | `complete` | 100% |
| Phase 3 | 前端 - 状态管理 | `complete` | 100% |
| Phase 4 | 前端 - 页面 | `complete` | 100% |
| Phase 5 | 前端 - 管理路由 | `complete` | 100% |
| Phase 6 | 测试验证 | `pending` | 0% |

---

## Phase 1: 后端 - 数据模型 `complete`

- [x] 1.1 User 模型添加 password 字段
- [x] 1.2 重建数据库 (使用 Base.metadata.create_all)
- [x] 1.3 更新种子数据添加密码

### 涉及文件
- `app/models/user.py` ✅
- `scripts/seed_dev_data.py` ✅

---

## Phase 2: 后端 - API `complete`

- [x] 2.1 修改登录 API 验证密码
- [x] 2.2 新增注册 API
- [x] 2.3 添加注册和密码验证测试用例

### 涉及文件
- `app/routers/auth.py` ✅
- `app/schemas/user.py` ✅
- `app/tests/test_auth.py` ✅

### 测试结果
- 18 tests passed

---

## Phase 3: 前端 - 状态管理 `complete`

- [x] 3.1 创建 AuthContext 管理登录状态
- [x] 3.2 更新 api-client 自动附加 user_id
- [x] 3.3 添加 register API 函数
- [x] 3.4 在 RootLayout 中添加 Providers

### 涉及文件
- `frontend/contexts/AuthContext.tsx` ✅ (新建)
- `frontend/components/Providers.tsx` ✅ (新建)
- `frontend/lib/api-client.ts` ✅
- `frontend/app/layout.tsx` ✅

---

## Phase 4: 前端 - 页面 `complete`

- [x] 4.1 更新登录页面使用 AuthContext
- [x] 4.2 创建/更新注册页面（含角色选择）
- [x] 4.3 添加权限检查组件 RequireRole
- [x] 4.4 更新 Header 使用 AuthContext

### 涉及文件
- `frontend/app/login/page.tsx` ✅
- `frontend/app/register/page.tsx` ✅
- `frontend/components/auth/RequireRole.tsx` ✅ (新建)
- `frontend/components/layout/Header.tsx` ✅
- `frontend/components/layout/Sidebar.tsx` ✅
- `frontend/components/layout/PageLayout.tsx` ✅

---

## Phase 5: 前端 - 管理路由 `complete`

- [x] 5.1 创建 /manage 路由结构
- [x] 5.2 创建管理仪表盘页面
- [x] 5.3 创建活动管理页面
- [x] 5.4 Header 添加组织者管理入口

### 涉及文件
- `frontend/app/manage/layout.tsx` ✅ (新建)
- `frontend/app/manage/page.tsx` ✅ (新建)
- `frontend/app/manage/categories/page.tsx` ✅ (新建)

---

## Phase 6: 测试验证 `pending`

等待手动验证：

- [ ] 6.1 测试登录：alice/alice (参赛者)
- [ ] 6.2 测试登录：techcorp/techcorp (组织者)
- [ ] 6.3 验证参赛者无法访问 /manage/*
- [ ] 6.4 验证组织者能看到管理功能

---

## 使用说明

### 测试账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| techcorp | techcorp | 组织者 |
| alice | alice | 参赛者 |
| bob | bob | 参赛者 |
| carol | carol | 参赛者 |

### 权限区分

**参赛者可以:**
- 浏览所有页面
- 发布帖子
- 加入团队和活动

**组织者额外可以:**
- 访问 `/manage/*` 管理页面
- Header 显示"管理"导航链接
- 下拉菜单显示"管理中心"入口
- 创建活动

### 启动方式

```bash
make start  # 启动前后端
```

然后访问:
- http://localhost:3000/login - 登录
- http://localhost:3000/register - 注册（可选角色）
- http://localhost:3000/manage - 管理中心（仅组织者）
