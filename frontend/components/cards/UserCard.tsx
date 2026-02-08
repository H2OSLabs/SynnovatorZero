"use client"

import Link from "next/link"
import { FileText, Calendar, Heart } from "lucide-react"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface UserCardProps {
  id: number
  username: string
  display_name?: string
  bio?: string
  avatar_url?: string
  role?: "participant" | "organizer" | "admin"
  post_count?: number
  event_count?: number
  like_count?: number
  is_following?: boolean
  onFollow?: () => void
  className?: string
}

export function UserCard({
  id,
  username,
  display_name,
  bio,
  avatar_url,
  role,
  post_count = 0,
  event_count = 0,
  like_count = 0,
  is_following = false,
  onFollow,
  className,
}: UserCardProps) {
  // Truncate bio
  const truncatedBio = bio
    ? bio.slice(0, 60) + (bio.length > 60 ? "..." : "")
    : null

  const handleFollowClick = (e: React.MouseEvent) => {
    e.preventDefault()
    e.stopPropagation()
    onFollow?.()
  }

  return (
    <Link href={`/users/${id}`} prefetch={false}>
      <Card className={cn("bg-nf-secondary border-none hover:bg-nf-secondary/80 transition-colors cursor-pointer", className)}>
        <CardHeader className="p-4 pb-2">
          <div className="flex items-center gap-3">
            <Avatar className="h-12 w-12">
              <AvatarImage src={avatar_url} />
              <AvatarFallback className="bg-gradient-to-br from-nf-lime to-nf-cyan text-nf-near-black font-bold">
                {(display_name || username).charAt(0).toUpperCase()}
              </AvatarFallback>
            </Avatar>
            <div className="flex-1">
              <h3 className="font-heading font-semibold text-nf-white">
                {display_name || username}
              </h3>
              <p className="text-sm text-nf-muted">@{username}</p>
            </div>
          </div>
        </CardHeader>

        {truncatedBio && (
          <CardContent className="px-4 py-2">
            <p className="text-sm text-nf-muted line-clamp-2">{truncatedBio}</p>
          </CardContent>
        )}

        <CardContent className="p-4 pt-2">
          {/* Stats */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4 text-sm text-nf-muted">
              <div className="flex items-center gap-1">
                <FileText className="h-4 w-4" />
                <span>{post_count}</span>
              </div>
              <div className="flex items-center gap-1">
                <Calendar className="h-4 w-4" />
                <span>{event_count}</span>
              </div>
              <div className="flex items-center gap-1">
                <Heart className="h-4 w-4" />
                <span>{like_count}</span>
              </div>
            </div>
            {onFollow && (
              <Button
                size="sm"
                variant={is_following ? "secondary" : "default"}
                onClick={handleFollowClick}
                className={cn(
                  "h-8",
                  !is_following && "bg-nf-lime text-nf-near-black hover:bg-nf-lime/90"
                )}
              >
                {is_following ? "已关注" : "+ 关注"}
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    </Link>
  )
}
