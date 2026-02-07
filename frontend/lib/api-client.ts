/**
 * API client for Synnovator backend
 */

import { getEnv } from './env'

// Lazy getter to ensure window.__ENV__ is available when called
const getApiBase = () => getEnv().API_URL
const STORAGE_KEY = 'synnovator_user'

interface ApiOptions extends RequestInit {
  userId?: number
  skipAuth?: boolean  // Skip auto-attaching user_id from localStorage
}

function formatApiErrorMessage(status: number, detail?: string): string {
  const raw = typeof detail === 'string' ? detail.trim() : ''

  const detailMap: Record<string, string> = {
    'Unknown error': '未知错误',
    'Not Found': '资源不存在',
    'User not found': '用户不存在',
    'Not authenticated': '未登录或登录已过期',
    'Invalid credentials': '用户名或密码错误',
    'Validation error': '参数校验失败',
  }

  if (raw && detailMap[raw]) return detailMap[raw]

  if (status === 400) return raw || `请求参数错误（HTTP ${status}）`
  if (status === 401) return raw || '未登录或登录已过期'
  if (status === 403) return raw || '没有权限执行该操作'
  if (status === 404) return raw || '资源不存在'
  if (status === 409) return raw || '资源冲突，请刷新后重试'
  if (status === 422) return raw || '参数校验失败'
  if (status >= 500) return raw || `服务器错误（HTTP ${status}）`

  return raw || `请求失败（HTTP ${status}）`
}

function isAbortError(error: unknown): boolean {
  if (!error || typeof error !== 'object') return false
  return 'name' in error && (error as { name?: unknown }).name === 'AbortError'
}

/**
 * Get current user_id from localStorage
 */
function getStoredUserId(): number | null {
  if (typeof window === 'undefined') return null
  const stored = localStorage.getItem(STORAGE_KEY)
  if (!stored) return null
  try {
    const user = JSON.parse(stored)
    return user.user_id || null
  } catch {
    return null
  }
}

async function apiFetch<T>(endpoint: string, options: ApiOptions = {}): Promise<T> {
  const { userId, skipAuth, headers: customHeaders, signal: providedSignal, ...rest } = options

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...customHeaders,
  }

  // Use provided userId, or auto-attach from localStorage
  const effectiveUserId = userId ?? (skipAuth ? null : getStoredUserId())
  if (effectiveUserId) {
    (headers as Record<string, string>)['X-User-Id'] = String(effectiveUserId)
  }

  const timeoutMs = typeof window === 'undefined' ? 3000 : 15000
  const controller = providedSignal ? null : new AbortController()
  const signal = providedSignal ?? controller?.signal
  const timeoutId = controller ? setTimeout(() => controller.abort(), timeoutMs) : null

  let response: Response
  try {
    response = await fetch(`${getApiBase()}${endpoint}`, {
      ...rest,
      headers,
      signal,
    }).finally(() => {
      if (timeoutId) clearTimeout(timeoutId)
    })
  } catch (e) {
    if (isAbortError(e)) {
      throw new Error('请求超时，请稍后重试')
    }
    throw new Error('网络异常，请检查网络后重试')
  }

  if (!response.ok) {
    let detail: string | undefined
    try {
      const data = await response.clone().json()
      if (data && typeof data === 'object' && 'detail' in data && typeof (data as { detail?: unknown }).detail === 'string') {
        detail = (data as { detail: string }).detail
      }
    } catch {}

    const message = formatApiErrorMessage(response.status, detail)
    throw new Error(message)
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return {} as T
  }

  return response.json()
}

// Auth
export async function login(username: string, password?: string) {
  return apiFetch<{ user_id: number; username: string; role: string }>('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })
}

export async function logout(userId: number) {
  return apiFetch('/auth/logout', {
    method: 'POST',
    userId,
  })
}

export async function register(data: {
  username: string
  email: string
  password: string
  role: 'participant' | 'organizer'
}) {
  return apiFetch<{ user_id: number; username: string; role: string }>('/auth/register', {
    method: 'POST',
    body: JSON.stringify(data),
    skipAuth: true,
  })
}

// Users
export async function createUser(data: {
  username: string
  email: string
  role?: string
  avatar_url?: string
  bio?: string
}) {
  return apiFetch<{ id: number; username: string; email: string; role: string }>('/users', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export async function getUser(userId: number) {
  return apiFetch<User>(`/users/${userId}`)
}

export interface User {
  id: number
  username: string
  email: string
  role: 'participant' | 'organizer' | 'admin'
  display_name?: string | null
  avatar_url?: string | null
  bio?: string | null
  follower_count: number
  following_count: number
  created_at?: string
  updated_at?: string | null
  deleted_at?: string | null
}

export async function listUsers(skip = 0, limit = 20, role?: User['role']) {
  const params = new URLSearchParams({ skip: String(skip), limit: String(limit) })
  if (role) params.set('role', role)
  return apiFetch<{ items: User[]; total: number; skip: number; limit: number }>(`/users?${params.toString()}`)
}

// User Relations
export async function followUser(currentUserId: number, targetUserId: number) {
  return apiFetch(`/users/${targetUserId}/follow`, {
    method: 'POST',
    userId: currentUserId,
  })
}

export async function unfollowUser(currentUserId: number, targetUserId: number) {
  return apiFetch(`/users/${targetUserId}/follow`, {
    method: 'DELETE',
    userId: currentUserId,
  })
}

export async function checkFollowing(currentUserId: number, targetUserId: number): Promise<boolean> {
  try {
    const response = await apiFetch<{ items: Array<{ target_user_id: number }> }>(
      `/users/${currentUserId}/following?limit=1000`,
      { userId: currentUserId }
    )
    return response.items.some(item => item.target_user_id === targetUserId)
  } catch {
    return false
  }
}

export async function getFollowers(userId: number, skip = 0, limit = 20) {
  return apiFetch<{ items: Array<{ source_user_id: number; created_at: string }>; total: number }>(
    `/users/${userId}/followers?skip=${skip}&limit=${limit}`
  )
}

export async function getFollowing(userId: number, skip = 0, limit = 20) {
  return apiFetch<{ items: Array<{ target_user_id: number; created_at: string }>; total: number }>(
    `/users/${userId}/following?skip=${skip}&limit=${limit}`
  )
}

// Events
export type CategoryStatus = 'draft' | 'published' | 'closed'
export type CategoryType = 'competition' | 'operation'

export interface Event {
  id: number
  name: string
  description: string
  type: CategoryType
  status: CategoryStatus
  tags?: string[] | null
  cover_image?: string | null
  start_date?: string | null
  end_date?: string | null
  created_by?: number | null
  content?: string | null
  participant_count: number
  created_at?: string
  updated_at?: string | null
  deleted_at?: string | null
}

export async function getCategories(
  skip = 0,
  limit = 20,
  filters?: { status?: CategoryStatus; type?: CategoryType }
) {
  const params = new URLSearchParams({ skip: String(skip), limit: String(limit) })
  if (filters?.status) params.set('status', filters.status)
  if (filters?.type) params.set('type', filters.type)
  return apiFetch<{ items: Event[]; total: number; skip: number; limit: number }>(
    `/events?${params.toString()}`
  )
}

export async function getCategory(categoryId: number) {
  return apiFetch<Event>(`/events/${categoryId}`)
}

export type PostStatus = 'draft' | 'pending_review' | 'published' | 'rejected'
export type PostVisibility = 'public' | 'private'

export interface Post {
  id: number
  title: string
  type: string
  tags?: string[] | null
  status: PostStatus
  visibility: PostVisibility
  content?: string | null
  created_by?: number | null
  like_count: number
  comment_count: number
  average_rating?: number | null
  created_at?: string
  updated_at?: string | null
  deleted_at?: string | null
}

export async function getPosts(skip = 0, limit = 20, filters?: { type?: string; status?: PostStatus }) {
  const params = new URLSearchParams({ skip: String(skip), limit: String(limit) })
  if (filters?.type) params.set('type', filters.type)
  if (filters?.status) params.set('status', filters.status)
  return apiFetch<{ items: Post[]; total: number; skip: number; limit: number }>(`/posts?${params.toString()}`)
}

export async function getPost(postId: number) {
  return apiFetch<Post>(`/posts/${postId}`)
}

export interface CreatePostData {
  title: string
  content?: string
  type?: string
  tags?: string[]
  status?: PostStatus
  visibility?: PostVisibility
  event_id?: number | null
}

export async function createPost(data: CreatePostData) {
  return apiFetch<Post>('/posts', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export async function updatePost(postId: number, data: Partial<CreatePostData>) {
  return apiFetch<Post>(`/posts/${postId}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  })
}

export async function deletePost(postId: number) {
  return apiFetch<void>(`/posts/${postId}`, {
    method: 'DELETE',
  })
}

export type GroupVisibility = 'public' | 'private'

export interface Group {
  id: number
  name: string
  description?: string | null
  visibility: GroupVisibility
  max_members?: number | null
  require_approval?: boolean | null
  created_by?: number | null
  created_at?: string
  updated_at?: string | null
  deleted_at?: string | null
}

export interface Member {
  id: number
  group_id: number
  user_id: number
  role: 'owner' | 'admin' | 'member'
  status: 'pending' | 'accepted' | 'rejected'
  joined_at?: string | null
  status_changed_at?: string | null
  created_at?: string
  updated_at?: string | null
}

export async function getGroups(skip = 0, limit = 20, filters?: { visibility?: GroupVisibility }) {
  const params = new URLSearchParams({ skip: String(skip), limit: String(limit) })
  if (filters?.visibility) params.set('visibility', filters.visibility)
  return apiFetch<{ items: Group[]; total: number; skip: number; limit: number }>(`/groups?${params.toString()}`)
}

export async function getGroup(groupId: number) {
  return apiFetch<Group>(`/groups/${groupId}`)
}

export interface CreateGroupData {
  name: string
  description?: string
  visibility?: GroupVisibility
  max_members?: number
  require_approval?: boolean
}

export async function createGroup(data: CreateGroupData) {
  return apiFetch<Group>('/groups', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export async function updateGroup(groupId: number, data: Partial<CreateGroupData>) {
  return apiFetch<Group>(`/groups/${groupId}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  })
}

export async function deleteGroup(groupId: number) {
  return apiFetch<void>(`/groups/${groupId}`, {
    method: 'DELETE',
  })
}

export async function getGroupMembers(
  groupId: number,
  skip = 0,
  limit = 100,
  filters?: { status?: Member['status'] }
) {
  const params = new URLSearchParams({ skip: String(skip), limit: String(limit) })
  if (filters?.status) params.set('status', filters.status)
  return apiFetch<{ items: Member[]; total: number; skip: number; limit: number }>(
    `/groups/${groupId}/members?${params.toString()}`
  )
}

// Notifications
export async function getNotifications(userId: number, skip = 0, limit = 20, isRead?: boolean) {
  let url = `/notifications?skip=${skip}&limit=${limit}`
  if (isRead !== undefined) {
    url += `&is_read=${isRead}`
  }
  return apiFetch<{
    items: Array<{
      id: number
      type: string
      title?: string
      content: string
      related_url?: string
      is_read: boolean
      created_at: string
    }>
    total: number
  }>(url, { userId })
}

export async function getUnreadCount(userId: number) {
  return apiFetch<{ unread_count: number }>('/notifications/unread-count', { userId })
}

export async function markNotificationAsRead(userId: number, notificationId: number) {
  return apiFetch(`/notifications/${notificationId}`, {
    method: 'PATCH',
    userId,
    body: JSON.stringify({ is_read: true }),
  })
}

export async function markAllNotificationsAsRead(userId: number) {
  return apiFetch<{ marked_count: number }>('/notifications/read-all', {
    method: 'POST',
    userId,
  })
}

// Interactions (Comments, Likes, Ratings)
export interface Interaction {
  id: number
  type: 'like' | 'comment' | 'rating'
  value?: string | { score: number } | null
  parent_id?: number | null
  created_by?: number | null
  created_at: string
  updated_at?: string | null
  deleted_at?: string | null
}

export async function getPostComments(postId: number, skip = 0, limit = 100) {
  return apiFetch<{ items: Interaction[]; total: number; skip: number; limit: number }>(
    `/posts/${postId}/comments?skip=${skip}&limit=${limit}`
  )
}

export async function addPostComment(postId: number, value: string, parentId?: number) {
  return apiFetch<Interaction>(`/posts/${postId}/comments`, {
    method: 'POST',
    body: JSON.stringify({ type: 'comment', value, parent_id: parentId }),
  })
}

export async function likePost(postId: number) {
  return apiFetch<Interaction>(`/posts/${postId}/likes`, {
    method: 'POST',
    body: JSON.stringify({ type: 'like' }),
  })
}

export async function unlikePost(postId: number) {
  return apiFetch<void>(`/posts/${postId}/likes`, {
    method: 'DELETE',
  })
}

export async function checkPostLiked(postId: number): Promise<boolean> {
  try {
    await apiFetch<{ liked: boolean }>(`/posts/${postId}/likes/check`)
    return true
  } catch {
    return false
  }
}

// Post Resources
export interface PostResource {
  id: number
  post_id: number
  resource_id: number
  display_type: 'attachment' | 'inline'
  position?: number | null
  created_at: string
}

export interface Resource {
  id: number
  filename: string
  display_name?: string | null
  file_type?: string | null
  file_size?: number | null
  url?: string | null
  created_by?: number | null
  created_at: string
}

export async function getPostResources(postId: number) {
  return apiFetch<PostResource[]>(`/posts/${postId}/resources`)
}

export async function getResource(resourceId: number) {
  return apiFetch<Resource>(`/resources/${resourceId}`)
}

// Event-related APIs
export interface EventRule {
  id: number
  event_id: number
  rule_id: number
  priority: number
  position?: number | null
  created_at: string
}

export interface EventPost {
  id: number
  event_id: number
  post_id: number
  submission_type: string
  status: string
  position?: number | null
  created_at: string
}

export interface EventGroup {
  id: number
  event_id: number
  group_id: number
  status: string
  position?: number | null
  created_at: string
}

export async function getEventRules(eventId: number) {
  return apiFetch<EventRule[]>(`/events/${eventId}/rules`)
}

export async function getEventPosts(eventId: number) {
  return apiFetch<EventPost[]>(`/events/${eventId}/posts`)
}

export async function getEventGroups(eventId: number) {
  return apiFetch<EventGroup[]>(`/events/${eventId}/groups`)
}

// Rules
export interface Rule {
  id: number
  name: string
  description?: string | null
  type: string
  config?: Record<string, unknown> | null
  created_by?: number | null
  created_at: string
}

export async function getRule(ruleId: number) {
  return apiFetch<Rule>(`/rules/${ruleId}`)
}
