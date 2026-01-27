import { render, screen } from "@testing-library/react"
import { CategoryDetail } from "@/components/pages/category-detail"

describe("CategoryDetail", () => {
  it("renders without crashing", () => {
    render(<CategoryDetail />)
  })

  it("renders the header with brand name", () => {
    render(<CategoryDetail />)
    expect(screen.getByText("协创者")).toBeInTheDocument()
  })

  it("renders the category title", () => {
    render(<CategoryDetail />)
    expect(screen.getByText("西建·滇水源 | 上海第七届大学生AI+国际创业大赛")).toBeInTheDocument()
  })

  it("renders the prize amount", () => {
    render(<CategoryDetail />)
    expect(screen.getByText("880万元")).toBeInTheDocument()
  })

  it("renders detail tabs", () => {
    render(<CategoryDetail />)
    expect(screen.getByText("详情")).toBeInTheDocument()
    expect(screen.getByText("排榜")).toBeInTheDocument()
    expect(screen.getByText("讨论区")).toBeInTheDocument()
  })
})
