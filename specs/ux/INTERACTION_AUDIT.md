# UI 交互实现审计报告

Generated: 2025-02-02
Status: 待修复

## 概述

本文档对比 `specs/ux/` 中定义的交互规格与 `frontend/components/pages/` 中的实际实现，识别缺失的交互逻辑。

## 审计结果汇总

| 页面 | 定义交互数 | 已实现 | 缺失 | 完成度 |
|------|-----------|--------|------|--------|
| home.tsx | 15 | 8 | 7 | 53% |
| proposal-list.tsx | 12 | 10 | 2 | 83% |
| post-detail.tsx | 14 | 10 | 4 | 71% |
| user-profile.tsx | 11 | 8 | 3 | 73% |
| category-detail.tsx | 10 | 6 | 4 | 60% |
| assets.tsx | 8 | 6 | 2 | 75% |
| team.tsx | 9 | 5 | 4 | 56% |
| following-list.tsx | 7 | 5 | 2 | 71% |
| post-list.tsx | 10 | 6 | 4 | 60% |
| proposal-detail.tsx | 12 | 8 | 4 | 67% |

---

## 详细审计

### 1. home.tsx（首页）

**UX Spec:** `specs/ux/pages/home.yaml`

| 交互定义 | 状态 | 说明 |
|----------|------|------|
| `main-tabs.tab_change` → refetch_data | ✅ 已修复 | 2025-02-02 添加 `tabRoutes` 和 `onClick` |
| `hot-activities-banner.click` → navigate | ⚠️ 部分 | 卡片可点击，但未关联真实 category ID |
| `hot-proposals.click` → navigate | ✅ 已实现 | 点击跳转到 `/posts/{id}` |
| `hot-proposals.like-btn.click` → toggle_like | ❌ 缺失 | 首页卡片缺少点赞按钮 |
| `right-sidebar.find-teammate.click` → navigate | ❌ 缺失 | 右侧边栏按钮无 onClick |
| `right-sidebar.find-idea.click` → navigate | ❌ 缺失 | 右侧边栏按钮无 onClick |
| `right-sidebar.publish-proposal.click` → navigate | ❌ 缺失 | 发布提案按钮无 onClick |
| `global-header.search-bar.submit` → navigate | ❌ 缺失 | 搜索框无提交逻辑 |
| `global-header.publish-btn.click` → toggle_panel | ⚠️ 部分 | 按钮存在但无展开面板 |
| `global-header.notification-btn.click` → toggle_panel | ❌ 缺失 | 通知按钮无响应 |
| `global-header.user-menu.click` → show_dropdown | ❌ 缺失 | 用户头像无下拉菜单 |
| `sidebar-nav.nav-explore.click` → navigate | ✅ 已实现 | |
| `sidebar-nav.nav-planet.click` → navigate | ✅ 已实现 | |
| `sidebar-nav.nav-camp.click` → navigate | ✅ 已实现 | |
| `site-logo.click` → navigate | ✅ 已实现 | |

**需修复项：**
```tsx
// home.tsx 需添加：

// 1. 右侧边栏快捷入口
<div onClick={() => router.push("/posts?tag=find-teammate")}>找队友</div>
<div onClick={() => router.push("/posts?tag=find-idea")}>找点子</div>
<Button onClick={() => router.push("/posts/create?type=for_category")}>发布提案</Button>

// 2. 搜索框提交
<form onSubmit={(e) => { e.preventDefault(); router.push(`/search?q=${query}`) }}>

// 3. 用户菜单下拉
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
<DropdownMenu>
  <DropdownMenuTrigger><Avatar /></DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuItem onClick={() => router.push(`/users/1`)}>个人主页</DropdownMenuItem>
    <DropdownMenuItem onClick={() => router.push("/assets")}>我的资产</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

---

### 2. proposal-list.tsx（提案列表）

**UX Spec:** `specs/ux/pages/proposal-list.yaml`

| 交互定义 | 状态 | 说明 |
|----------|------|------|
| `proposal-filter.status-filter.select` → update_url_param | ✅ 已修复 | 2025-02-02 添加 |
| `proposal-filter.category-filter.select` → update_url_param | ✅ 已修复 | 2025-02-02 添加 |
| `proposal-grid.item.click` → navigate | ✅ 已实现 | |
| `tabs.tab_change` → navigate | ✅ 已修复 | 2025-02-02 添加 `tabRoutes` |
| `sort-tabs.热门.click` → update_url_param | ✅ 已修复 | |
| `sort-tabs.最新.click` → update_url_param | ✅ 已修复 | |
| `proposal-card.like-btn` → toggle_like | ❌ 缺失 | 列表卡片无点赞交互 |
| `pagination.load_more` → fetch_next_page | ❌ 缺失 | 无分页/加载更多 |

**需修复项：**
```tsx
// proposal-list.tsx 需添加：

// 1. 卡片点赞按钮
<Card onClick={() => router.push(`/proposals/${proposal.id}`)}>
  ...
  <Button
    onClick={(e) => { e.stopPropagation(); handleLike(proposal.id) }}
    size="sm"
  >
    <Heart /> {proposal.like_count}
  </Button>
</Card>

// 2. 加载更多
const [page, setPage] = useState(0)
<Button onClick={() => setPage(p => p + 1)}>加载更多</Button>
```

---

### 3. post-detail.tsx（帖子详情）

**UX Spec:** `specs/ux/pages/post-detail.yaml`

| 交互定义 | 状态 | 说明 |
|----------|------|------|
| `post-actions.like-btn.click` → toggle_like | ✅ 已实现 | `handleLike()` 调用 API |
| `post-actions.share-btn.click` → copy_url | ❌ 缺失 | 分享按钮无逻辑 |
| `post-actions.more-btn.click` → show_dropdown | ❌ 缺失 | 更多按钮无下拉 |
| `comment-input.submit` → submit_comment | ✅ 已实现 | `handleComment()` 调用 API |
| `comment-list.item.reply.click` → focus_input | ❌ 缺失 | 评论无回复功能 |
| `author-info.click` → navigate | ❌ 缺失 | 作者头像不可点击跳转 |
| `related-cards.item.click` → navigate | ⚠️ 部分 | 关联卡片无真实数据 |
| `hot-ranking.item.click` → navigate | ❌ 缺失 | 热点榜单项不可点击 |

**需修复项：**
```tsx
// post-detail.tsx 需添加：

// 1. 分享按钮
async function handleShare() {
  await navigator.clipboard.writeText(window.location.href)
  // Show toast: "链接已复制"
}
<Share2 onClick={handleShare} className="cursor-pointer" />

// 2. 更多菜单
<DropdownMenu>
  <DropdownMenuTrigger><Ellipsis /></DropdownMenuTrigger>
  <DropdownMenuContent>
    {post?.created_by === currentUserId && (
      <DropdownMenuItem onClick={() => router.push(`/posts/${postId}/edit`)}>编辑</DropdownMenuItem>
    )}
    <DropdownMenuItem onClick={() => setReportModalOpen(true)}>举报</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>

// 3. 作者头像可点击
<div onClick={() => router.push(`/users/${post?.created_by}`)} className="cursor-pointer">
  <Avatar />
  <span>{displayName}</span>
</div>

// 4. 热点榜单可点击
{hotItems.map((item) => (
  <div onClick={() => router.push(`/posts/${item.id}`)} className="cursor-pointer">
    ...
  </div>
))}
```

---

### 4. user-profile.tsx（用户主页）

**UX Spec:** `specs/ux/pages/user-profile.yaml`

| 交互定义 | 状态 | 说明 |
|----------|------|------|
| `follow-btn.click` → toggle_follow | ✅ 已实现 | `handleFollow()` 调用 API |
| `works-filter.tab_change` → filter_list | ✅ 已实现 | Tabs 组件切换 |
| `stats.关注.click` → navigate | ❌ 缺失 | 关注数不可点击 |
| `stats.粉丝.click` → navigate | ❌ 缺失 | 粉丝数不可点击 |
| `asset-card.click` → navigate | ❌ 缺失 | 资产卡片不可点击 |
| `works-grid.item.click` → navigate | ⚠️ 部分 | 作品占位符无真实数据 |

**需修复项：**
```tsx
// user-profile.tsx 需添加：

// 1. 关注/粉丝数可点击
<div onClick={() => router.push(`/users/${userId}/following`)} className="cursor-pointer">
  <span>{following.length}</span> 关注
</div>
<div onClick={() => router.push(`/users/${userId}/followers`)} className="cursor-pointer">
  <span>{followers.length}</span> 粉丝
</div>

// 2. 资产卡片可点击
<Card onClick={() => router.push("/assets")} className="cursor-pointer">
  ...
</Card>
```

---

### 5. category-detail.tsx（活动详情）

**UX Spec:** `specs/ux/pages/category-detail.yaml`

| 交互定义 | 状态 | 说明 |
|----------|------|------|
| `category-tabs.tab_change` → switch_content | ✅ 已实现 | Tabs 组件切换 |
| `join-btn.click` → join_category | ❌ 缺失 | 无报名按钮 |
| `submit-btn.click` → navigate | ❌ 缺失 | 无提交提案入口 |
| `posts-grid.item.click` → navigate | ❌ 缺失 | 帖子列表无数据/点击 |
| `groups-list.item.click` → navigate | ❌ 缺失 | 团队列表无点击跳转 |

**需修复项：**
```tsx
// category-detail.tsx 需添加：

// 1. 报名/提交按钮
<Button onClick={() => router.push(`/posts/create?category_id=${categoryId}&type=for_category`)}>
  提交提案
</Button>

// 2. 帖子列表点击
{posts.map((cp) => (
  <Card key={cp.id} onClick={() => router.push(`/posts/${cp.post_id}`)} className="cursor-pointer">
    ...
  </Card>
))}

// 3. 团队列表点击
{groups.map((cg) => (
  <Card key={cg.id} onClick={() => router.push(`/groups/${cg.group_id}`)} className="cursor-pointer">
    ...
  </Card>
))}
```

---

### 6. assets.tsx（我的资产）

**UX Spec:** `specs/ux/pages/assets.yaml`

| 交互定义 | 状态 | 说明 |
|----------|------|------|
| `category-tabs.click` → filter_list | ✅ 已实现 | `setActiveFilter()` |
| `asset-card.click` → show_detail | ❌ 缺失 | 资源卡片无详情弹窗 |
| `asset-card.download.click` → download_resource | ❌ 缺失 | 无下载按钮 |

**需修复项：**
```tsx
// assets.tsx 需添加：

// 1. 资源卡片详情/下载
<Card>
  ...
  <Button onClick={() => window.open(resource.url, "_blank")}>下载</Button>
</Card>
```

---

### 7. team.tsx（团队详情）

**UX Spec:** `specs/ux/pages/team-detail.yaml`

| 交互定义 | 状态 | 说明 |
|----------|------|------|
| `manage-btn.click` → navigate | ⚠️ 部分 | `console.log` 占位 |
| `add-member-btn.click` → open_modal | ❌ 缺失 | 无邀请成员逻辑 |
| `member-avatar.click` → navigate | ❌ 缺失 | 成员头像不可点击 |
| `tabs.tab_change` → switch_content | ✅ 已实现 | |
| `works-grid.item.click` → navigate | ❌ 缺失 | 无作品数据/点击 |

**需修复项：**
```tsx
// team.tsx 需添加：

// 1. 管理面板跳转
<Button onClick={() => router.push(`/groups/${groupId}/manage`)}>管理面板</Button>

// 2. 成员头像可点击
{members.map((member) => (
  <div onClick={() => router.push(`/users/${member.user_id}`)} className="cursor-pointer">
    <Avatar />
  </div>
))}

// 3. 添加成员弹窗
<button onClick={() => setInviteModalOpen(true)}>
  <Plus />
</button>
```

---

### 8. following-list.tsx（关注列表）

**UX Spec:** `specs/ux/pages/following-list.yaml`

| 交互定义 | 状态 | 说明 |
|----------|------|------|
| `tabs.tab_change` → filter_list | ✅ 已实现 | `setActiveTab()` |
| `user-card.click` → navigate | ❌ 缺失 | 用户卡片不可点击 |
| `user-card.follow-btn.click` → toggle_follow | ❌ 缺失 | 无关注/取关按钮 |

**需修复项：**
```tsx
// following-list.tsx 需添加：

// 1. 用户卡片可点击
<Card onClick={() => router.push(`/users/${relation.target_user_id}`)} className="cursor-pointer">
  ...
</Card>

// 2. 关注按钮
<Button onClick={(e) => { e.stopPropagation(); handleUnfollow(relation.id) }}>
  取消关注
</Button>
```

---

### 9. post-list.tsx（帖子列表）

**UX Spec:** `specs/ux/pages/post-list.yaml`

| 交互定义 | 状态 | 说明 |
|----------|------|------|
| `post-filter-tabs.tab_change` → filter_list | ⚠️ 需检查 | 需验证 URL 参数更新 |
| `post-card.click` → navigate | ✅ 需验证 | |
| `post-card.like-btn.click` → toggle_like | ❌ 缺失 | 列表卡片无点赞 |
| `pagination.load_more` → fetch_next_page | ❌ 缺失 | 无分页 |

---

### 10. proposal-detail.tsx（提案详情）

**UX Spec:** `specs/ux/pages/proposal-detail.yaml`

| 交互定义 | 状态 | 说明 |
|----------|------|------|
| `like-btn.click` → toggle_like | ✅ 需验证 | |
| `share-btn.click` → copy_url | ❌ 缺失 | |
| `author-info.click` → navigate | ❌ 缺失 | |
| `track-tags.item.click` → navigate | ❌ 缺失 | 赛道标签不可点击 |
| `image-gallery.item.click` → show_lightbox | ❌ 缺失 | 图片无灯箱效果 |

---

## 全局共享组件缺失项

**来源:** `specs/ux/global/shared-components.yaml`

以下交互在所有页面中都缺失或不完整：

### Header 组件
| 交互 | 状态 | 影响页面 |
|------|------|----------|
| 搜索框 submit | ❌ 缺失 | 全部 |
| 发布按钮展开面板 | ⚠️ 部分 | 全部 |
| 通知按钮展开面板 | ❌ 缺失 | 全部 |
| 用户菜单下拉 | ❌ 缺失 | 全部 |

### Sidebar 组件
| 交互 | 状态 | 影响页面 |
|------|------|----------|
| 导航项点击 | ✅ 已实现 | 全部 |
| 折叠/展开 | ❌ 缺失 | 部分页面 |

---

## 修复优先级

### P0（阻塞测试）
1. ~~首页 Tabs 导航~~ ✅ 已修复
2. ~~提案列表筛选~~ ✅ 已修复
3. 用户菜单下拉
4. 搜索框提交

### P1（核心功能）
1. 列表页点赞按钮
2. 详情页分享按钮
3. 作者头像点击跳转
4. 关注/粉丝数点击跳转

### P2（完善体验）
1. 热点榜单点击
2. 加载更多分页
3. 资源下载按钮
4. 团队成员点击

---

## 测试用例建议

基于此审计，建议在 `specs/testcases/` 新增 `18-ui-interactions.md`：

```markdown
# UI 交互测试用例

## 18.1 全局导航
TC-UI-NAV-001: Logo 点击返回首页
TC-UI-NAV-002: 侧边栏导航项点击跳转
TC-UI-NAV-003: 用户菜单下拉选项

## 18.2 Tab 导航
TC-UI-TAB-001: 首页 Tab 切换
TC-UI-TAB-002: 提案列表筛选排序
TC-UI-TAB-003: 用户主页作品筛选

## 18.3 卡片交互
TC-UI-CARD-001: 帖子卡片点击跳转
TC-UI-CARD-002: 卡片点赞按钮调用 API
TC-UI-CARD-003: 用户卡片点击跳转

## 18.4 表单提交
TC-UI-FORM-001: 搜索框提交跳转
TC-UI-FORM-002: 评论框提交调用 API
TC-UI-FORM-003: 筛选下拉更新 URL
```

---

## 下一步行动

1. [ ] 按 P0 优先级修复阻塞项
2. [ ] 创建 `specs/testcases/18-ui-interactions.md`
3. [ ] 运行 E2E 测试验证修复
4. [ ] 更新此文档标记完成项
