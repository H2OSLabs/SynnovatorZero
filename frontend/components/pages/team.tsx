"use client"

import { Plus, Users, Wallet } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { AppLayout } from "@/components/layout/app-layout"

const members = [
  { id: 1, color: "bg-[#555555]" },
  { id: 2, color: "bg-[#777777]" },
]

const assets = [
  { label: "AI/Agent", value: "0", unit: "TOPS", highlight: true },
  { label: "证书", value: "1", unit: "张证书", highlight: false },
  { label: "文件", value: "16", unit: "个文件", highlight: false },
]

export function Team({ groupId }: { groupId: number }) {
  return (
    <AppLayout navMode="compact" activeNav="探索">
      {/* Team Header Row */}
      <div className="flex items-center gap-5">
        {/* Team Avatar */}
        <div className="w-[80px] h-[80px] rounded-full bg-[#555555] shrink-0" />

        {/* Team Info */}
        <div className="flex flex-col gap-1.5 flex-1">
          <h1 className="text-[22px] font-semibold text-[var(--nf-white)]">
            团队
          </h1>
          <div className="flex items-center gap-4">
            <span className="text-[13px] text-[var(--nf-muted)]">
              <span className="font-mono text-[var(--nf-white)]">12</span> 帖子
            </span>
            <span className="text-[13px] text-[var(--nf-muted)]">
              <span className="font-mono text-[var(--nf-white)]">6</span> 关注
            </span>
          </div>
          <p className="text-[13px] text-[var(--nf-muted)]">
            未来的协会与创新型创新技术开发运营企业
          </p>
        </div>

        {/* Manage Button */}
        <Button className="bg-[var(--nf-dark-bg)] text-[var(--nf-light-gray)] hover:bg-[var(--nf-dark-bg)]/80 rounded-lg px-4 py-2">
          <span className="text-sm">管理面板</span>
        </Button>
      </div>

      {/* Members Section */}
      <section className="flex flex-col gap-3">
        <div className="flex items-center gap-2">
          <Users className="w-4 h-4 text-[var(--nf-lime)]" />
          <span className="text-[16px] font-semibold text-[var(--nf-white)]">队员</span>
        </div>
        <div className="flex items-center gap-3">
          {members.map((member) => (
            <div
              key={member.id}
              className={`w-[48px] h-[48px] rounded-full ${member.color}`}
            />
          ))}
          {/* Add Member Button */}
          <button className="w-[48px] h-[48px] rounded-full bg-[var(--nf-card-bg)] border border-[var(--nf-dark-bg)] flex items-center justify-center">
            <Plus className="w-5 h-5 text-[var(--nf-muted)]" />
          </button>
        </div>
      </section>

      {/* Assets Section */}
      <section className="flex flex-col gap-3">
        <div className="flex items-center gap-2">
          <Wallet className="w-4 h-4 text-[var(--nf-lime)]" />
          <span className="text-[16px] font-semibold text-[var(--nf-white)]">资产</span>
        </div>
        <div className="grid grid-cols-3 gap-4">
          {assets.map((asset) => (
            <Card
              key={asset.label}
              className="bg-[var(--nf-card-bg)] border border-[var(--nf-dark-bg)] rounded-[12px] h-[100px] p-4 flex flex-col justify-center"
            >
              <span
                className={`text-[14px] font-bold ${
                  asset.highlight
                    ? "text-[var(--nf-lime)]"
                    : "text-[var(--nf-white)]"
                }`}
              >
                {asset.label}
              </span>
              <span className="text-[13px] text-[var(--nf-muted)]">
                <span className="font-mono">{asset.value}</span> {asset.unit}
              </span>
            </Card>
          ))}
        </div>
      </section>

      {/* Tabs */}
      <Tabs defaultValue="proposals" className="flex flex-col gap-4">
        <TabsList className="w-full justify-start bg-transparent border-b border-[var(--nf-dark-bg)] rounded-none h-auto p-0 gap-0">
          <TabsTrigger
            value="proposals"
            className="rounded-none border-b-2 border-transparent px-4 py-2.5 text-[15px] font-medium text-[var(--nf-muted)] data-[state=active]:text-[var(--nf-lime)] data-[state=active]:border-[var(--nf-lime)] data-[state=active]:font-semibold data-[state=active]:bg-transparent data-[state=active]:shadow-none"
          >
            提案
          </TabsTrigger>
          <TabsTrigger
            value="posts"
            className="rounded-none border-b-2 border-transparent px-4 py-2.5 text-[15px] font-medium text-[var(--nf-muted)] data-[state=active]:text-[var(--nf-lime)] data-[state=active]:border-[var(--nf-lime)] data-[state=active]:font-semibold data-[state=active]:bg-transparent data-[state=active]:shadow-none"
          >
            帖子
          </TabsTrigger>
          <TabsTrigger
            value="favorites"
            className="rounded-none border-b-2 border-transparent px-4 py-2.5 text-[15px] font-medium text-[var(--nf-muted)] data-[state=active]:text-[var(--nf-lime)] data-[state=active]:border-[var(--nf-lime)] data-[state=active]:font-semibold data-[state=active]:bg-transparent data-[state=active]:shadow-none"
          >
            收藏
          </TabsTrigger>
        </TabsList>

        <TabsContent value="proposals">
          {/* Single image card placeholder */}
          <div className="w-[200px] h-[200px] rounded-[12px] bg-[#555555]" />
        </TabsContent>

        <TabsContent value="posts">
          <p className="text-[13px] text-[var(--nf-muted)]">暂无帖子</p>
        </TabsContent>

        <TabsContent value="favorites">
          <p className="text-[13px] text-[var(--nf-muted)]">暂无收藏</p>
        </TabsContent>
      </Tabs>
    </AppLayout>
  )
}
