/**
 * Unit tests for API client functions
 * Tests the actual implementation with mocked fetch
 */

// Use jest.doMock to avoid the automatic mock from moduleNameMapper
// We need to import the real module, not the mock

// Mock the env module first
jest.mock('../lib/env', () => ({
  getEnv: () => ({ API_URL: 'http://localhost:8000' }),
}))

// Import the real api-client directly (not through @/ alias which is mocked)
const apiClient = jest.requireActual('../lib/api-client') as typeof import('../lib/api-client')

describe('api-client', () => {
  const mockFetch = jest.fn()
  const originalFetch = global.fetch

  beforeAll(() => {
    global.fetch = mockFetch
  })

  afterAll(() => {
    global.fetch = originalFetch
  })

  beforeEach(() => {
    mockFetch.mockClear()
    // Clear localStorage
    if (typeof window !== 'undefined') {
      localStorage.clear()
    }
  })

  // Helper to create mock response
  const mockJsonResponse = (data: unknown, status = 200) => {
    return Promise.resolve({
      ok: status >= 200 && status < 300,
      status,
      json: () => Promise.resolve(data),
    } as Response)
  }

  const mockErrorResponse = (status: number, detail: string) => {
    return Promise.resolve({
      ok: false,
      status,
      json: () => Promise.resolve({ detail }),
    } as Response)
  }

  describe('User APIs', () => {
    test('getUser fetches user by ID', async () => {
      const mockUser = {
        id: 1,
        username: 'testuser',
        email: 'test@example.com',
        role: 'participant',
        follower_count: 10,
        following_count: 5,
      }
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockUser))

      const result = await apiClient.getUser(1)

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/users/1',
        expect.objectContaining({
          headers: expect.objectContaining({
            'Content-Type': 'application/json',
          }),
        })
      )
      expect(result).toEqual(mockUser)
    })

    test('listUsers with pagination and role filter', async () => {
      const mockResponse = {
        items: [{ id: 1, username: 'user1' }],
        total: 1,
        skip: 0,
        limit: 10,
      }
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockResponse))

      const result = await apiClient.listUsers(0, 10, 'organizer')

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/users?skip=0&limit=10&role=organizer',
        expect.anything()
      )
      expect(result).toEqual(mockResponse)
    })

    test('listUsers without role filter', async () => {
      const mockResponse = { items: [], total: 0, skip: 0, limit: 20 }
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockResponse))

      await apiClient.listUsers(10, 20)

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/users?skip=10&limit=20',
        expect.anything()
      )
    })
  })

  describe('Post APIs', () => {
    test('getPost fetches post by ID', async () => {
      const mockPost = {
        id: 1,
        title: 'Test Post',
        type: 'general',
        status: 'published',
        visibility: 'public',
        like_count: 5,
        comment_count: 3,
      }
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockPost))

      const result = await apiClient.getPost(1)

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/posts/1',
        expect.anything()
      )
      expect(result).toEqual(mockPost)
    })

    test('getPosts with filters', async () => {
      const mockResponse = { items: [], total: 0, skip: 0, limit: 20 }
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockResponse))

      await apiClient.getPosts(0, 20, { type: 'article', status: 'published' })

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/posts?skip=0&limit=20&type=article&status=published',
        expect.anything()
      )
    })

    test('createPost sends POST request with data', async () => {
      const mockPost = { id: 1, title: 'New Post', status: 'draft' }
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockPost))

      const data = {
        title: 'New Post',
        content: 'Content here',
        type: 'article',
      }
      const result = await apiClient.createPost(data)

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/posts',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(data),
        })
      )
      expect(result).toEqual(mockPost)
    })

    test('updatePost sends PATCH request', async () => {
      const mockPost = { id: 1, title: 'Updated', status: 'published' }
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockPost))

      const data = { title: 'Updated', status: 'published' as const }
      await apiClient.updatePost(1, data)

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/posts/1',
        expect.objectContaining({
          method: 'PATCH',
          body: JSON.stringify(data),
        })
      )
    })

    test('deletePost sends DELETE request', async () => {
      mockFetch.mockReturnValueOnce(
        Promise.resolve({
          ok: true,
          status: 204,
          json: () => Promise.resolve({}),
        } as Response)
      )

      await apiClient.deletePost(1)

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/posts/1',
        expect.objectContaining({
          method: 'DELETE',
        })
      )
    })
  })

  describe('Interaction APIs', () => {
    test('getPostComments fetches comments for a post', async () => {
      const mockComments = {
        items: [
          { id: 1, type: 'comment', value: 'Great post!', created_by: 1 },
        ],
        total: 1,
        skip: 0,
        limit: 100,
      }
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockComments))

      const result = await apiClient.getPostComments(1)

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/posts/1/comments?skip=0&limit=100',
        expect.anything()
      )
      expect(result).toEqual(mockComments)
    })

    test('getPostComments with custom pagination', async () => {
      const mockComments = { items: [], total: 0, skip: 10, limit: 50 }
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockComments))

      await apiClient.getPostComments(1, 10, 50)

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/posts/1/comments?skip=10&limit=50',
        expect.anything()
      )
    })

    test('addPostComment sends POST request', async () => {
      const mockComment = {
        id: 1,
        type: 'comment',
        value: 'Nice!',
        created_by: 1,
        created_at: '2026-02-08T00:00:00Z',
      }
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockComment))

      const result = await apiClient.addPostComment(1, 'Nice!')

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/posts/1/comments',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ type: 'comment', value: 'Nice!', parent_id: undefined }),
        })
      )
      expect(result).toEqual(mockComment)
    })

    test('addPostComment with parent_id for reply', async () => {
      const mockComment = { id: 2, type: 'comment', value: 'Reply', parent_id: 1 }
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockComment))

      await apiClient.addPostComment(1, 'Reply', 1)

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/posts/1/comments',
        expect.objectContaining({
          body: JSON.stringify({ type: 'comment', value: 'Reply', parent_id: 1 }),
        })
      )
    })

    test('likePost sends POST request', async () => {
      const mockLike = { id: 1, type: 'like', created_by: 1 }
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockLike))

      const result = await apiClient.likePost(1)

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/posts/1/likes',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ type: 'like' }),
        })
      )
      expect(result).toEqual(mockLike)
    })

    test('unlikePost sends DELETE request', async () => {
      mockFetch.mockReturnValueOnce(
        Promise.resolve({
          ok: true,
          status: 204,
          json: () => Promise.resolve({}),
        } as Response)
      )

      await apiClient.unlikePost(1)

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/posts/1/likes',
        expect.objectContaining({
          method: 'DELETE',
        })
      )
    })
  })

  describe('Post Resource APIs', () => {
    test('getPostResources fetches resources for a post', async () => {
      const mockResources = [
        { id: 1, post_id: 1, resource_id: 10, display_type: 'attachment' },
      ]
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockResources))

      const result = await apiClient.getPostResources(1)

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/posts/1/resources',
        expect.anything()
      )
      expect(result).toEqual(mockResources)
    })

    test('getResource fetches resource by ID', async () => {
      const mockResource = {
        id: 10,
        filename: 'document.pdf',
        file_type: 'application/pdf',
        file_size: 1024,
        url: '/uploads/document.pdf',
      }
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockResource))

      const result = await apiClient.getResource(10)

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/resources/10',
        expect.anything()
      )
      expect(result).toEqual(mockResource)
    })
  })

  describe('Event APIs', () => {
    test('getCategory fetches event by ID', async () => {
      const mockEvent = {
        id: 1,
        name: 'Hackathon 2026',
        type: 'competition',
        status: 'published',
        participant_count: 100,
      }
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockEvent))

      const result = await apiClient.getCategory(1)

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/events/1',
        expect.anything()
      )
      expect(result).toEqual(mockEvent)
    })

    test('getCategories with filters', async () => {
      const mockResponse = { items: [], total: 0, skip: 0, limit: 20 }
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockResponse))

      await apiClient.getCategories(0, 20, { status: 'published', type: 'competition' })

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/events?skip=0&limit=20&status=published&type=competition',
        expect.anything()
      )
    })

    test('getEventRules fetches rules for an event', async () => {
      const mockRules = [
        { id: 1, event_id: 1, rule_id: 10, priority: 1 },
      ]
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockRules))

      const result = await apiClient.getEventRules(1)

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/events/1/rules',
        expect.anything()
      )
      expect(result).toEqual(mockRules)
    })

    test('getEventPosts fetches posts for an event', async () => {
      const mockPosts = [
        { id: 1, event_id: 1, post_id: 5, submission_type: 'entry', status: 'accepted' },
      ]
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockPosts))

      const result = await apiClient.getEventPosts(1)

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/events/1/posts',
        expect.anything()
      )
      expect(result).toEqual(mockPosts)
    })

    test('getEventGroups fetches groups for an event', async () => {
      const mockGroups = [
        { id: 1, event_id: 1, group_id: 3, status: 'registered' },
      ]
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockGroups))

      const result = await apiClient.getEventGroups(1)

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/events/1/groups',
        expect.anything()
      )
      expect(result).toEqual(mockGroups)
    })
  })

  describe('Rule APIs', () => {
    test('getRule fetches rule by ID', async () => {
      const mockRule = {
        id: 10,
        name: 'Submission Guidelines',
        type: 'submission',
        description: 'Rules for submitting entries',
      }
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockRule))

      const result = await apiClient.getRule(10)

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/rules/10',
        expect.anything()
      )
      expect(result).toEqual(mockRule)
    })
  })

  describe('Group APIs', () => {
    test('getGroup fetches group by ID', async () => {
      const mockGroup = {
        id: 1,
        name: 'Team Alpha',
        visibility: 'public',
        max_members: 5,
      }
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockGroup))

      const result = await apiClient.getGroup(1)

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/groups/1',
        expect.anything()
      )
      expect(result).toEqual(mockGroup)
    })

    test('getGroupMembers fetches members with filters', async () => {
      const mockMembers = {
        items: [{ id: 1, group_id: 1, user_id: 1, role: 'owner', status: 'accepted' }],
        total: 1,
        skip: 0,
        limit: 100,
      }
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockMembers))

      const result = await apiClient.getGroupMembers(1, 0, 100, { status: 'accepted' })

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/groups/1/members?skip=0&limit=100&status=accepted',
        expect.anything()
      )
      expect(result).toEqual(mockMembers)
    })

    test('createGroup sends POST request', async () => {
      const mockGroup = { id: 1, name: 'New Team', visibility: 'public' }
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockGroup))

      const data = { name: 'New Team', visibility: 'public' as const }
      await apiClient.createGroup(data)

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/groups',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(data),
        })
      )
    })
  })

  describe('Error handling', () => {
    test('throws error on non-OK response', async () => {
      mockFetch.mockReturnValueOnce(mockErrorResponse(404, 'User not found'))

      await expect(apiClient.getUser(999)).rejects.toThrow('User not found')
    })

    test('throws HTTP status on unknown error format', async () => {
      mockFetch.mockReturnValueOnce(
        Promise.resolve({
          ok: false,
          status: 500,
          json: () => Promise.reject(new Error('Parse error')),
        } as Response)
      )

      await expect(apiClient.getUser(1)).rejects.toThrow('Unknown error')
    })

    test('handles 204 No Content response', async () => {
      mockFetch.mockReturnValueOnce(
        Promise.resolve({
          ok: true,
          status: 204,
          json: () => Promise.resolve({}),
        } as Response)
      )

      const result = await apiClient.deletePost(1)
      expect(result).toEqual({})
    })
  })

  describe('Auth APIs', () => {
    test('login sends POST request', async () => {
      const mockResponse = { user_id: 1, username: 'testuser', role: 'participant' }
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockResponse))

      const result = await apiClient.login('testuser', 'password123')

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/auth/login',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ username: 'testuser', password: 'password123' }),
        })
      )
      expect(result).toEqual(mockResponse)
    })

    test('register skips auth header', async () => {
      const mockResponse = { user_id: 1, username: 'newuser', role: 'participant' }
      mockFetch.mockReturnValueOnce(mockJsonResponse(mockResponse))

      await apiClient.register({
        username: 'newuser',
        email: 'new@example.com',
        password: 'password123',
        role: 'participant',
      })

      // Verify skipAuth works (no X-User-Id header)
      expect(mockFetch).toHaveBeenCalled()
      const callArgs = mockFetch.mock.calls[0]
      expect(callArgs[1].headers['X-User-Id']).toBeUndefined()
    })
  })
})
