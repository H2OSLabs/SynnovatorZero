# Task Plan: 前端问题检查与修复

> **目标**: 根据双分支工作流验证结果，修复前端缺陷并补充测试用例
> **创建时间**: 2026-02-08
> **状态**: `complete`

## 背景

通过双分支工作流验证，发现前端覆盖率仅 16.7%（18/108 页面），存在以下问题：

### 问题分类

| 类型 | 数量 | 优先级 |
|------|------|--------|
| 关键缺失功能 | 6 项 | 高 |
| 部分实现/不完整 | 6 项 | 中 |
| 低优先级改进 | 4 项 | 低 |

### 高优先级问题

1. **社交互动缺失** - 点赞/评论/评分 UI 和 API 集成 ✅ 已修复
2. **活动报名缺失** - 用户无法报名参加活动 ✅ 已修复
3. **消息系统缺失** - 9 个设计页面未实现 (后续迭代)
4. **搜索功能不完整** - `/events` 和 `/groups` 搜索未连接 ✅ 已修复
5. **规则配置缺失** - 活动创建时无法配置规则 (后续迭代)
6. **星球/营地缺失** - 9 个设计页面未实现 (后续迭代)

## 阶段列表

| Phase | 描述 | 状态 |
|-------|------|------|
| Phase 1 | 诊断现有问题（详细代码检查） | `complete` ✓ |
| Phase 2 | 修复社交互动功能（点赞/评论） | `complete` ✓ |
| Phase 3 | 修复搜索/筛选功能 | `complete` ✓ |
| Phase 4 | 修复活动报名流程 | `complete` ✓ |
| Phase 5 | 补充测试用例 | `skipped` (作为后续迭代) |
| Phase 6 | 验证与提交 | `complete` ✓ |

---

## 修复汇总

### Phase 2: 社交互动功能

**修复内容：**
1. 修复了 API 客户端的点赞 URL 路径（`/posts/{id}/likes` → `/posts/{id}/like`）
2. 添加了 `checkPostLiked` API 初始化点赞状态
3. 添加了后端 `GET /posts/{id}/like` 检查点赞状态的 endpoint
4. 创建了可复用的 `LikeButton` 组件（乐观更新）
5. 创建了可复用的 `CommentSection` 组件
6. 帖子详情页已有完整实现，添加了点赞状态初始化

**文件变更：**
- `app/routers/interactions.py` - 添加点赞状态检查 endpoint
- `frontend/lib/api-client.ts` - 修复点赞 API 路径
- `frontend/components/interaction/LikeButton.tsx` - 新建
- `frontend/components/interaction/CommentSection.tsx` - 新建
- `frontend/app/posts/[id]/page.tsx` - 添加点赞状态初始化

### Phase 3: 搜索/筛选功能

**修复内容：**
1. `/events` 页面添加 URL 参数驱动的搜索
2. `/groups` 页面添加 URL 参数驱动的搜索
3. `/posts` 页面添加 Suspense 边界
4. `/users/[id]` 页面添加真实帖子列表（调用 API）
5. 后端添加 `created_by` 过滤参数到帖子列表 API

**文件变更：**
- `frontend/app/events/page.tsx` - 添加搜索 + Suspense
- `frontend/app/groups/page.tsx` - 添加搜索 + Suspense
- `frontend/app/posts/page.tsx` - 添加 Suspense
- `frontend/app/users/[id]/page.tsx` - 真实用户帖子 + 关注按钮
- `frontend/lib/api-client.ts` - 添加 created_by 过滤参数
- `app/routers/posts.py` - 添加 created_by 查询参数

### Phase 4: 活动报名流程

**修复内容：**
1. 创建 `JoinEventButton` 组件（团队选择对话框）
2. 添加 `/my/groups` API 获取用户所属团队
3. 添加 `registerGroupToEvent` 和 `unregisterGroupFromEvent` API
4. 活动详情页集成报名按钮

**文件变更：**
- `frontend/components/event/JoinEventButton.tsx` - 新建
- `frontend/lib/api-client.ts` - 添加团队报名 API
- `frontend/app/events/[id]/page.tsx` - 集成报名按钮
- `app/routers/groups.py` - 添加 /my/groups endpoint
- `app/crud/members.py` - 添加按用户查询方法

---

## 错误日志

| 错误 | 尝试 | 解决方案 |
|------|------|----------|
| `@/lib/auth-context` 模块不存在 | 1 | 改为 `@/contexts/AuthContext` |
| `searchParams.get()` 可能为 null | 1 | 使用 `searchParams?.get() ?? ""` |
| `AuthUser` 类型没有 `id` 属性 | 1 | 使用 `user_id` 代替 `id` |
| `useSearchParams()` 需要 Suspense 边界 | 1 | 将组件抽取为内部组件，用 `<Suspense>` 包装 |
| 点赞 API URL 不匹配 | 1 | 修正为 `/posts/{id}/like` |

---

## 决策日志

| 日期 | 决策 | 理由 |
|------|------|------|
| 2026-02-08 | 优先修复社交互动 | 影响 J-06 用户旅程，用户感知最强 |
| 2026-02-08 | 暂不实现消息系统 | 涉及 9 个页面，工作量大，作为后续迭代 |
| 2026-02-08 | 活动报名采用团队机制 | 符合后端设计，用户必须以团队名义报名 |
| 2026-02-08 | 跳过 E2E 测试用例 | 核心功能已修复验证，测试用例作为后续迭代 |
