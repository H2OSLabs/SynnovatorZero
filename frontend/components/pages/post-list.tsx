"use client"

import {
  Menu, Search, Plus, Bell, Compass, Globe, Tent,
  Flame, Lightbulb,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"

const mainTabs = ["帖子", "提案广场", "资源", "团队", "活动", "找队友", "找点子", "官方"]

const teamCards = [
  { name: "金发发前端", image: "https://images.unsplash.com/photo-1640183295767-d237218daafd?w=400&h=300&fit=crop" },
  { name: "你意想不到的", image: "https://images.unsplash.com/photo-1543132220-e7fef0b974e7?w=400&h=300&fit=crop" },
  { name: "JioNan", image: "https://images.unsplash.com/photo-1593579491833-457b2c451e38?w=400&h=300&fit=crop" },
  { name: "JioNan", image: "https://images.unsplash.com/photo-1717494760896-3c2f7b173c40?w=400&h=300&fit=crop" },
]

const ideaCards = [
  { name: "金发发前端", image: "https://images.unsplash.com/photo-1518463732211-f1e67dfcec66?w=400&h=300&fit=crop" },
  { name: "你意想不到的", image: "https://images.unsplash.com/photo-1671250216070-0c61aa9eb854?w=400&h=300&fit=crop" },
  { name: "JioNan", image: "https://images.unsplash.com/photo-1679485322984-4270db63261e?w=400&h=300&fit=crop" },
  { name: "JioNan", image: "https://images.unsplash.com/photo-1603847551264-ccf92e79aab9?w=400&h=300&fit=crop" },
]

export function PostList() {
  return (
    <div className="flex flex-col h-screen bg-[var(--nf-near-black)]">
      {/* Header */}
      <header className="flex items-center h-14 px-6 bg-[var(--nf-card-bg)]">
        <div className="flex items-center gap-4">
          <Menu className="w-6 h-6 text-[var(--nf-white)]" />
          <span className="font-heading text-[18px] font-bold text-[var(--nf-lime)]">协创者</span>
        </div>
        <div className="flex items-center gap-2 w-[400px] mx-auto bg-[var(--nf-dark-bg)] rounded-[21px] px-4 py-2">
          <Search className="w-4 h-4 text-[var(--nf-muted)]" />
          <span className="text-sm text-[var(--nf-muted)]">搜索</span>
        </div>
        <div className="flex items-center gap-4">
          <Button className="bg-[var(--nf-lime)] text-[var(--nf-surface)] hover:bg-[var(--nf-lime)]/90 rounded-[21px] px-5 py-2 gap-1.5">
            <Plus className="w-3.5 h-3.5" />
            <span className="text-[13px] font-medium">发布新内容</span>
          </Button>
          <Bell className="w-[22px] h-[22px] text-[var(--nf-white)]" />
          <div className="w-8 h-8 rounded-full bg-[#555555]" />
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar */}
        <aside className="w-[180px] bg-[var(--nf-card-bg)] p-4 px-3 flex flex-col gap-1">
          <div className="flex items-center gap-2.5 px-4 py-2.5 bg-[var(--nf-lime)] rounded-lg">
            <Compass className="w-5 h-5 text-[var(--nf-surface)]" />
            <span className="text-sm font-semibold text-[var(--nf-surface)]">探索</span>
          </div>
          <div className="flex items-center gap-2.5 px-4 py-2.5 rounded-lg">
            <Globe className="w-5 h-5 text-[var(--nf-muted)]" />
            <span className="text-sm text-[var(--nf-muted)]">星球</span>
          </div>
          <div className="flex items-center gap-2.5 px-4 py-2.5 rounded-lg">
            <Tent className="w-5 h-5 text-[var(--nf-muted)]" />
            <span className="text-sm text-[var(--nf-muted)]">营地</span>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto p-6 px-8 flex flex-col gap-6">
          {/* Tabs Row */}
          <div className="flex items-center gap-6">
            {mainTabs.map((tab, i) => (
              <div key={tab} className="flex flex-col items-center gap-1.5">
                <span className={`text-[15px] ${i === 0 ? "font-semibold text-[var(--nf-lime)]" : "text-[var(--nf-muted)]"}`}>
                  {tab}
                </span>
                {i === 0 && <div className="w-8 h-[3px] rounded-sm bg-[var(--nf-lime)]" />}
              </div>
            ))}
          </div>

          {/* Section: 找队友 */}
          <section className="flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Flame className="w-5 h-5 text-[var(--nf-lime)]" />
                <span className="font-heading text-[18px] font-bold text-[var(--nf-white)]">找队友</span>
              </div>
              <span className="text-[13px] text-[var(--nf-muted)] cursor-pointer">查看更多</span>
            </div>
            <div className="grid grid-cols-4 gap-4">
              {teamCards.map((card, i) => (
                <Card key={`team-${i}`} className="w-[240px] bg-[var(--nf-card-bg)] border-none rounded-[12px] overflow-hidden">
                  <div
                    className="w-full h-[160px] bg-cover bg-center"
                    style={{ backgroundImage: `url(${card.image})` }}
                  />
                  <div className="flex items-center gap-1.5 px-3 py-2.5">
                    <div className="w-6 h-6 rounded-full bg-[#555555]" />
                    <span className="text-[12px] text-[var(--nf-white)]">{card.name}</span>
                  </div>
                </Card>
              ))}
            </div>
          </section>

          {/* Section: 找点子 */}
          <section className="flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Lightbulb className="w-5 h-5 text-[var(--nf-lime)]" />
                <span className="font-heading text-[18px] font-bold text-[var(--nf-white)]">找点子</span>
              </div>
              <span className="text-[13px] text-[var(--nf-muted)] cursor-pointer">查看更多</span>
            </div>
            <div className="grid grid-cols-4 gap-4">
              {ideaCards.map((card, i) => (
                <Card key={`idea-${i}`} className="w-[240px] bg-[var(--nf-card-bg)] border-none rounded-[12px] overflow-hidden">
                  <div
                    className="w-full h-[160px] bg-cover bg-center"
                    style={{ backgroundImage: `url(${card.image})` }}
                  />
                  <div className="flex items-center gap-1.5 px-3 py-2.5">
                    <div className="w-6 h-6 rounded-full bg-[#555555]" />
                    <span className="text-[12px] text-[var(--nf-white)]">{card.name}</span>
                  </div>
                </Card>
              ))}
            </div>
          </section>
        </main>
      </div>
    </div>
  )
}
