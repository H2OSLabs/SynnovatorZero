import { render, screen, waitFor } from "@testing-library/react"
import { Assets } from "@/components/pages/assets"

describe("Assets", () => {
  it("renders without crashing", async () => {
    render(<Assets />)
    await waitFor(() => {
      expect(screen.getByText("协创者")).toBeInTheDocument()
    })
  })

  it("renders the header with brand name", async () => {
    render(<Assets />)
    await waitFor(() => {
      expect(screen.getByText("协创者")).toBeInTheDocument()
    })
  })

  it("renders the page title", async () => {
    render(<Assets />)
    await waitFor(() => {
      expect(screen.getByText("我的资产")).toBeInTheDocument()
    })
  })

  it("renders asset filter categories", async () => {
    render(<Assets />)
    await waitFor(() => {
      expect(screen.getByText("全部")).toBeInTheDocument()
      expect(screen.getByText("图片")).toBeInTheDocument()
      expect(screen.getByText("文件")).toBeInTheDocument()
    })
  })

  it("renders fallback asset cards when API returns empty", async () => {
    render(<Assets />)
    await waitFor(() => {
      const titles = screen.getAllByText("大赛官方天翼云算力")
      expect(titles.length).toBeGreaterThan(0)
    })
  })
})
