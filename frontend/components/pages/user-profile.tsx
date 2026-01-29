"use client"

import { Share2, Wallet } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { AppLayout } from "@/components/layout/app-layout"

const stats = [
  { value: "12", label: "帖子" },
  { value: "6", label: "关注" },
  { value: "6", label: "粉丝" },
]

const assets = [
  { title: "AI/Agent", detail: "0 TOPS" },
  { title: "证书", detail: "1张证书" },
  { title: "文件", detail: "15个文件" },
]

const profileTabs = ["帖子", "提案", "收藏", "更多"]

export function UserProfile({ userId }: { userId: number }) {
  const router = useRouter()
  const [user, setUser] = useState<UserType | null>(null)
  const [following, setFollowing] = useState<UserUserRelation[]>([])
  const [followers, setFollowers] = useState<UserUserRelation[]>([])
  const [loading, setLoading] = useState(true)
  const [isFollowing, setIsFollowing] = useState(false)
  const [activeTab, setActiveTab] = useState("帖子")

  async function handleFollow() {
    try {
      if (isFollowing) {
        await unfollowUser(userId, 1)
      } else {
        await followUser(userId, 1)
      }
      setIsFollowing(!isFollowing)
    } catch (err) {
      console.error("Follow action failed:", err)
    }
  }

  useEffect(() => {
    let cancelled = false
    async function fetchData() {
      setLoading(true)
      try {
        const [userData, followingData, followersData] = await Promise.all([
          getUser(userId),
          getFollowing(userId),
          getFollowers(userId),
        ])
        if (!cancelled) {
          setUser(userData)
          setFollowing(followingData)
          setFollowers(followersData)
        }
      } catch (err) {
        console.error("Failed to fetch user data:", err)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    fetchData()
    return () => { cancelled = true }
  }, [userId])

  const stats = [
    { value: "12", label: "帖子" },
    { value: String(following.length || 6), label: "关注" },
    { value: String(followers.length || 6), label: "粉丝" },
  ]

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-[var(--nf-near-black)]">
        <span className="text-[var(--nf-muted)] text-lg">加载中...</span>
      </div>
    )
  }
  return (
    <AppLayout
      navMode="compact"
      activeNav="探索"
      sidebar={
        <div className="w-full h-full bg-[var(--nf-card-bg)] rounded-[12px]" />
      }
    >
      {/* Profile Header Row */}
      <div className="flex items-center gap-5">
        {/* Avatar */}
        <div className="w-[90px] h-[90px] rounded-full bg-[var(--nf-dark-bg)] shrink-0" />

        {/* Info */}
        <div className="flex flex-col gap-2 flex-1">
          <span className="text-[22px] font-semibold text-[var(--nf-white)]">
            他人名字
          </span>
          <div className="flex items-center gap-6">
            {stats.map((stat) => (
              <div key={stat.label} className="flex items-center gap-1.5">
                <span className="font-mono text-[16px] font-semibold text-[var(--nf-white)]">
                  {stat.value}
                </span>
                <span className="text-[12px] text-[var(--nf-muted)]">
                  {stat.label}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-3 shrink-0">
          <span className="text-[12px] text-[var(--nf-muted)]">粉丝相互</span>
          <Button className="bg-[var(--nf-lime)] text-[var(--nf-surface)] hover:bg-[var(--nf-lime)]/90 rounded-lg px-5 py-2 text-sm font-medium">
            关注
          </Button>
          <Button className="bg-[var(--nf-dark-bg)] text-[var(--nf-light-gray)] hover:bg-[var(--nf-dark-bg)]/80 rounded-lg px-3 py-2">
            <Share2 className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Bio */}
      <p className="text-[13px] text-[var(--nf-muted)]">
        Personal Signature：大学在读生，热爱编程和设计，欢迎互相交流合作！
      </p>

      {/* Asset Section */}
      <div className="flex flex-col gap-3">
        <div className="flex items-center gap-2">
          <Wallet className="w-[18px] h-[18px] text-[var(--nf-lime)]" />
          <span className="text-[16px] font-semibold text-[var(--nf-white)]">资产</span>
        </div>
        <div className="grid grid-cols-3 gap-4">
          {assets.map((asset) => (
            <Card
              key={asset.title}
              className="bg-[var(--nf-card-bg)] border border-[var(--nf-dark-bg)] rounded-[12px] h-[120px] flex flex-col items-start justify-center px-5 gap-1.5"
            >
              <span className="text-[16px] font-bold text-[var(--nf-lime)]">
                {asset.title}
              </span>
              <span className="text-[13px] text-[var(--nf-light-gray)]">
                {asset.detail}
              </span>
            </Card>
          ))}
        </div>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="帖子" className="w-full">
        <TabsList className="w-full justify-start bg-transparent border-b border-[var(--nf-dark-bg)] rounded-none h-auto p-0 gap-0">
          {profileTabs.map((tab) => (
            <TabsTrigger
              key={tab}
              value={tab}
              className="rounded-none border-b-2 border-transparent px-4 py-2.5 text-sm text-[var(--nf-muted)] data-[state=active]:text-[var(--nf-lime)] data-[state=active]:border-[var(--nf-lime)] data-[state=active]:font-semibold data-[state=active]:bg-transparent data-[state=active]:shadow-none"
            >
              {tab}
            </TabsTrigger>
          ))}
        </TabsList>

        <TabsContent value="帖子" className="mt-5">
          <div className="grid grid-cols-3 gap-4">
            {[1, 2, 3].map((item) => (
              <div
                key={item}
                className="w-full h-[260px] rounded-[12px] bg-[var(--nf-dark-bg)]"
              />
            ))}
          </div>
        </TabsContent>

        <TabsContent value="提案" className="mt-5">
          <div className="min-h-[260px] flex items-center justify-center">
            <span className="text-sm text-[var(--nf-muted)]">暂无提案</span>
          </div>
        </TabsContent>

        <TabsContent value="收藏" className="mt-5">
          <div className="min-h-[260px] flex items-center justify-center">
            <span className="text-sm text-[var(--nf-muted)]">暂无收藏</span>
          </div>
        </TabsContent>

        <TabsContent value="更多" className="mt-5">
          <div className="min-h-[260px] flex items-center justify-center">
            <span className="text-sm text-[var(--nf-muted)]">暂无更多内容</span>
          </div>
        </TabsContent>
      </Tabs>
    </AppLayout>
  )
}
