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

---

# Findings: 工作流遗漏根因分析 (2026-02-08)

> **分析目标**: 为什么 `/my/*` 系列页面在开发工作流中被遗漏

---

## 1. 发现总结

### 1.1 根因链条

```
用户旅程文档有描述 → 测试用例有定义 → 工作流阶段错误处理 → 页面未实现
       ✅                 ✅                  ❌
```

**根因**：工作流阶段 7 (07-frontend-components.md) 将 `/my/*` 路由**错误地标记为"不存在的错误路由"**，而非"需要实现的路由"。

### 1.2 证据

**用户旅程有描述** (✅):
- `docs/user-journeys/13-planet-camp.md` 第 17-19 行：
  - 展示个人提案 → `READ post (created_by: current_user)`
  - 展示团队提案 → `READ post (group_id IN user_groups)`
  - 展示参加的团队 → `READ group (user_id: current_user)`

**测试用例有定义** (✅):
- `specs/testcases/29-planet-camp.md`:
  - TC-CAMP-010: 查看个人提案列表 → "我的提案"板块
  - TC-CAMP-011: 查看团队提案列表 → "团队提案"板块
  - TC-CAMP-012: 查看参加的团队列表 → "我的团队"板块

**工作流阶段错误处理** (❌):
- `docs/development-workflow/07-frontend-components.md` 第 254-261 行：
  ```markdown
  **常见错误路由**：
  | ❌ 错误 | ✅ 正确 | 说明 |
  | `/my/posts` | `/posts` | 不存在 `/my/` 前缀 |
  | `/my/groups` | `/groups` | 不存在 `/my/` 前缀 |
  ```

**问题**：工作流文档把"尚未实现的路由"误认为"错误路由"，导致：
1. 开发者看到这个表格，认为 `/my/*` 不应该存在
2. 侧边栏导航保留了这些链接（因为 UI 设计需要）
3. 形成了"导航存在但页面不存在"的不一致状态

---

## 2. 深层原因分析

### 2.1 工作流设计缺陷

| 缺陷 | 影响 |
|------|------|
| **阶段 7 没有"页面清单验证"步骤** | 不会检查导航中引用的路由是否都已实现 |
| **阶段 4/5 没有"筛选视图"识别** | UI 设计阶段没有明确识别"我的XX"这类筛选视图需求 |
| **测试用例与页面实现的映射不明确** | TC-CAMP-010~012 定义了功能，但没有对应到具体页面路由 |

### 2.2 Skill 覆盖缺失

| Skill | 应该做但没做 |
|-------|-------------|
| **ui-spec-generator** | 应该从 Sidebar 导航提取所有路由，并验证每个路由都有对应页面 |
| **openapi-to-components** | 应该为"我的XX"这类筛选视图生成对应页面 |
| **tests-kit Guard** | 应该检查测试用例中的 UI 描述是否都有对应实现 |

### 2.3 营地页面实现与测试用例对比

| 测试用例 | 当前实现 | 差距 |
|---------|---------|------|
| TC-CAMP-010: 我的提案 | 显示所有提案（无 created_by 筛选） | ❌ 应筛选当前用户 |
| TC-CAMP-011: 团队提案 | 未实现 | ❌ 需要新板块 |
| TC-CAMP-012: 我的团队 | 未实现 | ❌ 需要新板块 |

---

## 3. 改进建议

### 3.1 工作流改进：新增阶段 7.9 路由完整性验证

```markdown
## 7.9 路由完整性验证 ⭐

> 确保所有导航链接都指向实际存在的页面。

**验证脚本**：
\`\`\`bash
# 1. 提取所有导航中的 href
grep -rh 'href="/' frontend/components/layout/*.tsx | \
  grep -oE 'href="[^"]*"' | \
  sed 's/href="//;s/"$//' | \
  sort -u > /tmp/nav-routes.txt

# 2. 提取所有存在的页面路由
find frontend/app -name "page.tsx" | \
  sed 's|frontend/app||;s|/page.tsx||;s|\[|\{|g;s|\]|\}|g' | \
  sort -u > /tmp/existing-routes.txt

# 3. 对比差异
echo "=== 导航中引用但不存在的路由 ==="
comm -23 /tmp/nav-routes.txt /tmp/existing-routes.txt
\`\`\`
```

### 3.2 文档修正

修改 `07-frontend-components.md` 第 254-261 行：

**修改前**：
```markdown
| ❌ 错误 | ✅ 正确 | 说明 |
| `/my/posts` | `/posts` | 不存在 `/my/` 前缀 |
```

**修改后**：
```markdown
| 路由 | 状态 | 说明 |
| `/my/posts` | 待实现 | 当前用户的帖子筛选视图 |
| `/my/groups` | 待实现 | 当前用户的团队筛选视图 |
```

---

## 4. 实现优先级

| 优先级 | 页面 | 依据 |
|--------|------|------|
| P0 | 营地页面增强 | TC-CAMP-010~012 已定义，当前实现不完整 |
| P1 | `/my/posts` | 复用 `/posts` 逻辑 + created_by 筛选 |
| P1 | `/my/groups` | 复用 `/groups` 逻辑 + member 筛选 |
| P1 | `/my/events` | 复用 `/events` 逻辑 + 参与活动筛选 |
| P2 | `/my/favorites` | 需要 interaction API |
| P2 | `/my/following` | 需要 user:user 关系 API |

---

## 5. 结论

### 根因总结

1. **直接原因**：工作流文档错误地将待实现路由标记为"错误路由"
2. **间接原因**：缺少"路由完整性验证"步骤
3. **深层原因**：测试用例 → 页面实现的映射链条不完整

### 预防措施

1. 添加阶段 7.9 路由完整性验证脚本
2. 在 UI 设计阶段明确识别"筛选视图"需求
3. 修正工作流文档中的错误标记
4. 增强 tests-kit 的 UI 覆盖检查

---

# Findings: 收藏功能缺失根因分析 (2026-02-08)

> **分析目标**: 为什么"查看我的收藏列表"功能缺失

---

## 1. 根因定位

### 1.1 文档链追溯

| 阶段 | 文档 | 是否覆盖 | 证据 |
|------|------|----------|------|
| **用户旅程** | `06-social-interaction.md` | ❌ **缺失** | 只有"点赞/取消点赞/查看点赞数"，无"查看点赞列表" |
| **测试用例** | `25-social-interaction.md` | ❌ **缺失** | 只有点赞操作测试，无列表查询测试 |
| **API 设计** | OpenAPI spec | ❌ **缺失** | 无 `/users/{id}/likes` 端点 |
| **前端实现** | `/my/favorites` | ❌ **占位符** | 页面存在但无功能 |

### 1.2 对比分析：点赞 vs 关注

**关注功能（完整）**:
```markdown
# 06-social-interaction.md 第 44-45 行
| 取消关注 | 取消对内容的关注 | DELETE interaction（type: follow） |
| 查看关注列表 | 查看自己关注的所有内容 | READ interaction（type: follow, created_by） |
                ^^^^^^^^^^^^^^^^
```

**点赞功能（不完整）**:
```markdown
# 06-social-interaction.md 第 11-13 行
| 点赞帖子 | 对喜欢的帖子点赞 | CREATE interaction |
| 取消点赞 | 取消之前的点赞 | DELETE interaction |
| 查看点赞数 | 查看帖子的点赞统计 | READ post（like_count） |
# ❌ 缺少: 查看点赞列表 | 查看自己点赞的所有内容 | READ interaction（type: like, created_by）
```

---

## 2. 根因结论

**根因在阶段 0.5（领域建模/用户旅程）**，不是实现阶段的问题。

| 层级 | 问题 |
|------|------|
| **L1: 用户旅程** | 6.1 点赞章节缺少"查看点赞列表"用户旅程 |
| **L2: 测试用例** | 因 L1 缺失，未生成对应测试用例 |
| **L3: API 设计** | 因 L2 缺失，OpenAPI spec 未定义端点 |
| **L4: 实现** | 因 L3 缺失，后端无 API，前端无数据来源 |

---

## 3. 与 `/my/*` 页面问题对比

| 问题 | 根因阶段 | 根因类型 |
|------|----------|----------|
| `/my/posts` 等缺失 | 阶段 7（前端组件开发） | 工作流文档错误标记 |
| 收藏列表功能缺失 | **阶段 0.5（用户旅程）** | **需求文档遗漏** |

**关键区别**：
- `/my/*` 页面：用户旅程有描述，但工作流阶段处理错误
- 收藏列表：**用户旅程本身就没有描述这个需求**

---

## 4. 改进建议

### 4.1 补充用户旅程文档

在 `docs/user-journeys/06-social-interaction.md` 第 13 行后添加：

```markdown
| 查看点赞列表 | 查看自己点赞的所有内容 | `READ interaction`（type: like, created_by: current_user） |
```

### 4.2 补充测试用例

在 `specs/testcases/25-social-interaction.md` 添加：

```markdown
**TC-SOCIAL-006：查看点赞列表**
用户查看自己点赞的所有帖子，系统返回按时间倒序的帖子列表。

**TC-SOCIAL-007：点赞列表分页**
用户点赞超过 100 个帖子时，系统支持分页查询。
```

### 4.3 Skill 改进：domain-modeler

在 `domain-modeler` skill 中添加**对称性检查**：

```yaml
checks:
  - type: symmetry_check
    description: "对于 CREATE/DELETE 操作，检查是否有对应的 LIST 操作"
    example: |
      如果存在:
        - CREATE interaction（type: like）
        - DELETE interaction（type: like）
      则应该存在:
        - READ interaction（type: like, created_by: current_user）→ 查看我的点赞列表
```

---

## 5. 总结

| 问题类型 | 根因阶段 | 修复方式 |
|----------|----------|----------|
| `/my/*` 页面缺失 | 阶段 7 工作流 | 修正文档 + 添加验证步骤 |
| 收藏列表功能缺失 | **阶段 0.5 用户旅程** | **补充需求文档 + 添加对称性检查** |

**核心教训**：需求文档的完整性直接影响后续所有阶段。domain-modeler 应增加"操作对称性检查"，确保 CREATE/DELETE 操作都有对应的 LIST 操作。
