"use client"

import { useState, useEffect } from "react"
import {
  Menu, Search, Zap, Bell, User,
  Compass, Globe, Mountain,
  Share2, Wallet,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { getUser, getFollowing, getFollowers } from "@/lib/api-client"
import type { User as UserType, UserUserRelation } from "@/lib/types"

const assets = [
  { title: "AI/Agent", detail: "0 TOPS" },
  { title: "证书", detail: "1张证书" },
  { title: "文件", detail: "15个文件" },
]

const profileTabs = ["帖子", "提案", "收藏", "更多"]

export function UserProfile({ userId }: { userId: number }) {
  const [user, setUser] = useState<UserType | null>(null)
  const [following, setFollowing] = useState<UserUserRelation[]>([])
  const [followers, setFollowers] = useState<UserUserRelation[]>([])
  const [loading, setLoading] = useState(true)

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
    <div className="flex flex-col h-screen bg-[var(--nf-near-black)]">
      {/* Header */}
      <header className="flex items-center justify-between h-14 px-6 border-b border-[var(--nf-dark-bg)] bg-[var(--nf-near-black)]">
        <div className="flex items-center gap-4">
          <Menu className="w-6 h-6 text-[var(--nf-white)]" />
          <span className="font-heading text-[20px] font-bold text-[var(--nf-lime)]">
            协创者
          </span>
        </div>
        <div className="flex items-center gap-2 w-[400px] bg-[var(--nf-card-bg)] border border-[var(--nf-dark-bg)] rounded-[21px] px-5 py-2.5">
          <Search className="w-4 h-4 text-[var(--nf-muted)]" />
          <span className="text-sm text-[var(--nf-muted)]">搜索</span>
        </div>
        <div className="flex items-center gap-3">
          <Button className="bg-[var(--nf-lime)] text-[var(--nf-surface)] hover:bg-[var(--nf-lime)]/90 rounded-full px-[18px] py-2 gap-1.5">
            <Zap className="w-4 h-4" />
            <span className="text-sm font-medium">发布新内容</span>
          </Button>
          <Bell className="w-6 h-6 text-[var(--nf-white)]" />
          <Avatar className="w-8 h-8 bg-[var(--nf-blue)]">
            <AvatarFallback className="bg-[var(--nf-blue)]">
              <User className="w-4 h-4 text-[var(--nf-white)]" />
            </AvatarFallback>
          </Avatar>
        </div>
      </header>

      {/* Body */}
      <div className="flex flex-1 overflow-hidden">
        {/* Compact Sidebar */}
        <aside className="w-[60px] bg-[var(--nf-near-black)] border-r border-[var(--nf-dark-bg)] flex flex-col items-center gap-2 pt-4">
          <div className="w-10 h-10 rounded-lg flex items-center justify-center">
            <Compass className="w-5 h-5 text-[var(--nf-muted)]" />
          </div>
          <div className="w-10 h-10 rounded-lg flex items-center justify-center">
            <Globe className="w-5 h-5 text-[var(--nf-muted)]" />
          </div>
          <div className="w-10 h-10 rounded-lg flex items-center justify-center">
            <Mountain className="w-5 h-5 text-[var(--nf-muted)]" />
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto py-6 px-8 flex flex-col gap-6">
          {/* Profile Header Row */}
          <div className="flex items-center gap-5">
            {/* Avatar */}
            <div className="w-[90px] h-[90px] rounded-full bg-[var(--nf-dark-bg)] shrink-0" />

            {/* Info */}
            <div className="flex flex-col gap-2 flex-1">
              <span className="text-[22px] font-semibold text-[var(--nf-white)]">
                {user?.display_name || user?.username || "他人名字"}
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
            {user?.bio ?? "Personal Signature：大学在读生，热爱编程和设计，欢迎互相交流合作！"}
          </p>
          {user?.role && (
            <Badge variant="outline" className="w-fit bg-[var(--nf-card-bg)] border-[var(--nf-dark-bg)] text-[var(--nf-light-gray)] text-[12px] px-2.5 py-1 rounded-sm">
              {user.role === "participant" ? "参赛者" : user.role === "organizer" ? "组织者" : user.role === "admin" ? "管理员" : user.role}
            </Badge>
          )}

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
        </main>

        {/* Right Panel */}
        <aside className="w-[360px] p-4 shrink-0">
          <div className="w-full h-full bg-[#F5F5F5] rounded-[12px]" />
        </aside>
      </div>
    </div>
  )
}
