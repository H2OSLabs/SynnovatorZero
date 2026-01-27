import { render, screen } from "@testing-library/react"
import { ProposalList } from "@/components/pages/proposal-list"

describe("ProposalList", () => {
  it("renders without crashing", () => {
    render(<ProposalList />)
  })

  it("renders the header with brand name", () => {
    render(<ProposalList />)
    expect(screen.getByText("协创者")).toBeInTheDocument()
  })

  it("renders the publish button", () => {
    render(<ProposalList />)
    expect(screen.getByText("发布新内容")).toBeInTheDocument()
  })

  it("renders the active tab badge", () => {
    render(<ProposalList />)
    expect(screen.getByText("提案广场")).toBeInTheDocument()
  })

  it("renders the filter row", () => {
    render(<ProposalList />)
    expect(screen.getByText("赛道探索")).toBeInTheDocument()
  })
})
