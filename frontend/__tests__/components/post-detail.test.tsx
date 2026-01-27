import { render, screen } from "@testing-library/react"
import { PostDetail } from "@/components/pages/post-detail"

describe("PostDetail", () => {
  it("renders without crashing", () => {
    render(<PostDetail />)
  })

  it("renders the header with brand name", () => {
    render(<PostDetail />)
    expect(screen.getByText("协创者")).toBeInTheDocument()
  })

  it("renders the post title", () => {
    render(<PostDetail />)
    expect(screen.getByText("帖子名帖子名帖子名帖子名帖子名帖子名帖子名帖子名")).toBeInTheDocument()
  })

  it("renders related cards section", () => {
    render(<PostDetail />)
    expect(screen.getByText("关联卡片")).toBeInTheDocument()
  })

  it("renders content section", () => {
    render(<PostDetail />)
    expect(screen.getByText("内容详情")).toBeInTheDocument()
  })

  it("renders hot topics sidebar", () => {
    render(<PostDetail />)
    expect(screen.getByText("协创热点榜")).toBeInTheDocument()
  })
})
