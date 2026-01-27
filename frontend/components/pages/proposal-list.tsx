"use client"

import {
  Menu, Search, Zap, Bell, User,
  Compass, Globe, Mountain, SlidersHorizontal,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"

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
    <div className="flex flex-col h-screen bg-[var(--nf-near-black)]">
      {/* Header */}
      <header className="flex items-center justify-between h-14 px-6 border-b border-[var(--nf-dark-bg)] bg-[var(--nf-near-black)]">
        <div className="flex items-center gap-4">
          <Menu className="w-6 h-6 text-[var(--nf-white)]" />
          <span className="font-heading text-[20px] font-bold text-[var(--nf-lime)]">协创者</span>
        </div>
        <div className="flex items-center gap-2 w-[400px] bg-[var(--nf-card-bg)] border border-[var(--nf-dark-bg)] rounded-[21px] px-5 py-2.5">
          <Search className="w-4 h-4 text-[var(--nf-muted)]" />
          <span className="text-sm text-[var(--nf-muted)]">搜索</span>
        </div>
        <div className="flex items-center gap-3">
          <Button className="bg-[var(--nf-lime)] text-[var(--nf-surface)] hover:bg-[var(--nf-lime)]/90 rounded-full px-4 py-2 gap-2">
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

      <div className="flex flex-1 overflow-hidden">
        {/* Compact Sidebar */}
        <aside className="w-[60px] bg-[var(--nf-near-black)] flex flex-col items-center gap-3 pt-4 px-3">
          <Compass className="w-6 h-6 text-[var(--nf-muted)]" />
          <Globe className="w-6 h-6 text-[var(--nf-muted)]" />
          <Mountain className="w-6 h-6 text-[var(--nf-muted)]" />
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto p-4 px-6 flex flex-col gap-4">
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
        </main>
      </div>
    </div>
  )
}
