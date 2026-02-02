"use client"

import { User, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { AppLayout } from "@/components/layout/app-layout"

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
  const userCards = fallbackUserCards

  return (
    <AppLayout
      sidebar={
        <>
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
        </>
      }
    >
      {/* Tabs Row */}
      <div className="flex items-center gap-4">
        <Badge className="bg-[var(--nf-lime)] text-[var(--nf-surface)] hover:bg-[var(--nf-lime)]/90 rounded-full px-4 py-1.5 text-[13px] font-semibold">
          全部好友
        </Badge>
        <span className="text-[13px] text-[var(--nf-muted)] cursor-pointer hover:text-[var(--nf-white)]">
          我关注的
        </span>
      </div>

      {/* User Cards Grid */}
      <div className="flex flex-wrap gap-4">
        {userCards.map((user, i) => (
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
    </AppLayout>
  )
}
