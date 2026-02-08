"use client"

import { Suspense, useEffect, useMemo, useState } from "react"
import { Search, SlidersHorizontal, Plus } from "lucide-react"
import Link from "next/link"
import { useRouter, useSearchParams } from "next/navigation"
import { PageLayout } from "@/components/layout/PageLayout"
import { CategoryCard } from "@/components/cards/CategoryCard"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { getCategories, type Event } from "@/lib/api-client"

function EventsContent() {
  const router = useRouter()
  const searchParams = useSearchParams()

  const [activeTab, setActiveTab] = useState("all")
  const [searchQuery, setSearchQuery] = useState("")
  const [events, setCategories] = useState<Event[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Initialize search query from URL
  useEffect(() => {
    const q = searchParams?.get("q") ?? ""
    setSearchQuery(q)
  }, [searchParams])

  function updateParams(patch: { q?: string | null }) {
    const next = new URLSearchParams(searchParams?.toString() ?? "")
    if (patch.q !== undefined) {
      if (!patch.q) next.delete("q")
      else next.set("q", patch.q)
    }
    const qs = next.toString()
    router.replace(qs ? `/events?${qs}` : "/events")
  }

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true)
      setError(null)
      try {
        const status =
          activeTab === "ongoing"
            ? "published"
            : activeTab === "upcoming"
              ? "draft"
              : activeTab === "ended"
                ? "closed"
                : undefined
        const resp = await getCategories(0, 100, status ? { status } : undefined)
        setCategories(resp.items)
      } catch (e) {
        setError(e instanceof Error ? e.message : "加载失败")
        setCategories([])
      } finally {
        setIsLoading(false)
      }
    }
    fetchData()
  }, [activeTab])

  // Client-side search filtering
  const filteredCategories = useMemo(() => {
    const q = searchQuery.trim().toLowerCase()
    if (!q) return events
    return events.filter((cat) => {
      const inName = cat.name?.toLowerCase().includes(q)
      const inDesc = cat.description?.toLowerCase().includes(q)
      const inTags = (cat.tags ?? []).some((t) => t?.toLowerCase().includes(q))
      return inName || inDesc || inTags
    })
  }, [events, searchQuery])

  return (
    <PageLayout variant="compact">
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
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key !== "Enter") return
              updateParams({ q: searchQuery.trim() || null })
            }}
            onBlur={() => {
              updateParams({ q: searchQuery.trim() || null })
            }}
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
          {isLoading ? (
            <div className="text-center py-16">
              <p className="text-nf-muted">加载中...</p>
            </div>
          ) : error ? (
            <div className="text-center py-16">
              <p className="text-nf-muted">{error}</p>
            </div>
          ) : filteredCategories.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredCategories.map((cat) => (
                <CategoryCard
                  key={cat.id}
                  id={cat.id}
                  name={cat.name}
                  description={cat.description}
                  type={cat.type}
                  status={cat.status}
                  tags={cat.tags ?? []}
                  cover_image={cat.cover_image ?? undefined}
                  start_date={cat.start_date ?? undefined}
                  end_date={cat.end_date ?? undefined}
                  participant_count={cat.participant_count ?? 0}
                />
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

export default function EventsPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-nf-dark flex items-center justify-center text-nf-muted">加载中...</div>}>
      <EventsContent />
    </Suspense>
  )
}
