# Findings & Decisions

## 当前任务: 前端页面重构开发

### 项目当前状态 (2026-02-03)
- 后端已完成 (373 tests passed)
- 前端代码已删除，从头开始重做
- 保留了 shadcn/ui 组件 (25个) 和业务组件 (10个)
- 当前可访问页面: `/`（其余页面按路由规划逐步实现）

### User Journey 覆盖分析

**已有 UI 设计 (14/16):**
- J2 浏览探索 → 7.1 首页, 7.2 探索页
- J3 注册 → 7.9 登录/注册页
- J4 登录 → 7.9 登录/注册页
- J5 加入组 → 7.6 团队详情页
- J7 加入活动 → 7.3 活动详情页
- J9 发送帖子 → 7.5 创建/编辑帖子页
- J10 颁奖 → 7.8 排名页
- J11 编辑 Post → 7.5 创建/编辑帖子页
- J12 删除 Post → 8.5.2 对话框组件
- J13 社区互动 → 7.4 帖子详情页
- J14 关注好友 → 7.7 用户主页
- J15 多阶段赛道 → 7.10 多阶段活动页
- J16 资产转移 → 7.5 附件管理

**缺失 UI 设计 (2/16):**
- J6 创建活动 → ❌ 需要补充 7.11 创建活动页
- J8 创建团队 → ❌ 需要补充 7.12 创建团队页

### 页面路由规划

| 路由 | 布局 | Journey | 优先级 |
|------|------|---------|--------|
| `/` | Landing | J2 | P0 |
| `/login` | Landing | J4 | P0 |
| `/register` | Landing | J3 | P0 |
| `/explore` | Compact | J2 | P0 |
| `/events` | Compact | J2, J7 | P0 |
| `/events/[id]` | Full | J7, J10, J15 | P0 |
| `/posts` | Compact | J2 | P1 |
| `/posts/[id]` | Full | J13 | P1 |
| `/posts/create` | Focus | J9 | P1 |
| `/posts/[id]/edit` | Focus | J11 | P1 |
| `/groups` | Compact | J5 | P1 |
| `/groups/[id]` | Full | J5 | P1 |
| `/groups/create` | Focus | J8 | P2 |
| `/events/create` | Focus | J6 | P2 |
| `/users/[id]` | Full | J14 | P1 |
| `/settings` | Full | - | P2 |

### 布局变体规范 (from ui-design-spec 1.2)

| 变体 | Sidebar | Panel | 适用 |
|------|---------|-------|------|
| Full | 展开 168px | 显示 328px | 详情页 |
| Compact | 收起 60px | 显示 | 列表页 |
| Focus | 隐藏 | 隐藏 | 编辑页 |
| Landing | 隐藏 | 隐藏 | 首页/登录 |

### 组件开发顺序

**Phase 4: 布局组件**
1. Header (60px 高度, 固定顶部)
2. Sidebar (168px/60px 宽度, 可收起)
3. Panel (328px 宽度, 右侧面板)
4. PageLayout (组合 4 种布局变体)

**Phase 5: 卡片组件**
1. CategoryCard (活动卡片)
2. PostCard (帖子卡片)
3. GroupCard (团队卡片)
4. UserCard (用户卡片)

**Phase 6: 页面 Body**
按优先级实现 P0 → P1 → P2 页面

---

## 历史记录

### 后端开发 (2026-01-27)
- 从零依赖底层模块开始，逐层向上开发 Synnovator 后端
- 8 层依赖图: user/resource → rule/group/event → post/interaction → 关系 → 规则引擎 → 集成
- 最终 373 tests passed

### 技术决策
| Decision | Rationale |
|----------|-----------|
| 后端包名 `app/` | api-builder 模板兼容 |
| 路由使用 `/events` | 比 `/events` 更符合 Hackathon 语义 |
| 布局 4 种变体 | 符合 ui-design-spec 1.2 定义 |
| 复用已有业务组件 | LoginForm, RegisterForm 等已实现 |

---
*Update this file after every 2 view/browser/search operations*
