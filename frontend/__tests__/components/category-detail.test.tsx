import { render, screen, waitFor } from "@testing-library/react"
import { CategoryDetail } from "@/components/pages/category-detail"

describe("CategoryDetail", () => {
  it("renders without crashing", async () => {
    render(<CategoryDetail categoryId={1} />)
    await waitFor(() => {
      expect(screen.getByText("协创者")).toBeInTheDocument()
    })
  })

  it("renders the header with brand name", async () => {
    render(<CategoryDetail categoryId={1} />)
    await waitFor(() => {
      expect(screen.getByText("协创者")).toBeInTheDocument()
    })
  })

  it("renders the category title from API", async () => {
    render(<CategoryDetail categoryId={1} />)
    await waitFor(() => {
      expect(screen.getByText(/西建·滇水源/)).toBeInTheDocument()
    })
  })

  it("renders detail tabs", async () => {
    render(<CategoryDetail categoryId={1} />)
    await waitFor(() => {
      expect(screen.getByText("详情")).toBeInTheDocument()
      expect(screen.getByText("排榜")).toBeInTheDocument()
      expect(screen.getByText("讨论区")).toBeInTheDocument()
    })
  })
})
