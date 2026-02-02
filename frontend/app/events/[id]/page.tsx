"use client"

import { use } from "react"
import Link from "next/link"
import { ArrowLeft, Calendar, Users, Clock, Award, FileText, UserPlus } from "lucide-react"
import { PageLayout } from "@/components/layout/PageLayout"
import { Panel, PanelSection, PanelCard } from "@/components/layout/Panel"
import { PostCard } from "@/components/cards/PostCard"
import { GroupCard } from "@/components/cards/GroupCard"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

// Mock data
const mockCategory = {
  id: 1,
  name: "AI 创新挑战赛 2024",
  description: "探索人工智能的无限可能，用 AI 改变世界",
  content: `## 活动介绍

本次 AI 创新挑战赛旨在发掘和培养人工智能领域的创新人才，鼓励参赛者利用 AI 技术解决实际问题。

## 奖项设置

- 一等奖：¥50,000 + 孵化支持
- 二等奖：¥30,000
- 三等奖：¥10,000
- 优秀奖：¥5,000 × 10

## 参赛要求

1. 团队人数：2-5 人
2. 提交格式：PDF + 演示视频
3. 作品需原创，不得抄袭`,
  type: "competition",
  status: "published",
  tags: ["AI", "Machine Learning", "Deep Learning"],
  cover_image: null,
  start_date: "2024-03-01",
  end_date: "2024-03-30",
  created_by: { id: 1, username: "techcorp", display_name: "TechCorp" },
  participant_count: 128,
}

const mockPosts = [
  { id: 1, title: "基于大模型的智能教育平台", type: "for_category", status: "published", tags: ["AI"], like_count: 128, comment_count: 32, created_by: { id: 1, username: "alice", display_name: "Alice" } },
  { id: 2, title: "智能客服机器人", type: "for_category", status: "published", tags: ["AI", "NLP"], like_count: 96, comment_count: 24, created_by: { id: 2, username: "bob", display_name: "Bob" } },
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

export default function EventDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params)

  const statusConfig = {
    published: { label: "进行中", className: "bg-nf-lime text-nf-near-black" },
    draft: { label: "草稿", className: "bg-nf-orange text-nf-near-black" },
    closed: { label: "已结束", className: "bg-nf-muted text-nf-white" },
  }

  const statusInfo = statusConfig[mockCategory.status as keyof typeof statusConfig]

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
              <span className="text-nf-white font-medium">{mockCategory.participant_count}</span>
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
              <p className="text-nf-white">{mockCategory.start_date}</p>
            </div>
            <div>
              <p className="text-xs text-nf-muted">结束时间</p>
              <p className="text-nf-white">{mockCategory.end_date}</p>
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
    <PageLayout variant="full" user={null} panel={panelContent}>
      {/* Back Button */}
      <Link href="/events" className="inline-flex items-center gap-2 text-nf-muted hover:text-nf-white mb-6">
        <ArrowLeft className="h-4 w-4" />
        返回活动列表
      </Link>

      {/* Cover Image */}
      <div className="relative aspect-video bg-nf-surface rounded-xl mb-6 overflow-hidden">
        {mockCategory.cover_image ? (
          <img src={mockCategory.cover_image} alt={mockCategory.name} className="w-full h-full object-cover" />
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
          🏆 {mockCategory.name}
        </h1>
        <div className="flex items-center gap-4 text-nf-muted">
          <span>由 {mockCategory.created_by.display_name} 主办</span>
          <span>·</span>
          <span>{mockCategory.start_date} - {mockCategory.end_date}</span>
        </div>
        <div className="flex gap-2 mt-4">
          {mockCategory.tags.map((tag) => (
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
              {mockCategory.content}
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
