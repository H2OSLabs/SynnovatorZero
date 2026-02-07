import { render, screen } from "@testing-library/react"
import { Header } from "@/components/layout/Header"

jest.mock("next/link", () => ({
  __esModule: true,
  default: ({ href, children, ...props }: { href: string; children: React.ReactNode }) => (
    <a href={href} {...props}>
      {children}
    </a>
  ),
}))

jest.mock("@/components/ui/dropdown-menu", () => ({
  DropdownMenu: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  DropdownMenuTrigger: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  DropdownMenuContent: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  DropdownMenuItem: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  DropdownMenuSeparator: () => <div />,
}))

jest.mock("@/components/notification/NotificationDropdown", () => ({
  NotificationDropdown: () => null,
}))

jest.mock("@/components/search/SearchModal", () => ({
  SearchModal: () => null,
}))

jest.mock("@/contexts/AuthContext", () => ({
  useAuth: () => ({
    user: { user_id: 1, username: "test", role: "participant" },
    logout: jest.fn(),
    isOrganizer: false,
    isAdmin: false,
  }),
}))

describe("Header", () => {
  it("用户菜单中的“我的帖子/我的团队”不会指向不存在的 /my 路由", () => {
    render(<Header />)

    const myPosts = screen.getByText("我的帖子").closest("a")
    const myGroups = screen.getByText("我的团队").closest("a")

    expect(myPosts).toHaveAttribute("href", "/posts")
    expect(myGroups).toHaveAttribute("href", "/groups")
  })
})
