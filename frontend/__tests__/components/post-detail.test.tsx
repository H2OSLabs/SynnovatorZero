import { render, screen, waitFor } from "@testing-library/react"
import { PostDetail } from "@/components/pages/post-detail"

describe("PostDetail", () => {
  it("renders without crashing", async () => {
    render(<PostDetail postId={1} />)
    await waitFor(() => {
      expect(screen.getByText("协创者")).toBeInTheDocument()
    })
  })

  it("renders the header with brand name", async () => {
    render(<PostDetail postId={1} />)
    await waitFor(() => {
      expect(screen.getByText("协创者")).toBeInTheDocument()
    })
  })

  it("renders the post title from API", async () => {
    render(<PostDetail postId={1} />)
    await waitFor(() => {
      expect(screen.getByText("帖子名帖子名帖子名帖子名帖子名帖子名帖子名帖子名")).toBeInTheDocument()
    })
  })

  it("renders content section", async () => {
    render(<PostDetail postId={1} />)
    await waitFor(() => {
      expect(screen.getByText("内容详情")).toBeInTheDocument()
    })
  })

  it("renders hot topics sidebar", async () => {
    render(<PostDetail postId={1} />)
    await waitFor(() => {
      expect(screen.getByText("协创热点榜")).toBeInTheDocument()
    })
  })
})
