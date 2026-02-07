import { render, screen, waitFor } from '@testing-library/react'
import SettingsPage from '@/app/settings/page'
import { getUser } from '@/lib/api-client'

jest.mock('next/navigation', () => ({
  useRouter: () => ({ push: jest.fn() }),
}))

jest.mock('@/components/layout/PageLayout', () => ({
  PageLayout: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}))

describe('SettingsPage', () => {
  beforeEach(() => {
    localStorage.setItem('synnovator_user', JSON.stringify({ user_id: 1 }))
    ;(getUser as jest.Mock).mockResolvedValue({
      id: 1,
      username: 'testuser',
      email: 'test@example.com',
      role: 'participant',
      display_name: '测试用户',
      bio: '简介',
    })
  })

  afterEach(() => {
    localStorage.clear()
    jest.clearAllMocks()
  })

  it('renders Chinese UI text', async () => {
    render(<SettingsPage />)

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: '设置' })).toBeInTheDocument()
    })

    expect(screen.getByText('个人资料')).toBeInTheDocument()
    expect(screen.getByText('更换头像')).toBeInTheDocument()
    expect(screen.getByText('显示名称')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: '保存修改' })).toBeInTheDocument()
  })
})
