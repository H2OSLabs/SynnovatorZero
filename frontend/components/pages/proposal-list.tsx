"use client"

import { User, SlidersHorizontal } from "lucide-react"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { AppLayout } from "@/components/layout/app-layout"

const tabs = ["帖子", "提案广场", "资源", "团队", "活动", "找队友", "找点子", "官方"]

const proposals = [
  {
    title: "善意百宝——一人人需要扫有轮AI直辅学习平台",
    author: "LIGHTNING鲸",
    avatarColor: "bg-[var(--nf-lime)]",
    avatarTextColor: "text-[var(--nf-surface)]",
    image: "https://images.unsplash.com/photo-1764083292882-fd28776d0022?w=600&h=400&fit=crop",
  },
  {
    title: "探索发言——多人创新教育AI直辅学习平台",
    author: "LIGHTNING鲸",
    avatarColor: "bg-[var(--nf-blue)]",
    avatarTextColor: "text-[var(--nf-white)]",
    image: "https://images.unsplash.com/photo-1767481626838-839c89704569?w=600&h=400&fit=crop",
  },
  {
    title: "探索百宝——多人创新教育平台介绍文字",
    author: "Jacksen",
    avatarColor: "bg-[var(--nf-orange)]",
    avatarTextColor: "text-[var(--nf-white)]",
    image: "https://images.unsplash.com/photo-1766802981831-8baf453bb1ee?w=600&h=400&fit=crop",
  },
  {
    title: "善意百宝——多人创新教育系统学习服务",
    author: "LIGHTNING鲸",
    avatarColor: "bg-[var(--nf-lime)]",
    avatarTextColor: "text-[var(--nf-surface)]",
    image: "https://images.unsplash.com/photo-1620206299334-6378dde8c8e1?w=600&h=400&fit=crop",
  },
]

export function ProposalList() {
  return (
    <AppLayout navMode="compact" activeNav="探索">
      {/* Tabs */}
      <div className="flex items-center gap-4">
        {tabs.map((tab, i) =>
          tab === "提案广场" ? (
            <Badge
              key={tab}
              className="bg-[var(--nf-lime)] text-[var(--nf-surface)] hover:bg-[var(--nf-lime)]/90 rounded-full px-4 py-1.5 text-[13px] font-semibold"
            >
              {tab}
            </Badge>
          ) : (
            <span key={tab} className="text-[13px] text-[var(--nf-muted)] cursor-pointer hover:text-[var(--nf-white)]">
              {tab}
            </span>
          )
        )}
      </div>

      {/* Filter Row */}
      <div className="flex items-center gap-3">
        <SlidersHorizontal className="w-4 h-4 text-[var(--nf-lime)]" />
        <span className="text-[13px] font-medium text-[var(--nf-lime)]">赛道探索</span>
        <div className="w-px h-4 bg-[var(--nf-dark-bg)]" />
        <span className="text-[13px] text-[var(--nf-muted)]">热门</span>
        <div className="w-px h-4 bg-[var(--nf-dark-bg)]" />
        <span className="text-[13px] text-[var(--nf-muted)]">最新</span>
      </div>

      {/* Proposal Grid */}
      <div className="grid grid-cols-2 gap-4">
        {proposals.map((prop, i) => (
          <Card key={i} className="bg-[var(--nf-card-bg)] border-none rounded-[12px] overflow-hidden">
            <div
              className="w-full h-[180px] bg-cover bg-center"
              style={{ backgroundImage: `url(${prop.image})` }}
            />
            <div className="p-3 flex flex-col gap-2">
              <p className="text-[13px] font-medium text-[var(--nf-white)]">{prop.title}</p>
              <div className="flex items-center gap-2">
                <div className={`w-5 h-5 rounded-full ${prop.avatarColor} flex items-center justify-center`}>
                  <User className="w-2.5 h-2.5" />
                </div>
                <span className="text-[11px] text-[var(--nf-muted)]">{prop.author}</span>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </AppLayout>
  )
}
