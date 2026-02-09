jest.mock('../lib/env', () => ({
  getEnv: () => ({ API_URL: 'http://example.test/api' }),
}))

describe('search-api', () => {
  const originalFetch = global.fetch
  const mockFetch = jest.fn()

  beforeAll(() => {
    global.fetch = mockFetch
  })

  afterAll(() => {
    global.fetch = originalFetch
  })

  beforeEach(() => {
    mockFetch.mockReset()
  })

  it('searchUsers 结果链接指向 /users/:id', async () => {
    const { searchUsers } = await import('../lib/search-api')

    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => ({
        items: [
          { id: 1, username: 'alice', display_name: 'Alice' },
          { id: 2, username: 'bob', display_name: 'Bob' },
        ],
        total: 2,
      }),
    } as Response)

    const results = await searchUsers('ali', 5)

    expect(mockFetch).toHaveBeenCalledWith('http://example.test/api/users?limit=100')
    expect(results[0]?.url).toBe('/users/1')
  })

  it('searchPosts 结果链接统一指向 /posts/:id', async () => {
    const { searchPosts } = await import('../lib/search-api')

    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => ({
        items: [
          { id: 10, title: 'P1', type: 'proposal', status: 'published', created_by: 1 },
          { id: 11, title: 'G1', type: 'general', status: 'published', created_by: 1 },
        ],
        total: 2,
      }),
    } as Response)

    const results = await searchPosts('1', 5)

    expect(mockFetch).toHaveBeenCalledWith('http://example.test/api/posts?limit=100&status=published')
    expect(results.map(r => r.url)).toEqual(['/posts/10', '/posts/11'])
  })
})
