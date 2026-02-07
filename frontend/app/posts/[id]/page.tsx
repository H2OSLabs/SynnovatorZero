"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { useParams, useRouter } from "next/navigation"
import { ArrowLeft, Heart, MessageCircle, Star, Share2, Edit, Trash2, Loader2 } from "lucide-react"
import { PageLayout } from "@/components/layout/PageLayout"
import { Panel, PanelSection, PanelCard } from "@/components/layout/Panel"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Textarea } from "@/components/ui/textarea"
import {
  getPost,
  getPostComments,
  getPostResources,
  getUser,
  addPostComment,
  likePost,
  unlikePost,
  deletePost,
  Post,
  Interaction,
  PostResource,
  User,
} from "@/lib/api-client"

interface CommentWithUser extends Interaction {
  user?: User
}

interface ResourceWithDetails extends PostResource {
  filename?: string
  display_name?: string
  file_size?: number
}

export default function PostDetailPage() {
  const params = useParams()
  const router = useRouter()
  const id = Number(params.id)

  const [post, setPost] = useState<Post | null>(null)
  const [author, setAuthor] = useState<User | null>(null)
  const [comments, setComments] = useState<CommentWithUser[]>([])
  const [resources, setResources] = useState<ResourceWithDetails[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [liked, setLiked] = useState(false)
  const [likeCount, setLikeCount] = useState(0)
  const [commentText, setCommentText] = useState("")
  const [submittingComment, setSubmittingComment] = useState(false)
  const [deleting, setDeleting] = useState(false)

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true)
        setError(null)

        // Fetch post data
        const postData = await getPost(id)
        setPost(postData)
        setLikeCount(postData.like_count)

        // Fetch author details if available
        if (postData.created_by) {
          try {
            const authorData = await getUser(postData.created_by)
            setAuthor(authorData)
          } catch {
            // Author might not exist or be deleted
          }
        }

        // Fetch comments with user details
        const commentsData = await getPostComments(id)
        const commentsWithUsers = await Promise.all(
          commentsData.items.map(async (comment) => {
            if (comment.created_by) {
              try {
                const user = await getUser(comment.created_by)
                return { ...comment, user }
              } catch {
                return comment
              }
            }
            return comment
          })
        )
        setComments(commentsWithUsers)

        // Fetch resources
        const resourcesData = await getPostResources(id)
        setResources(resourcesData)
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load post")
      } finally {
        setLoading(false)
      }
    }

    if (id) {
      fetchData()
    }
  }, [id])

  const formatDate = (dateStr?: string) => {
    if (!dateStr) return ""
    return new Date(dateStr).toLocaleDateString("zh-CN", {
      year: "numeric",
      month: "long",
      day: "numeric",
    })
  }

  const formatFileSize = (bytes?: number | null) => {
    if (!bytes) return "Unknown size"
    if (bytes < 1024) return bytes + " B"
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB"
    return (bytes / (1024 * 1024)).toFixed(1) + " MB"
  }

  const handleLike = async () => {
    try {
      if (liked) {
        await unlikePost(id)
        setLiked(false)
        setLikeCount((c) => c - 1)
      } else {
        await likePost(id)
        setLiked(true)
        setLikeCount((c) => c + 1)
      }
    } catch (err) {
      console.error("Failed to toggle like:", err)
    }
  }

  const handleComment = async () => {
    if (!commentText.trim()) return

    try {
      setSubmittingComment(true)
      const newComment = await addPostComment(id, commentText)

      // Fetch user details for the new comment
      let commentWithUser: CommentWithUser = newComment
      if (newComment.created_by) {
        try {
          const user = await getUser(newComment.created_by)
          commentWithUser = { ...newComment, user }
        } catch {
          // Ignore user fetch error
        }
      }

      setComments((prev) => [commentWithUser, ...prev])
      setCommentText("")
    } catch (err) {
      console.error("Failed to add comment:", err)
    } finally {
      setSubmittingComment(false)
    }
  }

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this post?")) return

    try {
      setDeleting(true)
      await deletePost(id)
      router.push("/posts")
    } catch (err) {
      console.error("Failed to delete post:", err)
      setDeleting(false)
    }
  }

  if (loading) {
    return (
      <PageLayout variant="full">
        <div className="flex items-center justify-center min-h-[400px]">
          <Loader2 className="h-8 w-8 animate-spin text-nf-lime" />
        </div>
      </PageLayout>
    )
  }

  if (error || !post) {
    return (
      <PageLayout variant="full">
        <div className="text-center py-12">
          <p className="text-nf-error mb-4">{error || "Post not found"}</p>
          <Link href="/posts">
            <Button variant="outline">Back to posts</Button>
          </Link>
        </div>
      </PageLayout>
    )
  }

  const panelContent = (
    <Panel title="Author Info">
      <PanelSection>
        <PanelCard>
          <div className="flex items-center gap-3 mb-4">
            <Avatar className="h-16 w-16">
              <AvatarImage src={author?.avatar_url || undefined} />
              <AvatarFallback className="bg-gradient-to-br from-nf-lime to-nf-cyan text-nf-near-black text-xl">
                {author?.display_name?.charAt(0) || author?.username?.charAt(0) || "?"}
              </AvatarFallback>
            </Avatar>
            <div>
              <h3 className="font-semibold text-nf-white">
                {author?.display_name || author?.username || "Unknown"}
              </h3>
              {author?.username && (
                <p className="text-sm text-nf-muted">@{author.username}</p>
              )}
            </div>
          </div>
          {author?.bio && (
            <p className="text-sm text-nf-muted mb-4">{author.bio}</p>
          )}
          {author && (
            <Link href={`/users/${author.id}`}>
              <Button className="w-full bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
                View Profile
              </Button>
            </Link>
          )}
        </PanelCard>
      </PanelSection>

      <PanelSection title="Stats">
        <PanelCard>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-2 text-nf-muted">
                <Heart className="h-4 w-4" /> Likes
              </span>
              <span className="text-nf-white font-medium">{likeCount}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-2 text-nf-muted">
                <MessageCircle className="h-4 w-4" /> Comments
              </span>
              <span className="text-nf-white font-medium">{comments.length}</span>
            </div>
            {post.average_rating && (
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-2 text-nf-muted">
                  <Star className="h-4 w-4" /> Rating
                </span>
                <span className="text-nf-white font-medium">{post.average_rating.toFixed(1)}</span>
              </div>
            )}
          </div>
        </PanelCard>
      </PanelSection>

      {resources.length > 0 && (
        <PanelSection title="Attachments">
          <div className="space-y-2">
            {resources.map((res) => (
              <a
                key={res.id}
                href="#"
                className="flex items-center gap-3 p-3 bg-nf-dark rounded-lg hover:bg-nf-secondary transition-colors"
              >
                <span className="text-lg">📄</span>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-nf-white truncate">
                    {res.display_name || res.filename || `Resource ${res.resource_id}`}
                  </p>
                  <p className="text-xs text-nf-muted">{formatFileSize(res.file_size)}</p>
                </div>
              </a>
            ))}
          </div>
        </PanelSection>
      )}
    </Panel>
  )

  return (
    <PageLayout variant="full" panel={panelContent}>
      {/* Back Button */}
      <Link href="/posts" className="inline-flex items-center gap-2 text-nf-muted hover:text-nf-white mb-6">
        <ArrowLeft className="h-4 w-4" />
        Back to posts
      </Link>

      {/* Post Header */}
      <div className="mb-8">
        <h1 className="font-heading text-3xl font-bold text-nf-white mb-4">
          {post.title}
        </h1>
        <div className="flex items-center gap-4 mb-4">
          <Avatar className="h-10 w-10">
            <AvatarImage src={author?.avatar_url || undefined} />
            <AvatarFallback className="bg-nf-dark">
              {author?.display_name?.charAt(0) || author?.username?.charAt(0) || "?"}
            </AvatarFallback>
          </Avatar>
          <div>
            <p className="text-nf-white">{author?.display_name || author?.username || "Unknown"}</p>
            <p className="text-sm text-nf-muted">
              {post.type} · {formatDate(post.created_at)}
            </p>
          </div>
        </div>
        {post.tags && post.tags.length > 0 && (
          <div className="flex gap-2 flex-wrap">
            {post.tags.map((tag) => (
              <Badge key={tag} variant="secondary" className="bg-nf-dark">
                {tag}
              </Badge>
            ))}
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="flex items-center gap-2 mb-8 pb-8 border-b border-nf-secondary">
        <Button
          variant={liked ? "default" : "outline"}
          className={liked ? "bg-nf-error border-nf-error" : "border-nf-secondary"}
          onClick={handleLike}
        >
          <Heart className={`h-4 w-4 mr-2 ${liked ? "fill-current" : ""}`} />
          {likeCount}
        </Button>
        <Button variant="outline" className="border-nf-secondary">
          <Share2 className="h-4 w-4 mr-2" />
          Share
        </Button>
        {/* Author actions */}
        <div className="ml-auto flex gap-2">
          <Link href={`/posts/${id}/edit`}>
            <Button variant="outline" className="border-nf-secondary">
              <Edit className="h-4 w-4 mr-2" />
              Edit
            </Button>
          </Link>
          <Button
            variant="outline"
            className="border-nf-error text-nf-error hover:bg-nf-error hover:text-nf-white"
            onClick={handleDelete}
            disabled={deleting}
          >
            {deleting ? (
              <Loader2 className="h-4 w-4 mr-2 animate-spin" />
            ) : (
              <Trash2 className="h-4 w-4 mr-2" />
            )}
            Delete
          </Button>
        </div>
      </div>

      {/* Post Content */}
      <article className="prose prose-invert max-w-none mb-12">
        <div className="whitespace-pre-wrap text-nf-light-gray">
          {post.content}
        </div>
      </article>

      {/* Comments Section */}
      <section className="border-t border-nf-secondary pt-8">
        <h2 className="font-heading text-xl font-semibold text-nf-white mb-6">
          Comments ({comments.length})
        </h2>

        {/* Comment Input */}
        <div className="mb-8">
          <Textarea
            placeholder="Write a comment..."
            className="bg-nf-surface border-nf-secondary mb-3"
            value={commentText}
            onChange={(e) => setCommentText(e.target.value)}
          />
          <Button
            className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90"
            onClick={handleComment}
            disabled={submittingComment || !commentText.trim()}
          >
            {submittingComment ? (
              <Loader2 className="h-4 w-4 mr-2 animate-spin" />
            ) : null}
            Submit
          </Button>
        </div>

        {/* Comments List */}
        <div className="space-y-6">
          {comments.map((comment) => (
            <div key={comment.id} className="flex gap-4">
              <Avatar className="h-10 w-10">
                <AvatarImage src={comment.user?.avatar_url || undefined} />
                <AvatarFallback className="bg-nf-dark">
                  {comment.user?.display_name?.charAt(0) || comment.user?.username?.charAt(0) || "?"}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-medium text-nf-white">
                    {comment.user?.display_name || comment.user?.username || "Unknown"}
                  </span>
                  <span className="text-xs text-nf-muted">
                    {formatDate(comment.created_at)}
                  </span>
                </div>
                <p className="text-nf-light-gray mb-2">
                  {typeof comment.value === 'string' ? comment.value : ''}
                </p>
              </div>
            </div>
          ))}
          {comments.length === 0 && (
            <p className="text-nf-muted text-center py-8">No comments yet. Be the first to comment!</p>
          )}
        </div>
      </section>
    </PageLayout>
  )
}
