"use client"

import { useState } from "react"
import { Search, SlidersHorizontal } from "lucide-react"
import { PageLayout } from "@/components/layout/PageLayout"
import { CategoryCard } from "@/components/cards/CategoryCard"
import { PostCard } from "@/components/cards/PostCard"
import { GroupCard } from "@/components/cards/GroupCard"
import { UserCard } from "@/components/cards/UserCard"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

// Mock data
const mockCategories = [
  { id: 1, name: "AI 创新挑战赛 2024", type: "competition" as const, status: "published" as const, tags: ["AI"], participant_count: 128 },
  { id: 2, name: "Web3 黑客马拉松", type: "competition" as const, status: "published" as const, tags: ["Web3"], participant_count: 86 },
]

const mockPosts = [
  { id: 1, title: "基于大模型的智能教育平台", type: "for_category", status: "published", tags: ["AI"], like_count: 128, comment_count: 32, created_by: { id: 1, username: "alice", display_name: "Alice" } },
  { id: 2, title: "去中心化身份认证系统", type: "for_category", status: "published", tags: ["Web3"], like_count: 96, comment_count: 24, created_by: { id: 2, username: "bob", display_name: "Bob" } },
]

const mockGroups = [
  { id: 1, name: "创新先锋队", visibility: "public" as const, member_count: 5, description: "热爱技术，热爱开源" },
  { id: 2, name: "AI 实验室", visibility: "public" as const, member_count: 8, description: "探索 AI 的无限可能" },
]

const mockUsers = [
  { id: 1, username: "alice", display_name: "Alice", bio: "全栈开发者", post_count: 20, event_count: 5, like_count: 500 },
  { id: 2, username: "bob", display_name: "Bob", bio: "Web3 爱好者", post_count: 15, event_count: 3, like_count: 320 },
]

export default function ExplorePage() {
  const [activeTab, setActiveTab] = useState("all")

  return (
    <PageLayout variant="compact" user={null}>
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="font-heading text-3xl font-bold text-nf-white mb-2">🔍 探索</h1>
        <p className="text-nf-muted">发现最新的 Hackathon 活动和精彩项目</p>
      </div>

      {/* Search & Filter */}
      <div className="flex gap-4 mb-6">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-nf-muted" />
          <Input
            placeholder="搜索活动、帖子、团队、用户..."
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
          <TabsTrigger value="events">活动</TabsTrigger>
          <TabsTrigger value="posts">帖子</TabsTrigger>
          <TabsTrigger value="groups">团队</TabsTrigger>
          <TabsTrigger value="users">用户</TabsTrigger>
        </TabsList>

        <TabsContent value="all">
          <div className="space-y-8">
            {/* Events Section */}
            <section>
              <h2 className="font-heading text-xl font-semibold text-nf-white mb-4">活动</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {mockCategories.map((cat) => (
                  <CategoryCard key={cat.id} {...cat} />
                ))}
              </div>
            </section>

            {/* Posts Section */}
            <section>
              <h2 className="font-heading text-xl font-semibold text-nf-white mb-4">帖子</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {mockPosts.map((post) => (
                  <PostCard key={post.id} {...post} />
                ))}
              </div>
            </section>

            {/* Groups Section */}
            <section>
              <h2 className="font-heading text-xl font-semibold text-nf-white mb-4">团队</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {mockGroups.map((group) => (
                  <GroupCard key={group.id} {...group} />
                ))}
              </div>
            </section>
          </div>
        </TabsContent>

        <TabsContent value="events">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockCategories.map((cat) => (
              <CategoryCard key={cat.id} {...cat} />
            ))}
          </div>
        </TabsContent>

        <TabsContent value="posts">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockPosts.map((post) => (
              <PostCard key={post.id} {...post} />
            ))}
          </div>
        </TabsContent>

        <TabsContent value="groups">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockGroups.map((group) => (
              <GroupCard key={group.id} {...group} />
            ))}
          </div>
        </TabsContent>

        <TabsContent value="users">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockUsers.map((user) => (
              <UserCard key={user.id} {...user} />
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </PageLayout>
  )
}
