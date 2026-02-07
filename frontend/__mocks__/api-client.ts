/**
 * Mock API client for testing
 */

export const login = jest.fn().mockResolvedValue({
  user_id: 1,
  username: 'testuser',
  role: 'participant',
})

export const logout = jest.fn().mockResolvedValue({})

export const createUser = jest.fn().mockResolvedValue({
  id: 1,
  username: 'testuser',
  email: 'test@example.com',
  role: 'participant',
})

export const getUser = jest.fn().mockResolvedValue({
  id: 1,
  username: 'testuser',
  email: 'test@example.com',
  role: 'participant',
  follower_count: 0,
  following_count: 0,
})

export const listUsers = jest.fn().mockResolvedValue({
  items: [],
  total: 0,
  skip: 0,
  limit: 20,
})

export const followUser = jest.fn().mockResolvedValue({})
export const unfollowUser = jest.fn().mockResolvedValue({})
export const checkFollowing = jest.fn().mockResolvedValue(false)

export const getFollowers = jest.fn().mockResolvedValue({
  items: [],
  total: 0,
})

export const getFollowing = jest.fn().mockResolvedValue({
  items: [],
  total: 0,
})

export const getCategories = jest.fn().mockResolvedValue({
  items: [],
  total: 0,
  skip: 0,
  limit: 20,
})

export const getCategory = jest.fn().mockResolvedValue({
  id: 1,
  name: 'Test Event',
  description: 'Test description',
  type: 'competition',
  status: 'draft',
  participant_count: 0,
})

export const getPosts = jest.fn().mockResolvedValue({
  items: [],
  total: 0,
  skip: 0,
  limit: 20,
})

export const getPost = jest.fn().mockResolvedValue({
  id: 1,
  title: 'Test Post',
  type: 'general',
  status: 'draft',
  visibility: 'public',
  like_count: 0,
  comment_count: 0,
})

export const getGroups = jest.fn().mockResolvedValue({
  items: [],
  total: 0,
  skip: 0,
  limit: 20,
})

export const getGroup = jest.fn().mockResolvedValue({
  id: 1,
  name: 'Test Group',
  visibility: 'public',
})

export const getGroupMembers = jest.fn().mockResolvedValue({
  items: [],
  total: 0,
  skip: 0,
  limit: 100,
})

export const getNotifications = jest.fn().mockResolvedValue({
  items: [],
  total: 0,
})

export const getUnreadCount = jest.fn().mockResolvedValue({
  unread_count: 0,
})

export const markNotificationAsRead = jest.fn().mockResolvedValue({})
export const markAllNotificationsAsRead = jest.fn().mockResolvedValue({ marked_count: 0 })

// Interactions (Comments, Likes)
export const getPostComments = jest.fn().mockResolvedValue({
  items: [],
  total: 0,
  skip: 0,
  limit: 100,
})

export const addPostComment = jest.fn().mockResolvedValue({
  id: 1,
  type: 'comment',
  value: 'Test comment',
  created_by: 1,
  created_at: new Date().toISOString(),
})

export const likePost = jest.fn().mockResolvedValue({
  id: 1,
  type: 'like',
  created_by: 1,
  created_at: new Date().toISOString(),
})

export const unlikePost = jest.fn().mockResolvedValue({})

export const checkPostLiked = jest.fn().mockResolvedValue(false)

// Post Resources
export const getPostResources = jest.fn().mockResolvedValue([])

export const getResource = jest.fn().mockResolvedValue({
  id: 1,
  filename: 'test.pdf',
  file_type: 'application/pdf',
  created_at: new Date().toISOString(),
})

// Event Relations
export const getEventRules = jest.fn().mockResolvedValue([])
export const getEventPosts = jest.fn().mockResolvedValue([])
export const getEventGroups = jest.fn().mockResolvedValue([])

// Rules
export const getRule = jest.fn().mockResolvedValue({
  id: 1,
  name: 'Test Rule',
  type: 'general',
  created_at: new Date().toISOString(),
})

// CRUD operations
export const createPost = jest.fn().mockResolvedValue({
  id: 1,
  title: 'Test Post',
  type: 'general',
  status: 'draft',
  visibility: 'public',
  like_count: 0,
  comment_count: 0,
})

export const updatePost = jest.fn().mockResolvedValue({
  id: 1,
  title: 'Updated Post',
  type: 'general',
  status: 'draft',
  visibility: 'public',
  like_count: 0,
  comment_count: 0,
})

export const deletePost = jest.fn().mockResolvedValue({})

export const createGroup = jest.fn().mockResolvedValue({
  id: 1,
  name: 'Test Group',
  visibility: 'public',
})

export const updateGroup = jest.fn().mockResolvedValue({
  id: 1,
  name: 'Updated Group',
  visibility: 'public',
})

export const deleteGroup = jest.fn().mockResolvedValue({})

export const register = jest.fn().mockResolvedValue({
  user_id: 1,
  username: 'newuser',
  role: 'participant',
})
