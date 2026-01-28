"use client"

import { useState, useEffect } from "react"
import {
  Menu, Search, Zap, Bell, User, ChevronDown,
  Compass, Globe, Mountain, Wallet,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { listResources } from "@/lib/api-client"
import type { Resource } from "@/lib/types"

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
  const [resources, setResources] = useState<Resource[]>([])
  const [loading, setLoading] = useState(true)
  const [activeFilter, setActiveFilter] = useState<string>("all")

  useEffect(() => {
    let cancelled = false
    async function fetchData() {
      setLoading(true)
      try {
        const data = await listResources(0, 20)
        if (!cancelled) {
          setResources(data.items)
        }
      } catch (err) {
        console.error("Failed to fetch resources:", err)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    fetchData()
    return () => { cancelled = true }
  }, [])

  const filteredResources = activeFilter === "all"
    ? resources
    : resources.filter((r) => r.mime_type?.startsWith(activeFilter))

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
          <span className="font-heading text-[20px] font-bold text-[var(--nf-lime)]">
            协创者
          </span>
        </div>
        <div className="flex items-center gap-2 w-[400px] bg-[var(--nf-card-bg)] border border-[var(--nf-dark-bg)] rounded-[21px] px-5 py-2.5">
          <Search className="w-4 h-4 text-[var(--nf-muted)]" />
          <span className="text-sm text-[var(--nf-muted)]">搜索</span>
        </div>
        <div className="flex items-center gap-3">
          <Button className="bg-[var(--nf-lime)] text-[var(--nf-surface)] hover:bg-[var(--nf-lime)]/90 rounded-full px-[18px] py-2 gap-1.5">
            <Zap className="w-4 h-4" />
            <span className="text-sm font-medium">发布新内容</span>
          </Button>
          <Bell className="w-6 h-6 text-[var(--nf-white)]" />
          <Avatar className="w-8 h-8 bg-[var(--nf-blue)]">
            <AvatarFallback className="bg-[var(--nf-blue)]">
              <User className="w-4 h-4 text-[var(--nf-white)]" />
            </AvatarFallback>
          </Avatar>
          <ChevronDown className="w-4 h-4 text-[var(--nf-white)]" />
        </div>
      </header>

      {/* Body */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar */}
        <aside className="w-[140px] bg-[var(--nf-near-black)] p-4 px-3 flex flex-col gap-1">
          <div className="flex items-center gap-2.5 px-3 py-2.5 bg-[var(--nf-lime)] rounded-full">
            <Compass className="w-[18px] h-[18px] text-[var(--nf-surface)]" />
            <span className="text-sm font-semibold text-[var(--nf-surface)]">探索</span>
          </div>
          <div className="flex items-center gap-2.5 px-3 py-2.5 rounded-full">
            <Globe className="w-[18px] h-[18px] text-[var(--nf-muted)]" />
            <span className="text-sm text-[var(--nf-muted)]">星球</span>
          </div>
          <div className="flex items-center gap-2.5 px-3 py-2.5 rounded-full">
            <Mountain className="w-[18px] h-[18px] text-[var(--nf-muted)]" />
            <span className="text-sm text-[var(--nf-muted)]">营地</span>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto px-8 py-6 flex flex-col gap-5">
          {/* Title Row */}
          <div className="flex items-center gap-2">
            <Wallet className="w-5 h-5 text-[var(--nf-lime)]" />
            <span className="text-[20px] font-semibold text-[var(--nf-white)]">
              我的资产
            </span>
          </div>

          {/* Category Tabs */}
          <div className="grid grid-cols-3 gap-4">
            {/* All - Filter */}
            <Card
              className={`h-[100px] bg-[var(--nf-card-bg)] rounded-[12px] p-4 flex items-center gap-4 cursor-pointer ${activeFilter === "all" ? "border-2 border-[var(--nf-lime)]" : "border border-[var(--nf-dark-bg)]"}`}
              onClick={() => setActiveFilter("all")}
            >
              <div className="w-[60px] h-[60px] rounded-lg bg-[var(--nf-dark-bg)] shrink-0" />
              <div className="flex flex-col gap-1">
                <span className={`text-[16px] font-bold ${activeFilter === "all" ? "text-[var(--nf-lime)]" : "text-[var(--nf-white)]"}`}>
                  全部
                </span>
                <span className="font-mono text-[13px] text-[var(--nf-light-gray)]">
                  {resources.length} 个资源
                </span>
              </div>
            </Card>

            {/* Image Filter */}
            <Card
              className={`h-[100px] bg-[var(--nf-card-bg)] rounded-[12px] flex items-center justify-center cursor-pointer ${activeFilter === "image" ? "border-2 border-[var(--nf-lime)]" : "border border-[var(--nf-dark-bg)]"}`}
              onClick={() => setActiveFilter("image")}
            >
              <span className={`text-[16px] font-semibold ${activeFilter === "image" ? "text-[var(--nf-lime)]" : "text-[var(--nf-white)]"}`}>
                图片
              </span>
            </Card>

            {/* Document Filter */}
            <Card
              className={`h-[100px] bg-[var(--nf-card-bg)] rounded-[12px] flex items-center justify-center cursor-pointer ${activeFilter === "application" ? "border-2 border-[var(--nf-lime)]" : "border border-[var(--nf-dark-bg)]"}`}
              onClick={() => setActiveFilter("application")}
            >
              <span className={`text-[16px] font-semibold ${activeFilter === "application" ? "text-[var(--nf-lime)]" : "text-[var(--nf-white)]"}`}>
                文件
              </span>
            </Card>
          </div>

          {/* Assets Grid */}
          <div className="grid grid-cols-2 gap-4">
            {filteredResources.length > 0 ? filteredResources.map((resource) => (
              <Card
                key={resource.id}
                className="bg-[var(--nf-card-bg)] border border-[var(--nf-dark-bg)] rounded-[12px] p-4 flex flex-col gap-2"
              >
                <span className="text-[15px] font-semibold text-[var(--nf-white)]">
                  {resource.display_name || resource.filename}
                </span>

                <div className="flex items-center gap-2">
                  {resource.mime_type && (
                    <Badge
                      className="rounded-sm px-2 py-0.5 text-[11px] border-transparent bg-[var(--nf-lime)] text-[var(--nf-surface)]"
                    >
                      {resource.mime_type.split("/")[1] || resource.mime_type}
                    </Badge>
                  )}
                  {resource.file_size && (
                    <Badge
                      className="rounded-sm px-2 py-0.5 text-[11px] border-transparent bg-[var(--nf-orange)] text-[var(--nf-white)]"
                    >
                      {(resource.file_size / 1024).toFixed(1)} KB
                    </Badge>
                  )}
                </div>

                <p className="text-[12px] text-[var(--nf-muted)]">
                  {resource.description || "暂无描述"}
                </p>

                <div className="flex items-center justify-between mt-auto">
                  <div className="flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-[#00B42A]" />
                    <span className="text-[11px] text-[#00B42A]">可用</span>
                  </div>
                  {resource.created_at && (
                    <span className="text-[11px] text-[var(--nf-muted)]">
                      创建于: {new Date(resource.created_at).toLocaleDateString()}
                    </span>
                  )}
                </div>
              </Card>
            )) : fallbackAssetCards.map((asset, index) => (
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
        </main>

        {/* Right Panel */}
        <aside className="w-[360px] p-4">
          <div className="h-full bg-[#F5F5F5] rounded-[12px]" />
        </aside>
      </div>
    </div>
  )
}
