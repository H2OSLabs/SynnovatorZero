"use client"

import { useState } from "react"
import { Search, SlidersHorizontal, Plus } from "lucide-react"
import Link from "next/link"
import { PageLayout } from "@/components/layout/PageLayout"
import { GroupCard } from "@/components/cards/GroupCard"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

// Mock data
const mockGroups = [
  { id: 1, name: "创新先锋队", visibility: "public" as const, member_count: 5, event_count: 2, description: "热爱技术，热爱开源，我们是一群热情的创客！" },
  { id: 2, name: "AI 实验室", visibility: "public" as const, member_count: 8, event_count: 3, description: "探索 AI 的无限可能，用技术改变世界" },
  { id: 3, name: "Web3 先锋", visibility: "public" as const, member_count: 4, event_count: 1, description: "去中心化的未来由我们创造" },
  { id: 4, name: "设计创意组", visibility: "public" as const, member_count: 6, event_count: 2, description: "用设计传递价值，用创意点亮生活" },
  { id: 5, name: "全栈开发团", visibility: "public" as const, member_count: 7, event_count: 4, description: "从前端到后端，我们无所不能" },
  { id: 6, name: "数据科学家", visibility: "private" as const, member_count: 3, event_count: 1, description: "用数据洞察一切" },
]

export default function GroupsPage() {
  const [activeTab, setActiveTab] = useState("all")

  const filteredGroups = mockGroups.filter((group) => {
    if (activeTab === "all") return true
    if (activeTab === "public") return group.visibility === "public"
    if (activeTab === "private") return group.visibility === "private"
    return true
  })

  return (
    <PageLayout variant="compact" user={null}>
      {/* Page Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="font-heading text-3xl font-bold text-nf-white mb-2">👥 团队</h1>
          <p className="text-nf-muted">发现优秀团队，寻找志同道合的伙伴</p>
        </div>
        <Link href="/groups/create">
          <Button className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
            <Plus className="h-4 w-4 mr-2" />
            创建团队
          </Button>
        </Link>
      </div>

      {/* Search & Filter */}
      <div className="flex gap-4 mb-6">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-nf-muted" />
          <Input
            placeholder="搜索团队..."
            className="pl-10 bg-nf-surface border-nf-secondary"
          />
        </div>
        <Button variant="outline" className="border-nf-secondary">
          <SlidersHorizontal className="h-4 w-4 mr-2" />
          筛选
        </Button>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="bg-nf-surface border-nf-secondary mb-6">
          <TabsTrigger value="all">全部</TabsTrigger>
          <TabsTrigger value="public">🌐 公开</TabsTrigger>
          <TabsTrigger value="private">🔒 私密</TabsTrigger>
        </TabsList>

        <TabsContent value={activeTab}>
          {filteredGroups.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredGroups.map((group) => (
                <GroupCard key={group.id} {...group} />
              ))}
            </div>
          ) : (
            <div className="text-center py-16">
              <p className="text-nf-muted">暂无团队</p>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </PageLayout>
  )
}
