// Global mock for @/lib/api-client used in tests
// Returns empty/default data so components render with fallback content

const emptyPaginated = { items: [], total: 0, skip: 0, limit: 100 };

export const listUsers = jest.fn().mockResolvedValue(emptyPaginated);
export const getUser = jest.fn().mockResolvedValue({
  id: 1, username: "testuser", email: "test@test.com", display_name: "他人名字",
  bio: "test bio", role: "participant",
});
export const createUser = jest.fn().mockResolvedValue({ id: 1 });
export const getFollowing = jest.fn().mockResolvedValue([]);
export const getFollowers = jest.fn().mockResolvedValue([]);
export const followUser = jest.fn().mockResolvedValue({ id: 1 });
export const unfollowUser = jest.fn().mockResolvedValue(undefined);
export const checkFriend = jest.fn().mockResolvedValue({ is_friend: false });

export const listPosts = jest.fn().mockResolvedValue(emptyPaginated);
export const getPost = jest.fn().mockResolvedValue({
  id: 1, title: "帖子名帖子名帖子名帖子名帖子名帖子名帖子名帖子名", body: "content",
  type: "general", status: "published", visibility: "public", tags: ["通知公告", "我的学校/公...", "通知公告", "活动信息..."],
  created_by: 1, like_count: 234, comment_count: 56, average_rating: 4.5,
});
export const createPost = jest.fn().mockResolvedValue({ id: 1 });
export const updatePost = jest.fn().mockResolvedValue({ id: 1 });

export const likePost = jest.fn().mockResolvedValue({});
export const unlikePost = jest.fn().mockResolvedValue(undefined);
export const listComments = jest.fn().mockResolvedValue(emptyPaginated);
export const addComment = jest.fn().mockResolvedValue({ id: 1 });
export const listRatings = jest.fn().mockResolvedValue(emptyPaginated);
export const addRating = jest.fn().mockResolvedValue({ id: 1 });
export const listPostResources = jest.fn().mockResolvedValue([]);
export const listRelatedPosts = jest.fn().mockResolvedValue([]);

export const listCategories = jest.fn().mockResolvedValue(emptyPaginated);
export const getCategory = jest.fn().mockResolvedValue({
  id: 1, name: "西建·滇水源 | 上海第七届大学生AI+国际创业大赛", description: "test",
  type: "competition", status: "published", created_by: 1,
});
export const listCategoryPosts = jest.fn().mockResolvedValue([]);
export const listCategoryGroups = jest.fn().mockResolvedValue([]);
export const listCategoryRules = jest.fn().mockResolvedValue([]);

export const listGroups = jest.fn().mockResolvedValue(emptyPaginated);
export const getGroup = jest.fn().mockResolvedValue({
  id: 1, name: "团队", description: "test team", visibility: "public",
  require_approval: true, max_members: 10, created_by: 1,
});
export const listGroupMembers = jest.fn().mockResolvedValue(emptyPaginated);

export const listResources = jest.fn().mockResolvedValue(emptyPaginated);
export const getResource = jest.fn().mockResolvedValue({ id: 1, filename: "test.pdf" });
