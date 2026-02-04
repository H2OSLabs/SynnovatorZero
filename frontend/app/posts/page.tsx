"use client"

import { useEffect, useState } from "react"
import { Search, SlidersHorizontal, Plus } from "lucide-react"
import Link from "next/link"
import { PageLayout } from "@/components/layout/PageLayout"
import { PostCard } from "@/components/cards/PostCard"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { getPosts, getUser, type Post } from "@/lib/api-client"

export default function PostsPage() {
  const [activeTab, setActiveTab] = useState("all")
  const [posts, setPosts] = useState<Post[]>([])
  const [usersById, setUsersById] = useState<Record<number, { id: number; username: string; display_name?: string; avatar_url?: string }>>({})
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true)
      setError(null)
      try {
        const resp = await getPosts(0, 100)
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
          map[u.id] = { id: u.id, username: u.username, display_name: u.display_name, avatar_url: u.avatar_url }
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
  }, [])

  const filteredPosts = posts.filter((post) => {
    if (activeTab === "all") return true
    if (activeTab === "proposals") return post.type === "for_category"
    if (activeTab === "teams") return post.type === "team"
    if (activeTab === "general") return post.type === "general"
    return true
  })

  return (
    <PageLayout variant="compact">
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
