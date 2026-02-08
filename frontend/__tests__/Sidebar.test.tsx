import { render } from "@testing-library/react"
import { Sidebar } from "@/components/layout/Sidebar"

const LinkMock = jest.fn(
  ({
    href,
    children,
  }: {
    href: string
    children: React.ReactNode
    prefetch?: boolean
  }) => <a href={href}>{children}</a>
)

jest.mock("next/link", () => ({
  __esModule: true,
  default: (props: { href: string; children: React.ReactNode; prefetch?: boolean }) => LinkMock(props),
}))

jest.mock("@/contexts/AuthContext", () => ({
  useAuth: () => ({
    user: { user_id: 1, username: "test", role: "participant" },
  }),
}))

// 需要认证的页面路径
const authRequiredPaths = [
  "/notifications",
  "/my/events",
  "/my/posts",
  "/my/groups",
  "/my/favorites",
  "/my/following",
]

// 公开页面路径
const publicPaths = ["/", "/explore", "/events", "/camps", "/posts", "/groups"]

describe("Sidebar", () => {
  beforeEach(() => {
    LinkMock.mockClear()
  })

  it.each(authRequiredPaths)("认证页面 %s 禁用预取", (path) => {
    render(<Sidebar collapsed={false} />)

    const call = LinkMock.mock.calls.find(([props]) => props.href === path)
    expect(call?.[0].prefetch).toBe(false)
  })

  it.each(publicPaths)("公开页面 %s 启用预取", (path) => {
    render(<Sidebar collapsed={false} />)

    const call = LinkMock.mock.calls.find(([props]) => props.href === path)
    expect(call?.[0].prefetch).toBe(true)
  })
})
