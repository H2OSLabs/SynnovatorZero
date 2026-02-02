"use client"

import { use, useState } from "react"
import Link from "next/link"
import { ArrowLeft, Heart, MessageCircle, Star, Share2, Edit, Trash2 } from "lucide-react"
import { PageLayout } from "@/components/layout/PageLayout"
import { Panel, PanelSection, PanelCard } from "@/components/layout/Panel"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Textarea } from "@/components/ui/textarea"

// Mock data
const mockPost = {
  id: 1,
  title: "基于大模型的智能教育平台",
  body: `## 项目介绍

我们开发了一个基于大语言模型的个性化学习平台，能够根据学生的学习进度自动调整教学内容。

## 核心功能

1. **个性化学习路径** - 根据学生的知识水平和学习风格，自动生成定制化的学习计划
2. **智能问答** - 24/7 在线的 AI 助教，随时解答学习中的问题
3. **作业批改** - 自动批改作业并给出详细的反馈建议
4. **知识图谱** - 可视化展示知识点之间的关联

## 技术栈

- 前端：Next.js + TypeScript + Tailwind CSS
- 后端：Python + FastAPI + LangChain
- 数据库：PostgreSQL + Redis
- AI：GPT-4 + 自训练模型

## 团队成员

- Alice - 全栈开发
- Bob - AI 工程师
- Carol - 产品设计`,
  type: "for_category",
  status: "published",
  tags: ["AI", "Education", "LLM", "个性化学习"],
  created_at: "2024-03-10T10:30:00Z",
  created_by: {
    id: 1,
    username: "alice",
    display_name: "Alice Chen",
    avatar_url: null,
    bio: "全栈开发者，热爱 AI 和教育科技",
  },
  group: {
    id: 1,
    name: "Team Innovators",
  },
  like_count: 128,
  comment_count: 32,
  average_rating: 4.5,
}

const mockComments = [
  { id: 1, text: "很棒的项目！个性化学习路径这个功能很有价值。", created_by: { id: 2, username: "bob", display_name: "Bob" }, created_at: "2024-03-10T12:00:00Z", like_count: 12 },
  { id: 2, text: "技术栈选择很合理，期待看到更多进展！", created_by: { id: 3, username: "carol", display_name: "Carol" }, created_at: "2024-03-10T14:30:00Z", like_count: 8 },
]

const mockResources = [
  { id: 1, filename: "proposal.pdf", display_name: "项目提案", file_size: 2400000 },
  { id: 2, filename: "demo.zip", display_name: "演示文件", file_size: 15000000 },
]

export default function PostDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params)
  const [liked, setLiked] = useState(false)
  const [commentText, setCommentText] = useState("")

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString("zh-CN", {
      year: "numeric",
      month: "long",
      day: "numeric",
    })
  }

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + " B"
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB"
    return (bytes / (1024 * 1024)).toFixed(1) + " MB"
  }

  const panelContent = (
    <Panel title="👤 作者信息">
      <PanelSection>
        <PanelCard>
          <div className="flex items-center gap-3 mb-4">
            <Avatar className="h-16 w-16">
              <AvatarImage src={mockPost.created_by.avatar_url || undefined} />
              <AvatarFallback className="bg-gradient-to-br from-nf-lime to-nf-cyan text-nf-near-black text-xl">
                {mockPost.created_by.display_name.charAt(0)}
              </AvatarFallback>
            </Avatar>
            <div>
              <h3 className="font-semibold text-nf-white">{mockPost.created_by.display_name}</h3>
              <p className="text-sm text-nf-muted">@{mockPost.created_by.username}</p>
            </div>
          </div>
          <p className="text-sm text-nf-muted mb-4">{mockPost.created_by.bio}</p>
          <Button className="w-full bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
            + 关注
          </Button>
        </PanelCard>
      </PanelSection>

      <PanelSection title="📊 互动统计">
        <PanelCard>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-2 text-nf-muted">
                <Heart className="h-4 w-4" /> 点赞
              </span>
              <span className="text-nf-white font-medium">{mockPost.like_count}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-2 text-nf-muted">
                <MessageCircle className="h-4 w-4" /> 评论
              </span>
              <span className="text-nf-white font-medium">{mockPost.comment_count}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-2 text-nf-muted">
                <Star className="h-4 w-4" /> 评分
              </span>
              <span className="text-nf-white font-medium">{mockPost.average_rating}</span>
            </div>
          </div>
        </PanelCard>
      </PanelSection>

      <PanelSection title="📎 附件">
        <div className="space-y-2">
          {mockResources.map((res) => (
            <a
              key={res.id}
              href="#"
              className="flex items-center gap-3 p-3 bg-nf-dark rounded-lg hover:bg-nf-secondary transition-colors"
            >
              <span className="text-lg">📄</span>
              <div className="flex-1 min-w-0">
                <p className="text-sm text-nf-white truncate">{res.display_name}</p>
                <p className="text-xs text-nf-muted">{formatFileSize(res.file_size)}</p>
              </div>
            </a>
          ))}
        </div>
      </PanelSection>
    </Panel>
  )

  return (
    <PageLayout variant="full" user={null} panel={panelContent}>
      {/* Back Button */}
      <Link href="/posts" className="inline-flex items-center gap-2 text-nf-muted hover:text-nf-white mb-6">
        <ArrowLeft className="h-4 w-4" />
        返回帖子列表
      </Link>

      {/* Post Header */}
      <div className="mb-8">
        <h1 className="font-heading text-3xl font-bold text-nf-white mb-4">
          💡 {mockPost.title}
        </h1>
        <div className="flex items-center gap-4 mb-4">
          <Avatar className="h-10 w-10">
            <AvatarFallback className="bg-nf-dark">
              {mockPost.created_by.display_name.charAt(0)}
            </AvatarFallback>
          </Avatar>
          <div>
            <p className="text-nf-white">{mockPost.created_by.display_name}</p>
            <p className="text-sm text-nf-muted">
              {mockPost.group?.name} · {formatDate(mockPost.created_at)}
            </p>
          </div>
        </div>
        <div className="flex gap-2 flex-wrap">
          {mockPost.tags.map((tag) => (
            <Badge key={tag} variant="secondary" className="bg-nf-dark">
              {tag}
            </Badge>
          ))}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex items-center gap-2 mb-8 pb-8 border-b border-nf-secondary">
        <Button
          variant={liked ? "default" : "outline"}
          className={liked ? "bg-nf-error border-nf-error" : "border-nf-secondary"}
          onClick={() => setLiked(!liked)}
        >
          <Heart className={`h-4 w-4 mr-2 ${liked ? "fill-current" : ""}`} />
          {liked ? mockPost.like_count + 1 : mockPost.like_count}
        </Button>
        <Button variant="outline" className="border-nf-secondary">
          <Share2 className="h-4 w-4 mr-2" />
          分享
        </Button>
        {/* Author actions */}
        <div className="ml-auto flex gap-2">
          <Link href={`/posts/${id}/edit`}>
            <Button variant="outline" className="border-nf-secondary">
              <Edit className="h-4 w-4 mr-2" />
              编辑
            </Button>
          </Link>
          <Button variant="outline" className="border-nf-error text-nf-error hover:bg-nf-error hover:text-nf-white">
            <Trash2 className="h-4 w-4 mr-2" />
            删除
          </Button>
        </div>
      </div>

      {/* Post Content */}
      <article className="prose prose-invert max-w-none mb-12">
        <div className="whitespace-pre-wrap text-nf-light-gray">
          {mockPost.body}
        </div>
      </article>

      {/* Comments Section */}
      <section className="border-t border-nf-secondary pt-8">
        <h2 className="font-heading text-xl font-semibold text-nf-white mb-6">
          💬 评论 ({mockComments.length})
        </h2>

        {/* Comment Input */}
        <div className="mb-8">
          <Textarea
            placeholder="写下你的评论..."
            className="bg-nf-surface border-nf-secondary mb-3"
            value={commentText}
            onChange={(e) => setCommentText(e.target.value)}
          />
          <Button className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
            发送
          </Button>
        </div>

        {/* Comments List */}
        <div className="space-y-6">
          {mockComments.map((comment) => (
            <div key={comment.id} className="flex gap-4">
              <Avatar className="h-10 w-10">
                <AvatarFallback className="bg-nf-dark">
                  {comment.created_by.display_name.charAt(0)}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-medium text-nf-white">
                    {comment.created_by.display_name}
                  </span>
                  <span className="text-xs text-nf-muted">
                    {formatDate(comment.created_at)}
                  </span>
                </div>
                <p className="text-nf-light-gray mb-2">{comment.text}</p>
                <div className="flex items-center gap-4 text-sm text-nf-muted">
                  <button className="hover:text-nf-white flex items-center gap-1">
                    <Heart className="h-4 w-4" />
                    {comment.like_count}
                  </button>
                  <button className="hover:text-nf-white">回复</button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </PageLayout>
  )
}
