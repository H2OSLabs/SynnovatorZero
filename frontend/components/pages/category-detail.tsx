"use client"

import { User } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { AppLayout } from "@/components/layout/app-layout"

const detailTabs = ["详情", "排榜", "讨论区", "成员", "赛程安排", "关联活动"]

export function CategoryDetail() {
  return (
    <AppLayout activeNav="星球">
      {/* Banner Row */}
      <div className="flex gap-6">
        <div
          className="w-[320px] h-[200px] rounded-[12px] bg-cover bg-center shrink-0 bg-[var(--nf-dark-bg)]"
        />
        <div className="flex flex-col gap-3">
          <h1 className="text-[20px] font-semibold text-[var(--nf-white)]">
            西建·滇水源 | 上海第七届大学生AI+国际创业大赛
          </h1>
          <div className="flex items-center gap-2">
            <User className="w-3.5 h-3.5 text-[var(--nf-muted)]" />
            <span className="text-[13px] text-[var(--nf-muted)]">大赛</span>
          </div>
          <span className="font-mono text-[32px] font-bold text-[var(--nf-lime)]">880万元</span>
          <div className="flex flex-col gap-1">
            <span className="text-[12px] text-[var(--nf-muted)]">2025/01/28</span>
            <span className="text-[12px] text-[var(--nf-muted)]">2025/02/26</span>
            <span className="text-[12px] text-[var(--nf-muted)]">2025/03/26</span>
          </div>
          <Badge variant="outline" className="w-fit bg-[var(--nf-card-bg)] border-[var(--nf-dark-bg)] text-[var(--nf-light-gray)] text-[12px] px-2.5 py-1 rounded-sm">
            LIGHTNING鲸
          </Badge>
        </div>
      </div>

      {/* Detail Tabs */}
      <Tabs defaultValue="详情" className="w-full">
        <TabsList className="w-full justify-start bg-transparent border-b border-[var(--nf-dark-bg)] rounded-none h-auto p-0 gap-0">
          {detailTabs.map((tab) => (
            <TabsTrigger
              key={tab}
              value={tab}
              className="rounded-none border-b-2 border-transparent px-4 py-2.5 text-sm text-[var(--nf-muted)] data-[state=active]:text-[var(--nf-lime)] data-[state=active]:border-[var(--nf-lime)] data-[state=active]:font-semibold data-[state=active]:bg-transparent data-[state=active]:shadow-none"
            >
              {tab}
            </TabsTrigger>
          ))}
        </TabsList>
        <TabsContent value="详情" className="mt-5">
          <div className="w-full min-h-[400px] bg-[var(--nf-card-bg)] rounded-[12px] p-6">
            <p className="text-sm text-[var(--nf-muted)]">活动详情内容区域</p>
          </div>
        </TabsContent>
      </Tabs>
    </AppLayout>
  )
}
