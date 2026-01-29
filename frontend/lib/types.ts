// TypeScript types matching backend Pydantic schemas

export interface User {
  id: number;
  username: string;
  email: string;
  display_name?: string | null;
  bio?: string | null;
  role: "participant" | "organizer" | "admin";
  created_at?: string | null;
  deleted_at?: string | null;
}

export interface Post {
  id: number;
  title: string;
  body?: string | null;
  type: string;
  status: string;
  visibility: string;
  tags?: string[] | null;
  render_type?: string | null;
  created_by: number;
  like_count: number;
  comment_count: number;
  average_rating?: number | null;
  created_at?: string | null;
}

export interface Category {
  id: number;
  name: string;
  description?: string | null;
  type: "competition" | "operation";
  status: "draft" | "published" | "closed";
  created_by: number;
  prize_pool?: string | null;
  start_date?: string | null;
  end_date?: string | null;
  submission_start?: string | null;
  submission_deadline?: string | null;
  created_at?: string | null;
}

export interface Group {
  id: number;
  name: string;
  description?: string | null;
  visibility: "public" | "private";
  require_approval: boolean;
  max_members?: number | null;
  created_by: number;
  created_at?: string | null;
}

export interface Resource {
  id: number;
  filename: string;
  url?: string | null;
  display_name?: string | null;
  description?: string | null;
  mime_type?: string | null;
  file_size?: number | null;
  created_by?: number | null;
  created_at?: string | null;
}

export interface Rule {
  id: number;
  name: string;
  description?: string | null;
  max_submissions?: number | null;
  min_team_size?: number | null;
  max_team_size?: number | null;
  scoring_criteria?: object | null;
  checks?: object[] | null;
  created_by: number;
}

export interface Interaction {
  id: number;
  type: "like" | "comment" | "rating";
  value?: Record<string, unknown> | null;
  parent_id?: number | null;
  created_by: number;
  created_at?: string | null;
}

export interface Member {
  id: number;
  group_id: number;
  user_id: number;
  role: "owner" | "admin" | "member";
  status: "pending" | "accepted" | "rejected";
  joined_at?: string | null;
}

export interface UserUserRelation {
  id: number;
  source_user_id: number;
  target_user_id: number;
  relation_type: "follow" | "block";
}

export interface CategoryPost {
  id: number;
  category_id: number;
  post_id: number;
  relation_type: string;
}

export interface CategoryGroup {
  id: number;
  category_id: number;
  group_id: number;
}

export interface PostResource {
  id: number;
  post_id: number;
  resource_id: number;
  display_type?: string | null;
  position?: number | null;
}

export interface PostPost {
  id: number;
  source_post_id: number;
  target_post_id: number;
  relation_type: string;
  position?: number | null;
}

export interface CategoryRule {
  id: number;
  category_id: number;
  rule_id: number;
  priority: number;
}

// Paginated response wrapper
export interface Paginated<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}
