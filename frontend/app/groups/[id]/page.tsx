"use client"

import { use } from "react"
import Link from "next/link"
import { ArrowLeft, Users, Calendar, FileText, Settings, UserPlus, Share2 } from "lucide-react"
import { PageLayout } from "@/components/layout/PageLayout"
import { Panel, PanelSection, PanelCard } from "@/components/layout/Panel"
import { PostCard } from "@/components/cards/PostCard"
import { CategoryCard } from "@/components/cards/CategoryCard"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

// Mock data
const mockGroup = {
  id: 1,
  name: "创新先锋队",
  description: "热爱技术，热爱开源，我们是一群热情的创客！我们专注于 AI 和 Web3 领域的创新，已经参加过多次 Hackathon 并获得优异成绩。",
  visibility: "public",
  require_approval: true,
  member_count: 5,
  created_by: { id: 1, username: "alice", display_name: "Alice Chen" },
}

const mockMembers = [
  { id: 1, username: "alice", display_name: "Alice Chen", role: "owner", status: "accepted" },
  { id: 2, username: "bob", display_name: "Bob Wang", role: "member", status: "accepted" },
  { id: 3, username: "carol", display_name: "Carol Li", role: "member", status: "accepted" },
  { id: 4, username: "dave", display_name: "Dave Zhang", role: "member", status: "accepted" },
  { id: 5, username: "eve", display_name: "Eve Liu", role: "member", status: "pending" },
]

const mockPosts = [
  { id: 1, title: "基于大模型的智能教育平台", type: "for_category", status: "published", tags: ["AI"], like_count: 128, comment_count: 32, created_by: { id: 1, username: "alice", display_name: "Alice" } },
]

const mockCategories = [
  { id: 1, name: "AI 创新挑战赛 2024", type: "competition" as const, status: "published" as const, tags: ["AI"], participant_count: 128 },
]

export default function GroupDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params)

  const panelContent = (
    <Panel title="👥 团队操作">
      <PanelSection>
        <div className="space-y-3">
          <Button className="w-full bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
            <UserPlus className="h-4 w-4 mr-2" />
            申请加入
          </Button>
          <Button variant="outline" className="w-full border-nf-secondary">
            <Share2 className="h-4 w-4 mr-2" />
            分享团队
          </Button>
        </div>
      </PanelSection>

      <PanelSection title="📊 团队统计">
        <PanelCard>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-2 text-nf-muted">
                <Users className="h-4 w-4" /> 成员
              </span>
              <span className="text-nf-white font-medium">{mockGroup.member_count}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-2 text-nf-muted">
                <Calendar className="h-4 w-4" /> 参与活动
              </span>
              <span className="text-nf-white font-medium">{mockCategories.length}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-2 text-nf-muted">
                <FileText className="h-4 w-4" /> 发布帖子
              </span>
              <span className="text-nf-white font-medium">{mockPosts.length}</span>
            </div>
          </div>
        </PanelCard>
      </PanelSection>

      <PanelSection title="🏆 荣誉墙">
        <PanelCard>
          <p className="text-sm text-nf-muted text-center py-4">暂无获奖记录</p>
        </PanelCard>
      </PanelSection>
    </Panel>
  )

  return (
    <PageLayout variant="full" user={null} panel={panelContent}>
      {/* Back Button */}
      <Link href="/groups" className="inline-flex items-center gap-2 text-nf-muted hover:text-nf-white mb-6">
        <ArrowLeft className="h-4 w-4" />
        返回团队列表
      </Link>

      {/* Group Header */}
      <div className="flex items-start gap-6 mb-8">
        <Avatar className="h-24 w-24 rounded-xl">
          <AvatarFallback className="rounded-xl bg-gradient-to-br from-nf-cyan to-nf-pink text-nf-white text-3xl font-bold">
            {mockGroup.name.charAt(0)}
          </AvatarFallback>
        </Avatar>
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h1 className="font-heading text-3xl font-bold text-nf-white">{mockGroup.name}</h1>
            <Badge variant="secondary" className="bg-nf-dark">
              {mockGroup.visibility === "public" ? "🌐 公开" : "🔒 私密"}
            </Badge>
          </div>
          <p className="text-nf-muted mb-2">
            {mockGroup.member_count} 成员 · {mockCategories.length} 活动参与
          </p>
        </div>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="about">
        <TabsList className="bg-nf-surface border-nf-secondary mb-6">
          <TabsTrigger value="about">📋 简介</TabsTrigger>
          <TabsTrigger value="members">👥 成员</TabsTrigger>
          <TabsTrigger value="events">📅 活动</TabsTrigger>
          <TabsTrigger value="posts">📝 帖子</TabsTrigger>
        </TabsList>

        <TabsContent value="about">
          <div className="bg-nf-surface rounded-xl p-6">
            <h2 className="font-heading text-xl font-semibold text-nf-white mb-4">团队简介</h2>
            <p className="text-nf-light-gray whitespace-pre-wrap">{mockGroup.description}</p>
          </div>
        </TabsContent>

        <TabsContent value="members">
          <div className="space-y-4">
            {mockMembers.map((member) => (
              <div
                key={member.id}
                className="flex items-center gap-4 p-4 bg-nf-surface rounded-lg"
              >
                <Avatar className="h-12 w-12">
                  <AvatarFallback className="bg-nf-dark">
                    {member.display_name.charAt(0)}
                  </AvatarFallback>
                </Avatar>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-nf-white">{member.display_name}</span>
                    {member.role === "owner" && (
                      <Badge className="bg-nf-lime text-nf-near-black text-xs">创建者</Badge>
                    )}
                    {member.status === "pending" && (
                      <Badge variant="secondary" className="bg-nf-orange text-nf-near-black text-xs">待审批</Badge>
                    )}
                  </div>
                  <p className="text-sm text-nf-muted">@{member.username}</p>
                </div>
                {member.status === "pending" && (
                  <div className="flex gap-2">
                    <Button size="sm" className="bg-nf-lime text-nf-near-black">通过</Button>
                    <Button size="sm" variant="outline" className="border-nf-secondary">拒绝</Button>
                  </div>
                )}
              </div>
            ))}
            <Button variant="outline" className="w-full border-nf-secondary">
              <UserPlus className="h-4 w-4 mr-2" />
              邀请成员
            </Button>
          </div>
        </TabsContent>

        <TabsContent value="events">
          {mockCategories.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {mockCategories.map((cat) => (
                <CategoryCard key={cat.id} {...cat} />
              ))}
            </div>
          ) : (
            <div className="text-center py-16">
              <p className="text-nf-muted">暂未参与活动</p>
            </div>
          )}
        </TabsContent>

        <TabsContent value="posts">
          {mockPosts.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {mockPosts.map((post) => (
                <PostCard key={post.id} {...post} />
              ))}
            </div>
          ) : (
            <div className="text-center py-16">
              <p className="text-nf-muted">暂无帖子</p>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </PageLayout>
  )
}
