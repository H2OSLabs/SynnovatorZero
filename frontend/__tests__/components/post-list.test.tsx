import { render, screen } from "@testing-library/react"
import { PostList } from "@/components/pages/post-list"

describe("PostList", () => {
  it("renders without crashing", () => {
    render(<PostList />)
  })

  it("renders the header with brand name", () => {
    render(<PostList />)
    expect(screen.getByText("协创者")).toBeInTheDocument()
  })

  it("renders the publish button", () => {
    render(<PostList />)
    expect(screen.getByText("发布新内容")).toBeInTheDocument()
  })

  it("renders the tabs row", () => {
    render(<PostList />)
    expect(screen.getByText("帖子")).toBeInTheDocument()
    expect(screen.getByText("提案广场")).toBeInTheDocument()
  })

  it("renders section headers", () => {
    render(<PostList />)
    expect(screen.getAllByText("找队友").length).toBeGreaterThan(0)
    expect(screen.getAllByText("找点子").length).toBeGreaterThan(0)
  })
})
