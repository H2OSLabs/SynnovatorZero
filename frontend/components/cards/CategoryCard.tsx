"use client"

import Link from "next/link"
import { Calendar, Users } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { cn } from "@/lib/utils"

interface CategoryCardProps {
  id: number
  name: string
  description?: string
  type: "competition" | "operation"
  status: "draft" | "published" | "closed"
  tags?: string[]
  cover_image?: string
  start_date?: string
  end_date?: string
  created_by?: {
    id: number
    display_name?: string
    username: string
  }
  participant_count?: number
  className?: string
}

const statusConfig = {
  published: { label: "进行中", className: "bg-nf-lime text-nf-near-black" },
  draft: { label: "草稿", className: "bg-nf-orange text-nf-near-black" },
  closed: { label: "已结束", className: "bg-nf-muted text-nf-white" },
}

export function CategoryCard({
  id,
  name,
  description,
  type,
  status,
  tags = [],
  cover_image,
  start_date,
  end_date,
  created_by,
  participant_count = 0,
  className,
}: CategoryCardProps) {
  const statusInfo = statusConfig[status]

  const formatDateRange = () => {
    if (!start_date || !end_date) return null
    const start = new Date(start_date).toLocaleDateString("zh-CN", { month: "2-digit", day: "2-digit" })
    const end = new Date(end_date).toLocaleDateString("zh-CN", { month: "2-digit", day: "2-digit" })
    return `${start} - ${end}`
  }

  return (
    <Link href={`/events/${id}`}>
      <Card className={cn("bg-nf-secondary border-none hover:bg-nf-secondary/80 transition-colors cursor-pointer overflow-hidden", className)}>
        {/* Cover Image */}
        <div className="relative aspect-video bg-nf-dark">
          {cover_image ? (
            <img src={cover_image} alt={name} className="w-full h-full object-cover" />
          ) : (
            <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-nf-secondary to-nf-dark">
              <Calendar className="h-12 w-12 text-nf-muted" />
            </div>
          )}
          {/* Status Badge */}
          <Badge className={cn("absolute top-3 left-3", statusInfo.className)}>
            {statusInfo.label}
          </Badge>
        </div>

        <CardHeader className="p-4 pb-2">
          <h3 className="font-heading font-semibold text-nf-white line-clamp-2">{name}</h3>
          {(created_by || formatDateRange()) && (
            <p className="text-sm text-nf-muted">
              {created_by && (created_by.display_name || created_by.username)}
              {created_by && formatDateRange() && " · "}
              {formatDateRange()}
            </p>
          )}
        </CardHeader>

        <CardFooter className="p-4 pt-2 flex items-center justify-between">
          <div className="flex items-center gap-2 flex-wrap">
            {tags.slice(0, 2).map((tag) => (
              <Badge key={tag} variant="secondary" className="bg-nf-dark text-nf-white text-xs">
                {tag}
              </Badge>
            ))}
          </div>
          <div className="flex items-center gap-1 text-sm text-nf-muted">
            <Users className="h-4 w-4" />
            <span>{participant_count} 报名</span>
          </div>
        </CardFooter>
      </Card>
    </Link>
  )
}
