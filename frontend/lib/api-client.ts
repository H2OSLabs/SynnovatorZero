/**
 * API client for Synnovator backend
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

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
    avatar_url?: string
    bio?: string
    follower_count: number
    following_count: number
  }>(`/users/${userId}`)
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
export async function getCategories(skip = 0, limit = 20) {
  return apiFetch<{
    items: Array<{
      id: number
      name: string
      type: string
      stage: string
      description?: string
      participant_count: number
    }>
    total: number
  }>(`/categories?skip=${skip}&limit=${limit}`)
}

export async function getCategory(categoryId: number) {
  return apiFetch<{
    id: number
    name: string
    type: string
    stage: string
    description?: string
    cover_image_url?: string
    start_time?: string
    end_time?: string
    registration_deadline?: string
    participant_count: number
  }>(`/categories/${categoryId}`)
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
