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

describe("Sidebar", () => {
  beforeEach(() => {
    LinkMock.mockClear()
  })

  it("“我的帖子”链接禁用预取，避免 Next 预取请求被中止时报错", () => {
    render(<Sidebar collapsed={false} />)

    const myPostsCall = LinkMock.mock.calls.find(([props]) => props.href === "/my/posts")
    expect(myPostsCall?.[0].prefetch).toBe(false)
  })
})

