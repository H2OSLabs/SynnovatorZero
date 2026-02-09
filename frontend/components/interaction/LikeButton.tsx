"use client"

import { useState, useEffect } from "react"
import { Heart } from "lucide-react"
import { Button } from "@/components/ui/button"
import { likePost, unlikePost, checkPostLiked } from "@/lib/api-client"
import { useAuth } from "@/contexts/AuthContext"
import { cn } from "@/lib/utils"

interface LikeButtonProps {
  postId: number
  initialCount?: number
  onCountChange?: (newCount: number) => void
  className?: string
}

export function LikeButton({ postId, initialCount = 0, onCountChange, className }: LikeButtonProps) {
  const { user } = useAuth()
  const [liked, setLiked] = useState(false)
  const [count, setCount] = useState(initialCount)
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    if (!user) return
    // Check initial like status
    checkPostLiked(postId).then(setLiked).catch(() => setLiked(false))
  }, [postId, user])

  const handleClick = async () => {
    if (!user) return
    if (isLoading) return

    setIsLoading(true)
    const prevLiked = liked
    const prevCount = count

    // Optimistic update
    setLiked(!prevLiked)
    const newCount = prevLiked ? count - 1 : count + 1
    setCount(newCount)
    onCountChange?.(newCount)

    try {
      if (prevLiked) {
        await unlikePost(postId)
      } else {
        await likePost(postId)
      }
    } catch {
      // Rollback on error
      setLiked(prevLiked)
      setCount(prevCount)
      onCountChange?.(prevCount)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Button
      variant="ghost"
      size="sm"
      className={cn(
        "gap-1.5 text-nf-muted hover:text-nf-white",
        liked && "text-red-500 hover:text-red-400",
        className
      )}
      onClick={handleClick}
      disabled={!user || isLoading}
    >
      <Heart className={cn("h-4 w-4", liked && "fill-current")} />
      <span>{count}</span>
    </Button>
  )
}
