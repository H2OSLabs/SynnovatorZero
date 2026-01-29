import { render, screen, waitFor } from "@testing-library/react"
import { Team } from "@/components/pages/team"

describe("Team", () => {
  it("renders without crashing", async () => {
    render(<Team groupId={1} />)
    await waitFor(() => {
      expect(screen.getByText("协创者")).toBeInTheDocument()
    })
  })

  it("renders the header with brand name", async () => {
    render(<Team groupId={1} />)
    await waitFor(() => {
      expect(screen.getByText("协创者")).toBeInTheDocument()
    })
  })

  it("renders the team name from API", async () => {
    render(<Team groupId={1} />)
    await waitFor(() => {
      expect(screen.getByRole("heading", { name: "团队" })).toBeInTheDocument()
    })
  })

  it("renders the manage button", async () => {
    render(<Team groupId={1} />)
    await waitFor(() => {
      expect(screen.getByText("管理面板")).toBeInTheDocument()
    })
  })

  it("renders the members section", async () => {
    render(<Team groupId={1} />)
    await waitFor(() => {
      expect(screen.getByText("队员")).toBeInTheDocument()
    })
  })

  it("renders the assets section", async () => {
    render(<Team groupId={1} />)
    await waitFor(() => {
      expect(screen.getByText("资产")).toBeInTheDocument()
    })
  })

  it("renders team tabs", async () => {
    render(<Team groupId={1} />)
    await waitFor(() => {
      expect(screen.getByRole("tab", { name: "提案" })).toBeInTheDocument()
      expect(screen.getByRole("tab", { name: "帖子" })).toBeInTheDocument()
      expect(screen.getByRole("tab", { name: "收藏" })).toBeInTheDocument()
    })
  })
})
