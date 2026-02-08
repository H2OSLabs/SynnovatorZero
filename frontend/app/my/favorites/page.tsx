"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { Heart, Loader2 } from "lucide-react"
import { PageLayout } from "@/components/layout/PageLayout"
import { PostCard } from "@/components/cards/PostCard"
import { Button } from "@/components/ui/button"
import { type Post, type User } from "@/lib/api-client"
import { useAuth } from "@/contexts/AuthContext"

interface PostWithAuthor extends Post {
  author?: User
}

export default function MyFavoritesPage() {
  const { user } = useAuth()
  const [posts, setPosts] = useState<PostWithAuthor[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (!user) return

    const fetchFavorites = async () => {
      setIsLoading(true)
      try {
        // Note: Backend doesn't have a dedicated "my likes" endpoint yet
        // For now, we'll show a placeholder message
        // In production, this would call: GET /users/{id}/likes or similar
        setPosts([])
      } catch {
        setPosts([])
      } finally {
        setIsLoading(false)
      }
    }
    fetchFavorites()
  }, [user])

  if (!user) {
    return (
      <PageLayout variant="compact">
        <div className="text-center py-16">
          <Heart className="h-16 w-16 text-nf-muted mx-auto mb-4" />
          <h1 className="text-xl font-semibold text-nf-white mb-2">请先登录</h1>
          <p className="text-nf-muted mb-6">登录后查看您的收藏</p>
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
            我的收藏
          </h1>
          <p className="text-nf-muted">您点赞收藏的所有内容</p>
        </div>
        <Link href="/explore">
          <Button variant="outline" className="border-nf-secondary">
            发现更多内容
          </Button>
        </Link>
      </div>

      {/* Content */}
      {isLoading ? (
        <div className="flex items-center justify-center py-16">
          <Loader2 className="h-8 w-8 animate-spin text-nf-lime" />
        </div>
      ) : posts.length === 0 ? (
        <div className="text-center py-16">
          <Heart className="h-16 w-16 text-nf-muted mx-auto mb-4" />
          <p className="text-nf-muted mb-4">暂无收藏内容</p>
          <p className="text-nf-muted text-sm mb-6">点赞喜欢的内容，它们将出现在这里</p>
          <Link href="/explore">
            <Button className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
              去发现内容
            </Button>
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {posts.map((post) => (
            <PostCard
              key={post.id}
              id={post.id}
              title={post.title}
              body={post.content ?? undefined}
              type={post.type}
              status={post.status}
              tags={post.tags ?? []}
              created_at={post.created_at ?? undefined}
              created_by={
                post.author
                  ? {
                      id: post.author.id,
                      username: post.author.username,
                      display_name: post.author.display_name ?? undefined,
                      avatar_url: post.author.avatar_url ?? undefined,
                    }
                  : undefined
              }
              like_count={post.like_count ?? 0}
              comment_count={post.comment_count ?? 0}
            />
          ))}
        </div>
      )}
    </PageLayout>
  )
}
