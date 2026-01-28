import { render, waitFor } from "@testing-library/react"
import HomePage from "@/app/page"
import PostsPage from "@/app/posts/page"
import PostDetailPage from "@/app/posts/[id]/page"
import ProposalsPage from "@/app/proposals/page"
import ProposalDetailPage from "@/app/proposals/[id]/page"
import CategoryDetailPage from "@/app/categories/[id]/page"
import ProfilePage from "@/app/profile/page"
import TeamPage from "@/app/team/page"
import FollowingPage from "@/app/following/page"
import AssetsPage from "@/app/assets/page"

const routePages = [
  { name: "HomePage", Component: HomePage, props: {} },
  { name: "PostsPage", Component: PostsPage, props: {} },
  { name: "PostDetailPage", Component: PostDetailPage, props: { params: { id: "1" } } },
  { name: "ProposalsPage", Component: ProposalsPage, props: {} },
  { name: "ProposalDetailPage", Component: ProposalDetailPage, props: { params: { id: "1" } } },
  { name: "CategoryDetailPage", Component: CategoryDetailPage, props: { params: { id: "1" } } },
  { name: "ProfilePage", Component: ProfilePage, props: {} },
  { name: "TeamPage", Component: TeamPage, props: {} },
  { name: "FollowingPage", Component: FollowingPage, props: {} },
  { name: "AssetsPage", Component: AssetsPage, props: {} },
]

describe("Route Pages", () => {
  it.each(routePages)("$name renders without crashing", async ({ Component, props }) => {
    const { container } = render(<Component {...(props as any)} />)
    await waitFor(() => {
      expect(container).toBeTruthy()
    })
  })
})
