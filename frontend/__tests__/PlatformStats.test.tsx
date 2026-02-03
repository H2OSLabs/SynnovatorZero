import { render, screen, waitFor, act } from '@testing-library/react'
import { PlatformStats } from '@/components/home'

// Mock fetch
const mockFetch = jest.fn()
global.fetch = mockFetch

describe('PlatformStats', () => {
  beforeEach(() => {
    mockFetch.mockClear()
  })

  it('renders loading state initially', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({
        user_count: 100,
        category_count: 10,
        post_count: 50,
      }),
    })

    await act(async () => {
      render(<PlatformStats />)
    })

    expect(screen.getByText('平台统计')).toBeInTheDocument()
    expect(screen.getByText('注册用户')).toBeInTheDocument()
    expect(screen.getByText('活动数量')).toBeInTheDocument()
    expect(screen.getByText('作品数量')).toBeInTheDocument()
  })

  it('fetches and displays stats', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({
        user_count: 100,
        category_count: 10,
        post_count: 50,
      }),
    })

    await act(async () => {
      render(<PlatformStats />)
    })

    await waitFor(() => {
      expect(screen.getByText('100')).toBeInTheDocument()
    })

    expect(screen.getByText('10')).toBeInTheDocument()
    expect(screen.getByText('50')).toBeInTheDocument()
  })

  it('shows error state on fetch failure', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
    })

    await act(async () => {
      render(<PlatformStats />)
    })

    await waitFor(() => {
      expect(screen.getByText('加载统计数据失败')).toBeInTheDocument()
    })

    expect(screen.getByText('重试')).toBeInTheDocument()
  })

  it('calls API with correct URL', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({
        user_count: 0,
        category_count: 0,
        post_count: 0,
      }),
    })

    await act(async () => {
      render(<PlatformStats />)
    })

    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/stats')
      )
    })
  })

  it('formats large numbers with locale string', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({
        user_count: 1000000,
        category_count: 10,
        post_count: 50,
      }),
    })

    await act(async () => {
      render(<PlatformStats />)
    })

    await waitFor(() => {
      // toLocaleString() should format 1000000 with comma separators
      expect(screen.getByText('1,000,000')).toBeInTheDocument()
    })
  })
})
