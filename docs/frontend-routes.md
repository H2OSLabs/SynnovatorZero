# 前端路由映射表

> **维护说明**：每次添加新页面时，同步更新本文档。
>
> **验证方法**：`find frontend/app -name "page.tsx" | sort`

## 路由列表

| 路由 | 页面文件 | 描述 |
|------|---------|------|
| `/` | `app/page.tsx` | 首页 |
| `/explore` | `app/explore/page.tsx` | 探索页 |
| `/login` | `app/login/page.tsx` | 登录 |
| `/register` | `app/register/page.tsx` | 注册 |
| `/settings` | `app/settings/page.tsx` | 用户设置 |

### 帖子 (Posts)

| 路由 | 页面文件 | 描述 |
|------|---------|------|
| `/posts` | `app/posts/page.tsx` | 帖子列表 |
| `/posts/create` | `app/posts/create/page.tsx` | 创建帖子 |
| `/posts/[id]` | `app/posts/[id]/page.tsx` | 帖子详情 |
| `/posts/[id]/edit` | `app/posts/[id]/edit/page.tsx` | 编辑帖子 |
| `/my/posts` | `app/my/posts/page.tsx` | 我的帖子 |

**`/posts` 查询参数**

| 参数 | 示例 | 说明 |
|------|------|------|
| `q` | `/posts?q=llm` | 关键词搜索（标题/内容/标签） |
| `type` | `/posts?type=proposal` | 类型筛选（`proposal`/`team`/`general`） |
| `status` | `/posts?status=published` | 状态筛选（`draft`/`pending_review`/`published`/`rejected`） |
| `tags` | `/posts?tags=AI,Web3` | 标签筛选（逗号分隔，匹配任一标签） |

### 活动 (Events)

| 路由 | 页面文件 | 描述 |
|------|---------|------|
| `/events` | `app/events/page.tsx` | 活动列表 |
| `/events/create` | `app/events/create/page.tsx` | 创建活动 |
| `/events/[id]` | `app/events/[id]/page.tsx` | 活动详情 |

### 团队 (Groups)

| 路由 | 页面文件 | 描述 |
|------|---------|------|
| `/groups` | `app/groups/page.tsx` | 团队列表 |
| `/groups/create` | `app/groups/create/page.tsx` | 创建团队 |
| `/groups/[id]` | `app/groups/[id]/page.tsx` | 团队详情 |

### 用户 (Users)

| 路由 | 页面文件 | 描述 |
|------|---------|------|
| `/users/[id]` | `app/users/[id]/page.tsx` | 用户主页 |

### 管理 (Manage)

| 路由 | 页面文件 | 描述 |
|------|---------|------|
| `/manage` | `app/manage/page.tsx` | 管理首页 |
| `/manage/events` | `app/manage/events/page.tsx` | 活动管理 |

---

## 不存在的路由（常见错误）

以下路由**不存在**，如果在代码中发现这些路由的引用，需要修正：

| ❌ 错误路由 | ✅ 正确路由 | 说明 |
|------------|-----------|------|
| `/my/groups` | `/groups` | 不存在 `/my/` 前缀 |
| `/my/events` | `/events` | 不存在 `/my/` 前缀 |
| `/profile` | `/users/[id]` | 使用 `/users/{userId}` |
| `/profile/[id]` | `/users/[id]` | 使用 `/users/` 不是 `/profile/` |
| `/proposals` | `/posts` | 提案是帖子的一种类型 |
| `/proposals/[id]` | `/posts/[id]` | 使用 `/posts/` |
| `/categories` | `/events` | category 已重命名为 event |
| `/categories/[id]` | `/events/[id]` | 使用 `/events/` |

---

## 路由验证脚本

```bash
# 检查是否有不存在的路由引用
grep -rn "href=\"/my/" frontend/ --include="*.tsx"
grep -rn "href=\"/profile" frontend/ --include="*.tsx"
grep -rn "href=\"/proposals" frontend/ --include="*.tsx"
grep -rn "href=\"/categories" frontend/ --include="*.tsx"

# 如有输出，说明存在错误路由引用，需要修正
```

---

## 动态路由参数

| 路由模式 | 参数名 | 类型 | 示例 |
|---------|-------|------|------|
| `/posts/[id]` | `id` | number | `/posts/123` |
| `/events/[id]` | `id` | number | `/events/456` |
| `/groups/[id]` | `id` | number | `/groups/789` |
| `/users/[id]` | `id` | number | `/users/1` |

**参数安全处理**：

```typescript
// 路由参数可能为 undefined，需要安全处理
const id = params?.id ? Number(params.id) : NaN
if (!Number.isFinite(id)) {
  return <div>无效的 ID</div>
}
```
