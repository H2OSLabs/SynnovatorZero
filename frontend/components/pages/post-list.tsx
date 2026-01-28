"use client"

import { Flame, Lightbulb } from "lucide-react"
import { Card } from "@/components/ui/card"
import { AppLayout } from "@/components/layout/app-layout"

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
    <AppLayout>
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
    </AppLayout>
  )
}
