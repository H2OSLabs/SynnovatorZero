import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import { AuthProvider, useAuth } from '@/contexts/AuthContext'
import { getUser } from '@/lib/api-client'

const mockGetUser = getUser

function Consumer() {
  const { user, isLoading } = useAuth()
  if (isLoading) return React.createElement('div', null, 'loading')
  return React.createElement('div', null, user ? user.username : 'anonymous')
}

describe('AuthContext', () => {
  const STORAGE_KEY = 'synnovator_user'

  beforeEach(() => {
    localStorage.clear()
    ;(mockGetUser as any).mockReset()
  })

  it('clears stale localStorage user when user does not exist', async () => {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({ user_id: 999, username: 'stale', role: 'participant' })
    )
    ;(mockGetUser as any).mockRejectedValueOnce(new Error('User not found'))

    render(React.createElement(AuthProvider, null, React.createElement(Consumer)))

    await waitFor(() => {
      expect(screen.getByText('anonymous')).toBeInTheDocument()
    })

    expect(localStorage.getItem(STORAGE_KEY)).toBeNull()
  })

  it('keeps localStorage user when user exists', async () => {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({ user_id: 1, username: 'testuser', role: 'participant' })
    )
    ;(mockGetUser as any).mockResolvedValueOnce({
      id: 1,
      username: 'testuser',
      email: 'test@example.com',
      role: 'participant',
      follower_count: 0,
      following_count: 0,
    })

    render(React.createElement(AuthProvider, null, React.createElement(Consumer)))

    await waitFor(() => {
      expect(screen.getByText('testuser')).toBeInTheDocument()
    })

    expect(localStorage.getItem(STORAGE_KEY)).not.toBeNull()
  })
})

