import { render, screen } from "@testing-library/react"
import { UserProfile } from "@/components/pages/user-profile"

describe("UserProfile", () => {
  it("renders without crashing", () => {
    render(<UserProfile />)
  })

  it("renders the header with brand name", () => {
    render(<UserProfile />)
    expect(screen.getByText("协创者")).toBeInTheDocument()
  })

  it("renders the user name", () => {
    render(<UserProfile />)
    expect(screen.getByText("他人名字")).toBeInTheDocument()
  })

  it("renders the follow button", () => {
    render(<UserProfile />)
    expect(screen.getByRole("button", { name: "关注" })).toBeInTheDocument()
  })

  it("renders the assets section", () => {
    render(<UserProfile />)
    expect(screen.getByText("资产")).toBeInTheDocument()
  })

  it("renders profile tabs", () => {
    render(<UserProfile />)
    expect(screen.getByRole("tab", { name: "帖子" })).toBeInTheDocument()
    expect(screen.getByRole("tab", { name: "提案" })).toBeInTheDocument()
    expect(screen.getByRole("tab", { name: "收藏" })).toBeInTheDocument()
  })
})
