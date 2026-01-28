"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import {
  Menu, Search, Zap, Bell, User,
  Compass, Globe, Mountain,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { getCategory, listCategoryPosts, listCategoryGroups } from "@/lib/api-client"
import type { Category, CategoryPost, CategoryGroup } from "@/lib/types"

const detailTabs = ["详情", "排榜", "讨论区", "成员", "赛程安排", "关联活动"]

export function CategoryDetail({ categoryId }: { categoryId: number }) {
  const router = useRouter()
  const [activeTab, setActiveTab] = useState("详情")
  const [category, setCategory] = useState<Category | null>(null)
  const [posts, setPosts] = useState<CategoryPost[]>([])
  const [groups, setGroups] = useState<CategoryGroup[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    async function fetchData() {
      setLoading(true)
      try {
        const [cat, catPosts, catGroups] = await Promise.all([
          getCategory(categoryId),
          listCategoryPosts(categoryId),
          listCategoryGroups(categoryId),
        ])
        if (!cancelled) {
          setCategory(cat)
          setPosts(catPosts)
          setGroups(catGroups)
        }
      } catch (err) {
        console.error("Failed to fetch category data:", err)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    fetchData()
    return () => { cancelled = true }
  }, [categoryId])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-[var(--nf-near-black)]">
        <span className="text-[var(--nf-muted)] text-lg">加载中...</span>
      </div>
    )
  }
  return (
    <div className="flex flex-col h-screen bg-[var(--nf-near-black)]">
      {/* Header */}
      <header className="flex items-center justify-between h-14 px-6 border-b border-[var(--nf-dark-bg)] bg-[var(--nf-near-black)]">
        <div className="flex items-center gap-4">
          <Menu className="w-6 h-6 text-[var(--nf-white)]" />
          <span className="font-heading text-[20px] font-bold text-[var(--nf-lime)] cursor-pointer" onClick={() => router.push("/")}>协创者</span>
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
        {/* Left Sidebar */}
        <aside className="w-[140px] bg-[var(--nf-near-black)] p-4 px-3 flex flex-col gap-1">
          <div className="flex items-center gap-2.5 px-3 py-2.5 rounded-full cursor-pointer" onClick={() => router.push("/")}>
            <Compass className="w-[18px] h-[18px] text-[var(--nf-muted)]" />
            <span className="text-sm text-[var(--nf-muted)]">探索</span>
          </div>
          <div className="flex items-center gap-2.5 px-3 py-2.5 bg-[var(--nf-lime)] rounded-full cursor-pointer" onClick={() => router.push("/categories/1")}>
            <Globe className="w-[18px] h-[18px] text-[var(--nf-surface)]" />
            <span className="text-sm font-semibold text-[var(--nf-surface)]">星球</span>
          </div>
          <div className="flex items-center gap-2.5 px-3 py-2.5 rounded-full cursor-pointer" onClick={() => router.push("/team")}>
            <Mountain className="w-[18px] h-[18px] text-[var(--nf-muted)]" />
            <span className="text-sm text-[var(--nf-muted)]">营地</span>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto p-6 px-8 flex flex-col gap-5">
          {/* Banner Row */}
          <div className="flex gap-6">
            <div
              className="w-[320px] h-[200px] rounded-[12px] bg-cover bg-center shrink-0 bg-[var(--nf-dark-bg)]"
            />
            <div className="flex flex-col gap-3">
              <h1 className="text-[20px] font-semibold text-[var(--nf-white)]">
                {category?.name ?? "西建·滇水源 | 上海第七届大学生AI+国际创业大赛"}
              </h1>
              <div className="flex items-center gap-2">
                <User className="w-3.5 h-3.5 text-[var(--nf-muted)]" />
                <span className="text-[13px] text-[var(--nf-muted)]">{category?.type === "competition" ? "大赛" : category?.type === "operation" ? "运营" : "大赛"}</span>
              </div>
              <span className="font-mono text-[32px] font-bold text-[var(--nf-lime)]">{category?.prize_pool ?? "880万元"}</span>
              <div className="flex flex-col gap-1">
                <span className="text-[12px] text-[var(--nf-muted)]">{category?.start_date ?? "2025/01/28"}</span>
                <span className="text-[12px] text-[var(--nf-muted)]">{category?.submission_deadline ?? "2025/02/26"}</span>
                <span className="text-[12px] text-[var(--nf-muted)]">{category?.end_date ?? "2025/03/26"}</span>
              </div>
              <Badge variant="outline" className="w-fit bg-[var(--nf-card-bg)] border-[var(--nf-dark-bg)] text-[var(--nf-light-gray)] text-[12px] px-2.5 py-1 rounded-sm">
                {category?.status === "published" ? "进行中" : category?.status === "draft" ? "草稿" : category?.status === "closed" ? "已结束" : "LIGHTNING鲸"}
              </Badge>
            </div>
          </div>

          {/* Detail Tabs */}
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
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
                <p className="text-sm text-[var(--nf-muted)]">{category?.description ?? "活动详情内容区域"}</p>
                {posts.length > 0 && (
                  <div className="mt-4">
                    <span className="text-sm text-[var(--nf-white)] font-semibold">关联帖子: {posts.length}</span>
                  </div>
                )}
                {groups.length > 0 && (
                  <div className="mt-2">
                    <span className="text-sm text-[var(--nf-white)] font-semibold">参赛团队: {groups.length}</span>
                  </div>
                )}
              </div>
            </TabsContent>
          </Tabs>
        </main>
      </div>
    </div>
  )
}
