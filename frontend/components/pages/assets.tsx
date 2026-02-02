"use client"

import { Wallet } from "lucide-react"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { AppLayout } from "@/components/layout/app-layout"

const fallbackAssetCards = [
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
  const assetCards = fallbackAssetCards

  return (
    <AppLayout
      sidebar={
        <div className="w-full h-full bg-[var(--nf-card-bg)] rounded-[12px]" />
      }
    >
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
    </AppLayout>
  )
}
