'use client'

import { useState, useEffect } from 'react'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { ScrollArea } from '@/components/ui/scroll-area'
import { UserFollowButton } from './UserFollowButton'
import { getFollowers, getUser } from '@/lib/api-client'

interface FollowerInfo {
  id: number
  username: string
  avatar_url?: string
  bio?: string
}

interface FollowersListProps {
  userId: number
  currentUserId?: number
  limit?: number
  showFollowButton?: boolean
  className?: string
}

export function FollowersList({
  userId,
  currentUserId,
  limit = 20,
  showFollowButton = true,
  className = '',
}: FollowersListProps) {
  const [followers, setFollowers] = useState<FollowerInfo[]>([])
  const [total, setTotal] = useState(0)
  const [skip, setSkip] = useState(0)
  const [isLoading, setIsLoading] = useState(true)
  const [hasMore, setHasMore] = useState(false)

  const fetchFollowers = async (offset: number, append: boolean = false) => {
    setIsLoading(true)
    try {
      const { items, total: totalCount } = await getFollowers(userId, offset, limit)
      setTotal(totalCount)
      setHasMore(offset + items.length < totalCount)

      // Fetch user details for each follower
      const followerDetails = await Promise.all(
        items.map(async (item) => {
          try {
            const user = await getUser(item.source_user_id)
            return {
              id: user.id,
              username: user.username,
              avatar_url: user.avatar_url,
              bio: user.bio,
            }
          } catch {
            return {
              id: item.source_user_id,
              username: `User ${item.source_user_id}`,
            }
          }
        })
      )

      if (append) {
        setFollowers(prev => [...prev, ...followerDetails])
      } else {
        setFollowers(followerDetails)
      }
    } catch (err) {
      console.error('Failed to fetch followers:', err)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchFollowers(0)
  }, [userId])

  const loadMore = () => {
    const newSkip = skip + limit
    setSkip(newSkip)
    fetchFollowers(newSkip, true)
  }

  if (isLoading && followers.length === 0) {
    return (
      <div className={`space-y-4 ${className}`}>
        {Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="flex items-center gap-3">
            <Skeleton className="w-10 h-10 rounded-full bg-nf-dark-bg" />
            <div className="flex-1">
              <Skeleton className="h-4 w-24 mb-1 bg-nf-dark-bg" />
              <Skeleton className="h-3 w-40 bg-nf-dark-bg" />
            </div>
          </div>
        ))}
      </div>
    )
  }

  if (followers.length === 0) {
    return (
      <div className={`flex flex-col items-center justify-center py-8 text-nf-muted ${className}`}>
        <span className="text-3xl mb-2">👥</span>
        <span className="text-sm">暂无粉丝</span>
      </div>
    )
  }

  return (
    <div className={className}>
      <div className="text-sm text-nf-muted mb-4">
        共 {total} 位粉丝
      </div>
      <ScrollArea className="h-[400px]">
        <div className="space-y-3">
          {followers.map(follower => (
            <div
              key={follower.id}
              className="flex items-center gap-3 p-2 rounded-lg hover:bg-nf-dark-bg/50 transition-colors"
            >
              <Avatar className="w-10 h-10">
                <AvatarImage src={follower.avatar_url} alt={follower.username} />
                <AvatarFallback className="bg-nf-dark-bg text-nf-lime">
                  {follower.username.charAt(0).toUpperCase()}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1 min-w-0">
                <p className="font-medium text-nf-white truncate">
                  {follower.username}
                </p>
                {follower.bio && (
                  <p className="text-sm text-nf-muted truncate">
                    {follower.bio}
                  </p>
                )}
              </div>
              {showFollowButton && currentUserId && currentUserId !== follower.id && (
                <UserFollowButton
                  currentUserId={currentUserId}
                  targetUserId={follower.id}
                  size="sm"
                />
              )}
            </div>
          ))}
        </div>
        {hasMore && (
          <div className="mt-4 flex justify-center">
            <Button
              variant="outline"
              size="sm"
              onClick={loadMore}
              disabled={isLoading}
              className="border-nf-dark-bg text-nf-muted hover:text-nf-white"
            >
              {isLoading ? '加载中...' : '加载更多'}
            </Button>
          </div>
        )}
      </ScrollArea>
    </div>
  )
}
