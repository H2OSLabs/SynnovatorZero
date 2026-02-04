"use client"

import Link from "next/link"
import { useParams } from "next/navigation"
import { ArrowLeft, MapPin, Link as LinkIcon, Calendar, FileText, Heart, Users, MessageCircle } from "lucide-react"
import { PageLayout } from "@/components/layout/PageLayout"
import { Panel, PanelSection, PanelCard } from "@/components/layout/Panel"
import { PostCard } from "@/components/cards/PostCard"
import { GroupCard } from "@/components/cards/GroupCard"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

// Mock data
const mockUser = {
  id: 1,
  username: "alice",
  display_name: "Alice Chen",
  email: "alice@example.com",
  bio: "全栈开发者，热爱 AI 和教育科技。喜欢参加各种 Hackathon，用技术解决实际问题。",
  avatar_url: null,
  cover_image: null,
  role: "participant",
  location: "北京",
  website: "github.com/alice",
  created_at: "2024-01-01",
  following_count: 100,
  follower_count: 50,
  friend_count: 25,
}

const mockPosts = [
  { id: 1, title: "基于大模型的智能教育平台", type: "for_category", status: "published", tags: ["AI", "Education"], like_count: 128, comment_count: 32, created_by: { id: 1, username: "alice", display_name: "Alice" } },
  { id: 2, title: "参赛心得分享", type: "general", status: "published", tags: ["心得"], like_count: 45, comment_count: 12, created_by: { id: 1, username: "alice", display_name: "Alice" } },
]

const mockGroups = [
  { id: 1, name: "创新先锋队", visibility: "public" as const, member_count: 5, description: "热爱技术，热爱开源" },
]

const mockStats = {
  post_count: 20,
  event_count: 5,
  total_likes: 500,
}

export default function UserProfilePage() {
  const params = useParams()
  const id = params.id as string

  const panelContent = (
    <Panel title="👤 用户操作">
      <PanelSection>
        <div className="space-y-3">
          <Button className="w-full bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
            + 关注
          </Button>
          <Button variant="outline" className="w-full border-nf-secondary">
            <MessageCircle className="h-4 w-4 mr-2" />
            发消息
          </Button>
        </div>
      </PanelSection>

      <PanelSection title="📊 用户统计">
        <PanelCard>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-2 text-nf-muted">
                <Calendar className="h-4 w-4" /> 参与活动
              </span>
              <span className="text-nf-white font-medium">{mockStats.event_count}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-2 text-nf-muted">
                <FileText className="h-4 w-4" /> 发布帖子
              </span>
              <span className="text-nf-white font-medium">{mockStats.post_count}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-2 text-nf-muted">
                <Heart className="h-4 w-4" /> 获赞总数
              </span>
              <span className="text-nf-white font-medium">{mockStats.total_likes}</span>
            </div>
          </div>
        </PanelCard>
      </PanelSection>

      <PanelSection title="🏷️ 常用标签">
        <div className="flex flex-wrap gap-2">
          <Badge variant="secondary" className="bg-nf-dark">AI</Badge>
          <Badge variant="secondary" className="bg-nf-dark">Education</Badge>
          <Badge variant="secondary" className="bg-nf-dark">TypeScript</Badge>
          <Badge variant="secondary" className="bg-nf-dark">React</Badge>
        </div>
      </PanelSection>
    </Panel>
  )

  return (
    <PageLayout variant="full" panel={panelContent}>
      {/* Cover Image */}
      <div className="relative h-48 -mx-8 -mt-8 mb-20 bg-gradient-to-br from-nf-secondary to-nf-dark">
        {/* Profile Section */}
        <div className="absolute -bottom-16 left-8 flex items-end gap-6">
          <Avatar className="h-32 w-32 border-4 border-nf-dark">
            <AvatarImage src={mockUser.avatar_url || undefined} />
            <AvatarFallback className="bg-gradient-to-br from-nf-lime to-nf-cyan text-nf-near-black text-4xl font-bold">
              {mockUser.display_name.charAt(0)}
            </AvatarFallback>
          </Avatar>
        </div>
      </div>

      {/* User Info */}
      <div className="mb-8">
        <h1 className="font-heading text-3xl font-bold text-nf-white mb-1">
          {mockUser.display_name}
        </h1>
        <p className="text-nf-muted mb-4">@{mockUser.username}</p>

        {/* Bio */}
        <p className="text-nf-light-gray mb-4 max-w-2xl">{mockUser.bio}</p>

        {/* Meta Info */}
        <div className="flex items-center gap-4 text-sm text-nf-muted mb-4">
          {mockUser.location && (
            <span className="flex items-center gap-1">
              <MapPin className="h-4 w-4" />
              {mockUser.location}
            </span>
          )}
          {mockUser.website && (
            <a href={`https://${mockUser.website}`} target="_blank" rel="noopener noreferrer" className="flex items-center gap-1 hover:text-nf-lime">
              <LinkIcon className="h-4 w-4" />
              {mockUser.website}
            </a>
          )}
        </div>

        {/* Follow Stats */}
        <div className="flex items-center gap-6 text-sm">
          <span className="text-nf-white">
            <strong>{mockUser.following_count}</strong>{" "}
            <span className="text-nf-muted">关注</span>
          </span>
          <span className="text-nf-white">
            <strong>{mockUser.follower_count}</strong>{" "}
            <span className="text-nf-muted">粉丝</span>
          </span>
          <span className="text-nf-white">
            <strong>{mockUser.friend_count}</strong>{" "}
            <span className="text-nf-muted">好友</span>
          </span>
        </div>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="posts">
        <TabsList className="bg-nf-surface border-nf-secondary mb-6">
          <TabsTrigger value="posts">📝 帖子</TabsTrigger>
          <TabsTrigger value="groups">👥 团队</TabsTrigger>
          <TabsTrigger value="events">📅 活动</TabsTrigger>
          <TabsTrigger value="favorites">❤️ 收藏</TabsTrigger>
        </TabsList>

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

        <TabsContent value="groups">
          {mockGroups.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {mockGroups.map((group) => (
                <GroupCard key={group.id} {...group} />
              ))}
            </div>
          ) : (
            <div className="text-center py-16">
              <p className="text-nf-muted">暂未加入团队</p>
            </div>
          )}
        </TabsContent>

        <TabsContent value="events">
          <div className="text-center py-16">
            <p className="text-nf-muted">暂未参与活动</p>
          </div>
        </TabsContent>

        <TabsContent value="favorites">
          <div className="text-center py-16">
            <p className="text-nf-muted">暂无收藏</p>
          </div>
        </TabsContent>
      </Tabs>
    </PageLayout>
  )
}
