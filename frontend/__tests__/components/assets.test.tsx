import { render, screen } from "@testing-library/react"
import { Assets } from "@/components/pages/assets"

describe("Assets", () => {
  it("renders without crashing", () => {
    render(<Assets />)
  })

  it("renders the header with brand name", () => {
    render(<Assets />)
    expect(screen.getByText("协创者")).toBeInTheDocument()
  })

  it("renders the page title", () => {
    render(<Assets />)
    expect(screen.getByText("我的资产")).toBeInTheDocument()
  })

  it("renders asset category tabs", () => {
    render(<Assets />)
    expect(screen.getByText("AI/Agent")).toBeInTheDocument()
    expect(screen.getByText("证书")).toBeInTheDocument()
    expect(screen.getByText("文件")).toBeInTheDocument()
  })

  it("renders asset cards", () => {
    render(<Assets />)
    const titles = screen.getAllByText("大赛官方天翼云算力")
    expect(titles.length).toBeGreaterThan(0)
  })
})
