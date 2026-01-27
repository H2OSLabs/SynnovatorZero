import { render, screen } from "@testing-library/react"
import { Team } from "@/components/pages/team"

describe("Team", () => {
  it("renders without crashing", () => {
    render(<Team />)
  })

  it("renders the header with brand name", () => {
    render(<Team />)
    expect(screen.getByText("协创者")).toBeInTheDocument()
  })

  it("renders the team name", () => {
    render(<Team />)
    expect(screen.getByRole("heading", { name: "团队" })).toBeInTheDocument()
  })

  it("renders the manage button", () => {
    render(<Team />)
    expect(screen.getByText("管理面板")).toBeInTheDocument()
  })

  it("renders the members section", () => {
    render(<Team />)
    expect(screen.getByText("队员")).toBeInTheDocument()
  })

  it("renders the assets section", () => {
    render(<Team />)
    expect(screen.getByText("资产")).toBeInTheDocument()
  })

  it("renders team tabs", () => {
    render(<Team />)
    expect(screen.getByRole("tab", { name: "提案" })).toBeInTheDocument()
    expect(screen.getByRole("tab", { name: "帖子" })).toBeInTheDocument()
    expect(screen.getByRole("tab", { name: "收藏" })).toBeInTheDocument()
  })
})
