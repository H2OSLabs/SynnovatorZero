"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { UserPlus, Loader2 } from "lucide-react"
import { PageLayout } from "@/components/layout/PageLayout"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { getFollowing, getUser, type User } from "@/lib/api-client"
import { useAuth } from "@/contexts/AuthContext"

export default function MyFollowingPage() {
  const { user } = useAuth()
  const [following, setFollowing] = useState<User[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (!user) return

    const fetchFollowing = async () => {
      setIsLoading(true)
      try {
        const resp = await getFollowing(user.user_id)
        // Fetch user details for each followed user
        const users: User[] = []
        for (const item of resp.items || []) {
          try {
            const userDetail = await getUser(item.target_user_id)
            users.push(userDetail)
          } catch {
            // User might be deleted
          }
        }
        setFollowing(users)
      } catch {
        setFollowing([])
      } finally {
        setIsLoading(false)
      }
    }
    fetchFollowing()
  }, [user])

  if (!user) {
    return (
      <PageLayout variant="compact">
        <div className="text-center py-16">
          <UserPlus className="h-16 w-16 text-nf-muted mx-auto mb-4" />
          <h1 className="text-xl font-semibold text-nf-white mb-2">请先登录</h1>
          <p className="text-nf-muted mb-6">登录后查看您的关注列表</p>
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
            我的关注
          </h1>
          <p className="text-nf-muted">您关注的用户 ({following.length})</p>
        </div>
        <Link href="/explore">
          <Button variant="outline" className="border-nf-secondary">
            发现更多用户
          </Button>
        </Link>
      </div>

      {/* Content */}
      {isLoading ? (
        <div className="flex items-center justify-center py-16">
          <Loader2 className="h-8 w-8 animate-spin text-nf-lime" />
        </div>
      ) : following.length === 0 ? (
        <div className="text-center py-16">
          <UserPlus className="h-16 w-16 text-nf-muted mx-auto mb-4" />
          <p className="text-nf-muted mb-4">您还没有关注任何人</p>
          <p className="text-nf-muted text-sm mb-6">发现并关注感兴趣的创作者</p>
          <Link href="/explore">
            <Button className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
              去发现用户
            </Button>
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {following.map((followedUser) => (
            <Link
              key={followedUser.id}
              href={`/users/${followedUser.id}`}
              className="flex items-center gap-4 p-4 bg-nf-surface rounded-lg hover:bg-nf-secondary transition-colors"
            >
              <Avatar className="h-12 w-12">
                <AvatarImage src={followedUser.avatar_url ?? undefined} />
                <AvatarFallback className="bg-nf-dark text-nf-lime">
                  {(followedUser.display_name || followedUser.username)?.[0]?.toUpperCase() || "U"}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1 min-w-0">
                <h3 className="font-medium text-nf-white truncate">
                  {followedUser.display_name || followedUser.username}
                </h3>
                <p className="text-sm text-nf-muted truncate">@{followedUser.username}</p>
              </div>
            </Link>
          ))}
        </div>
      )}
    </PageLayout>
  )
}
