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
