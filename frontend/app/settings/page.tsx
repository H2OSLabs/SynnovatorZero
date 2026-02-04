"use client"

import { useState } from "react"
import { User, Bell, Shield, Palette, Upload } from "lucide-react"
import { PageLayout } from "@/components/layout/PageLayout"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Separator } from "@/components/ui/separator"

// Mock user data
const mockUser = {
  id: 1,
  username: "alice",
  display_name: "Alice Chen",
  email: "alice@example.com",
  bio: "全栈开发者，热爱 AI 和教育科技",
  avatar_url: null,
  location: "北京",
  website: "github.com/alice",
}

export default function SettingsPage() {
  const [formData, setFormData] = useState({
    display_name: mockUser.display_name,
    username: mockUser.username,
    email: mockUser.email,
    bio: mockUser.bio,
    location: mockUser.location,
    website: mockUser.website,
  })

  const handleSave = () => {
    // TODO: API call
    console.log(formData)
  }

  return (
    <PageLayout variant="full">
      <div className="max-w-3xl">
        <h1 className="font-heading text-3xl font-bold text-nf-white mb-2">⚙️ 设置</h1>
        <p className="text-nf-muted mb-8">管理你的账户设置和偏好</p>

        <Tabs defaultValue="profile" className="space-y-6">
          <TabsList className="bg-nf-surface border-nf-secondary">
            <TabsTrigger value="profile" className="gap-2">
              <User className="h-4 w-4" />
              个人资料
            </TabsTrigger>
            <TabsTrigger value="notifications" className="gap-2">
              <Bell className="h-4 w-4" />
              通知
            </TabsTrigger>
            <TabsTrigger value="privacy" className="gap-2">
              <Shield className="h-4 w-4" />
              隐私
            </TabsTrigger>
            <TabsTrigger value="appearance" className="gap-2">
              <Palette className="h-4 w-4" />
              外观
            </TabsTrigger>
          </TabsList>

          <TabsContent value="profile" className="space-y-6">
            {/* Avatar */}
            <div className="flex items-center gap-6">
              <Avatar className="h-24 w-24">
                <AvatarImage src={mockUser.avatar_url || undefined} />
                <AvatarFallback className="bg-gradient-to-br from-nf-lime to-nf-cyan text-nf-near-black text-2xl font-bold">
                  {mockUser.display_name.charAt(0)}
                </AvatarFallback>
              </Avatar>
              <div>
                <Button variant="outline" className="border-nf-secondary mb-2">
                  <Upload className="h-4 w-4 mr-2" />
                  更换头像
                </Button>
                <p className="text-xs text-nf-muted">支持 JPG, PNG, 最大 2MB</p>
              </div>
            </div>

            <Separator className="bg-nf-secondary" />

            {/* Display Name */}
            <div>
              <label className="block text-sm font-medium text-nf-white mb-2">显示名称</label>
              <Input
                className="bg-nf-surface border-nf-secondary"
                value={formData.display_name}
                onChange={(e) => setFormData({ ...formData, display_name: e.target.value })}
              />
            </div>

            {/* Username */}
            <div>
              <label className="block text-sm font-medium text-nf-white mb-2">用户名</label>
              <div className="flex items-center gap-2">
                <span className="text-nf-muted">@</span>
                <Input
                  className="bg-nf-surface border-nf-secondary"
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                />
              </div>
            </div>

            {/* Email */}
            <div>
              <label className="block text-sm font-medium text-nf-white mb-2">邮箱</label>
              <Input
                type="email"
                className="bg-nf-surface border-nf-secondary"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              />
            </div>

            {/* Bio */}
            <div>
              <label className="block text-sm font-medium text-nf-white mb-2">个人简介</label>
              <Textarea
                className="bg-nf-surface border-nf-secondary"
                value={formData.bio}
                onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
              />
            </div>

            {/* Location */}
            <div>
              <label className="block text-sm font-medium text-nf-white mb-2">所在地</label>
              <Input
                className="bg-nf-surface border-nf-secondary"
                value={formData.location}
                onChange={(e) => setFormData({ ...formData, location: e.target.value })}
              />
            </div>

            {/* Website */}
            <div>
              <label className="block text-sm font-medium text-nf-white mb-2">个人网站</label>
              <Input
                className="bg-nf-surface border-nf-secondary"
                placeholder="github.com/username"
                value={formData.website}
                onChange={(e) => setFormData({ ...formData, website: e.target.value })}
              />
            </div>

            <Button className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90" onClick={handleSave}>
              保存更改
            </Button>
          </TabsContent>

          <TabsContent value="notifications" className="space-y-6">
            <div className="bg-nf-surface rounded-xl p-6">
              <h3 className="font-heading text-lg font-semibold text-nf-white mb-4">通知偏好</h3>
              <div className="space-y-4">
                {[
                  { id: "email_comments", label: "有人评论我的帖子", desc: "通过邮件通知" },
                  { id: "email_likes", label: "有人点赞我的帖子", desc: "通过邮件通知" },
                  { id: "email_follows", label: "有人关注我", desc: "通过邮件通知" },
                  { id: "email_events", label: "活动更新", desc: "参与的活动有新动态" },
                ].map((item) => (
                  <label key={item.id} className="flex items-center justify-between p-3 bg-nf-dark rounded-lg cursor-pointer">
                    <div>
                      <span className="text-nf-white">{item.label}</span>
                      <p className="text-xs text-nf-muted">{item.desc}</p>
                    </div>
                    <input type="checkbox" defaultChecked className="h-4 w-4" />
                  </label>
                ))}
              </div>
            </div>
          </TabsContent>

          <TabsContent value="privacy" className="space-y-6">
            <div className="bg-nf-surface rounded-xl p-6">
              <h3 className="font-heading text-lg font-semibold text-nf-white mb-4">隐私设置</h3>
              <div className="space-y-4">
                {[
                  { id: "profile_public", label: "公开个人主页", desc: "允许所有人查看你的主页" },
                  { id: "show_email", label: "显示邮箱", desc: "在个人主页显示邮箱地址" },
                  { id: "allow_messages", label: "允许私信", desc: "允许其他用户发送私信" },
                ].map((item) => (
                  <label key={item.id} className="flex items-center justify-between p-3 bg-nf-dark rounded-lg cursor-pointer">
                    <div>
                      <span className="text-nf-white">{item.label}</span>
                      <p className="text-xs text-nf-muted">{item.desc}</p>
                    </div>
                    <input type="checkbox" defaultChecked className="h-4 w-4" />
                  </label>
                ))}
              </div>
            </div>

            <div className="bg-nf-surface rounded-xl p-6">
              <h3 className="font-heading text-lg font-semibold text-nf-error mb-4">危险区域</h3>
              <p className="text-sm text-nf-muted mb-4">删除账户将永久移除你的所有数据，此操作不可撤销。</p>
              <Button variant="outline" className="border-nf-error text-nf-error hover:bg-nf-error hover:text-nf-white">
                删除账户
              </Button>
            </div>
          </TabsContent>

          <TabsContent value="appearance" className="space-y-6">
            <div className="bg-nf-surface rounded-xl p-6">
              <h3 className="font-heading text-lg font-semibold text-nf-white mb-4">主题</h3>
              <div className="flex gap-4">
                <button className="flex-1 p-4 rounded-lg border-2 border-nf-lime bg-nf-lime/10">
                  <span className="text-2xl mb-2 block">🌙</span>
                  <span className="text-nf-lime">深色模式</span>
                </button>
                <button className="flex-1 p-4 rounded-lg border-2 border-nf-secondary opacity-50 cursor-not-allowed">
                  <span className="text-2xl mb-2 block">☀️</span>
                  <span className="text-nf-muted">浅色模式</span>
                  <p className="text-xs text-nf-muted mt-1">即将推出</p>
                </button>
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </PageLayout>
  )
}
