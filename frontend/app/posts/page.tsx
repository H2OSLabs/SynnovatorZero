"use client"

import { Suspense, useEffect, useMemo, useState } from "react"
import { Search, SlidersHorizontal, Plus } from "lucide-react"
import Link from "next/link"
import { useRouter, useSearchParams } from "next/navigation"
import { PageLayout } from "@/components/layout/PageLayout"
import { PostCard } from "@/components/cards/PostCard"
import { PostsFilterDialog } from "@/components/post/PostsFilterDialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { getPosts, getUser, type Post, type PostStatus } from "@/lib/api-client"

function PostsContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const paramsKey = searchParams?.toString() ?? ""

  const [activeTab, setActiveTab] = useState("all")
  const [searchQuery, setSearchQuery] = useState("")
  const [filterOpen, setFilterOpen] = useState(false)
  const [posts, setPosts] = useState<Post[]>([])
  const [usersById, setUsersById] = useState<Record<number, { id: number; username: string; display_name?: string; avatar_url?: string }>>({})
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const applied = useMemo(() => {
    const q = searchParams?.get("q") ?? ""
    const type = searchParams?.get("type") ?? undefined
    const status = (searchParams?.get("status") ?? undefined) as PostStatus | undefined
    const tagsText = searchParams?.get("tags") ?? ""
    const tags = tagsText
      ? tagsText
          .split(",")
          .map((t) => t.trim())
          .filter(Boolean)
      : []
    return { q, type, status, tags }
  }, [paramsKey, searchParams])

  useEffect(() => {
    setSearchQuery(applied.q)
    if (!applied.type) {
      setActiveTab("all")
      return
    }
    if (applied.type === "proposal") setActiveTab("proposals")
    else if (applied.type === "team") setActiveTab("teams")
    else if (applied.type === "general") setActiveTab("general")
    else setActiveTab("all")
  }, [applied.q, applied.type])

  function updateParams(patch: { q?: string | null; type?: string | null; status?: PostStatus | null; tags?: string[] | null }) {
    const next = new URLSearchParams(searchParams?.toString() ?? "")

    if (patch.q !== undefined) {
      if (!patch.q) next.delete("q")
      else next.set("q", patch.q)
    }
    if (patch.type !== undefined) {
      if (!patch.type) next.delete("type")
      else next.set("type", patch.type)
    }
    if (patch.status !== undefined) {
      if (!patch.status) next.delete("status")
      else next.set("status", patch.status)
    }
    if (patch.tags !== undefined) {
      if (!patch.tags?.length) next.delete("tags")
      else next.set("tags", patch.tags.join(","))
    }

    const qs = next.toString()
    router.replace(qs ? `/posts?${qs}` : "/posts")
  }

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true)
      setError(null)
      try {
        const resp = await getPosts(0, 100, {
          type: applied.type,
          status: applied.status,
          tags: applied.tags.length ? applied.tags : undefined,
          q: applied.q.trim() ? applied.q.trim() : undefined,
        })
        setPosts(resp.items)

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
        const map: Record<number, { id: number; username: string; display_name?: string; avatar_url?: string }> = {}
        for (const u of users) {
          if (!u) continue
          map[u.id] = {
            id: u.id,
            username: u.username,
            display_name: u.display_name ?? undefined,
            avatar_url: u.avatar_url ?? undefined,
          }
        }
        setUsersById(map)
      } catch (e) {
        setError(e instanceof Error ? e.message : "加载失败")
        setPosts([])
        setUsersById({})
      } finally {
        setIsLoading(false)
      }
    }
    fetchData()
  }, [applied.q, applied.status, applied.tags, applied.type])

  const filteredPosts = useMemo(() => {
    const q = applied.q.trim().toLowerCase()
    const requiredTags = applied.tags.map((t) => t.toLowerCase())

    return posts.filter((post) => {
      if (activeTab === "proposals" && post.type !== "proposal") return false
      if (activeTab === "teams" && post.type !== "team") return false
      if (activeTab === "general" && post.type !== "general") return false

      if (q) {
        const inTitle = post.title?.toLowerCase().includes(q)
        const inContent = (post.content ?? "").toLowerCase().includes(q)
        const inTags = (post.tags ?? []).some((t) => (t ?? "").toLowerCase().includes(q))
        if (!inTitle && !inContent && !inTags) return false
      }

      if (requiredTags.length) {
        const postTags = (post.tags ?? []).map((t) => (t ?? "").toLowerCase())
        const matched = requiredTags.some((t) => postTags.includes(t))
        if (!matched) return false
      }

      return true
    })
  }, [activeTab, applied.q, applied.tags, posts])

  return (
    <PageLayout variant="compact">
      <PostsFilterDialog
        open={filterOpen}
        onOpenChange={setFilterOpen}
        value={{ type: applied.type, status: applied.status, tags: applied.tags }}
        onApply={(next) => {
          updateParams({
            type: next.type ?? null,
            status: next.status ?? null,
            tags: next.tags ?? null,
          })
        }}
        onReset={() => {
          updateParams({ type: null, status: null, tags: null })
        }}
      />

      {/* Page Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="font-heading text-3xl font-bold text-nf-white mb-2">📝 帖子</h1>
          <p className="text-nf-muted">浏览社区帖子和项目作品</p>
        </div>
        <Link href="/posts/create">
          <Button className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
            <Plus className="h-4 w-4 mr-2" />
            发布帖子
          </Button>
        </Link>
      </div>

      {/* Search & Filter */}
      <div className="flex gap-4 mb-6">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-nf-muted" />
          <Input
            placeholder="搜索帖子..."
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
        <Button variant="outline" className="border-nf-secondary" onClick={() => setFilterOpen(true)}>
          <SlidersHorizontal className="h-4 w-4 mr-2" />
          筛选
        </Button>
      </div>

      {/* Tabs */}
      <Tabs
        value={activeTab}
        onValueChange={(nextTab) => {
          setActiveTab(nextTab)
          if (nextTab === "proposals") updateParams({ type: "proposal" })
          else if (nextTab === "teams") updateParams({ type: "team" })
          else if (nextTab === "general") updateParams({ type: "general" })
          else updateParams({ type: null })
        }}
      >
        <TabsList className="bg-nf-surface border-nf-secondary mb-6">
          <TabsTrigger value="all">全部</TabsTrigger>
          <TabsTrigger value="proposals">💡 提案</TabsTrigger>
          <TabsTrigger value="teams">👥 找队友</TabsTrigger>
          <TabsTrigger value="general">📝 日常</TabsTrigger>
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
          ) : filteredPosts.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredPosts.map((post) => (
                <PostCard
                  key={post.id}
                  id={post.id}
                  title={post.title}
                  body={post.content ?? undefined}
                  type={post.type}
                  status={post.status}
                  tags={post.tags ?? []}
                  created_at={post.created_at ?? undefined}
                  created_by={post.created_by ? usersById[post.created_by] : undefined}
                  like_count={post.like_count ?? 0}
                  comment_count={post.comment_count ?? 0}
                />
              ))}
            </div>
          ) : (
            <div className="text-center py-16">
              <p className="text-nf-muted">暂无帖子</p>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </PageLayout>
  )
}

export default function PostsPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-nf-dark flex items-center justify-center text-nf-muted">加载中...</div>}>
      <PostsContent />
    </Suspense>
  )
}
