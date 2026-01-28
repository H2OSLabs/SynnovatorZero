import type {
  User, Post, Category, Group, Resource, Interaction, Member,
  UserUserRelation, CategoryPost, CategoryGroup, PostResource, PostPost,
  CategoryRule, Paginated,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

// --- Helpers ---

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`API ${res.status}: ${detail}`);
  }
  if (res.status === 204) return undefined as unknown as T;
  return res.json();
}

function authHeaders(userId: number | null): Record<string, string> {
  return userId ? { "X-User-Id": String(userId) } : {};
}

// --- Users ---

export async function listUsers(skip = 0, limit = 100): Promise<Paginated<User>> {
  return request(`/users?skip=${skip}&limit=${limit}`);
}

export async function getUser(id: number): Promise<User> {
  return request(`/users/${id}`);
}

export async function createUser(data: { username: string; email: string; display_name?: string; bio?: string; role?: string }): Promise<User> {
  return request("/users", { method: "POST", body: JSON.stringify(data) });
}

export async function getFollowing(userId: number): Promise<UserUserRelation[]> {
  return request(`/users/${userId}/following`);
}

export async function getFollowers(userId: number): Promise<UserUserRelation[]> {
  return request(`/users/${userId}/followers`);
}

export async function followUser(targetId: number, currentUserId: number): Promise<UserUserRelation> {
  return request(`/users/${targetId}/follow`, { method: "POST", headers: authHeaders(currentUserId) });
}

export async function unfollowUser(targetId: number, currentUserId: number): Promise<void> {
  return request(`/users/${targetId}/follow`, { method: "DELETE", headers: authHeaders(currentUserId) });
}

export async function checkFriend(userId: number, otherId: number): Promise<{ is_friend: boolean }> {
  return request(`/users/${userId}/is-friend/${otherId}`);
}

// --- Posts ---

export async function listPosts(params?: { skip?: number; limit?: number; type?: string; status?: string }): Promise<Paginated<Post>> {
  const q = new URLSearchParams();
  if (params?.skip) q.set("skip", String(params.skip));
  if (params?.limit) q.set("limit", String(params.limit));
  if (params?.type) q.set("type", params.type);
  if (params?.status) q.set("status", params.status);
  return request(`/posts?${q.toString()}`);
}

export async function getPost(id: number, userId?: number | null): Promise<Post> {
  return request(`/posts/${id}`, userId ? { headers: authHeaders(userId) } : undefined);
}

export async function createPost(data: { title: string; body?: string; type?: string; tags?: string[] }, userId: number): Promise<Post> {
  return request("/posts", { method: "POST", body: JSON.stringify(data), headers: authHeaders(userId) });
}

export async function updatePost(id: number, data: Record<string, unknown>): Promise<Post> {
  return request(`/posts/${id}`, { method: "PATCH", body: JSON.stringify(data) });
}

// --- Post interactions ---

export async function likePost(postId: number, userId: number): Promise<unknown> {
  return request(`/posts/${postId}/like`, { method: "POST", headers: authHeaders(userId) });
}

export async function unlikePost(postId: number, userId: number): Promise<void> {
  return request(`/posts/${postId}/like`, { method: "DELETE", headers: authHeaders(userId) });
}

export async function listComments(postId: number, skip = 0, limit = 20): Promise<Paginated<Interaction>> {
  return request(`/posts/${postId}/comments?skip=${skip}&limit=${limit}`);
}

export async function addComment(postId: number, value: Record<string, unknown>, userId: number, parentId?: number): Promise<Interaction> {
  return request(`/posts/${postId}/comments`, {
    method: "POST",
    body: JSON.stringify({ value, parent_id: parentId }),
    headers: authHeaders(userId),
  });
}

export async function listRatings(postId: number, skip = 0, limit = 20): Promise<Paginated<Interaction>> {
  return request(`/posts/${postId}/ratings?skip=${skip}&limit=${limit}`);
}

export async function addRating(postId: number, value: Record<string, unknown>, userId: number): Promise<Interaction> {
  return request(`/posts/${postId}/ratings`, {
    method: "POST",
    body: JSON.stringify({ value }),
    headers: authHeaders(userId),
  });
}

// --- Post relations ---

export async function listPostResources(postId: number): Promise<PostResource[]> {
  return request(`/posts/${postId}/resources`);
}

export async function listRelatedPosts(postId: number, relationType?: string): Promise<PostPost[]> {
  const q = relationType ? `?relation_type=${relationType}` : "";
  return request(`/posts/${postId}/related${q}`);
}

// --- Categories ---

export async function listCategories(skip = 0, limit = 100): Promise<Paginated<Category>> {
  return request(`/categories?skip=${skip}&limit=${limit}`);
}

export async function getCategory(id: number, userId?: number | null): Promise<Category> {
  return request(`/categories/${id}`, userId ? { headers: authHeaders(userId) } : undefined);
}

export async function listCategoryPosts(categoryId: number, relationType?: string, userId?: number | null): Promise<CategoryPost[]> {
  const q = relationType ? `?relation_type=${relationType}` : "";
  return request(`/categories/${categoryId}/posts${q}`, userId ? { headers: authHeaders(userId) } : undefined);
}

export async function listCategoryGroups(categoryId: number): Promise<CategoryGroup[]> {
  return request(`/categories/${categoryId}/groups`);
}

export async function listCategoryRules(categoryId: number): Promise<CategoryRule[]> {
  return request(`/categories/${categoryId}/rules`);
}

// --- Groups ---

export async function listGroups(params?: { skip?: number; limit?: number; visibility?: string }): Promise<Paginated<Group>> {
  const q = new URLSearchParams();
  if (params?.skip) q.set("skip", String(params.skip));
  if (params?.limit) q.set("limit", String(params.limit));
  if (params?.visibility) q.set("visibility", params.visibility);
  return request(`/groups?${q.toString()}`);
}

export async function getGroup(id: number, userId?: number | null): Promise<Group> {
  return request(`/groups/${id}`, userId ? { headers: authHeaders(userId) } : undefined);
}

export async function listGroupMembers(groupId: number, status?: string): Promise<Paginated<Member>> {
  const q = status ? `?status=${status}` : "";
  return request(`/groups/${groupId}/members${q}`);
}

// --- Resources ---

export async function listResources(skip = 0, limit = 100): Promise<Paginated<Resource>> {
  return request(`/resources?skip=${skip}&limit=${limit}`);
}

export async function getResource(id: number): Promise<Resource> {
  return request(`/resources/${id}`);
}
