# 阶段 7: 前端组件开发

> 组件优先策略：先实现 UI 组件，再组合成页面。

## 7.0 Figma 设计参考

> **原型验证原则**：功能优先，不追求像素级还原。

| 资源类型 | 文件位置 | 数量 |
|---------|---------|------|
| 页面设计 | `specs/design/figma/pages/*.md` | 104 |
| 组件库 | `specs/design/figma/components.md` | 54 |
| 图标库 | `specs/design/figma/icons.md` | 69 |

**页面设计索引：**

| 页面类型 | Figma 文件 | 前端路由 |
|---------|-----------|---------|
| 探索 | `pages/explore.md` | `/explore` |
| 内容/帖子 | `pages/content.md` | `/posts/*` |
| 团队 | `pages/team.md` | `/groups/*` |
| 用户 | `pages/profile.md` | `/users/*` |
| 设置 | `pages/settings.md` | `/settings` |
| 活动 | `pages/planet.md` | `/events/*` |

**Figma 使用原则：**
1. **功能优先**：确保 API 调用正常，数据流通顺畅
2. **布局参考**：页面整体布局参考 Figma，不追求像素级还原
3. **不做的事**：精确还原间距/颜色、完整实现所有 104 个设计、动效

## 7.1 shadcn 组件优先

开发任何 UI 组件前：

1. **检查 shadcn 是否有现成组件**
   ```bash
   # 使用 shadcn MCP 插件或查看 https://ui.shadcn.com/docs/components
   ```

2. **存在则直接安装**
   ```bash
   npx shadcn@latest add button card dialog
   ```

3. **不存在则创建自定义组件**
   - 遵循 shadcn 组件风格
   - 放置在 `frontend/components/ui/`

## 7.2 组件开发顺序

```
1. frontend/components/ui/        # 基础 UI 组件
   ├── button.tsx                 # (shadcn)
   ├── card.tsx                   # (shadcn)
   └── event-card.tsx             # (自定义)

2. frontend/components/           # 业务组件
   ├── header.tsx
   ├── sidebar.tsx
   └── event-list.tsx

3. frontend/app/**/page.tsx       # 页面组件
```

## 7.3 Mock 认证配置

> 默认使用 Mock 登录，仅当用户明确要求时才实现真实认证。

```typescript
// frontend/lib/auth.ts
export function getMockUserId(): string {
  return localStorage.getItem('mockUserId') || 'user_1';
}

// 在 API 请求中添加 header
const headers = {
  'Content-Type': 'application/json',
  'X-User-Id': getMockUserId(),
};
```

## 7.4 验证创建页面无 TODO 遗留 ⭐

```bash
# 检查创建/编辑页面是否有 TODO 遗留
grep -r "// TODO:" frontend/app/**/create/page.tsx && echo "❌ TODO!" || echo "✅ OK"
grep -r "// TODO:" frontend/app/**/edit/page.tsx && echo "❌ TODO!" || echo "✅ OK"

# 验证表单提交调用了 API
grep -A5 "handleSubmit" frontend/app/posts/create/page.tsx | grep -q "createPost"
```

## 7.5 增量测试

```bash
# TypeScript 编译验证
cd frontend && npx tsc --noEmit

# 启动开发服务器
npm run dev
```

## 7.6 Mock 数据替换为 API 调用

> 原型验证阶段：将页面中的 Mock 数据替换为真实 API 调用。

**标准模式：**

```typescript
"use client"

import { useState, useEffect } from "react"
import { getPost, getUser, type Post, type User } from "@/lib/api-client"
import { Loader2 } from "lucide-react"

export default function PostPage({ params }: { params: { id: string } }) {
  const id = Number(params.id)
  const [post, setPost] = useState<Post | null>(null)
  const [author, setAuthor] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchData() {
      setIsLoading(true)
      setError(null)
      try {
        const postData = await getPost(id)
        setPost(postData)
        if (postData.created_by) {
          const authorData = await getUser(postData.created_by)
          setAuthor(authorData)
        }
      } catch (e) {
        setError(e instanceof Error ? e.message : "Failed to load")
      } finally {
        setIsLoading(false)
      }
    }
    if (Number.isFinite(id)) fetchData()
  }, [id])

  if (isLoading) return <Loader2 className="animate-spin" />
  if (error || !post) return <div>{error || "Not found"}</div>
  return <PostContent post={post} author={author} />
}
```

**并行获取关联数据：**

```typescript
const commentsData = await getPostComments(postId)
const commentsWithUsers = await Promise.all(
  commentsData.items.map(async (comment) => {
    if (comment.created_by) {
      const user = await getUser(comment.created_by)
      return { ...comment, user }
    }
    return comment
  })
)
```

**替换检查清单：**
- [ ] 移除 `mockData` 常量
- [ ] 添加 `useState` 管理状态
- [ ] 添加 `useEffect` 获取数据
- [ ] 实现 Loading / Error / Empty 状态
- [ ] 验证 TypeScript 类型

## 下一步

完成前端开发后，进入 [阶段 8: E2E 测试](08-e2e-testing.md)。
