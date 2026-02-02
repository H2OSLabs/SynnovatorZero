"use client"

import Link from "next/link"
import { Users, Calendar } from "lucide-react"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { cn } from "@/lib/utils"

interface GroupCardProps {
  id: number
  name: string
  description?: string
  logo_url?: string
  visibility: "public" | "private"
  member_count?: number
  event_count?: number
  members?: Array<{
    id: number
    display_name?: string
    username: string
    avatar_url?: string
  }>
  className?: string
}

export function GroupCard({
  id,
  name,
  description,
  logo_url,
  visibility,
  member_count = 0,
  event_count = 0,
  members = [],
  className,
}: GroupCardProps) {
  // Truncate description
  const truncatedDesc = description
    ? description.slice(0, 80) + (description.length > 80 ? "..." : "")
    : null

  return (
    <Link href={`/groups/${id}`}>
      <Card className={cn("bg-nf-secondary border-none hover:bg-nf-secondary/80 transition-colors cursor-pointer", className)}>
        <CardHeader className="p-4 pb-2">
          <div className="flex items-center gap-3">
            <Avatar className="h-12 w-12 rounded-lg">
              {logo_url ? (
                <AvatarImage src={logo_url} className="rounded-lg" />
              ) : (
                <AvatarFallback className="rounded-lg bg-gradient-to-br from-nf-cyan to-nf-pink text-nf-white font-bold">
                  {name.charAt(0).toUpperCase()}
                </AvatarFallback>
              )}
            </Avatar>
            <div>
              <h3 className="font-heading font-semibold text-nf-white">{name}</h3>
              <p className="text-sm text-nf-muted">
                {member_count} 成员
                {event_count > 0 && ` · ${event_count} 活动参与`}
              </p>
            </div>
          </div>
        </CardHeader>

        {truncatedDesc && (
          <CardContent className="px-4 py-2">
            <p className="text-sm text-nf-muted line-clamp-2">{truncatedDesc}</p>
          </CardContent>
        )}

        <CardContent className="p-4 pt-2">
          {/* Member Avatars */}
          {members.length > 0 && (
            <div className="flex items-center">
              <div className="flex -space-x-2">
                {members.slice(0, 3).map((member) => (
                  <Avatar key={member.id} className="h-8 w-8 border-2 border-nf-secondary">
                    <AvatarImage src={member.avatar_url} />
                    <AvatarFallback className="text-xs bg-nf-dark">
                      {(member.display_name || member.username).charAt(0).toUpperCase()}
                    </AvatarFallback>
                  </Avatar>
                ))}
              </div>
              {member_count > 3 && (
                <span className="ml-2 text-sm text-nf-muted">+{member_count - 3}</span>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </Link>
  )
}
