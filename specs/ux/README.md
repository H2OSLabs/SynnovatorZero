# UX Interaction Specifications

Generated: 2025-01-30
Version: 1.0

## Summary

| Category | Count | Status |
|----------|-------|--------|
| Global | 1 | ✅ Complete |
| Components | 12 | ✅ Complete |
| Pages | 10 | ✅ Complete |
| Flows | 6 | ✅ Complete |
| Forms | 2 | ✅ Complete |
| State | 1 | ✅ Complete |

## Components

| Category | Components | Files |
|----------|------------|-------|
| Navigation | header, sidebar, tabs | [components/navigation/](components/navigation/) |
| Content | post-card, proposal-card, comment-item, user-card | [components/content/](components/content/) |
| Form | text-input, tag-input, markdown-editor | [components/form/](components/form/) |
| Feedback | toast, modal, loading | [components/feedback/](components/feedback/) |
| Action | like-button, follow-button, share-button | [components/action/](components/action/) |

## Pages

| Page | Route | File |
|------|-------|------|
| Home | `/` | [pages/home.yaml](pages/home.yaml) |
| Category Detail | `/categories/{id}` | [pages/category-detail.yaml](pages/category-detail.yaml) |
| User Profile | `/users/{id}` | [pages/user-profile.yaml](pages/user-profile.yaml) |
| Following List | `/users/{id}/following` | [pages/following-list.yaml](pages/following-list.yaml) |
| Team Detail | `/groups/{id}` | [pages/team-detail.yaml](pages/team-detail.yaml) |
| Post List | `/posts` | [pages/post-list.yaml](pages/post-list.yaml) |
| Post Detail | `/posts/{id}` | [pages/post-detail.yaml](pages/post-detail.yaml) |
| Proposal List | `/proposals` | [pages/proposal-list.yaml](pages/proposal-list.yaml) |
| Proposal Detail | `/proposals/{id}` | [pages/proposal-detail.yaml](pages/proposal-detail.yaml) |
| Assets | `/assets` | [pages/assets.yaml](pages/assets.yaml) |

## User Flows

### Content Flows
- [Create Post](flows/content/create-post.yaml) — 发布新帖子
- [Like Content](flows/content/like-content.yaml) — 点赞内容

### Team Flows
- [Join Team](flows/team/join-team.yaml) — 加入团队
- [Create Team](flows/team/create-team.yaml) — 创建团队

### Social Flows
- [Follow User](flows/social/follow-user.yaml) — 关注用户
- [Comment](flows/social/comment.yaml) — 发表评论

## Forms

- [Post Create Form](forms/post-create-form.yaml) — 创建帖子表单
- [Comment Form](forms/comment-form.yaml) — 评论表单

## State Management

- [State Management](state/state-management.yaml) — 全局状态与错误处理

## API Endpoints Reference

Based on `frontend/lib/api-client.ts`:

| Entity | Endpoints |
|--------|-----------|
| Users | `listUsers`, `getUser`, `createUser`, `getFollowing`, `getFollowers`, `followUser`, `unfollowUser` |
| Posts | `listPosts`, `getPost`, `createPost`, `updatePost`, `likePost`, `unlikePost`, `listComments`, `addComment`, `listRatings`, `addRating` |
| Categories | `listCategories`, `getCategory`, `listCategoryPosts`, `listCategoryGroups`, `listCategoryRules` |
| Groups | `listGroups`, `getGroup`, `listGroupMembers` |
| Resources | `listResources`, `getResource` |

## Placeholders (TODO)

- [ ] `pages/login.yaml` — Not designed in Figma
- [ ] `pages/post-create.yaml` — Form page not designed
- [ ] `flows/auth/login.yaml` — Authentication flow
- [ ] `flows/auth/register.yaml` — Registration flow
