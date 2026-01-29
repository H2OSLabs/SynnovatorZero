"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import {
  Menu, Search, Plus, Bell, ChevronDown, ChevronLeft, ChevronRight,
  Compass, Globe, Tent, User, Heart, Share2, Ellipsis,
  Zap, FileText,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { getPost, getUser, listComments, likePost, unlikePost, addComment } from "@/lib/api-client"
import type { Post, User as UserType, Interaction } from "@/lib/types"

const fallbackTags = ["通知公告", "我的学校/公...", "通知公告", "活动信息..."]

const hotItems = [
  { rank: 1, title: "热点标题内容热点标题内容", color: "text-[var(--nf-orange)]" },
  { rank: 2, title: "协创平台新功能发布公告", color: "text-[var(--nf-orange)]" },
  { rank: 3, title: "设计系统组件库更新通知", color: "text-[var(--nf-orange)]" },
  { rank: 4, title: "团队协作效率提升方案", color: "text-[var(--nf-lime)]" },
  { rank: 5, title: "创新项目孵化计划招募", color: "text-[var(--nf-lime)]" },
  { rank: 6, title: "前端技术架构分享会", color: "text-[var(--nf-muted)]" },
  { rank: 7, title: "用户体验优化实践总结", color: "text-[var(--nf-muted)]" },
  { rank: 8, title: "产品设计趋势年度报告", color: "text-[var(--nf-muted)]" },
  { rank: 9, title: "开源工具推荐合集分享", color: "text-[var(--nf-muted)]" },
  { rank: 10, title: "跨团队协作最佳实践", color: "text-[var(--nf-muted)]" },
]

const weekDays = ["日", "一", "二", "三", "四", "五", "六"]

export function PostDetail({ postId }: { postId: number }) {
  const router = useRouter()
  const [post, setPost] = useState<Post | null>(null)
  const [author, setAuthor] = useState<UserType | null>(null)
  const [comments, setComments] = useState<Interaction[]>([])
  const [loading, setLoading] = useState(true)
  const [liked, setLiked] = useState(false)
  const [likeCount, setLikeCount] = useState(0)
  const [commentText, setCommentText] = useState("")

  useEffect(() => {
    let cancelled = false
    async function fetchData() {
      setLoading(true)
      try {
        const fetchedPost = await getPost(postId)
        if (cancelled) return
        setPost(fetchedPost)
        setLikeCount(fetchedPost.like_count || 0)

        const [fetchedUser, fetchedComments] = await Promise.all([
          getUser(fetchedPost.created_by),
          listComments(postId, 0, 20),
        ])
        if (cancelled) return
        setAuthor(fetchedUser)
        setComments(fetchedComments.items)
      } catch (err) {
        console.error("Failed to fetch post detail:", err)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    fetchData()
    return () => { cancelled = true }
  }, [postId])

  async function handleLike() {
    try {
      if (liked) {
        await unlikePost(postId, 1)
        setLikeCount(prev => Math.max(0, prev - 1))
      } else {
        await likePost(postId, 1)
        setLikeCount(prev => prev + 1)
      }
      setLiked(!liked)
    } catch (err) {
      console.error("Like failed:", err)
    }
  }

  async function handleComment() {
    if (!commentText.trim()) return
    try {
      await addComment(postId, { text: commentText }, 1)
      setCommentText("")
      // Refresh comments
      const updated = await listComments(postId, 0, 20)
      setComments(updated.items || [])
    } catch (err) {
      console.error("Comment failed:", err)
    }
  }

  const tags = post?.tags ?? fallbackTags
  const displayName = author?.display_name || author?.username || "LIGHTNING鲸"
  const commentCount = post?.comment_count ?? 0

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-[var(--nf-near-black)]">
        <span className="text-[var(--nf-muted)] text-lg">加载中...</span>
      </div>
    )
  }
  return (
    <div className="flex flex-col h-screen bg-[var(--nf-near-black)]">
      {/* Header */}
      <header className="flex items-center justify-between h-14 px-6 border-b border-[var(--nf-dark-bg)] bg-[var(--nf-near-black)]">
        <div className="flex items-center gap-4">
          <Menu className="w-6 h-6 text-[var(--nf-white)]" />
          <span className="font-heading text-[20px] font-bold text-[var(--nf-lime)] cursor-pointer" onClick={() => router.push("/")}>协创者</span>
        </div>
        <div className="flex items-center gap-2 w-[420px] bg-[var(--nf-card-bg)] border border-[var(--nf-dark-bg)] rounded-[21px] px-5 py-2.5">
          <Search className="w-4 h-4 text-[var(--nf-muted)]" />
          <span className="text-sm text-[var(--nf-muted)]">搜索</span>
        </div>
        <div className="flex items-center gap-3">
          <Button className="bg-[var(--nf-lime)] text-[var(--nf-surface)] hover:bg-[var(--nf-lime)]/90 rounded-[21px] px-[18px] py-2 gap-1.5">
            <Plus className="w-3.5 h-3.5" />
            <span className="text-[13px] font-semibold">发布新内容</span>
          </Button>
          <Bell className="w-[22px] h-[22px] text-[var(--nf-white)]" />
          <Avatar className="w-8 h-8 bg-[var(--nf-blue)]">
            <AvatarFallback className="bg-[var(--nf-blue)] text-sm font-semibold text-[var(--nf-white)]">A</AvatarFallback>
          </Avatar>
          <ChevronDown className="w-4 h-4 text-[var(--nf-white)]" />
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* Compact Sidebar */}
        <aside className="w-14 bg-[var(--nf-near-black)] border-r border-[var(--nf-dark-bg)] flex flex-col items-center gap-2 pt-4">
          <div className="w-10 h-10 rounded-lg bg-[var(--nf-lime)] flex items-center justify-center cursor-pointer" onClick={() => router.push("/")}>
            <Compass className="w-5 h-5 text-[var(--nf-surface)]" />
          </div>
          <div className="w-10 h-10 rounded-lg flex items-center justify-center cursor-pointer" onClick={() => router.push("/categories/1")}>
            <Globe className="w-5 h-5 text-[var(--nf-muted)]" />
          </div>
          <div className="w-10 h-10 rounded-lg flex items-center justify-center cursor-pointer" onClick={() => router.push("/team")}>
            <Tent className="w-5 h-5 text-[var(--nf-muted)]" />
          </div>
        </aside>

        {/* Main Area */}
        <div className="flex flex-1 gap-6 p-6 px-8 overflow-y-auto">
          {/* Left Column */}
          <div className="flex-1 flex flex-col gap-5">
            {/* Author Row */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-[var(--nf-dark-bg)]" />
                <div className="flex flex-col gap-0.5">
                  <span className="text-[16px] font-semibold text-[var(--nf-white)]">{displayName}</span>
                  <span className="text-[12px] text-[var(--nf-muted)]">{author?.bio || "Alibaba team"}</span>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-1 cursor-pointer" onClick={handleLike}>
                  <Heart className={`w-4 h-4 ${liked ? "text-red-500 fill-red-500" : "text-[var(--nf-muted)]"}`} />
                  <span className={`font-mono text-[13px] ${liked ? "text-red-500" : "text-[var(--nf-muted)]"}`}>{likeCount}</span>
                </div>
                <Share2 className="w-4 h-4 text-[var(--nf-muted)]" />
                <Ellipsis className="w-4 h-4 text-[var(--nf-muted)]" />
              </div>
            </div>

            {/* Post Title */}
            <h1 className="font-heading text-[24px] font-bold text-[var(--nf-white)]">
              {post?.title || "帖子名帖子名帖子名帖子名帖子名帖子名帖子名帖子名"}
            </h1>

            {/* Tags */}
            <div className="flex gap-2">
              {tags.map((tag, i) => (
                <Badge key={i} className="bg-[var(--nf-lime)] text-[var(--nf-surface)] hover:bg-[var(--nf-lime)]/90 rounded-sm px-2.5 py-1 text-[12px] font-medium">
                  {tag}
                </Badge>
              ))}
            </div>

            {/* Related Cards */}
            <div className="flex flex-col gap-3">
              <div className="flex items-center gap-2">
                <Zap className="w-[18px] h-[18px] text-[var(--nf-lime)]" />
                <span className="text-[16px] font-semibold text-[var(--nf-white)]">关联卡片</span>
              </div>
              <div className="flex gap-4">
                <Card className="w-[260px] h-[180px] bg-[var(--nf-card-bg)] border-none rounded-[12px] overflow-hidden">
                  <div className="w-full h-[140px] bg-[var(--nf-dark-bg)]" />
                  <div className="flex items-center gap-1.5 px-3 py-2">
                    <div className="w-[18px] h-[18px] rounded-full bg-[var(--nf-dark-bg)]" />
                    <span className="text-[11px] text-[var(--nf-muted)]">LIGHTNING鲸</span>
                  </div>
                </Card>
                <Card className="w-[260px] h-[180px] bg-[var(--nf-dark-bg)] border-none rounded-[12px] flex flex-col items-center justify-center gap-2">
                  <div className="w-10 h-10 rounded-full bg-[var(--nf-muted)]" />
                  <span className="text-sm text-[var(--nf-white)]">我在团队没有名字</span>
                  <span className="text-[12px] text-[var(--nf-muted)]">大家好，这是我们的团队简介</span>
                </Card>
              </div>
            </div>

            {/* Content Section */}
            <div className="flex flex-col gap-3">
              <div className="flex items-center gap-2">
                <FileText className="w-[18px] h-[18px] text-[var(--nf-lime)]" />
                <span className="text-[16px] font-semibold text-[var(--nf-white)]">内容详情</span>
              </div>
              <Card className="bg-[var(--nf-card-bg)] border-none rounded-[12px] p-6 flex flex-col gap-4">
                <p className="text-sm text-[var(--nf-light-gray)]">
                  {post?.body || "帖子内容详情将在此处展示。包括用户发布的文字、图片等多媒体内容。帖子可以包含文字描述、图片附件和标签分类等信息。"}
                </p>
                <p className="text-[13px] text-[var(--nf-muted)]">Divesee — 创意灵感参考</p>
              </Card>
            </div>

            {/* Comment Section */}
            <div className="flex flex-col gap-3 mt-4">
              <h3 className="text-[16px] font-semibold text-[var(--nf-white)]">评论 ({comments.length})</h3>
              <div className="flex gap-2">
                <Input
                  value={commentText}
                  onChange={(e) => setCommentText(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleComment()}
                  placeholder="写下你的评论..."
                  className="flex-1 bg-[var(--nf-card-bg)] border-[var(--nf-dark-bg)] text-[var(--nf-white)] placeholder:text-[var(--nf-muted)]"
                />
                <Button onClick={handleComment} className="bg-[var(--nf-lime)] text-[var(--nf-surface)]">发送</Button>
              </div>
              {comments.map((c) => (
                <div key={c.id} className="bg-[var(--nf-card-bg)] rounded-lg p-3">
                  <span className="text-[12px] text-[var(--nf-muted)]">用户 {c.created_by}</span>
                  <p className="text-[13px] text-[var(--nf-white)] mt-1">{typeof c.value === "object" && c.value ? (c.value as any).text : String(c.value)}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Right Column */}
          <div className="w-[320px] flex flex-col gap-5 shrink-0">
            {/* Calendar */}
            <Card className="bg-[var(--nf-card-bg)] border border-[var(--nf-dark-bg)] rounded-[12px] overflow-hidden">
              <div className="flex items-center justify-between px-4 py-3 bg-[var(--nf-lime)]">
                <ChevronLeft className="w-4 h-4 text-[var(--nf-surface)]" />
                <span className="text-sm font-semibold text-[var(--nf-surface)]">2025年12月</span>
                <ChevronRight className="w-4 h-4 text-[var(--nf-surface)]" />
              </div>
              <div className="p-4 flex flex-col gap-1.5">
                <div className="grid grid-cols-7 gap-1">
                  {weekDays.map((d) => (
                    <span key={d} className="text-center text-[12px] text-[var(--nf-muted)]">{d}</span>
                  ))}
                </div>
                {[
                  [" ", "1", "2", "3", "4", "5", "6"],
                  ["7", "8", "9", "10", "11", "12", "13"],
                  ["14", "15", "16", "17", "18", "19", "20"],
                ].map((row, ri) => (
                  <div key={ri} className="grid grid-cols-7 gap-1">
                    {row.map((d, di) => (
                      <span key={di} className="text-center font-mono text-[12px] text-[var(--nf-white)]">{d}</span>
                    ))}
                  </div>
                ))}
              </div>
            </Card>

            {/* Hot Topics */}
            <Card className="bg-[var(--nf-card-bg)] border border-[var(--nf-dark-bg)] rounded-[12px] overflow-hidden">
              <div className="flex items-center justify-between px-4 py-3.5">
                <span className="text-[15px] font-semibold text-[var(--nf-white)]">协创热点榜</span>
                <div className="flex items-center gap-3">
                  <span className="text-[13px] font-medium text-[var(--nf-lime)]">提案</span>
                  <span className="text-[13px] text-[var(--nf-muted)]">帖子</span>
                </div>
              </div>
              <Separator className="bg-[var(--nf-dark-bg)]" />
              <div className="py-1">
                {hotItems.map((item) => (
                  <div key={item.rank} className="flex items-center gap-2.5 px-4 py-[7px]">
                    <span className={`font-mono text-sm font-bold ${item.color} w-4 text-center`}>
                      {item.rank}
                    </span>
                    <span className={`text-[13px] ${item.rank <= 5 ? "text-[var(--nf-white)]" : "text-[var(--nf-light-gray)]"}`}>
                      {item.title}
                    </span>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
