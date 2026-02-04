"use client"

import { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { X, Upload, Search } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Header } from "@/components/layout/Header"

export default function CreateGroupPage() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    visibility: "public",
    require_approval: true,
  })
  const [invitedUsers, setInvitedUsers] = useState<Array<{ id: number; username: string; display_name: string }>>([])
  const [searchQuery, setSearchQuery] = useState("")

  const handleRemoveUser = (userId: number) => {
    setInvitedUsers(invitedUsers.filter((u) => u.id !== userId))
  }

  const handleSubmit = () => {
    // TODO: API call
    console.log({ ...formData, invited_users: invitedUsers.map((u) => u.id) })
    router.push("/groups")
  }

  return (
    <div className="min-h-screen bg-nf-dark">
      <Header />

      {/* Top Bar */}
      <div className="fixed top-[60px] left-0 right-0 h-14 bg-nf-surface border-b border-nf-secondary z-40">
        <div className="max-w-4xl mx-auto h-full flex items-center justify-between px-4">
          <Link href="/groups" className="flex items-center gap-2 text-nf-muted hover:text-nf-white">
            <X className="h-5 w-5" />
            <span>取消</span>
          </Link>
          <h1 className="font-heading font-semibold text-nf-white">创建团队</h1>
          <Button
            size="sm"
            className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90"
            onClick={handleSubmit}
          >
            创建
          </Button>
        </div>
      </div>

      {/* Form Content */}
      <main className="pt-[124px] pb-12 max-w-4xl mx-auto px-4">
        <div className="space-y-8">
          {/* Team Logo */}
          <div>
            <label className="block text-sm font-medium text-nf-white mb-2">团队 Logo</label>
            <div className="flex items-center gap-6">
              <div className="w-24 h-24 rounded-xl border-2 border-dashed border-nf-secondary flex items-center justify-center hover:border-nf-lime transition-colors cursor-pointer">
                <Upload className="h-8 w-8 text-nf-muted" />
              </div>
              <div className="text-sm text-nf-muted">
                <p>点击上传团队 Logo (1:1)</p>
                <p>支持 JPG, PNG, 最大 2MB</p>
              </div>
            </div>
          </div>

          {/* Name */}
          <div>
            <label className="block text-sm font-medium text-nf-white mb-2">
              团队名称 <span className="text-nf-error">*</span>
            </label>
            <Input
              placeholder="输入团队名称，如「创新先锋队」"
              className="bg-nf-surface border-nf-secondary"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-nf-white mb-2">团队简介</label>
            <Textarea
              placeholder="介绍你的团队，展示团队特色和技术栈..."
              className="bg-nf-surface border-nf-secondary min-h-[150px]"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
          </div>

          {/* Visibility */}
          <div>
            <label className="block text-sm font-medium text-nf-white mb-2">可见性</label>
            <div className="flex gap-4">
              <button
                className={`flex-1 p-4 rounded-lg border-2 transition-colors ${
                  formData.visibility === "public"
                    ? "border-nf-lime bg-nf-lime/10"
                    : "border-nf-secondary hover:border-nf-muted"
                }`}
                onClick={() => setFormData({ ...formData, visibility: "public" })}
              >
                <span className="text-2xl mb-2 block">🌐</span>
                <span className={formData.visibility === "public" ? "text-nf-lime" : "text-nf-white"}>
                  公开
                </span>
                <p className="text-xs text-nf-muted mt-1">可被搜索发现</p>
              </button>
              <button
                className={`flex-1 p-4 rounded-lg border-2 transition-colors ${
                  formData.visibility === "private"
                    ? "border-nf-lime bg-nf-lime/10"
                    : "border-nf-secondary hover:border-nf-muted"
                }`}
                onClick={() => setFormData({ ...formData, visibility: "private" })}
              >
                <span className="text-2xl mb-2 block">🔒</span>
                <span className={formData.visibility === "private" ? "text-nf-lime" : "text-nf-white"}>
                  私密
                </span>
                <p className="text-xs text-nf-muted mt-1">仅通过邀请加入</p>
              </button>
            </div>
          </div>

          {/* Join Method */}
          <div>
            <label className="block text-sm font-medium text-nf-white mb-2">加入方式</label>
            <div className="space-y-2">
              <label className="flex items-center gap-3 p-3 bg-nf-surface rounded-lg cursor-pointer">
                <input
                  type="radio"
                  name="require_approval"
                  checked={!formData.require_approval}
                  onChange={() => setFormData({ ...formData, require_approval: false })}
                  className="text-nf-lime"
                />
                <div>
                  <span className="text-nf-white">自由加入</span>
                  <p className="text-xs text-nf-muted">任何人都可以直接加入</p>
                </div>
              </label>
              <label className="flex items-center gap-3 p-3 bg-nf-surface rounded-lg cursor-pointer">
                <input
                  type="radio"
                  name="require_approval"
                  checked={formData.require_approval}
                  onChange={() => setFormData({ ...formData, require_approval: true })}
                  className="text-nf-lime"
                />
                <div>
                  <span className="text-nf-white">需要审批</span>
                  <p className="text-xs text-nf-muted">申请需要团队管理员审批</p>
                </div>
              </label>
            </div>
          </div>

          {/* Invite Members */}
          <div className="border-t border-nf-secondary pt-8">
            <h2 className="font-heading text-lg font-semibold text-nf-white mb-4">👥 邀请成员（可选）</h2>
            <div className="relative mb-4">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-nf-muted" />
              <Input
                placeholder="搜索用户名或邮箱..."
                className="pl-10 bg-nf-surface border-nf-secondary"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            {invitedUsers.length > 0 && (
              <div className="space-y-2">
                <p className="text-sm text-nf-muted">已邀请：</p>
                {invitedUsers.map((user) => (
                  <div
                    key={user.id}
                    className="flex items-center gap-3 p-3 bg-nf-surface rounded-lg"
                  >
                    <Avatar className="h-8 w-8">
                      <AvatarFallback className="bg-nf-dark text-sm">
                        {user.display_name.charAt(0)}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                      <span className="text-nf-white">{user.display_name}</span>
                      <span className="text-nf-muted ml-1">@{user.username}</span>
                    </div>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-6 w-6"
                      onClick={() => handleRemoveUser(user.id)}
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Associated Event */}
          <div className="border-t border-nf-secondary pt-8">
            <h2 className="font-heading text-lg font-semibold text-nf-white mb-4">🎯 关联活动（可选）</h2>
            <Button variant="outline" className="w-full border-nf-secondary text-left justify-start">
              选择要报名的活动...
            </Button>
            <p className="text-xs text-nf-muted mt-2">选择后将自动报名该活动</p>
          </div>
        </div>
      </main>
    </div>
  )
}
