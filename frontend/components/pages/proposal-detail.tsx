"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import {
  ChevronLeft, Eye, Heart, MessageSquare,
  Star, Code, BarChart3, Clock, ArrowRight,
  Zap, Globe, User,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Separator } from "@/components/ui/separator"
import { AppLayout } from "@/components/layout/app-layout"

const detailTabs = ["提案详情", "团队信息", "评论区", "版本历史"]

const features = [
  {
    icon: Zap,
    title: "智能学习路径",
    description: "基于AI算法为每位学生定制个性化学习路径，实时调整难度与内容推荐。",
  },
  {
    icon: Star,
    title: "协作式课堂",
    description: "支持多人实时协作学习，融合语音、白板与代码编辑的沉浸式互动体验。",
  },
  {
    icon: Globe,
    title: "全球资源接入",
    description: "接入全球优质教育资源库，支持多语言翻译与跨文化学习交流。",
  },
]

const techStack = [
  { label: "前端框架", value: "Next.js 14 + React 18" },
  { label: "后端服务", value: "Python FastAPI + GraphQL" },
  { label: "AI 引擎", value: "GPT-4o + 自研推理模型" },
  { label: "数据存储", value: "PostgreSQL + Redis + S3" },
  { label: "部署架构", value: "Kubernetes + Cloudflare Edge" },
]

const teamMembers = [
  { name: "L", color: "bg-[var(--nf-lime)]", textColor: "text-[var(--nf-surface)]" },
  { name: "K", color: "bg-[var(--nf-blue)]", textColor: "text-[var(--nf-white)]" },
  { name: "J", color: "bg-[var(--nf-orange)]", textColor: "text-[var(--nf-white)]" },
  { name: "M", color: "bg-[var(--nf-pink)]", textColor: "text-[var(--nf-white)]" },
  { name: "Z", color: "bg-[var(--nf-cyan)]", textColor: "text-[var(--nf-surface)]" },
]

const relatedProposals = [
  {
    title: "探索发言——多人创新教育AI辅助平台",
    author: "LIGHTNING鲸",
    avatarColor: "bg-[var(--nf-blue)]",
  },
  {
    title: "全文智算——海天仿AI服装设计系统",
    author: "Jacksen",
    avatarColor: "bg-[var(--nf-orange)]",
  },
]

const milestones = [
  { date: "2025/01", label: "项目立项", status: "completed" },
  { date: "2025/03", label: "原型设计完成", status: "completed" },
  { date: "2025/05", label: "MVP 发布", status: "current" },
  { date: "2025/08", label: "公测上线", status: "upcoming" },
  { date: "2025/12", label: "正式版发布", status: "upcoming" },
]

function ProposalDetailSidebar() {
  return (
    <>
      {/* Team Info Card */}
      <Card className="bg-[var(--nf-card-bg)] border border-[var(--nf-dark-bg)] rounded-[12px] overflow-hidden">
        <div className="p-5 flex flex-col gap-4">
          <div className="flex items-center justify-between">
            <span className="text-[15px] font-semibold text-[var(--nf-white)]">团队信息</span>
            <Badge variant="outline" className="bg-transparent border-[var(--nf-lime)] text-[var(--nf-lime)] text-[11px] px-2 py-0.5 rounded-sm">
              5人团队
            </Badge>
          </div>
          <div className="flex flex-col gap-2">
            <span className="text-[14px] font-medium text-[var(--nf-white)]">Alibaba Innovation Lab</span>
            <span className="text-[12px] text-[var(--nf-muted)]">专注于AI教育与创新技术研发的跨学科团队</span>
          </div>
          <div className="flex items-center gap-[-8px]">
            {teamMembers.map((member, i) => (
              <Avatar
                key={i}
                className={`w-8 h-8 ${member.color} border-2 border-[var(--nf-card-bg)] ${i > 0 ? "-ml-2" : ""}`}
              >
                <AvatarFallback className={`${member.color} ${member.textColor} text-xs font-semibold`}>
                  {member.name}
                </AvatarFallback>
              </Avatar>
            ))}
          </div>
          <Button className="w-full bg-[var(--nf-dark-bg)] text-[var(--nf-light-gray)] hover:bg-[var(--nf-dark-bg)]/80 rounded-lg py-2.5 text-[13px] font-medium">
            查看团队
            <ArrowRight className="w-3.5 h-3.5 ml-1" />
          </Button>
        </div>
      </Card>

      {/* Related Proposals Card */}
      <Card className="bg-[var(--nf-card-bg)] border border-[var(--nf-dark-bg)] rounded-[12px] overflow-hidden">
        <div className="px-5 py-4 flex items-center justify-between">
          <span className="text-[15px] font-semibold text-[var(--nf-white)]">相关提案</span>
          <span className="text-[12px] text-[var(--nf-muted)] cursor-pointer hover:text-[var(--nf-lime)]">查看更多</span>
        </div>
        <Separator className="bg-[var(--nf-dark-bg)]" />
        <div className="p-4 flex flex-col gap-3">
          {relatedProposals.map((proposal, i) => (
            <div key={i} className="flex items-start gap-3 cursor-pointer group">
              <div className="w-[60px] h-[44px] rounded-lg bg-[var(--nf-dark-bg)] shrink-0" />
              <div className="flex flex-col gap-1.5 min-w-0">
                <span className="text-[13px] font-medium text-[var(--nf-white)] line-clamp-2 group-hover:text-[var(--nf-lime)]">
                  {proposal.title}
                </span>
                <div className="flex items-center gap-1.5">
                  <div className={`w-4 h-4 rounded-full ${proposal.avatarColor} flex items-center justify-center`}>
                    <User className="w-2 h-2 text-[var(--nf-white)]" />
                  </div>
                  <span className="text-[11px] text-[var(--nf-muted)]">{proposal.author}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Timeline Card */}
      <Card className="bg-[var(--nf-card-bg)] border border-[var(--nf-dark-bg)] rounded-[12px] overflow-hidden">
        <div className="px-5 py-4 flex items-center gap-2">
          <Clock className="w-4 h-4 text-[var(--nf-lime)]" />
          <span className="text-[15px] font-semibold text-[var(--nf-white)]">项目里程碑</span>
        </div>
        <Separator className="bg-[var(--nf-dark-bg)]" />
        <div className="p-5 flex flex-col gap-0">
          {milestones.map((milestone, i) => (
            <div key={i} className="flex gap-3">
              {/* Timeline line and dot */}
              <div className="flex flex-col items-center">
                <div
                  className={`w-2.5 h-2.5 rounded-full shrink-0 ${
                    milestone.status === "completed"
                      ? "bg-[var(--nf-lime)]"
                      : milestone.status === "current"
                        ? "bg-[var(--nf-cyan)]"
                        : "bg-[var(--nf-dark-bg)]"
                  }`}
                />
                {i < milestones.length - 1 && (
                  <div className="w-px h-8 bg-[var(--nf-dark-bg)]" />
                )}
              </div>
              {/* Content */}
              <div className="flex flex-col gap-0.5 pb-4">
                <span className="font-mono text-[11px] text-[var(--nf-muted)]">{milestone.date}</span>
                <span
                  className={`text-[13px] font-medium ${
                    milestone.status === "completed"
                      ? "text-[var(--nf-light-gray)]"
                      : milestone.status === "current"
                        ? "text-[var(--nf-cyan)]"
                        : "text-[var(--nf-muted)]"
                  }`}
                >
                  {milestone.label}
                </span>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </>
  )
}

export function ProposalDetail({ postId }: { postId: number }) {
  return (
    <AppLayout navMode="compact" activeNav="探索" sidebar={<ProposalDetailSidebar />}>
      {/* Back Link */}
      <div className="flex items-center gap-1 cursor-pointer group">
        <ChevronLeft className="w-4 h-4 text-[var(--nf-muted)] group-hover:text-[var(--nf-lime)]" />
        <span className="text-[13px] text-[var(--nf-muted)] group-hover:text-[var(--nf-lime)]">返回提案广场</span>
      </div>

      {/* Hero Image */}
      <div className="w-full h-[260px] rounded-[12px] bg-[var(--nf-card-bg)]" />

      {/* Title Section */}
      <div className="flex flex-col gap-3">
        <h1 className="font-heading text-[22px] font-bold text-[var(--nf-white)] leading-tight">
          善意百宝——一人人需要扫有轮AI直辅学习平台
        </h1>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Avatar className="w-8 h-8 bg-[var(--nf-lime)]">
              <AvatarFallback className="bg-[var(--nf-lime)] text-sm font-semibold text-[var(--nf-surface)]">L</AvatarFallback>
            </Avatar>
            <div className="flex flex-col">
              <span className="text-[14px] font-semibold text-[var(--nf-white)]">LIGHTNING鲸</span>
              <span className="text-[12px] text-[var(--nf-muted)]">Alibaba team</span>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1.5">
              <Eye className="w-4 h-4 text-[var(--nf-muted)]" />
              <span className="font-mono text-[13px] text-[var(--nf-muted)]">1.2k</span>
            </div>
            <div className="flex items-center gap-1.5">
              <Heart className="w-4 h-4 text-[var(--nf-muted)]" />
              <span className="font-mono text-[13px] text-[var(--nf-muted)]">234</span>
            </div>
            <div className="flex items-center gap-1.5">
              <MessageSquare className="w-4 h-4 text-[var(--nf-muted)]" />
              <span className="font-mono text-[13px] text-[var(--nf-muted)]">56</span>
            </div>
          </div>
        </div>
      </div>

      {/* Tags */}
      <div className="flex items-center gap-2">
        <Badge className="bg-[var(--nf-lime)] text-[var(--nf-surface)] hover:bg-[var(--nf-lime)]/90 rounded-sm px-2.5 py-1 text-[12px] font-medium">
          AI教育
        </Badge>
        <Badge className="bg-[var(--nf-lime)] text-[var(--nf-surface)] hover:bg-[var(--nf-lime)]/90 rounded-sm px-2.5 py-1 text-[12px] font-medium">
          创新项目
        </Badge>
        <Badge className="bg-[var(--nf-orange)] text-[var(--nf-white)] hover:bg-[var(--nf-orange)]/90 rounded-sm px-2.5 py-1 text-[12px] font-medium">
          协创大赛
        </Badge>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="提案详情" className="w-full">
        <TabsList className="w-full justify-start bg-transparent border-b border-[var(--nf-dark-bg)] rounded-none h-auto p-0 gap-0">
          {detailTabs.map((tab) => (
            <TabsTrigger
              key={tab}
              value={tab}
              className="rounded-none border-b-2 border-transparent px-4 py-2.5 text-sm text-[var(--nf-muted)] data-[state=active]:text-[var(--nf-lime)] data-[state=active]:border-[var(--nf-lime)] data-[state=active]:font-semibold data-[state=active]:bg-transparent data-[state=active]:shadow-none"
            >
              {tab}
            </TabsTrigger>
          ))}
        </TabsList>

        <TabsContent value="提案详情" className="mt-5 flex flex-col gap-6">
          {/* Project Overview */}
          <div className="flex flex-col gap-3">
            <div className="flex items-center gap-2">
              <Zap className="w-[18px] h-[18px] text-[var(--nf-lime)]" />
              <span className="text-[16px] font-semibold text-[var(--nf-white)]">项目概述</span>
            </div>
            <Card className="bg-[var(--nf-card-bg)] border-none rounded-[12px] p-5">
              <p className="text-sm text-[var(--nf-light-gray)] leading-relaxed">
                善意百宝是一个面向所有人的AI辅助学习平台，旨在通过人工智能技术降低教育门槛，让每个人都能获得个性化、高质量的学习体验。平台融合了自然语言处理、知识图谱和自适应学习算法，为用户提供从基础知识到专业技能的全方位学习支持。我们相信，教育的未来在于让AI成为每个人的专属导师，帮助学习者以最适合自己的方式和节奏掌握知识。
              </p>
            </Card>
          </div>

          {/* Core Features */}
          <div className="flex flex-col gap-3">
            <div className="flex items-center gap-2">
              <Star className="w-[18px] h-[18px] text-[var(--nf-lime)]" />
              <span className="text-[16px] font-semibold text-[var(--nf-white)]">核心功能</span>
            </div>
            <div className="grid grid-cols-3 gap-4">
              {features.map((feature) => (
                <Card key={feature.title} className="bg-[var(--nf-card-bg)] border-none rounded-[12px] p-5 flex flex-col gap-3">
                  <div className="w-10 h-10 rounded-lg bg-[var(--nf-dark-bg)] flex items-center justify-center">
                    <feature.icon className="w-5 h-5 text-[var(--nf-lime)]" />
                  </div>
                  <span className="text-[14px] font-semibold text-[var(--nf-white)]">{feature.title}</span>
                  <p className="text-[13px] text-[var(--nf-muted)] leading-relaxed">{feature.description}</p>
                </Card>
              ))}
            </div>
          </div>

          {/* Technical Architecture */}
          <div className="flex flex-col gap-3">
            <div className="flex items-center gap-2">
              <Code className="w-[18px] h-[18px] text-[var(--nf-lime)]" />
              <span className="text-[16px] font-semibold text-[var(--nf-white)]">技术架构</span>
            </div>
            <Card className="bg-[var(--nf-card-bg)] border-none rounded-[12px] p-5">
              <div className="flex flex-col gap-3">
                {techStack.map((item) => (
                  <div key={item.label} className="flex items-center gap-4">
                    <span className="text-[13px] font-medium text-[var(--nf-lime)] w-[90px] shrink-0">{item.label}</span>
                    <Separator orientation="vertical" className="h-4 bg-[var(--nf-dark-bg)]" />
                    <span className="text-[13px] text-[var(--nf-light-gray)]">{item.value}</span>
                  </div>
                ))}
              </div>
            </Card>
          </div>

          {/* Market Analysis */}
          <div className="flex flex-col gap-3">
            <div className="flex items-center gap-2">
              <BarChart3 className="w-[18px] h-[18px] text-[var(--nf-lime)]" />
              <span className="text-[16px] font-semibold text-[var(--nf-white)]">市场分析</span>
            </div>
            <Card className="bg-[var(--nf-card-bg)] border-none rounded-[12px] p-5 flex flex-col gap-4">
              <div className="grid grid-cols-3 gap-4">
                <div className="flex flex-col gap-1">
                  <span className="font-mono text-[24px] font-bold text-[var(--nf-lime)]">$340B</span>
                  <span className="text-[12px] text-[var(--nf-muted)]">全球在线教育市场规模</span>
                </div>
                <div className="flex flex-col gap-1">
                  <span className="font-mono text-[24px] font-bold text-[var(--nf-cyan)]">23.4%</span>
                  <span className="text-[12px] text-[var(--nf-muted)]">AI教育年复合增长率</span>
                </div>
                <div className="flex flex-col gap-1">
                  <span className="font-mono text-[24px] font-bold text-[var(--nf-orange)]">1.5亿</span>
                  <span className="text-[12px] text-[var(--nf-muted)]">目标用户群体规模</span>
                </div>
              </div>
              <Separator className="bg-[var(--nf-dark-bg)]" />
              <p className="text-[13px] text-[var(--nf-light-gray)] leading-relaxed">
                随着AI技术的快速发展，智能教育市场正在经历前所未有的增长。根据市场调研数据，全球在线教育市场规模预计在2026年达到3400亿美元，其中AI辅助学习领域增速最快。我们的平台定位于这一高速增长的赛道，以差异化的AI个性学习体验切入市场。
              </p>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="团队信息" className="mt-5">
          <Card className="bg-[var(--nf-card-bg)] border-none rounded-[12px] p-6">
            <p className="text-sm text-[var(--nf-muted)]">团队信息内容区域</p>
          </Card>
        </TabsContent>

        <TabsContent value="评论区" className="mt-5">
          <Card className="bg-[var(--nf-card-bg)] border-none rounded-[12px] p-6">
            <p className="text-sm text-[var(--nf-muted)]">评论区内容区域</p>
          </Card>
        </TabsContent>

        <TabsContent value="版本历史" className="mt-5">
          <Card className="bg-[var(--nf-card-bg)] border-none rounded-[12px] p-6">
            <p className="text-sm text-[var(--nf-muted)]">版本历史内容区域</p>
          </Card>
        </TabsContent>
      </Tabs>
    </AppLayout>
  )
}
