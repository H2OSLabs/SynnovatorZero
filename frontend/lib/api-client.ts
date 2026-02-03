/**
 * API client for Synnovator backend
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api'

interface ApiOptions extends RequestInit {
  userId?: number
}

async function apiFetch<T>(endpoint: string, options: ApiOptions = {}): Promise<T> {
  const { userId, headers: customHeaders, ...rest } = options

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...customHeaders,
  }

  if (userId) {
    (headers as Record<string, string>)['X-User-Id'] = String(userId)
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...rest,
    headers,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }))
    throw new Error(error.detail || `HTTP ${response.status}`)
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
  return apiFetch<{
    id: number
    username: string
    email: string
    role: string
    display_name?: string
    avatar_url?: string
    bio?: string
    follower_count: number
    following_count: number
  }>(`/users/${userId}`)
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

// Categories
export type CategoryStatus = 'draft' | 'published' | 'closed'
export type CategoryType = 'competition' | 'operation'

export interface Category {
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
  return apiFetch<{ items: Category[]; total: number; skip: number; limit: number }>(
    `/categories?${params.toString()}`
  )
}

export async function getCategory(categoryId: number) {
  return apiFetch<Category>(`/categories/${categoryId}`)
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
