"use client"

import { useState, useEffect } from "react"
import { Send, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { getPostComments, addPostComment, getUser, type Interaction, type User } from "@/lib/api-client"
import { useAuth } from "@/contexts/AuthContext"
import { toast } from "sonner"

interface CommentSectionProps {
  postId: number
  initialCount?: number
  onCountChange?: (newCount: number) => void
}

interface CommentWithAuthor extends Interaction {
  author?: User | null
}

export function CommentSection({ postId, initialCount = 0, onCountChange }: CommentSectionProps) {
  const { user } = useAuth()
  const [comments, setComments] = useState<CommentWithAuthor[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [newComment, setNewComment] = useState("")

  useEffect(() => {
    const fetchComments = async () => {
      setIsLoading(true)
      try {
        const resp = await getPostComments(postId)
        // Fetch author info for each comment
        const commentsWithAuthors = await Promise.all(
          resp.items.map(async (comment) => {
            if (!comment.created_by) return { ...comment, author: null }
            try {
              const author = await getUser(comment.created_by)
              return { ...comment, author }
            } catch {
              return { ...comment, author: null }
            }
          })
        )
        setComments(commentsWithAuthors)
      } catch {
        setComments([])
      } finally {
        setIsLoading(false)
      }
    }
    fetchComments()
  }, [postId])

  const handleSubmit = async () => {
    if (!user || !newComment.trim()) return
    if (isSubmitting) return

    setIsSubmitting(true)
    try {
      const comment = await addPostComment(postId, newComment.trim())
      // Fetch author info for new comment
      let author: User | null = null
      try {
        author = await getUser(user.user_id)
      } catch {}
      setComments((prev) => [...prev, { ...comment, author }])
      setNewComment("")
      const newCount = (initialCount ?? comments.length) + 1
      onCountChange?.(newCount)
      toast.success("评论已发布")
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "评论失败")
    } finally {
      setIsSubmitting(false)
    }
  }

  const formatTime = (dateStr: string) => {
    const date = new Date(dateStr)
    return date.toLocaleDateString("zh-CN", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  return (
    <div className="space-y-6">
      <h3 className="text-lg font-semibold text-nf-white">
        评论 ({comments.length})
      </h3>

      {/* Comment Form */}
      {user ? (
        <div className="flex gap-3">
          <Avatar className="h-10 w-10 shrink-0">
            <AvatarFallback className="bg-nf-secondary text-nf-white">
              {user.username.charAt(0).toUpperCase()}
            </AvatarFallback>
          </Avatar>
          <div className="flex-1 space-y-2">
            <Textarea
              placeholder="写下你的评论..."
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              className="bg-nf-surface border-nf-secondary min-h-[80px] resize-none"
            />
            <div className="flex justify-end">
              <Button
                size="sm"
                className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90"
                onClick={handleSubmit}
                disabled={!newComment.trim() || isSubmitting}
              >
                {isSubmitting ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <>
                    <Send className="h-4 w-4 mr-1" />
                    发布
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>
      ) : (
        <p className="text-nf-muted text-sm">登录后即可评论</p>
      )}

      {/* Comments List */}
      {isLoading ? (
        <div className="text-center py-8">
          <Loader2 className="h-6 w-6 animate-spin mx-auto text-nf-muted" />
        </div>
      ) : comments.length > 0 ? (
        <div className="space-y-4">
          {comments.map((comment) => (
            <div key={comment.id} className="flex gap-3">
              <Avatar className="h-10 w-10 shrink-0">
                <AvatarImage src={comment.author?.avatar_url ?? undefined} />
                <AvatarFallback className="bg-nf-secondary text-nf-white">
                  {(comment.author?.display_name ?? comment.author?.username ?? "U").charAt(0).toUpperCase()}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-medium text-nf-white">
                    {comment.author?.display_name ?? comment.author?.username ?? "用户"}
                  </span>
                  <span className="text-xs text-nf-muted">
                    {formatTime(comment.created_at)}
                  </span>
                </div>
                <p className="text-nf-light-gray whitespace-pre-wrap">
                  {typeof comment.value === "string" ? comment.value : ""}
                </p>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-nf-muted text-center py-8">暂无评论</p>
      )}
    </div>
  )
}
