import { render, screen, waitFor } from "@testing-library/react"
import { FollowingList } from "@/components/pages/following-list"

describe("FollowingList", () => {
  it("renders without crashing", async () => {
    render(<FollowingList userId={1} />)
    await waitFor(() => {
      expect(screen.getByText("协创者")).toBeInTheDocument()
    })
  })

  it("renders the header with brand name", async () => {
    render(<FollowingList userId={1} />)
    await waitFor(() => {
      expect(screen.getByText("协创者")).toBeInTheDocument()
    })
  })

  it("renders the publish button", async () => {
    render(<FollowingList userId={1} />)
    await waitFor(() => {
      expect(screen.getByText("发布新内容")).toBeInTheDocument()
    })
  })

  it("renders the friends tab", async () => {
    render(<FollowingList userId={1} />)
    await waitFor(() => {
      expect(screen.getByText(/全部好友/)).toBeInTheDocument()
    })
  })

  it("renders the promo banner", async () => {
    render(<FollowingList userId={1} />)
    await waitFor(() => {
      expect(screen.getByText("来协创,创个业")).toBeInTheDocument()
    })
  })
})
