"use client"

import { useState } from "react"
import { Search, SlidersHorizontal, Plus } from "lucide-react"
import Link from "next/link"
import { PageLayout } from "@/components/layout/PageLayout"
import { CategoryCard } from "@/components/cards/CategoryCard"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

// Mock data
const mockCategories = [
  { id: 1, name: "AI 创新挑战赛 2024", type: "competition" as const, status: "published" as const, tags: ["AI", "Machine Learning"], participant_count: 128, start_date: "2024-03-01", end_date: "2024-03-30" },
  { id: 2, name: "Web3 黑客马拉松", type: "competition" as const, status: "published" as const, tags: ["Web3", "Blockchain"], participant_count: 86, start_date: "2024-04-01", end_date: "2024-04-15" },
  { id: 3, name: "绿色科技创新大赛", type: "competition" as const, status: "published" as const, tags: ["Climate", "Sustainability"], participant_count: 64, start_date: "2024-05-01", end_date: "2024-05-31" },
  { id: 4, name: "开源社区贡献月", type: "operation" as const, status: "published" as const, tags: ["Open Source"], participant_count: 256, start_date: "2024-03-01", end_date: "2024-03-31" },
  { id: 5, name: "移动应用创新赛", type: "competition" as const, status: "draft" as const, tags: ["Mobile", "iOS", "Android"], participant_count: 0, start_date: "2024-06-01", end_date: "2024-06-30" },
  { id: 6, name: "2023 年度创新盛典", type: "competition" as const, status: "closed" as const, tags: ["Innovation"], participant_count: 512, start_date: "2023-11-01", end_date: "2023-12-15" },
]

export default function EventsPage() {
  const [activeTab, setActiveTab] = useState("all")

  const filteredCategories = mockCategories.filter((cat) => {
    if (activeTab === "all") return true
    if (activeTab === "ongoing") return cat.status === "published"
    if (activeTab === "upcoming") return cat.status === "draft"
    if (activeTab === "ended") return cat.status === "closed"
    return true
  })

  return (
    <PageLayout variant="compact" user={null}>
      {/* Page Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="font-heading text-3xl font-bold text-nf-white mb-2">📅 活动</h1>
          <p className="text-nf-muted">发现并参与各类 Hackathon 和创新大赛</p>
        </div>
        <Link href="/events/create">
          <Button className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
            <Plus className="h-4 w-4 mr-2" />
            创建活动
          </Button>
        </Link>
      </div>

      {/* Search & Filter */}
      <div className="flex gap-4 mb-6">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-nf-muted" />
          <Input
            placeholder="搜索活动..."
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
          <TabsTrigger value="ongoing">进行中</TabsTrigger>
          <TabsTrigger value="upcoming">即将开始</TabsTrigger>
          <TabsTrigger value="ended">已结束</TabsTrigger>
        </TabsList>

        <TabsContent value={activeTab}>
          {filteredCategories.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredCategories.map((cat) => (
                <CategoryCard key={cat.id} {...cat} />
              ))}
            </div>
          ) : (
            <div className="text-center py-16">
              <p className="text-nf-muted">暂无活动</p>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </PageLayout>
  )
}
