/**
 * TypeScript types for Synnovator API
 */

export interface User {
  id: number
  username: string
  email: string
  role: 'participant' | 'organizer' | 'admin'
  avatar_url?: string
  bio?: string
  follower_count: number
  following_count: number
  created_at: string
  updated_at: string
}

export interface LoginRequest {
  username: string
  password?: string
}

export interface LoginResponse {
  user_id: number
  username: string
  role: string
}

export interface UserCreate {
  username: string
  email: string
  password?: string
  role?: 'participant' | 'organizer' | 'admin'
  avatar_url?: string
  bio?: string
}

export interface Event {
  id: number
  name: string
  type: 'competition' | 'event' | 'campaign' | 'program'
  stage: 'draft' | 'registration' | 'in_progress' | 'judging' | 'completed' | 'cancelled'
  description?: string
  cover_image_url?: string
  start_time?: string
  end_time?: string
  registration_deadline?: string
  created_by: number
  participant_count: number
  created_at: string
  updated_at: string
}

export interface CategoryStage {
  stage: Event['stage']
  label: string
  description: string
}

export interface Notification {
  id: number
  user_id: number
  type: 'follow' | 'comment' | 'mention' | 'team_request' | 'award' | 'system'
  title?: string
  content: string
  related_url?: string
  actor_id?: number
  is_read: boolean
  created_at: string
}

export interface PaginatedList<T> {
  items: T[]
  total: number
  skip: number
  limit: number
}

export interface UserRelation {
  id: number
  source_user_id: number
  target_user_id: number
  relation_type: 'follow' | 'block'
  created_at: string
}

export interface FollowStats {
  is_following: boolean
  follower_count: number
  following_count: number
}
