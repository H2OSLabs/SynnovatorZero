import { render } from "@testing-library/react"
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
  { name: "HomePage", Component: HomePage },
  { name: "PostsPage", Component: PostsPage },
  { name: "PostDetailPage", Component: PostDetailPage },
  { name: "ProposalsPage", Component: ProposalsPage },
  { name: "ProposalDetailPage", Component: ProposalDetailPage },
  { name: "CategoryDetailPage", Component: CategoryDetailPage },
  { name: "ProfilePage", Component: ProfilePage },
  { name: "TeamPage", Component: TeamPage },
  { name: "FollowingPage", Component: FollowingPage },
  { name: "AssetsPage", Component: AssetsPage },
]

describe("Route Pages", () => {
  it.each(routePages)("$name renders without crashing", ({ Component }) => {
    const { container } = render(<Component />)
    expect(container).toBeTruthy()
  })
})
