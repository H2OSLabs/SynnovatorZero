"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { Edit3, Plus, Loader2 } from "lucide-react"
import { PageLayout } from "@/components/layout/PageLayout"
import { PostCard } from "@/components/cards/PostCard"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { getPosts, type Post } from "@/lib/api-client"
import { useAuth } from "@/contexts/AuthContext"

export default function MyPostsPage() {
  const { user } = useAuth()
  const [posts, setPosts] = useState<Post[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [activeTab, setActiveTab] = useState("all")

  useEffect(() => {
    if (!user) return

    const fetchPosts = async () => {
      setIsLoading(true)
      try {
        const resp = await getPosts(0, 100, { created_by: user.user_id })
        setPosts(resp.items)
      } catch {
        setPosts([])
      } finally {
        setIsLoading(false)
      }
    }
    fetchPosts()
  }, [user])

  const filteredPosts = posts.filter((post) => {
    if (activeTab === "published") return post.status === "published"
    if (activeTab === "pending") return post.status === "pending_review"
    if (activeTab === "draft") return post.status === "draft"
    return true
  })

  if (!user) {
    return (
      <PageLayout variant="compact">
        <div className="text-center py-16">
          <Edit3 className="h-16 w-16 text-nf-muted mx-auto mb-4" />
          <h1 className="text-xl font-semibold text-nf-white mb-2">请先登录</h1>
          <p className="text-nf-muted mb-6">登录后查看您的帖子</p>
          <Link href="/login">
            <Button className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
              立即登录
            </Button>
          </Link>
        </div>
      </PageLayout>
    )
  }

  return (
    <PageLayout variant="compact">
      {/* Page Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="font-heading text-3xl font-bold text-nf-white mb-2">
            我的帖子
          </h1>
          <p className="text-nf-muted">管理您发布的所有内容</p>
        </div>
        <Link href="/posts/create">
          <Button className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
            <Plus className="h-4 w-4 mr-2" />
            发布帖子
          </Button>
        </Link>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="bg-nf-surface border-nf-secondary mb-6">
          <TabsTrigger value="all">全部 ({posts.length})</TabsTrigger>
          <TabsTrigger value="published">
            已发布 ({posts.filter((p) => p.status === "published").length})
          </TabsTrigger>
          <TabsTrigger value="pending">
            待审核 ({posts.filter((p) => p.status === "pending_review").length})
          </TabsTrigger>
          <TabsTrigger value="draft">
            草稿 ({posts.filter((p) => p.status === "draft").length})
          </TabsTrigger>
        </TabsList>

        <TabsContent value={activeTab}>
          {isLoading ? (
            <div className="flex items-center justify-center py-16">
              <Loader2 className="h-8 w-8 animate-spin text-nf-lime" />
            </div>
          ) : filteredPosts.length === 0 ? (
            <div className="text-center py-16">
              <Edit3 className="h-16 w-16 text-nf-muted mx-auto mb-4" />
              <p className="text-nf-muted mb-4">暂无帖子</p>
              <Link href="/posts/create">
                <Button className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
                  发布第一篇帖子
                </Button>
              </Link>
            </div>
          ) : (
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
                  like_count={post.like_count ?? 0}
                  comment_count={post.comment_count ?? 0}
                />
              ))}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </PageLayout>
  )
}
