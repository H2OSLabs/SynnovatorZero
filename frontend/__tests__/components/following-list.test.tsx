import { render, screen } from "@testing-library/react"
import { FollowingList } from "@/components/pages/following-list"

describe("FollowingList", () => {
  it("renders without crashing", () => {
    render(<FollowingList />)
  })

  it("renders the header with brand name", () => {
    render(<FollowingList />)
    expect(screen.getByText("协创者")).toBeInTheDocument()
  })

  it("renders the publish button", () => {
    render(<FollowingList />)
    expect(screen.getByText("发布新内容")).toBeInTheDocument()
  })

  it("renders the friends tab", () => {
    render(<FollowingList />)
    expect(screen.getByText("全部好友")).toBeInTheDocument()
  })

  it("renders the promo banner", () => {
    render(<FollowingList />)
    expect(screen.getByText("来协创,创个业")).toBeInTheDocument()
  })
})
