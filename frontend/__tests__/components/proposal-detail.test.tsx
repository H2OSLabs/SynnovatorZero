import { render, screen } from "@testing-library/react"
import { ProposalDetail } from "@/components/pages/proposal-detail"

describe("ProposalDetail", () => {
  it("renders without crashing", () => {
    render(<ProposalDetail />)
  })

  it("renders the header with brand name", () => {
    render(<ProposalDetail />)
    expect(screen.getByText("协创者")).toBeInTheDocument()
  })

  it("renders the proposal title", () => {
    render(<ProposalDetail />)
    expect(screen.getByText("善意百宝——一人人需要扫有轮AI直辅学习平台")).toBeInTheDocument()
  })

  it("renders the back link", () => {
    render(<ProposalDetail />)
    expect(screen.getByText("返回提案广场")).toBeInTheDocument()
  })

  it("renders detail tabs", () => {
    render(<ProposalDetail />)
    expect(screen.getByRole("tab", { name: "提案详情" })).toBeInTheDocument()
    expect(screen.getByRole("tab", { name: "团队信息" })).toBeInTheDocument()
    expect(screen.getByRole("tab", { name: "评论区" })).toBeInTheDocument()
    expect(screen.getByRole("tab", { name: "版本历史" })).toBeInTheDocument()
  })

  it("renders the team info sidebar", () => {
    render(<ProposalDetail />)
    expect(screen.getByText("Alibaba Innovation Lab")).toBeInTheDocument()
  })

  it("renders project milestones", () => {
    render(<ProposalDetail />)
    expect(screen.getByText("项目里程碑")).toBeInTheDocument()
  })
})
