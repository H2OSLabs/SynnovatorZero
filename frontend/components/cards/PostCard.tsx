"use client"

import Link from "next/link"
import { Heart, MessageCircle } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { cn } from "@/lib/utils"
import { getPostTypeIcon } from "@/lib/post-type"

interface PostCardProps {
  id: number
  title: string
  body?: string
  type: string
  status: string
  tags?: string[]
  created_at?: string
  created_by?: {
    id: number
    display_name?: string
    username: string
    avatar_url?: string
  }
  group?: {
    id: number
    name: string
  }
  like_count?: number
  comment_count?: number
  className?: string
}

export function PostCard({
  id,
  title,
  body,
  type,
  status,
  tags = [],
  created_at,
  created_by,
  group,
  like_count = 0,
  comment_count = 0,
  className,
}: PostCardProps) {
  const formatDate = (dateStr?: string) => {
    if (!dateStr) return null
    return new Date(dateStr).toLocaleDateString("zh-CN", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    })
  }

  // Strip markdown and truncate body
  const truncatedBody = body
    ? body.replace(/[#*`\[\]]/g, "").slice(0, 100) + (body.length > 100 ? "..." : "")
    : null

  return (
    <Link href={`/posts/${id}`}>
      <Card className={cn("bg-nf-secondary border-none hover:bg-nf-secondary/80 transition-colors cursor-pointer", className)}>
        <CardHeader className="p-4 pb-2">
          <h3 className="font-heading font-semibold text-nf-white line-clamp-2">
            {getPostTypeIcon(type)} {title}
          </h3>
        </CardHeader>

        {truncatedBody && (
          <CardContent className="px-4 py-2">
            <p className="text-sm text-nf-muted line-clamp-2">{truncatedBody}</p>
          </CardContent>
        )}

        <CardContent className="px-4 py-2">
          <div className="flex items-center gap-3">
            {created_by && (
              <>
                <Avatar className="h-6 w-6">
                  <AvatarImage src={created_by.avatar_url} />
                  <AvatarFallback className="text-xs bg-nf-dark">
                    {(created_by.display_name || created_by.username).charAt(0).toUpperCase()}
                  </AvatarFallback>
                </Avatar>
                <div className="text-sm">
                  <span className="text-nf-white">{created_by.display_name || created_by.username}</span>
                  {group && <span className="text-nf-muted"> · {group.name}</span>}
                </div>
              </>
            )}
          </div>
          {created_at && (
            <p className="text-xs text-nf-muted mt-1">{formatDate(created_at)}</p>
          )}
        </CardContent>

        <CardFooter className="p-4 pt-2 flex items-center justify-between">
          <div className="flex items-center gap-2 flex-wrap">
            {tags.slice(0, 3).map((tag) => (
              <Badge key={tag} variant="secondary" className="bg-nf-dark text-nf-white text-xs">
                {tag}
              </Badge>
            ))}
          </div>
          <div className="flex items-center gap-3 text-sm text-nf-muted">
            <div className="flex items-center gap-1">
              <Heart className="h-4 w-4" />
              <span>{like_count}</span>
            </div>
            <div className="flex items-center gap-1">
              <MessageCircle className="h-4 w-4" />
              <span>{comment_count}</span>
            </div>
          </div>
        </CardFooter>
      </Card>
    </Link>
  )
}
