# Frontend-API Mapping

Backend Base URL:
- Client-side (browser): `API_URL`（生产通常为 `/api`，由 Nginx 反代）
- Server-side (Next.js Server Components): `INTERNAL_API_URL`（必须为绝对 URL，例如 `http://localhost:8000/api`）
Auth Header: `X-User-Id: <int>` (temporary)

## Meta Endpoints

| Purpose | HTTP Method | Endpoint | Notes |
|--------|-------------|----------|-------|
| Post type enum | GET | `/api/meta/post-types` | Returns allowed `post.type` values and default |

## Component → API Endpoint Mapping

### 1. Home (`components/pages/home.tsx`)

| UI Element | HTTP Method | Endpoint | Notes |
|-----------|-------------|----------|-------|
| Card Grid (featured posts) | GET | `/api/posts?limit=6&status=published` | Top posts for main content |
| Hot Proposals section | GET | `/api/posts?type=proposal&limit=4&status=published` | Proposals with type filter |
| "发布新内容" button | POST | `/api/posts` | Requires auth (X-User-Id) |
| Tab navigation | GET | `/api/events?limit=10` | Tabs map to events |

### 2. PostList (`components/pages/post-list.tsx`)

| UI Element | HTTP Method | Endpoint | Notes |
|-----------|-------------|----------|-------|
| Tab navigation | GET | `/api/events?limit=10` | Event tabs |
| 找队友 section | GET | `/api/groups?limit=4&visibility=public` | Public teams |
| 找点子 section | GET | `/api/posts?limit=4&status=published` | Latest published posts |

### 3. PostDetail (`components/pages/post-detail.tsx`)

| UI Element | HTTP Method | Endpoint | Notes |
|-----------|-------------|----------|-------|
| Post content | GET | `/api/posts/{id}` | Full post detail |
| Author info | GET | `/api/users/{userId}` | Post's created_by user |
| Like button | POST | `/api/posts/{id}/like` | Toggle like (auth required) |
| Unlike button | DELETE | `/api/posts/{id}/like` | Remove like (auth required) |
| Comments list | GET | `/api/posts/{id}/comments?limit=20` | Paginated comments |
| Add comment | POST | `/api/posts/{id}/comments` | Auth required, body: `{value: {text: "..."}}` |
| Ratings | GET | `/api/posts/{id}/ratings` | Rating list |
| Post resources | GET | `/api/posts/{id}/resources` | Attached files |
| Related posts | GET | `/api/posts/{id}/related` | Post-post relations |
| Tags display | — | Inline from post.tags | No separate API |

### 4. ProposalList (`components/pages/proposal-list.tsx`)

| UI Element | HTTP Method | Endpoint | Notes |
|-----------|-------------|----------|-------|
| Proposal grid | GET | `/api/posts?type=proposal&limit=10&status=published` | type=proposal for proposals |
| Event filter tabs | GET | `/api/events?limit=10` | Event list |

### 5. ProposalDetail (`components/pages/proposal-detail.tsx`)

| UI Element | HTTP Method | Endpoint | Notes |
|-----------|-------------|----------|-------|
| Proposal content | GET | `/api/posts/{id}` | Full proposal detail |
| Team info | GET | `/api/groups/{groupId}` | Team associated with proposal |
| Team members | GET | `/api/groups/{groupId}/members` | Member list |
| Comments tab | GET | `/api/posts/{id}/comments?limit=20` | Comments section |
| Add comment | POST | `/api/posts/{id}/comments` | Auth required |
| Like button | POST | `/api/posts/{id}/like` | Auth required |
| Ratings display | GET | `/api/posts/{id}/ratings` | Multi-dimensional ratings |
| Related proposals | GET | `/api/posts/{id}/related` | Related content |
| Version history | GET | `/api/posts/{id}/related?relation_type=reference` | Version links |

### 6. CategoryDetail (`components/pages/event-detail.tsx`)

| UI Element | HTTP Method | Endpoint | Notes |
|-----------|-------------|----------|-------|
| Event info banner | GET | `/api/events/{id}` | Name, description, status, type |
| Posts in event | GET | `/api/events/{id}/posts?relation_type=submission` | Submitted posts |
| Registered teams | GET | `/api/events/{id}/groups` | Team registrations |
| Event rules | GET | `/api/events/{id}/rules` | Linked rules |
| Associated events | GET | `/api/events/{id}/associations` | Stage/track/prerequisite |

### 7. UserProfile (`components/pages/user-profile.tsx`)

| UI Element | HTTP Method | Endpoint | Notes |
|-----------|-------------|----------|-------|
| Profile info | GET | `/api/users/{id}` | Username, display_name, bio, role |
| User's posts | GET | `/api/posts?limit=20&status=published` | Filter by created_by on frontend |
| Following count | GET | `/api/users/{id}/following` | Count from array length |
| Followers count | GET | `/api/users/{id}/followers` | Count from array length |
| Follow button | POST | `/api/users/{id}/follow` | Auth required |
| Unfollow button | DELETE | `/api/users/{id}/follow` | Auth required |
| User's resources | GET | `/api/resources?limit=20` | Filter by created_by on frontend |

### 8. Team (`components/pages/team.tsx`)

| UI Element | HTTP Method | Endpoint | Notes |
|-----------|-------------|----------|-------|
| Team info | GET | `/api/groups/{id}` | Name, description, visibility |
| Member list | GET | `/api/groups/{id}/members` | Members with roles/status |
| Add member | POST | `/api/groups/{id}/members` | Body: `{user_id, role}` |
| Update member | PATCH | `/api/groups/{id}/members/{userId}` | Status/role change |
| Remove member | DELETE | `/api/groups/{id}/members/{userId}` | Remove from team |

### 9. FollowingList (`components/pages/following-list.tsx`)

| UI Element | HTTP Method | Endpoint | Notes |
|-----------|-------------|----------|-------|
| Following list | GET | `/api/users/{id}/following` | Users I follow |
| Followers list | GET | `/api/users/{id}/followers` | Users following me |
| Follow user | POST | `/api/users/{userId}/follow` | Auth required |
| Unfollow user | DELETE | `/api/users/{userId}/follow` | Auth required |
| Friend check | GET | `/api/users/{id}/is-friend/{otherId}` | Mutual follow check |

### 10. Assets (`components/pages/assets.tsx`)

| UI Element | HTTP Method | Endpoint | Notes |
|-----------|-------------|----------|-------|
| Resource list | GET | `/api/resources?limit=20` | All resources |
| Create resource | POST | `/api/resources` | Auth required, body: ResourceCreate |
| Resource detail | GET | `/api/resources/{id}` | Single resource |

## Shared API Client Configuration

```typescript
// frontend/lib/api-client.ts
import { getEnv } from './env'

// 运行时获取 API URL（支持不同环境）
// - 开发环境: http://localhost:8000/api (来自 .env.development)
// - 生产环境: /api (来自 Docker 环境变量，通过 nginx 代理)
const getApiBase = () => getEnv().API_URL

// All endpoints use JSON content type
// Auth via X-User-Id header when logged in
// Pagination: ?skip=0&limit=100
// Soft-deleted items are automatically excluded by backend
```

## TypeScript Types (from backend schemas)

```typescript
// Core entities
interface User { id: number; username: string; email: string; display_name?: string; bio?: string; role: "participant"|"organizer"|"admin"; }
type PostType = "profile" | "team" | "event" | "proposal" | "certificate" | "general";
interface Post { id: number; title: string; body?: string; type: PostType; status: string; visibility: string; tags?: string[]; created_by: number; like_count: number; comment_count: number; average_rating?: number; }
interface Event { id: number; name: string; description?: string; type: "competition"|"operation"; status: "draft"|"published"|"closed"; created_by: number; }
interface Group { id: number; name: string; description?: string; visibility: "public"|"private"; require_approval: boolean; max_members?: number; created_by: number; }
interface Resource { id: number; filename: string; url?: string; display_name?: string; description?: string; mime_type?: string; file_size?: number; created_by?: number; }
interface Rule { id: number; name: string; description?: string; max_submissions?: number; scoring_criteria?: object; checks?: object[]; created_by: number; }
interface Interaction { id: number; type: "like"|"comment"|"rating"; value?: object; parent_id?: number; created_by: number; }

// Paginated responses
interface Paginated<T> { items: T[]; total: number; skip: number; limit: number; }
```

## Auth Flow

1. User logs in → receives user ID (simplified, no JWT yet)
2. Frontend stores user ID in local state/context
3. All authenticated requests include `X-User-Id: {userId}` header
4. Role-based endpoints (create event/rule) check user role server-side
