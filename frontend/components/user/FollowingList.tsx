'use client'

import { useState, useEffect } from 'react'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { ScrollArea } from '@/components/ui/scroll-area'
import { UserFollowButton } from './UserFollowButton'
import { getFollowing, getUser } from '@/lib/api-client'

interface FollowingInfo {
  id: number
  username: string
  avatar_url?: string
  bio?: string
}

interface FollowingListProps {
  userId: number
  currentUserId?: number
  limit?: number
  showFollowButton?: boolean
  className?: string
}

export function FollowingList({
  userId,
  currentUserId,
  limit = 20,
  showFollowButton = true,
  className = '',
}: FollowingListProps) {
  const [following, setFollowing] = useState<FollowingInfo[]>([])
  const [total, setTotal] = useState(0)
  const [skip, setSkip] = useState(0)
  const [isLoading, setIsLoading] = useState(true)
  const [hasMore, setHasMore] = useState(false)

  const fetchFollowing = async (offset: number, append: boolean = false) => {
    setIsLoading(true)
    try {
      const { items, total: totalCount } = await getFollowing(userId, offset, limit)
      setTotal(totalCount)
      setHasMore(offset + items.length < totalCount)

      // Fetch user details for each following
      const followingDetails = await Promise.all(
        items.map(async (item) => {
          try {
            const user = await getUser(item.target_user_id)
            return {
              id: user.id,
              username: user.username,
              avatar_url: user.avatar_url ?? undefined,
              bio: user.bio ?? undefined,
            }
          } catch {
            return {
              id: item.target_user_id,
              username: `User ${item.target_user_id}`,
            }
          }
        })
      )

      if (append) {
        setFollowing(prev => [...prev, ...followingDetails])
      } else {
        setFollowing(followingDetails)
      }
    } catch (err) {
      console.error('Failed to fetch following:', err)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchFollowing(0)
  }, [userId])

  const loadMore = () => {
    const newSkip = skip + limit
    setSkip(newSkip)
    fetchFollowing(newSkip, true)
  }

  // Handle unfollow - remove from list
  const handleFollowChange = (targetUserId: number, isFollowing: boolean) => {
    if (!isFollowing && userId === currentUserId) {
      // User unfollowed from their own following list
      setFollowing(prev => prev.filter(f => f.id !== targetUserId))
      setTotal(prev => prev - 1)
    }
  }

  if (isLoading && following.length === 0) {
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

  if (following.length === 0) {
    return (
      <div className={`flex flex-col items-center justify-center py-8 text-nf-muted ${className}`}>
        <span className="text-3xl mb-2">👤</span>
        <span className="text-sm">暂未关注任何人</span>
      </div>
    )
  }

  return (
    <div className={className}>
      <div className="text-sm text-nf-muted mb-4">
        共关注 {total} 人
      </div>
      <ScrollArea className="h-[400px]">
        <div className="space-y-3">
          {following.map(user => (
            <div
              key={user.id}
              className="flex items-center gap-3 p-2 rounded-lg hover:bg-nf-dark-bg/50 transition-colors"
            >
              <Avatar className="w-10 h-10">
                <AvatarImage src={user.avatar_url} alt={user.username} />
                <AvatarFallback className="bg-nf-dark-bg text-nf-lime">
                  {user.username.charAt(0).toUpperCase()}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1 min-w-0">
                <p className="font-medium text-nf-white truncate">
                  {user.username}
                </p>
                {user.bio && (
                  <p className="text-sm text-nf-muted truncate">
                    {user.bio}
                  </p>
                )}
              </div>
              {showFollowButton && currentUserId && currentUserId !== user.id && (
                <UserFollowButton
                  currentUserId={currentUserId}
                  targetUserId={user.id}
                  initialIsFollowing={userId === currentUserId}
                  size="sm"
                  onFollowChange={(isFollowing) => handleFollowChange(user.id, isFollowing)}
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
