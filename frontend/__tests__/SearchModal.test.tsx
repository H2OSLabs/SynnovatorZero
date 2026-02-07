import { render, screen, fireEvent, waitFor, act } from '@testing-library/react'
import { SearchModal } from '@/components/search'

// Mock search-api
jest.mock('@/lib/search-api', () => ({
  searchAll: jest.fn().mockResolvedValue({
    users: [],
    events: [],
    posts: [],
  }),
}))

describe('SearchModal', () => {
  it('renders without crashing', () => {
    render(<SearchModal />)
    // Modal is hidden by default, so nothing should be visible
  })

  it('opens with ⌘K keyboard shortcut', async () => {
    render(<SearchModal />)

    // Simulate ⌘K
    await act(async () => {
      fireEvent.keyDown(document, { key: 'k', metaKey: true })
    })

    await waitFor(() => {
      expect(screen.getByPlaceholderText(/搜索/)).toBeInTheDocument()
    })
  })

  it('opens with Ctrl+K keyboard shortcut', async () => {
    render(<SearchModal />)

    // Simulate Ctrl+K
    await act(async () => {
      fireEvent.keyDown(document, { key: 'k', ctrlKey: true })
    })

    await waitFor(() => {
      expect(screen.getByPlaceholderText(/搜索/)).toBeInTheDocument()
    })
  })

  it('can be opened via defaultOpen prop', async () => {
    await act(async () => {
      render(<SearchModal defaultOpen={true} />)
    })

    expect(screen.getByPlaceholderText(/搜索/)).toBeInTheDocument()
  })

  it('shows empty state message when no query', async () => {
    await act(async () => {
      render(<SearchModal defaultOpen={true} />)
    })

    expect(screen.getByText(/输入关键词/)).toBeInTheDocument()
  })

  it('keyboard shortcut toggles modal open state', async () => {
    render(<SearchModal />)

    // Initially modal should not be visible
    expect(screen.queryByPlaceholderText(/搜索/)).not.toBeInTheDocument()

    // Open with ⌘K
    await act(async () => {
      fireEvent.keyDown(document, { key: 'k', metaKey: true })
    })

    // Modal should now be visible
    await waitFor(() => {
      expect(screen.getByPlaceholderText(/搜索/)).toBeInTheDocument()
    })

    // Close with ⌘K again
    await act(async () => {
      fireEvent.keyDown(document, { key: 'k', metaKey: true })
    })

    // Modal should be hidden
    await waitFor(() => {
      expect(screen.queryByPlaceholderText(/搜索/)).not.toBeInTheDocument()
    })
  })
})
