"use client"

import Link from "next/link"
import { useParams } from "next/navigation"
import { useEffect, useState } from "react"
import { ArrowLeft, Calendar, Users, Clock, Award, FileText, UserPlus } from "lucide-react"
import { PageLayout } from "@/components/layout/PageLayout"
import { Panel, PanelSection, PanelCard } from "@/components/layout/Panel"
import { PostCard } from "@/components/cards/PostCard"
import { GroupCard } from "@/components/cards/GroupCard"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { getCategory, type Event } from "@/lib/api-client"

const mockPosts = [
  { id: 1, title: "基于大模型的智能教育平台", type: "proposal", status: "published", tags: ["AI"], like_count: 128, comment_count: 32, created_by: { id: 1, username: "alice", display_name: "Alice" } },
  { id: 2, title: "智能客服机器人", type: "proposal", status: "published", tags: ["AI", "NLP"], like_count: 96, comment_count: 24, created_by: { id: 2, username: "bob", display_name: "Bob" } },
]

const mockGroups = [
  { id: 1, name: "创新先锋队", visibility: "public" as const, member_count: 5, description: "热爱技术，热爱开源" },
  { id: 2, name: "AI 实验室", visibility: "public" as const, member_count: 4, description: "探索 AI 的无限可能" },
]

const mockRules = {
  min_team_size: 2,
  max_team_size: 5,
  max_submissions: 1,
  submission_format: ["PDF", "ZIP", "Video"],
  scoring_criteria: [
    { name: "创新性", weight: 30 },
    { name: "技术实现", weight: 30 },
    { name: "实用价值", weight: 25 },
    { name: "演示效果", weight: 15 },
  ],
}

export default function EventDetailPage() {
  const params = useParams()
  const id = params.id as string
  const categoryId = Number(id)
  const [event, setCategory] = useState<Event | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!Number.isFinite(categoryId)) {
      setError("无效的活动 ID")
      setIsLoading(false)
      return
    }
    const fetchData = async () => {
      setIsLoading(true)
      setError(null)
      try {
        const data = await getCategory(categoryId)
        setCategory(data)
      } catch (e) {
        setError(e instanceof Error ? e.message : "加载失败")
        setCategory(null)
      } finally {
        setIsLoading(false)
      }
    }
    fetchData()
  }, [categoryId])

  const statusConfig = {
    published: { label: "进行中", className: "bg-nf-lime text-nf-near-black" },
    draft: { label: "草稿", className: "bg-nf-orange text-nf-near-black" },
    closed: { label: "已结束", className: "bg-nf-muted text-nf-white" },
  }

  const statusInfo = statusConfig[(event?.status || "draft") as keyof typeof statusConfig]

  const startDate = event?.start_date ? new Date(event.start_date).toLocaleDateString("zh-CN") : null
  const endDate = event?.end_date ? new Date(event.end_date).toLocaleDateString("zh-CN") : null
  const dateRange = startDate && endDate ? `${startDate} - ${endDate}` : null

  const panelContent = (
    <Panel title="📊 活动概览">
      <PanelSection>
        <PanelCard>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-nf-muted">状态</span>
              <Badge className={statusInfo.className}>{statusInfo.label}</Badge>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-nf-muted">报名人数</span>
              <span className="text-nf-white font-medium">{event?.participant_count ?? 0}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-nf-muted">提交作品</span>
              <span className="text-nf-white font-medium">{mockPosts.length}</span>
            </div>
          </div>
        </PanelCard>
      </PanelSection>

      <PanelSection title="📅 重要日期">
        <PanelCard>
          <div className="space-y-3">
            <div>
              <p className="text-xs text-nf-muted">开始时间</p>
              <p className="text-nf-white">{startDate || "-"}</p>
            </div>
            <div>
              <p className="text-xs text-nf-muted">结束时间</p>
              <p className="text-nf-white">{endDate || "-"}</p>
            </div>
          </div>
        </PanelCard>
      </PanelSection>

      <PanelSection title="📋 规则摘要">
        <PanelCard>
          <ul className="space-y-2 text-sm">
            <li className="flex items-center gap-2">
              <Users className="h-4 w-4 text-nf-muted" />
              <span className="text-nf-white">{mockRules.min_team_size}-{mockRules.max_team_size} 人/团队</span>
            </li>
            <li className="flex items-center gap-2">
              <FileText className="h-4 w-4 text-nf-muted" />
              <span className="text-nf-white">格式: {mockRules.submission_format.join(", ")}</span>
            </li>
            <li className="flex items-center gap-2">
              <Clock className="h-4 w-4 text-nf-muted" />
              <span className="text-nf-white">每人限提交 {mockRules.max_submissions} 次</span>
            </li>
          </ul>
        </PanelCard>
      </PanelSection>

      <Button className="w-full bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
        <UserPlus className="h-4 w-4 mr-2" />
        报名参赛
      </Button>
    </Panel>
  )

  return (
    <PageLayout variant="full" panel={panelContent}>
      {/* Back Button */}
      <Link href="/events" className="inline-flex items-center gap-2 text-nf-muted hover:text-nf-white mb-6">
        <ArrowLeft className="h-4 w-4" />
        返回活动列表
      </Link>

      {/* Cover Image */}
      <div className="relative aspect-video bg-nf-surface rounded-xl mb-6 overflow-hidden">
        {event?.cover_image ? (
          <img src={event.cover_image} alt={event.name} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-nf-secondary to-nf-dark">
            <Calendar className="h-20 w-20 text-nf-muted" />
          </div>
        )}
        <Badge className={`absolute top-4 left-4 ${statusInfo.className}`}>
          {statusInfo.label}
        </Badge>
      </div>

      {/* Title & Meta */}
      <div className="mb-6">
        <h1 className="font-heading text-3xl font-bold text-nf-white mb-2">
          🏆 {event?.name || "活动"}
        </h1>
        <div className="flex items-center gap-4 text-nf-muted">
          <span>由 {event?.created_by ? `用户 #${event.created_by}` : "未知主办方"} 主办</span>
          <span>·</span>
          <span>{dateRange || "-"}</span>
        </div>
        <div className="flex gap-2 mt-4">
          {(event?.tags || []).map((tag) => (
            <Badge key={tag} variant="secondary" className="bg-nf-dark">
              {tag}
            </Badge>
          ))}
        </div>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="details">
        <TabsList className="bg-nf-surface border-nf-secondary mb-6">
          <TabsTrigger value="details">📋 详情</TabsTrigger>
          <TabsTrigger value="submissions">📝 提交</TabsTrigger>
          <TabsTrigger value="teams">👥 团队</TabsTrigger>
          <TabsTrigger value="ranking">🏅 排名</TabsTrigger>
        </TabsList>

        <TabsContent value="details">
          <div className="prose prose-invert max-w-none">
            <div className="whitespace-pre-wrap text-nf-light-gray">
              {isLoading ? "加载中..." : error ? error : event?.content || "暂无详情"}
            </div>
          </div>

          {/* Scoring Criteria */}
          <div className="mt-8">
            <h2 className="font-heading text-xl font-semibold text-nf-white mb-4">评分标准</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {mockRules.scoring_criteria.map((criteria) => (
                <div key={criteria.name} className="bg-nf-surface rounded-lg p-4 text-center">
                  <p className="text-2xl font-bold text-nf-lime mb-1">{criteria.weight}%</p>
                  <p className="text-sm text-nf-muted">{criteria.name}</p>
                </div>
              ))}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="submissions">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {mockPosts.map((post) => (
              <PostCard key={post.id} {...post} />
            ))}
          </div>
        </TabsContent>

        <TabsContent value="teams">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {mockGroups.map((group) => (
              <GroupCard key={group.id} {...group} />
            ))}
          </div>
        </TabsContent>

        <TabsContent value="ranking">
          <div className="space-y-4">
            {mockPosts.map((post, index) => (
              <div key={post.id} className="flex items-center gap-4 bg-nf-surface rounded-lg p-4">
                <div className="text-2xl font-bold text-nf-lime">#{index + 1}</div>
                <div className="flex-1">
                  <h3 className="font-medium text-nf-white">{post.title}</h3>
                  <p className="text-sm text-nf-muted">{post.created_by.display_name}</p>
                </div>
                <div className="text-right">
                  <p className="text-lg font-bold text-nf-white">⭐ 92.5</p>
                  <p className="text-xs text-nf-muted">平均分</p>
                </div>
              </div>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </PageLayout>
  )
}
