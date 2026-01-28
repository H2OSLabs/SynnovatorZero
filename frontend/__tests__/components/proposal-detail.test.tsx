import { render, screen, waitFor } from "@testing-library/react"
import { ProposalDetail } from "@/components/pages/proposal-detail"

describe("ProposalDetail", () => {
  it("renders without crashing", async () => {
    render(<ProposalDetail postId={1} />)
    await waitFor(() => {
      expect(screen.getByText("协创者")).toBeInTheDocument()
    })
  })

  it("renders the header with brand name", async () => {
    render(<ProposalDetail postId={1} />)
    await waitFor(() => {
      expect(screen.getByText("协创者")).toBeInTheDocument()
    })
  })

  it("renders the back link", async () => {
    render(<ProposalDetail postId={1} />)
    await waitFor(() => {
      expect(screen.getByText("返回提案广场")).toBeInTheDocument()
    })
  })

  it("renders detail tabs", async () => {
    render(<ProposalDetail postId={1} />)
    await waitFor(() => {
      expect(screen.getByRole("tab", { name: "提案详情" })).toBeInTheDocument()
      expect(screen.getByRole("tab", { name: "团队信息" })).toBeInTheDocument()
      expect(screen.getByRole("tab", { name: "评论区" })).toBeInTheDocument()
      expect(screen.getByRole("tab", { name: "版本历史" })).toBeInTheDocument()
    })
  })

  it("renders the team info sidebar", async () => {
    render(<ProposalDetail postId={1} />)
    await waitFor(() => {
      expect(screen.getByText("Alibaba Innovation Lab")).toBeInTheDocument()
    })
  })

  it("renders project milestones", async () => {
    render(<ProposalDetail postId={1} />)
    await waitFor(() => {
      expect(screen.getByText("项目里程碑")).toBeInTheDocument()
    })
  })
})
