# Findings: 前端问题诊断

> 更新时间: 2026-02-08
> 来源: 双分支工作流验证 + 详细代码检查

## 问题清单

### 高优先级问题 (需立即修复)

| # | 问题 | 文件 | 行号 | 说明 |
|---|------|------|------|------|
| 1 | 点赞状态未持久化 | `frontend/app/posts/[id]/page.tsx` | 52-53 | `liked` 初始化为 `false`，未从 API 获取 |
| 2 | 活动报名按钮未连接 | `frontend/app/events/[id]/page.tsx` | 250-253 | 无 onClick 处理器 |
| 3 | 活动搜索未实现 | `frontend/app/events/page.tsx` | 64-69 | 搜索输入无状态绑定 |
| 4 | 团队搜索未实现 | `frontend/app/groups/page.tsx` | 98-101 | 同上 |
| 5 | 用户帖子标签未实现 | `frontend/app/users/[id]/page.tsx` | 205-209 | 显示占位符而非真实帖子 |
| 6 | 关注按钮是 Mock | `frontend/app/users/[id]/page.tsx` | 55-60 | 未调用 API，仅本地状态 |
| 7 | API 缺少活动报名端点 | `frontend/lib/api-client.ts` | - | 无 joinEvent/leaveEvent 函数 |

### 中优先级问题

| # | 问题 | 文件 | 说明 |
|---|------|------|------|
| 8 | 无独立交互组件 | `frontend/components/` | LikeButton/CommentSection 内联在页面中 |
| 9 | 团队成员数缺失 | `frontend/app/events/[id]/page.tsx` | GroupCard 未传递 member_count |

## 问题详情

### 1. 点赞状态未持久化

**当前代码 (L52-53):**
```typescript
const [liked, setLiked] = useState(false)  // 始终初始化为 false
const [likeCount, setLikeCount] = useState(0)
```

**问题**: 用户刷新页面后，即使之前已点赞，按钮仍显示未点赞状态。

**修复方案**: 在 useEffect 中调用 API 检查点赞状态：
```typescript
useEffect(() => {
  async function checkLikeStatus() {
    const status = await checkPostLiked(id)
    setLiked(status.liked)
  }
  checkLikeStatus()
}, [id])
```

### 2. 活动报名按钮未连接

**当前代码 (L250-253):**
```typescript
<Button className="...">
  <UserPlus className="h-4 w-4 mr-2" />
  Join Event
</Button>
```

**问题**: 按钮无任何交互，点击无反应。

**修复方案**:
1. 添加 API 函数 `joinEvent(eventId)`
2. 添加状态 `const [isParticipant, setIsParticipant] = useState(false)`
3. 添加 `onClick={handleJoinEvent}` 处理器

### 3 & 4. 搜索功能未实现

**参考实现 (posts/page.tsx L187-199):**
```typescript
<Input
  placeholder="搜索帖子..."
  value={searchQuery}
  onChange={(e) => setSearchQuery(e.target.value)}
  onKeyDown={(e) => {
    if (e.key !== "Enter") return
    updateParams({ q: searchQuery.trim() || null })
  }}
/>
```

**修复**: 将此模式复制到 events/page.tsx 和 groups/page.tsx

### 5. 用户帖子标签未实现

**当前代码 (L205-209):**
```typescript
<TabsContent value="posts">
  <div className="text-center py-16">
    <p className="text-nf-muted">用户帖子将在这里展示</p>
  </div>
</TabsContent>
```

**修复**: 获取用户的帖子并显示：
```typescript
const [userPosts, setUserPosts] = useState<Post[]>([])
// 在 useEffect 中
const posts = await getPosts(0, 100, { created_by: id })
setUserPosts(posts.items)
```

### 6. 关注按钮是 Mock

**当前代码 (L55-60):**
```typescript
const handleFollow = async () => {
  // For demo purposes, we'll just toggle the state
  setIsFollowing(!isFollowing)
  setFollowerCount((c) => (isFollowing ? c - 1 : c + 1))
}
```

**问题**: 注释明确说 "For demo purposes"，未调用后端 API。

**修复**: 使用现有的 `UserFollowButton` 组件替代内联实现。

### 7. API 缺少活动报名端点

**需添加到 api-client.ts:**
```typescript
export async function joinEvent(eventId: number) {
  return apiFetch(`/events/${eventId}/join`, { method: 'POST' })
}

export async function leaveEvent(eventId: number) {
  return apiFetch(`/events/${eventId}/join`, { method: 'DELETE' })
}

export async function checkEventParticipation(eventId: number): Promise<boolean> {
  const res = await apiFetch(`/events/${eventId}/participation`)
  return res.is_participant
}
```

## 根因分析

| 问题类型 | 追溯阶段 | 根因 |
|---------|---------|------|
| 点赞状态 | Phase 7 (组件开发) | 状态初始化未考虑持久化 |
| 活动报名 | Phase 6 (API 客户端) | 缺少 API 端点绑定 |
| 搜索功能 | Phase 7 (组件开发) | 部分实现，未复制到所有页面 |
| 用户帖子 | Phase 7 (组件开发) | 占位符未替换为真实实现 |
| 关注按钮 | Phase 7 (组件开发) | 未使用已有的组件 |

## 修复优先级

1. **搜索功能** - 简单复制粘贴，快速见效
2. **关注按钮** - 使用现有组件，低风险
3. **点赞状态** - 添加 API 调用
4. **用户帖子** - 添加数据获取逻辑
5. **活动报名** - 需要后端 API 确认
