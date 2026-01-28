"use client"

import { useState, useEffect } from "react"
import {
  Menu, Search, Zap, Bell, User, ChevronDown,
  Compass, Globe, Mountain, X,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { getFollowing, getFollowers } from "@/lib/api-client"
import type { UserUserRelation } from "@/lib/types"

const fallbackUserCards = [
  { name: "个人", followers: 12 },
  { name: "个人", followers: 8 },
  { name: "个人", followers: 5 },
  { name: "个人", followers: 15 },
  { name: "个人", followers: 3 },
]

const galleryCards = [
  { name: "LIGHTNING鲸", image: "" },
  { name: "创意达人", image: "" },
  { name: "设计师小王", image: "" },
]

export function FollowingList({ userId }: { userId: number }) {
  const [following, setFollowing] = useState<UserUserRelation[]>([])
  const [followers, setFollowers] = useState<UserUserRelation[]>([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<"all" | "following">("all")

  useEffect(() => {
    let cancelled = false
    async function fetchData() {
      setLoading(true)
      try {
        const [followingData, followersData] = await Promise.all([
          getFollowing(userId),
          getFollowers(userId),
        ])
        if (!cancelled) {
          setFollowing(followingData)
          setFollowers(followersData)
        }
      } catch (err) {
        console.error("Failed to fetch following data:", err)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    fetchData()
    return () => { cancelled = true }
  }, [userId])

  const displayRelations = activeTab === "following" ? following : [...following, ...followers]

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
          <ChevronDown className="w-4 h-4 text-[var(--nf-white)]" />
        </div>
      </header>

      {/* Body */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar */}
        <aside className="w-[140px] bg-[var(--nf-near-black)] p-4 px-3 flex flex-col gap-1">
          <div className="flex items-center gap-2.5 px-3 py-2.5 bg-[var(--nf-lime)] rounded-full">
            <Compass className="w-[18px] h-[18px] text-[var(--nf-surface)]" />
            <span className="text-sm font-semibold text-[var(--nf-surface)]">探索</span>
          </div>
          <div className="flex items-center gap-2.5 px-3 py-2.5 rounded-full">
            <Globe className="w-[18px] h-[18px] text-[var(--nf-muted)]" />
            <span className="text-sm text-[var(--nf-muted)]">星球</span>
          </div>
          <div className="flex items-center gap-2.5 px-3 py-2.5 rounded-full">
            <Mountain className="w-[18px] h-[18px] text-[var(--nf-muted)]" />
            <span className="text-sm text-[var(--nf-muted)]">营地</span>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto p-4 px-6 flex flex-col gap-5">
          {/* Tabs Row */}
          <div className="flex items-center gap-4">
            <Badge
              className={`rounded-full px-4 py-1.5 text-[13px] font-semibold cursor-pointer ${activeTab === "all" ? "bg-[var(--nf-lime)] text-[var(--nf-surface)] hover:bg-[var(--nf-lime)]/90" : "bg-[var(--nf-card-bg)] text-[var(--nf-muted)] hover:text-[var(--nf-white)]"}`}
              onClick={() => setActiveTab("all")}
            >
              全部好友 ({following.length + followers.length})
            </Badge>
            <span
              className={`text-[13px] cursor-pointer ${activeTab === "following" ? "text-[var(--nf-lime)] font-semibold" : "text-[var(--nf-muted)] hover:text-[var(--nf-white)]"}`}
              onClick={() => setActiveTab("following")}
            >
              我关注的 ({following.length})
            </span>
          </div>

          {/* User Cards Grid */}
          <div className="flex flex-wrap gap-4">
            {displayRelations.length > 0 ? displayRelations.map((relation, i) => (
              <Card
                key={`user-${relation.id}-${i}`}
                className="w-[160px] bg-[var(--nf-card-bg)] border-none rounded-[12px] p-4 flex flex-col items-center gap-3"
              >
                <div className="w-16 h-16 rounded-full bg-[#555555] flex items-center justify-center">
                  <User className="w-6 h-6 text-[var(--nf-muted)]" />
                </div>
                <span className="text-[14px] font-medium text-[var(--nf-white)]">
                  用户 {relation.target_user_id}
                </span>
                <span className="text-[12px] text-[var(--nf-muted)]">
                  {relation.relation_type === "follow" ? "关注" : "屏蔽"}
                </span>
              </Card>
            )) : fallbackUserCards.map((user, i) => (
              <Card
                key={`user-${i}`}
                className="w-[160px] bg-[var(--nf-card-bg)] border-none rounded-[12px] p-4 flex flex-col items-center gap-3"
              >
                <div className="w-16 h-16 rounded-full bg-[#555555] flex items-center justify-center">
                  <User className="w-6 h-6 text-[var(--nf-muted)]" />
                </div>
                <span className="text-[14px] font-medium text-[var(--nf-white)]">
                  {user.name}
                </span>
                <span className="text-[12px] text-[var(--nf-muted)]">
                  {user.followers} 关注
                </span>
              </Card>
            ))}
          </div>

          {/* Image Gallery */}
          <div className="grid grid-cols-3 gap-4">
            {galleryCards.map((card) => (
              <Card
                key={card.name}
                className="bg-[var(--nf-card-bg)] border-none rounded-[12px] overflow-hidden"
              >
                <div className="w-full h-[140px] bg-[#555555]" />
                <div className="flex items-center gap-2 px-3 py-2.5">
                  <div className="w-6 h-6 rounded-full bg-[#555555] shrink-0" />
                  <span className="text-[12px] font-medium text-[var(--nf-white)]">
                    {card.name}
                  </span>
                </div>
              </Card>
            ))}
          </div>
        </main>

        {/* Right Sidebar */}
        <aside className="w-[280px] p-4 flex flex-col gap-4">
          {/* Promo Banner */}
          <div className="relative bg-[var(--nf-lime)] rounded-[16px] p-5 flex flex-col gap-2">
            <button className="absolute top-3 right-3 text-[var(--nf-surface)] hover:opacity-70">
              <X className="w-4 h-4" />
            </button>
            <span className="font-heading text-[22px] font-bold text-[var(--nf-surface)]">
              来协创,创个业
            </span>
            <span className="text-[12px] text-[var(--nf-dark-bg)]">
              来来看看Synnovator特色。
            </span>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-2">
            <Button className="flex-1 bg-[var(--nf-lime)] text-[var(--nf-surface)] hover:bg-[var(--nf-lime)]/90 rounded-lg py-2">
              <span className="text-[13px] font-semibold">团队天</span>
            </Button>
            <Button
              variant="outline"
              className="flex-1 border-[var(--nf-lime)] text-[var(--nf-lime)] bg-transparent hover:bg-[var(--nf-lime)]/10 rounded-lg py-2"
            >
              <span className="text-[13px] font-medium">我与子</span>
            </Button>
          </div>
        </aside>
      </div>
    </div>
  )
}
