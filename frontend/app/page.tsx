import Link from "next/link"
import { ArrowRight, Rocket, Users, Trophy, Lightbulb } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Header } from "@/components/layout/Header"
import { CategoryCard } from "@/components/cards/CategoryCard"
import { PostCard } from "@/components/cards/PostCard"
import { PlatformStats } from "@/components/home/PlatformStats"
import { getCategories, getPosts, getUser } from "@/lib/api-client"

export default async function HomePage() {
  let hotCategories: Array<{
    id: number
    name: string
    description: string
    type: "competition" | "operation"
    status: "draft" | "published" | "closed"
    tags?: string[]
    cover_image?: string
    start_date?: string
    end_date?: string
    participant_count?: number
  }> = []
  let featuredPosts: Array<{
    id: number
    title: string
    body?: string
    type: string
    status: string
    tags?: string[]
    like_count?: number
    comment_count?: number
    created_at?: string
    created_by?: { id: number; username: string; display_name?: string; avatar_url?: string }
  }> = []

  try {
    const resp = await getCategories(0, 4, { status: "published" })
    hotCategories = resp.items.map((c) => ({
      id: c.id,
      name: c.name,
      description: c.description,
      type: c.type,
      status: c.status,
      tags: c.tags ?? [],
      cover_image: c.cover_image ?? undefined,
      start_date: c.start_date ?? undefined,
      end_date: c.end_date ?? undefined,
      participant_count: c.participant_count ?? 0,
    }))
  } catch {
    hotCategories = []
  }

  try {
    const resp = await getPosts(0, 4, { status: "published" })
    const authorIds = Array.from(
      new Set(resp.items.map((p) => p.created_by).filter((v): v is number => typeof v === "number"))
    )
    const users = await Promise.all(
      authorIds.map(async (uid) => {
        try {
          return await getUser(uid)
        } catch {
          return null
        }
      })
    )
    const usersById: Record<number, { id: number; username: string; display_name?: string; avatar_url?: string }> = {}
    for (const u of users) {
      if (!u) continue
      usersById[u.id] = { id: u.id, username: u.username, display_name: u.display_name, avatar_url: u.avatar_url }
    }
    featuredPosts = resp.items.map((p) => ({
      id: p.id,
      title: p.title,
      body: p.content ?? undefined,
      type: p.type,
      status: p.status,
      tags: p.tags ?? [],
      like_count: p.like_count ?? 0,
      comment_count: p.comment_count ?? 0,
      created_at: p.created_at ?? undefined,
      created_by: p.created_by ? usersById[p.created_by] : undefined,
    }))
  } catch {
    featuredPosts = []
  }
  return (
    <div className="min-h-screen bg-nf-dark">
      {/* Header */}
      <Header user={null} />

      {/* Hero Section */}
      <section className="pt-[60px]">
        <div className="max-w-6xl mx-auto px-4 py-20 text-center">
          <div className="flex justify-center mb-6">
            <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-nf-lime to-nf-cyan flex items-center justify-center">
              <Rocket className="h-10 w-10 text-nf-near-black" />
            </div>
          </div>
          <h1 className="font-heading text-4xl md:text-5xl lg:text-6xl font-bold text-nf-white mb-4">
            创意在这里起飞
          </h1>
          <p className="text-lg md:text-xl text-nf-muted mb-8 max-w-2xl mx-auto">
            发现最激动人心的 Hackathon，与志同道合的人组队，将创意变为现实
          </p>
          <div className="flex flex-wrap gap-4 justify-center">
            <Link href="/explore">
              <Button size="lg" className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
                探索活动
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link href="/events/create">
              <Button size="lg" variant="outline" className="border-nf-secondary text-nf-white hover:bg-nf-secondary">
                发起活动
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-12 bg-nf-surface">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="w-14 h-14 rounded-xl bg-nf-lime/20 flex items-center justify-center mx-auto mb-4">
                <Trophy className="h-7 w-7 text-nf-lime" />
              </div>
              <h3 className="font-heading text-xl font-semibold text-nf-white mb-2">参与竞赛</h3>
              <p className="text-nf-muted">
                参加各类 Hackathon 和创新大赛，展示你的技术实力
              </p>
            </div>
            <div className="text-center p-6">
              <div className="w-14 h-14 rounded-xl bg-nf-cyan/20 flex items-center justify-center mx-auto mb-4">
                <Users className="h-7 w-7 text-nf-cyan" />
              </div>
              <h3 className="font-heading text-xl font-semibold text-nf-white mb-2">组建团队</h3>
              <p className="text-nf-muted">
                找到志同道合的伙伴，组建你的梦想团队
              </p>
            </div>
            <div className="text-center p-6">
              <div className="w-14 h-14 rounded-xl bg-nf-pink/20 flex items-center justify-center mx-auto mb-4">
                <Lightbulb className="h-7 w-7 text-nf-pink" />
              </div>
              <h3 className="font-heading text-xl font-semibold text-nf-white mb-2">分享创意</h3>
              <p className="text-nf-muted">
                发布你的项目作品，获取社区反馈和支持
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Hot Events */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex items-center justify-between mb-8">
            <h2 className="font-heading text-2xl font-bold text-nf-white">🔥 热门活动</h2>
            <Link href="/events" className="text-nf-lime hover:underline text-sm">
              查看更多 →
            </Link>
          </div>
          {hotCategories.length === 0 ? (
            <div className="bg-nf-secondary rounded-xl p-6 text-nf-muted">
              暂无活动数据，请确认后端已启动并已执行种子数据（make seed）
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {hotCategories.map((category) => (
                <CategoryCard key={category.id} {...category} />
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Featured Projects */}
      <section className="py-16 bg-nf-surface">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex items-center justify-between mb-8">
            <h2 className="font-heading text-2xl font-bold text-nf-white">💡 精选项目</h2>
            <Link href="/posts" className="text-nf-lime hover:underline text-sm">
              查看更多 →
            </Link>
          </div>
          {featuredPosts.length === 0 ? (
            <div className="bg-nf-card-bg border border-nf-dark-bg rounded-xl p-6 text-nf-muted">
              暂无项目数据，请确认后端已启动并已执行种子数据（make seed）
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {featuredPosts.map((post) => (
                <PostCard key={post.id} {...post} />
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Platform Stats */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="font-heading text-2xl font-bold text-nf-white text-center mb-8">📊 平台数据</h2>
          <PlatformStats />
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-nf-surface border-t border-nf-secondary">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center gap-6">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-nf-lime to-nf-cyan flex items-center justify-center">
                <span className="text-nf-near-black font-bold text-sm">S</span>
              </div>
              <span className="font-heading font-bold text-nf-white">协创者</span>
            </div>
            <div className="flex gap-6 text-sm text-nf-muted">
              <Link href="/about" className="hover:text-nf-white">关于我们</Link>
              <Link href="/help" className="hover:text-nf-white">帮助中心</Link>
              <Link href="/contact" className="hover:text-nf-white">联系我们</Link>
              <Link href="/privacy" className="hover:text-nf-white">隐私政策</Link>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-nf-secondary text-center text-sm text-nf-muted">
            © 2024 Synnovator. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  )
}
