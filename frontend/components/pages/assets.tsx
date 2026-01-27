"use client"

import {
  Menu, Search, Zap, Bell, User, ChevronDown,
  Compass, Globe, Mountain, Wallet,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"

const assetCards = [
  {
    title: "大赛官方天翼云算力",
    tags: [
      { label: "赛级资源", variant: "lime" as const },
      { label: "赢场\u00B7滇水源", variant: "orange" as const },
    ],
    description:
      "恭喜您获级资源！大赛已为数据乐队发放专属天翼云算力。详细说明请查看官方公告。",
    available: true,
    deadline: "2024.08.10",
  },
  {
    title: "大赛官方天翼云算力",
    tags: [
      { label: "赛级资源", variant: "lime" as const },
      { label: "赢场\u00B7滇水源", variant: "orange" as const },
    ],
    description:
      "恭喜您获级资源！大赛已为数据乐队发放专属天翼云算力。详细说明请查看官方公告。",
    available: true,
    deadline: "2024.08.10",
  },
  {
    title: "大赛官方天翼云算力",
    tags: [
      { label: "赛级资源", variant: "lime" as const },
      { label: "赢场\u00B7滇水源", variant: "orange" as const },
    ],
    description:
      "恭喜您获级资源！大赛已为数据乐队发放专属天翼云算力。详细说明请查看官方公告。",
    available: true,
    deadline: "2024.08.10",
  },
  {
    title: "大赛官方天翼云算力",
    tags: [
      { label: "赛级资源", variant: "lime" as const },
      { label: "赢场\u00B7滇水源", variant: "orange" as const },
    ],
    description:
      "恭喜您获级资源！大赛已为数据乐队发放专属天翼云算力。详细说明请查看官方公告。",
    available: true,
    deadline: "2024.08.10",
  },
]

export function Assets() {
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
        <main className="flex-1 overflow-y-auto px-8 py-6 flex flex-col gap-5">
          {/* Title Row */}
          <div className="flex items-center gap-2">
            <Wallet className="w-5 h-5 text-[var(--nf-lime)]" />
            <span className="text-[20px] font-semibold text-[var(--nf-white)]">
              我的资产
            </span>
          </div>

          {/* Category Tabs */}
          <div className="grid grid-cols-3 gap-4">
            {/* AI/Agent - Active */}
            <Card className="h-[100px] bg-[var(--nf-card-bg)] border-2 border-[var(--nf-lime)] rounded-[12px] p-4 flex items-center gap-4">
              <div className="w-[60px] h-[60px] rounded-lg bg-[var(--nf-dark-bg)] shrink-0" />
              <div className="flex flex-col gap-1">
                <span className="text-[16px] font-bold text-[var(--nf-lime)]">
                  AI/Agent
                </span>
                <span className="font-mono text-[13px] text-[var(--nf-light-gray)]">
                  0 TOPS
                </span>
              </div>
            </Card>

            {/* 证书 - Inactive */}
            <Card className="h-[100px] bg-[var(--nf-card-bg)] border border-[var(--nf-dark-bg)] rounded-[12px] flex items-center justify-center">
              <span className="text-[16px] font-semibold text-[var(--nf-white)]">
                证书
              </span>
            </Card>

            {/* 文件 - Inactive */}
            <Card className="h-[100px] bg-[var(--nf-card-bg)] border border-[var(--nf-dark-bg)] rounded-[12px] flex items-center justify-center">
              <span className="text-[16px] font-semibold text-[var(--nf-white)]">
                文件
              </span>
            </Card>
          </div>

          {/* Assets Grid */}
          <div className="grid grid-cols-2 gap-4">
            {assetCards.map((asset, index) => (
              <Card
                key={index}
                className="bg-[var(--nf-card-bg)] border border-[var(--nf-dark-bg)] rounded-[12px] p-4 flex flex-col gap-2"
              >
                <span className="text-[15px] font-semibold text-[var(--nf-white)]">
                  {asset.title}
                </span>

                <div className="flex items-center gap-2">
                  {asset.tags.map((tag) => (
                    <Badge
                      key={tag.label}
                      className={`rounded-sm px-2 py-0.5 text-[11px] border-transparent ${
                        tag.variant === "lime"
                          ? "bg-[var(--nf-lime)] text-[var(--nf-surface)]"
                          : "bg-[var(--nf-orange)] text-[var(--nf-white)]"
                      }`}
                    >
                      {tag.label}
                    </Badge>
                  ))}
                </div>

                <p className="text-[12px] text-[var(--nf-muted)]">
                  {asset.description}
                </p>

                <div className="flex items-center justify-between mt-auto">
                  <div className="flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-[#00B42A]" />
                    <span className="text-[11px] text-[#00B42A]">可用</span>
                  </div>
                  <span className="text-[11px] text-[var(--nf-muted)]">
                    截止日期: {asset.deadline}
                  </span>
                </div>
              </Card>
            ))}
          </div>
        </main>

        {/* Right Panel */}
        <aside className="w-[360px] p-4">
          <div className="h-full bg-[#F5F5F5] rounded-[12px]" />
        </aside>
      </div>
    </div>
  )
}
