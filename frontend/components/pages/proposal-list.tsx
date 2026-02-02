"use client"

import { useState, useEffect } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import {
  Menu, Search, Zap, Bell, User,
  Compass, Globe, Mountain, SlidersHorizontal,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { listCategories, listPosts } from "@/lib/api-client"
import type { Category, Post } from "@/lib/types"

const tabs = ["帖子", "提案广场", "资源", "团队", "活动", "找队友", "找点子", "官方"]

const tabRoutes: Record<string, string> = {
  帖子: "/posts",
  提案广场: "/proposals",
  资源: "/assets",
  团队: "/team",
  活动: "/",
  找队友: "/posts?tag=find-teammate",
  找点子: "/posts?tag=find-idea",
  官方: "/profile",
}

const fallbackProposals = [
  {
    title: "善意百宝——一人人需要扫有轮AI直辅学习平台",
    author: "LIGHTNING鲸",
    avatarColor: "bg-[var(--nf-lime)]",
    avatarTextColor: "text-[var(--nf-surface)]",
    image: "https://images.unsplash.com/photo-1764083292882-fd28776d0022?w=600&h=400&fit=crop",
  },
  {
    title: "探索发言——多人创新教育AI直辅学习平台",
    author: "LIGHTNING鲸",
    avatarColor: "bg-[var(--nf-blue)]",
    avatarTextColor: "text-[var(--nf-white)]",
    image: "https://images.unsplash.com/photo-1767481626838-839c89704569?w=600&h=400&fit=crop",
  },
  {
    title: "探索百宝——多人创新教育平台介绍文字",
    author: "Jacksen",
    avatarColor: "bg-[var(--nf-orange)]",
    avatarTextColor: "text-[var(--nf-white)]",
    image: "https://images.unsplash.com/photo-1766802981831-8baf453bb1ee?w=600&h=400&fit=crop",
  },
  {
    title: "善意百宝——多人创新教育系统学习服务",
    author: "LIGHTNING鲸",
    avatarColor: "bg-[var(--nf-lime)]",
    avatarTextColor: "text-[var(--nf-surface)]",
    image: "https://images.unsplash.com/photo-1620206299334-6378dde8c8e1?w=600&h=400&fit=crop",
  },
]

// Rotating avatar colors for API-fetched proposals
const avatarColors = [
  { bg: "bg-[var(--nf-lime)]", text: "text-[var(--nf-surface)]" },
  { bg: "bg-[var(--nf-blue)]", text: "text-[var(--nf-white)]" },
  { bg: "bg-[var(--nf-orange)]", text: "text-[var(--nf-white)]" },
  { bg: "bg-[var(--nf-pink)]", text: "text-[var(--nf-white)]" },
  { bg: "bg-[var(--nf-cyan)]", text: "text-[var(--nf-surface)]" },
]

export function ProposalList() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [proposals, setProposals] = useState<Post[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    async function fetchData() {
      setLoading(true)
      try {
        const statusParam = searchParams.get("status")
        const status = statusParam === "all" ? undefined : (statusParam ?? "published")
        const categoryId = searchParams.get("category_id")
        const sort = searchParams.get("sort") || "hot"
        const order_by = sort === "new" ? "created_at" : "like_count"
        const result = await listPosts({
          limit: 10,
          type: "for_category",
          status,
          category_id: categoryId ? Number(categoryId) : undefined,
          order_by,
          order: "desc",
        })
        if (cancelled) return
        setProposals(result.items)
      } catch (err) {
        console.error("Failed to fetch proposals:", err)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    fetchData()
    return () => { cancelled = true }
  }, [searchParams])

  useEffect(() => {
    let cancelled = false
    async function fetchCategories() {
      try {
        const data = await listCategories(0, 50)
        if (!cancelled) setCategories(data.items)
      } catch (err) {
        console.error("Failed to fetch categories:", err)
      }
    }
    fetchCategories()
    return () => { cancelled = true }
  }, [])

  function updateSearchParam(key: string, value: string | null) {
    const next = new URLSearchParams(searchParams.toString())
    if (value === null || value === "") next.delete(key)
    else next.set(key, value)
    router.push(`/proposals?${next.toString()}`)
  }

  const activeStatus = searchParams.get("status") || "published"
  const activeCategoryId = searchParams.get("category_id")
  const activeSort = searchParams.get("sort") || "hot"
  const activeCategoryLabel = activeCategoryId
    ? categories.find((c) => String(c.id) === String(activeCategoryId))?.name || `活动 ${activeCategoryId}`
    : "全部活动"
  return (
    <div className="flex flex-col h-screen bg-[var(--nf-near-black)]">
      {/* Header */}
      <header className="flex items-center justify-between h-14 px-6 border-b border-[var(--nf-dark-bg)] bg-[var(--nf-near-black)]">
        <div className="flex items-center gap-4">
          <Menu className="w-6 h-6 text-[var(--nf-white)]" />
          <span onClick={() => router.push("/")} className="cursor-pointer font-heading text-[20px] font-bold text-[var(--nf-lime)]">协创者</span>
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
        {/* Compact Sidebar */}
        <aside className="w-[60px] bg-[var(--nf-near-black)] flex flex-col items-center gap-3 pt-4 px-3">
          <Compass onClick={() => router.push("/")} className="cursor-pointer w-6 h-6 text-[var(--nf-muted)]" />
          <Globe onClick={() => router.push("/categories/1")} className="cursor-pointer w-6 h-6 text-[var(--nf-muted)]" />
          <Mountain onClick={() => router.push("/team")} className="cursor-pointer w-6 h-6 text-[var(--nf-muted)]" />
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto p-4 px-6 flex flex-col gap-4">
          {/* Tabs */}
          <div className="flex items-center gap-4">
            {tabs.map((tab, i) =>
              tab === "提案广场" ? (
                <Badge
                  key={tab}
                  onClick={() => router.push(tabRoutes[tab] ?? "/proposals")}
                  className="bg-[var(--nf-lime)] text-[var(--nf-surface)] hover:bg-[var(--nf-lime)]/90 rounded-full px-4 py-1.5 text-[13px] font-semibold"
                >
                  {tab}
                </Badge>
              ) : (
                <span
                  key={tab}
                  onClick={() => tabRoutes[tab] && router.push(tabRoutes[tab])}
                  className="text-[13px] text-[var(--nf-muted)] cursor-pointer hover:text-[var(--nf-white)]"
                >
                  {tab}
                </span>
              )
            )}
          </div>

          {/* Filter Row */}
          <div className="flex items-center gap-3">
            <SlidersHorizontal className="w-4 h-4 text-[var(--nf-lime)]" />
            <span className="text-[13px] font-medium text-[var(--nf-lime)]">赛道探索</span>
            <div className="w-px h-4 bg-[var(--nf-dark-bg)]" />
            <span
              onClick={() => updateSearchParam("sort", "hot")}
              className={`text-[13px] cursor-pointer ${activeSort === "hot" ? "text-[var(--nf-lime)] font-medium" : "text-[var(--nf-muted)]"}`}
            >
              热门
            </span>
            <div className="w-px h-4 bg-[var(--nf-dark-bg)]" />
            <span
              onClick={() => updateSearchParam("sort", "new")}
              className={`text-[13px] cursor-pointer ${activeSort === "new" ? "text-[var(--nf-lime)] font-medium" : "text-[var(--nf-muted)]"}`}
            >
              最新
            </span>
            <div className="ml-auto flex items-center gap-2">
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button
                    variant="outline"
                    className="h-8 rounded-full border-[var(--nf-dark-bg)] bg-[var(--nf-card-bg)] text-[12px] text-[var(--nf-light-gray)] hover:bg-[var(--nf-dark-bg)]"
                  >
                    {activeStatus === "all" ? "全部状态" : activeStatus === "published" ? "已发布" : activeStatus === "draft" ? "草稿" : activeStatus === "pending_review" ? "待审核" : activeStatus === "rejected" ? "已驳回" : "全部状态"}
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="min-w-[10rem]">
                  <DropdownMenuItem onClick={() => updateSearchParam("status", "all")}>全部状态</DropdownMenuItem>
                  <DropdownMenuItem onClick={() => updateSearchParam("status", "draft")}>草稿</DropdownMenuItem>
                  <DropdownMenuItem onClick={() => updateSearchParam("status", "pending_review")}>待审核</DropdownMenuItem>
                  <DropdownMenuItem onClick={() => updateSearchParam("status", "published")}>已发布</DropdownMenuItem>
                  <DropdownMenuItem onClick={() => updateSearchParam("status", "rejected")}>已驳回</DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>

              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button
                    variant="outline"
                    className="h-8 rounded-full border-[var(--nf-dark-bg)] bg-[var(--nf-card-bg)] text-[12px] text-[var(--nf-light-gray)] hover:bg-[var(--nf-dark-bg)]"
                  >
                    {activeCategoryLabel}
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="min-w-[12rem]">
                  <DropdownMenuItem onClick={() => updateSearchParam("category_id", null)}>全部活动</DropdownMenuItem>
                  {categories.map((c) => (
                    <DropdownMenuItem key={c.id} onClick={() => updateSearchParam("category_id", String(c.id))}>
                      {c.name}
                    </DropdownMenuItem>
                  ))}
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>

          {/* Proposal Grid */}
          <div className="grid grid-cols-2 gap-4">
            {loading ? (
              <div className="col-span-2 flex items-center justify-center py-12">
                <span className="text-[var(--nf-muted)] text-lg">加载中...</span>
              </div>
            ) : proposals.length > 0 ? (
              proposals.map((prop, i) => {
                const colorSet = avatarColors[i % avatarColors.length]
                return (
                  <Card key={prop.id} onClick={() => router.push(`/proposals/${prop.id}`)} className="cursor-pointer bg-[var(--nf-card-bg)] border-none rounded-[12px] overflow-hidden">
                    <div className="w-full h-[180px] bg-[var(--nf-dark-bg)]" />
                    <div className="p-3 flex flex-col gap-2">
                      <p className="text-[13px] font-medium text-[var(--nf-white)]">{prop.title}</p>
                      <div className="flex items-center gap-2">
                        <div className={`w-5 h-5 rounded-full ${colorSet.bg} flex items-center justify-center`}>
                          <User className="w-2.5 h-2.5" />
                        </div>
                        <span className="text-[11px] text-[var(--nf-muted)]">{"User " + prop.created_by}</span>
                      </div>
                    </div>
                  </Card>
                )
              })
            ) : (
              fallbackProposals.map((prop, i) => (
                <Card key={i} onClick={() => router.push("/proposals")} className="cursor-pointer bg-[var(--nf-card-bg)] border-none rounded-[12px] overflow-hidden">
                  <div
                    className="w-full h-[180px] bg-cover bg-center"
                    style={{ backgroundImage: `url(${prop.image})` }}
                  />
                  <div className="p-3 flex flex-col gap-2">
                    <p className="text-[13px] font-medium text-[var(--nf-white)]">{prop.title}</p>
                    <div className="flex items-center gap-2">
                      <div className={`w-5 h-5 rounded-full ${prop.avatarColor} flex items-center justify-center`}>
                        <User className="w-2.5 h-2.5" />
                      </div>
                      <span className="text-[11px] text-[var(--nf-muted)]">{prop.author}</span>
                    </div>
                  </div>
                </Card>
              ))
            )}
          </div>
        </main>
      </div>
    </div>
  )
}
