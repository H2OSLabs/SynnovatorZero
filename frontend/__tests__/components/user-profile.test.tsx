import { render, screen, waitFor } from "@testing-library/react"
import { UserProfile } from "@/components/pages/user-profile"

describe("UserProfile", () => {
  it("renders without crashing", async () => {
    render(<UserProfile userId={1} />)
    await waitFor(() => {
      expect(screen.getByText("协创者")).toBeInTheDocument()
    })
  })

  it("renders the header with brand name", async () => {
    render(<UserProfile userId={1} />)
    await waitFor(() => {
      expect(screen.getByText("协创者")).toBeInTheDocument()
    })
  })

  it("renders the user name from API", async () => {
    render(<UserProfile userId={1} />)
    await waitFor(() => {
      expect(screen.getByText("他人名字")).toBeInTheDocument()
    })
  })

  it("renders the follow button", async () => {
    render(<UserProfile userId={1} />)
    await waitFor(() => {
      expect(screen.getByRole("button", { name: "关注" })).toBeInTheDocument()
    })
  })

  it("renders the assets section", async () => {
    render(<UserProfile userId={1} />)
    await waitFor(() => {
      expect(screen.getByText("资产")).toBeInTheDocument()
    })
  })

  it("renders profile tabs", async () => {
    render(<UserProfile userId={1} />)
    await waitFor(() => {
      expect(screen.getByRole("tab", { name: "帖子" })).toBeInTheDocument()
      expect(screen.getByRole("tab", { name: "提案" })).toBeInTheDocument()
      expect(screen.getByRole("tab", { name: "收藏" })).toBeInTheDocument()
    })
  })
})
