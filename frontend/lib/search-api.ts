/**
 * Search API client for Synnovator
 */

import { getPostTypeLabel } from '@/lib/post-type'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

export interface SearchResult {
  type: 'user' | 'category' | 'post'
  id: number
  title: string
  subtitle?: string
  url: string
}

interface UserResult {
  id: number
  username: string
  display_name?: string
  bio?: string
}

interface CategoryResult {
  id: number
  name: string
  description?: string
  type: string
  status: string
}

interface PostResult {
  id: number
  title: string
  body?: string
  type: string
  status: string
  created_by: number
}

interface PaginatedResponse<T> {
  items: T[]
  total: number
}

async function fetchJson<T>(url: string): Promise<T> {
  const response = await fetch(url)
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`)
  }
  return response.json()
}

/**
 * Search users by username or display_name
 */
export async function searchUsers(query: string, limit = 5): Promise<SearchResult[]> {
  try {
    // Backend doesn't have a search endpoint, so we fetch and filter client-side
    const data = await fetchJson<PaginatedResponse<UserResult>>(
      `${API_BASE}/users?limit=100`
    )

    const q = query.toLowerCase()
    return data.items
      .filter(user =>
        user.username.toLowerCase().includes(q) ||
        (user.display_name && user.display_name.toLowerCase().includes(q))
      )
      .slice(0, limit)
      .map(user => ({
        type: 'user' as const,
        id: user.id,
        title: user.display_name || user.username,
        subtitle: `@${user.username}`,
        url: `/profile/${user.id}`,
      }))
  } catch {
    return []
  }
}

/**
 * Search categories by name
 */
export async function searchCategories(query: string, limit = 5): Promise<SearchResult[]> {
  try {
    const data = await fetchJson<PaginatedResponse<CategoryResult>>(
      `${API_BASE}/categories?limit=100`
    )

    const q = query.toLowerCase()
    return data.items
      .filter(cat =>
        cat.name.toLowerCase().includes(q) ||
        (cat.description && cat.description.toLowerCase().includes(q))
      )
      .slice(0, limit)
      .map(cat => ({
        type: 'category' as const,
        id: cat.id,
        title: cat.name,
        subtitle: cat.type === 'competition' ? '比赛' : '活动',
        url: `/categories/${cat.id}`,
      }))
  } catch {
    return []
  }
}

/**
 * Search posts by title
 */
export async function searchPosts(query: string, limit = 5): Promise<SearchResult[]> {
  try {
    const data = await fetchJson<PaginatedResponse<PostResult>>(
      `${API_BASE}/posts?limit=100&status=published`
    )

    const q = query.toLowerCase()
    return data.items
      .filter(post =>
        post.title.toLowerCase().includes(q) ||
        (post.body && post.body.toLowerCase().includes(q))
      )
      .slice(0, limit)
      .map(post => ({
        type: 'post' as const,
        id: post.id,
        title: post.title,
        subtitle: getPostTypeLabel(post.type),
        url: post.type === 'for_category' ? `/proposals/${post.id}` : `/posts/${post.id}`,
      }))
  } catch {
    return []
  }
}

/**
 * Search all content types
 */
export async function searchAll(query: string): Promise<{
  users: SearchResult[]
  categories: SearchResult[]
  posts: SearchResult[]
}> {
  if (!query.trim()) {
    return { users: [], categories: [], posts: [] }
  }

  const [users, categories, posts] = await Promise.all([
    searchUsers(query, 3),
    searchCategories(query, 3),
    searchPosts(query, 5),
  ])

  return { users, categories, posts }
}
