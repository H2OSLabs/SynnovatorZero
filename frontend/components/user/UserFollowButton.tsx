'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { followUser, unfollowUser, checkFollowing } from '@/lib/api-client'

interface UserFollowButtonProps {
  currentUserId: number
  targetUserId: number
  initialIsFollowing?: boolean
  onFollowChange?: (isFollowing: boolean) => void
  size?: 'default' | 'sm' | 'lg'
  className?: string
}

export function UserFollowButton({
  currentUserId,
  targetUserId,
  initialIsFollowing = false,
  onFollowChange,
  size = 'default',
  className = '',
}: UserFollowButtonProps) {
  const [isFollowing, setIsFollowing] = useState(initialIsFollowing)
  const [isLoading, setIsLoading] = useState(false)
  const [isChecking, setIsChecking] = useState(!initialIsFollowing)

  // Check follow status on mount if not provided
  useEffect(() => {
    if (initialIsFollowing === undefined) {
      setIsChecking(true)
      checkFollowing(currentUserId, targetUserId)
        .then(setIsFollowing)
        .finally(() => setIsChecking(false))
    }
  }, [currentUserId, targetUserId, initialIsFollowing])

  // Don't show button for self
  if (currentUserId === targetUserId) {
    return null
  }

  const handleClick = async () => {
    setIsLoading(true)
    try {
      if (isFollowing) {
        await unfollowUser(currentUserId, targetUserId)
        setIsFollowing(false)
        onFollowChange?.(false)
      } else {
        await followUser(currentUserId, targetUserId)
        setIsFollowing(true)
        onFollowChange?.(true)
      }
    } catch (err) {
      console.error('Follow action failed:', err)
    } finally {
      setIsLoading(false)
    }
  }

  if (isChecking) {
    return (
      <Button
        size={size}
        variant="outline"
        disabled
        className={`min-w-[80px] border-nf-dark-bg text-nf-muted ${className}`}
      >
        ...
      </Button>
    )
  }

  return (
    <Button
      size={size}
      variant={isFollowing ? 'outline' : 'default'}
      onClick={handleClick}
      disabled={isLoading}
      className={`min-w-[80px] transition-all ${
        isFollowing
          ? 'border-nf-dark-bg text-nf-muted hover:border-nf-error hover:text-nf-error hover:bg-nf-error/10'
          : 'bg-nf-lime text-nf-near-black hover:bg-nf-lime/90'
      } ${className}`}
    >
      {isLoading ? '...' : isFollowing ? '已关注' : '关注'}
    </Button>
  )
}
