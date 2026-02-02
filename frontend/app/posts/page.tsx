"use client"

import { useState } from "react"
import { Search, SlidersHorizontal, Plus } from "lucide-react"
import Link from "next/link"
import { PageLayout } from "@/components/layout/PageLayout"
import { PostCard } from "@/components/cards/PostCard"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

// Mock data
const mockPosts = [
  { id: 1, title: "基于大模型的智能教育平台", body: "我们开发了一个基于大语言模型的个性化学习平台...", type: "for_category", status: "published", tags: ["AI", "Education", "LLM"], like_count: 128, comment_count: 32, created_by: { id: 1, username: "alice", display_name: "Alice" }, created_at: "2024-03-10" },
  { id: 2, title: "去中心化身份认证系统", body: "利用区块链技术构建的下一代身份认证系统...", type: "for_category", status: "published", tags: ["Web3", "DID", "Privacy"], like_count: 96, comment_count: 24, created_by: { id: 2, username: "bob", display_name: "Bob" }, created_at: "2024-03-09" },
  { id: 3, title: "碳足迹追踪应用", body: "帮助用户记录和减少日常生活中的碳排放...", type: "for_category", status: "published", tags: ["Climate", "Mobile"], like_count: 72, comment_count: 18, created_by: { id: 3, username: "carol", display_name: "Carol" }, created_at: "2024-03-08" },
  { id: 4, title: "开源代码审查工具", body: "AI 驱动的代码审查助手，帮助开发者发现潜在 bug...", type: "for_category", status: "published", tags: ["DevTools", "AI"], like_count: 156, comment_count: 42, created_by: { id: 4, username: "dave", display_name: "Dave" }, created_at: "2024-03-07" },
  { id: 5, title: "找队友：AI 方向", body: "我们团队正在寻找 AI/ML 方向的伙伴，有兴趣的请联系...", type: "team", status: "published", tags: ["招募", "AI"], like_count: 45, comment_count: 12, created_by: { id: 5, username: "eve", display_name: "Eve" }, created_at: "2024-03-06" },
  { id: 6, title: "日常分享：参赛心得", body: "参加了这次黑客马拉松，收获满满...", type: "general", status: "published", tags: ["心得", "分享"], like_count: 89, comment_count: 28, created_by: { id: 6, username: "frank", display_name: "Frank" }, created_at: "2024-03-05" },
]

export default function PostsPage() {
  const [activeTab, setActiveTab] = useState("all")

  const filteredPosts = mockPosts.filter((post) => {
    if (activeTab === "all") return true
    if (activeTab === "proposals") return post.type === "for_category"
    if (activeTab === "teams") return post.type === "team"
    if (activeTab === "general") return post.type === "general"
    return true
  })

  return (
    <PageLayout variant="compact" user={null}>
      {/* Page Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="font-heading text-3xl font-bold text-nf-white mb-2">📝 帖子</h1>
          <p className="text-nf-muted">浏览社区帖子和项目作品</p>
        </div>
        <Link href="/posts/create">
          <Button className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
            <Plus className="h-4 w-4 mr-2" />
            发布帖子
          </Button>
        </Link>
      </div>

      {/* Search & Filter */}
      <div className="flex gap-4 mb-6">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-nf-muted" />
          <Input
            placeholder="搜索帖子..."
            className="pl-10 bg-nf-surface border-nf-secondary"
          />
        </div>
        <Button variant="outline" className="border-nf-secondary">
          <SlidersHorizontal className="h-4 w-4 mr-2" />
          筛选
        </Button>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="bg-nf-surface border-nf-secondary mb-6">
          <TabsTrigger value="all">全部</TabsTrigger>
          <TabsTrigger value="proposals">💡 提案</TabsTrigger>
          <TabsTrigger value="teams">👥 找队友</TabsTrigger>
          <TabsTrigger value="general">📝 日常</TabsTrigger>
        </TabsList>

        <TabsContent value={activeTab}>
          {filteredPosts.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredPosts.map((post) => (
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
