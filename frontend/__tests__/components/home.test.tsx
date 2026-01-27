import { render, screen } from "@testing-library/react"
import { Home } from "@/components/pages/home"

describe("Home", () => {
  it("renders without crashing", () => {
    render(<Home />)
  })

  it("renders the header with brand name", () => {
    render(<Home />)
    expect(screen.getByText("协创者")).toBeInTheDocument()
  })

  it("renders the publish button", () => {
    render(<Home />)
    expect(screen.getAllByText("发布新内容").length).toBeGreaterThan(0)
  })

  it("renders navigation sidebar items", () => {
    render(<Home />)
    expect(screen.getByText("探索")).toBeInTheDocument()
    expect(screen.getByText("星球")).toBeInTheDocument()
    expect(screen.getByText("营地")).toBeInTheDocument()
  })

  it("renders the hot proposals section", () => {
    render(<Home />)
    expect(screen.getByText("热门提案")).toBeInTheDocument()
  })

  it("renders the promo banner", () => {
    render(<Home />)
    expect(screen.getByText("来协创,创个业")).toBeInTheDocument()
  })
})
