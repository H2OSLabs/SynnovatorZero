"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import {
  Menu, Search, Zap, Bell, User, ChevronDown,
  Compass, Globe, Mountain, Flame, Users,
  Lightbulb, FileText, Ellipsis,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Separator } from "@/components/ui/separator"
import { listPosts, listCategories } from "@/lib/api-client"
import type { Post, Category } from "@/lib/types"

const tabs = ["热门", "提案广场", "资源", "提案专区", "找队友", "找点子", "官方"]

const tabRoutes: Record<string, string> = {
  热门: "/",
  提案广场: "/proposals",
  资源: "/assets",
  提案专区: "/proposals",
  找队友: "/posts?tag=find-teammate",
  找点子: "/posts?tag=find-idea",
  官方: "/profile",
}

const fallbackCards = [
  {
    title: "西建·滇水源 | 热帖神评选好礼!",
    author: "西建创新",
    image: "https://images.unsplash.com/photo-1718408954920-22f83687ea40?w=400&h=300&fit=crop",
  },
  {
    title: "全文智算——海天仿仿AI服装",
    author: "众创发酵",
    image: "https://images.unsplash.com/photo-1662947683270-136b00fbf3c7?w=400&h=300&fit=crop",
  },
  {
    title: "创新设计大赛·第七届",
    author: "JioNan",
    image: "https://images.unsplash.com/photo-1625333345462-1fdf591e6f73?w=400&h=300&fit=crop",
  },
]

const fallbackProposals = [
  {
    title: "百变一次创作者有创造数字身份协会AI声音数据效应同步竞赛",
    desc: "赛道推出系统的数字创作产品配套综合数据服务平台",
    author: "泉水,滇水源",
    avatarColor: "bg-[var(--nf-blue)]",
    image: "https://images.unsplash.com/photo-1603201866527-18fd9ff8fb9a?w=200&h=200&fit=crop",
  },
  {
    title: "全文智算——海天仿仿AI服装设计",
    desc: "\"全文智算\"搭配虚拟时尚技术，让AI帮你建立定制化标签式造型。",
    author: "Jacksen",
    avatarColor: "bg-[var(--nf-lime)]",
    image: "https://images.unsplash.com/photo-1731687863569-fb5bc94bb915?w=200&h=200&fit=crop",
  },
]

const quickLinks = [
  { icon: Users, label: "找交流群组" },
  { icon: FileText, label: "投交提案" },
  { icon: Ellipsis, label: "更多入口" },
]

export function Home() {
  const router = useRouter()
  const [posts, setPosts] = useState<Post[]>([])
  const [proposals, setProposals] = useState<Post[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchData() {
      try {
        const [postsRes, proposalsRes] = await Promise.all([
          listPosts({ limit: 6, status: "published" }),
          listPosts({ limit: 4, type: "for_category", status: "published" }),
        ])
        setPosts(postsRes.items)
        setProposals(proposalsRes.items)
      } catch (err) {
        console.error("Failed to fetch home data:", err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  return (
    <div className="flex flex-col h-screen bg-[var(--nf-near-black)]">
      {/* Header */}
      <header className="flex items-center justify-between h-14 px-6 border-b border-[var(--nf-dark-bg)] bg-[var(--nf-near-black)]">
        <div className="flex items-center gap-4">
          <Menu className="w-6 h-6 text-[var(--nf-white)]" />
          <span onClick={() => router.push("/")} className="cursor-pointer font-heading text-[20px] font-bold text-[var(--nf-lime)]">
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
          <div onClick={() => router.push("/")} className="cursor-pointer flex items-center gap-2.5 px-3 py-2.5 bg-[var(--nf-lime)] rounded-full">
            <Compass className="w-[18px] h-[18px] text-[var(--nf-surface)]" />
            <span className="text-sm font-semibold text-[var(--nf-surface)]">探索</span>
          </div>
          <div onClick={() => router.push("/categories/1")} className="cursor-pointer flex items-center gap-2.5 px-3 py-2.5 rounded-full">
            <Globe className="w-[18px] h-[18px] text-[var(--nf-muted)]" />
            <span className="text-sm text-[var(--nf-muted)]">星球</span>
          </div>
          <div onClick={() => router.push("/team")} className="cursor-pointer flex items-center gap-2.5 px-3 py-2.5 rounded-full">
            <Mountain className="w-[18px] h-[18px] text-[var(--nf-muted)]" />
            <span className="text-sm text-[var(--nf-muted)]">营地</span>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto p-4 px-6 flex flex-col gap-5">
          {/* Tabs */}
          <div className="flex items-center gap-4">
            {tabs.map((tab, i) =>
              i === 0 ? (
                <Badge
                  key={tab}
                  onClick={() => router.push(tabRoutes[tab] ?? "/")}
                  className="cursor-pointer bg-[var(--nf-lime)] text-[var(--nf-surface)] hover:bg-[var(--nf-lime)]/90 rounded-full px-4 py-1.5 text-[13px] font-semibold"
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

          {/* Card Grid */}
          {loading ? (
            <div className="flex items-center justify-center h-[180px] text-[var(--nf-muted)] text-sm">
              加载中...
            </div>
          ) : (
            <div className="grid grid-cols-3 gap-4">
              {(posts.length > 0
                ? posts.map((post) => ({
                    id: post.id,
                    title: post.title,
                    author: "User " + post.created_by,
                    image: "https://images.unsplash.com/photo-1718408954920-22f83687ea40?w=400&h=300&fit=crop",
                  }))
                : fallbackCards
              ).map((card) => (
                <Card key={card.title} onClick={() => router.push("id" in card && card.id ? `/posts/${card.id}` : "/posts")} className="cursor-pointer bg-[var(--nf-card-bg)] border-none rounded-[12px] overflow-hidden">
                  <div
                    className="w-full h-[180px] bg-cover bg-center"
                    style={{ backgroundImage: `url(${card.image})` }}
                  />
                  <div className="p-3 flex flex-col gap-1.5">
                    <p className="text-[13px] font-medium text-[var(--nf-white)]">{card.title}</p>
                    <div className="flex items-center gap-1.5">
                      <div className="w-[18px] h-[18px] rounded-full bg-[#555555]" />
                      <span className="text-[11px] text-[var(--nf-muted)]">{card.author}</span>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          )}

          {/* Hot Proposals Header */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Flame className="w-5 h-5 text-[var(--nf-orange)]" />
              <span className="text-[18px] font-semibold text-[var(--nf-white)]">热门提案</span>
            </div>
            <span onClick={() => router.push("/proposals")} className="text-[13px] text-[var(--nf-muted)] cursor-pointer">查看更多 &gt;</span>
          </div>

          {/* Proposal Grid */}
          <div className="grid grid-cols-2 gap-4">
            {(proposals.length > 0
              ? proposals.map((post) => ({
                  id: post.id,
                  title: post.title,
                  desc: post.body || "",
                  author: "User " + post.created_by,
                  avatarColor: "bg-[var(--nf-blue)]",
                  image: "https://images.unsplash.com/photo-1603201866527-18fd9ff8fb9a?w=200&h=200&fit=crop",
                }))
              : fallbackProposals
            ).map((prop) => (
              <Card key={prop.title} onClick={() => router.push("id" in prop && prop.id ? `/proposals/${prop.id}` : "/proposals")} className="cursor-pointer bg-[var(--nf-card-bg)] border-none rounded-[12px] p-3 flex gap-3">
                <div
                  className="w-[100px] h-[100px] rounded-lg bg-cover bg-center shrink-0"
                  style={{ backgroundImage: `url(${prop.image})` }}
                />
                <div className="flex flex-col gap-1.5 min-w-0">
                  <p className="text-[13px] font-medium text-[var(--nf-white)] line-clamp-2">{prop.title}</p>
                  <p className="text-[12px] text-[var(--nf-muted)] line-clamp-2">{prop.desc}</p>
                  <div className="flex items-center gap-2 mt-auto">
                    <div className={`w-5 h-5 rounded-full ${prop.avatarColor} flex items-center justify-center`}>
                      <User className="w-2.5 h-2.5 text-[var(--nf-white)]" />
                    </div>
                    <span className="text-[11px] text-[var(--nf-muted)]">{prop.author}</span>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </main>

        {/* Right Sidebar */}
        <aside className="w-[280px] p-4 flex flex-col gap-4">
          {/* Promo Banner */}
          <div className="bg-[var(--nf-lime)] rounded-[16px] p-5 flex flex-col gap-2">
            <span className="font-heading text-[22px] font-bold text-[var(--nf-surface)]">
              来协创,创个业
            </span>
            <span className="text-[12px] text-[var(--nf-dark-bg)]">
              来来看看Synnovator特特色。
            </span>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-2">
            <Button onClick={() => router.push("/posts")} className="flex-1 bg-[var(--nf-lime)] text-[var(--nf-surface)] hover:bg-[var(--nf-lime)]/90 rounded-full gap-1.5 py-2">
              <Users className="w-3.5 h-3.5" />
              <span className="text-[13px] font-semibold">找队友</span>
            </Button>
            <Button
              variant="outline"
              onClick={() => router.push("/posts")}
              className="flex-1 bg-[var(--nf-card-bg)] border-[var(--nf-dark-bg)] text-[var(--nf-light-gray)] hover:bg-[var(--nf-dark-bg)] rounded-full gap-1.5 py-2"
            >
              <Lightbulb className="w-3.5 h-3.5" />
              <span className="text-[13px] font-medium">找点子</span>
            </Button>
          </div>

          {/* Publish Section */}
          <div className="flex flex-col gap-2 py-3">
            <span className="text-sm font-semibold text-[var(--nf-white)]">发布提案</span>
            <span className="text-[12px] text-[var(--nf-muted)]">快来发布一个让世界惊艳的提案吧。</span>
            <Button onClick={() => router.push("/proposals")} className="bg-[var(--nf-dark-bg)] text-[var(--nf-light-gray)] hover:bg-[var(--nf-dark-bg)]/80 rounded-lg py-2.5">
              <span className="text-[13px] font-medium">立即发布</span>
            </Button>
          </div>

          {/* Quick Links */}
          <div className="flex flex-col gap-2">
            {quickLinks.map((link) => (
              <div key={link.label} className="flex items-center gap-2 py-2 cursor-pointer">
                <link.icon className="w-4 h-4 text-[var(--nf-muted)]" />
                <span className="text-[13px] text-[var(--nf-muted)]">{link.label}</span>
              </div>
            ))}
          </div>
        </aside>
      </div>
    </div>
  )
}
