# Task Plan: 前端页面重构开发

> **目标**: 根据 user-journeys.md 和 ui-design-spec.md，重新设计并实现前端页面
> **创建时间**: 2026-02-03
> **背景**: 上一版本代码已删除，从头开始重做前端

## 当前阶段

**Phase 2: 补充缺失的 UI 设计规范** - ✅ 已完成

## 阶段列表

| Phase | 描述 | 状态 | 完成度 |
|-------|------|------|--------|
| Phase 1 | 分析 User Journey 与 UI 设计的差距 | ✅ 完成 | 100% |
| Phase 2 | 补充缺失的 UI 设计规范 | ✅ 完成 | 100% |
| Phase 3 | 创建页面路由结构 | ✅ 完成 | 100% |
| Phase 4 | 实现布局组件 (Header/Sidebar/Panel) | ✅ 完成 | 100% |
| Phase 5 | 实现卡片组件 | ✅ 完成 | 100% |
| Phase 6 | 实现页面 Body 内容 | ✅ 完成 | 100% |
| Phase 7 | 集成测试与验证 | ⏳ 待开始 | 0% |

---

## Phase 1: 分析与差距检查 ✅

### 1.1 User Journey → 页面需求映射

| Journey | 描述 | 需要的页面路由 | UI 设计章节 | 状态 |
|---------|------|---------------|-------------|------|
| J2 | 浏览探索页 | `/`, `/explore` | 7.1 首页, 7.2 探索页 | ✅ 已有设计 |
| J3 | 注册 | `/register` | 7.9 登录/注册页 | ✅ 已有设计 |
| J4 | 登录 | `/login` | 7.9 登录/注册页 | ✅ 已有设计 |
| J5 | 加入组 | `/groups/[id]` | 7.6 团队详情页 | ✅ 已有设计 |
| J6 | 创建活动 | `/events/create` | 7.11 创建活动页 | ✅ 已补充 |
| J7 | 加入活动 | `/events/[id]` | 7.3 活动详情页 | ✅ 已有设计 |
| J8 | 创建团队 | `/groups/create` | 7.12 创建团队页 | ✅ 已补充 |
| J9 | 发送帖子 | `/posts/create`, `/posts/[id]/edit` | 7.5 创建/编辑帖子页 | ✅ 已有设计 |
| J10 | 活动结束与颁奖 | `/events/[id]/ranking` | 7.8 排名页 | ✅ 已有设计 |
| J11 | 编辑 Post | `/posts/[id]/edit` | 7.5 创建/编辑帖子页 | ✅ 已有设计 |
| J12 | 删除 Post | (对话框组件) | 8.5.2 对话框 | ✅ 已有设计 |
| J13 | 社区互动 | `/posts/[id]` | 7.4 帖子详情页 | ✅ 已有设计 |
| J14 | 关注与好友 | `/users/[id]` | 7.7 用户主页 | ✅ 已有设计 |
| J15 | 多阶段/多赛道 | `/events/[id]` | 7.10 多阶段活动页 | ✅ 已有设计 |
| J16 | 资产转移 | (帖子编辑页附件) | 7.5 附件管理 | ✅ 已有设计 |

**分析结果**: 16/16 User Journey 现在都有对应的 UI 设计 ✅

### 1.2 现有前端组件盘点

**shadcn/ui 基础组件 (25个):**
- 布局: sidebar, sheet, navigation-menu, breadcrumb, pagination, tabs
- 按钮表单: button, input, textarea, select, checkbox, radio-group
- 卡片展示: card, avatar, badge, skeleton, separator, scroll-area
- 交互反馈: dialog, alert-dialog, dropdown-menu, popover, command, tooltip, sonner

**已有业务组件 (10个):**
- `auth/LoginForm.tsx` - 登录表单
- `auth/RegisterForm.tsx` - 注册表单
- `user/UserFollowButton.tsx` - 关注按钮
- `user/FollowersList.tsx` - 粉丝列表
- `user/FollowingList.tsx` - 关注列表
- `category/CategoryStageView.tsx` - 活动阶段视图
- `category/CategoryTrackView.tsx` - 活动赛道视图
- `notification/NotificationDropdown.tsx` - 通知下拉
- `search/SearchModal.tsx` - 搜索弹窗
- `home/PlatformStats.tsx` - 平台统计

---

## Phase 2: 补充缺失的 UI 设计规范 ✅

已在 `specs/ui/ui-design-spec.md` 中补充:
- [x] 7.11 创建活动页 (Focus 布局, POST /categories)
- [x] 7.12 创建团队页 (Focus 布局, POST /groups)

---

## Phase 3: 创建页面路由结构

### 3.1 页面路由清单

按优先级分组:

**P0 - 核心页面 (必须实现):**
| 路由 | 布局 | 文件路径 | 对应 UI 设计 |
|------|------|---------|-------------|
| `/` | Landing | `app/page.tsx` | 7.1 首页 |
| `/login` | Landing | `app/login/page.tsx` | 7.9 登录页 |
| `/register` | Landing | `app/register/page.tsx` | 7.9 注册页 |
| `/explore` | Compact | `app/explore/page.tsx` | 7.2 探索页 |
| `/events` | Compact | `app/events/page.tsx` | 活动列表 |
| `/events/[id]` | Full | `app/events/[id]/page.tsx` | 7.3 活动详情 |

**P1 - 重要页面:**
| 路由 | 布局 | 文件路径 | 对应 UI 设计 |
|------|------|---------|-------------|
| `/posts` | Compact | `app/posts/page.tsx` | 帖子列表 |
| `/posts/[id]` | Full | `app/posts/[id]/page.tsx` | 7.4 帖子详情 |
| `/posts/create` | Focus | `app/posts/create/page.tsx` | 7.5 创建帖子 |
| `/posts/[id]/edit` | Focus | `app/posts/[id]/edit/page.tsx` | 7.5 编辑帖子 |
| `/groups` | Compact | `app/groups/page.tsx` | 团队列表 |
| `/groups/[id]` | Full | `app/groups/[id]/page.tsx` | 7.6 团队详情 |
| `/users/[id]` | Full | `app/users/[id]/page.tsx` | 7.7 用户主页 |

**P2 - 扩展页面:**
| 路由 | 布局 | 文件路径 | 对应 UI 设计 |
|------|------|---------|-------------|
| `/events/create` | Focus | `app/events/create/page.tsx` | 7.11 创建活动 |
| `/groups/create` | Focus | `app/groups/create/page.tsx` | 7.12 创建团队 |
| `/settings` | Full | `app/settings/page.tsx` | 设置页 |

### 3.2 待创建的路由文件

```
frontend/app/
├── page.tsx                    # / (已存在，需更新)
├── login/page.tsx              # /login
├── register/page.tsx           # /register
├── explore/page.tsx            # /explore
├── events/
│   ├── page.tsx                # /events
│   ├── [id]/page.tsx           # /events/[id]
│   └── create/page.tsx         # /events/create
├── posts/
│   ├── page.tsx                # /posts
│   ├── [id]/
│   │   ├── page.tsx            # /posts/[id]
│   │   └── edit/page.tsx       # /posts/[id]/edit
│   └── create/page.tsx         # /posts/create
├── groups/
│   ├── page.tsx                # /groups
│   ├── [id]/page.tsx           # /groups/[id]
│   └── create/page.tsx         # /groups/create
├── users/
│   └── [id]/page.tsx           # /users/[id]
└── settings/page.tsx           # /settings
```

---

## Phase 4: 实现布局组件

### 4.1 布局组件清单

| 组件 | 文件路径 | 描述 |
|------|---------|------|
| Header | `components/layout/Header.tsx` | 60px 顶部导航 |
| Sidebar | `components/layout/Sidebar.tsx` | 168px/60px 侧边栏 |
| Panel | `components/layout/Panel.tsx` | 328px 右侧面板 |
| PageLayout | `components/layout/PageLayout.tsx` | 4 种布局变体容器 |

### 4.2 布局变体

```tsx
type LayoutVariant = 'full' | 'compact' | 'focus' | 'landing'

// Full: Sidebar 展开 + Panel 显示
// Compact: Sidebar 收起 + Panel 显示
// Focus: 无 Sidebar + 无 Panel
// Landing: 无 Sidebar + 无 Panel (居中内容)
```

---

## Phase 5: 实现卡片组件

| 组件 | 文件路径 | 对应 UI 设计 |
|------|---------|-------------|
| CategoryCard | `components/cards/CategoryCard.tsx` | 8.2.1 活动卡片 |
| PostCard | `components/cards/PostCard.tsx` | 8.2.2 帖子卡片 |
| GroupCard | `components/cards/GroupCard.tsx` | 8.2.3 团队卡片 |
| UserCard | `components/cards/UserCard.tsx` | 8.2.4 用户卡片 |

---

## Phase 6: 实现页面 Body 内容

按优先级实现:
1. P0 页面 (首页、登录、探索、活动列表/详情)
2. P1 页面 (帖子、团队、用户)
3. P2 页面 (创建页面、设置)

---

## Phase 7: 集成测试与验证

- [ ] 所有页面路由可访问
- [ ] 布局变体正确渲染
- [ ] API 数据正确获取
- [ ] 用户交互功能正常
- [ ] E2E 测试覆盖核心 Journey

---

## 决策记录

| 日期 | 决策 | 原因 |
|------|------|------|
| 2026-02-03 | 路由使用 `/events` 而非 `/categories` | 更符合 Hackathon 平台语义 |
| 2026-02-03 | 布局组件使用 4 种变体 | 符合 ui-design-spec 1.2 节定义 |
| 2026-02-03 | 复用已有的业务组件 | LoginForm, RegisterForm 等已存在 |
| 2026-02-03 | 补充 7.11 创建活动页、7.12 创建团队页 | J6, J8 Journey 缺少 UI 设计 |

---

## 错误记录

| 错误 | 尝试 | 解决方案 |
|------|------|----------|
| (暂无) | | |
