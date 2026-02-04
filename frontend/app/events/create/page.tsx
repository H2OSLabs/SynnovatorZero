"use client"

import { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { X, Upload, Plus, Trash2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Header } from "@/components/layout/Header"

export default function CreateEventPage() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    content: "",
    type: "competition",
    tags: [] as string[],
    start_date: "",
    end_date: "",
  })
  const [tagInput, setTagInput] = useState("")

  const handleAddTag = () => {
    if (tagInput.trim() && !formData.tags.includes(tagInput.trim())) {
      setFormData({ ...formData, tags: [...formData.tags, tagInput.trim()] })
      setTagInput("")
    }
  }

  const handleRemoveTag = (tag: string) => {
    setFormData({ ...formData, tags: formData.tags.filter((t) => t !== tag) })
  }

  const handleSubmit = (status: "draft" | "published") => {
    // TODO: API call
    console.log({ ...formData, status })
    router.push("/events")
  }

  return (
    <div className="min-h-screen bg-nf-dark">
      <Header />

      {/* Top Bar */}
      <div className="fixed top-[60px] left-0 right-0 h-14 bg-nf-surface border-b border-nf-secondary z-40">
        <div className="max-w-4xl mx-auto h-full flex items-center justify-between px-4">
          <Link href="/events" className="flex items-center gap-2 text-nf-muted hover:text-nf-white">
            <X className="h-5 w-5" />
            <span>取消</span>
          </Link>
          <h1 className="font-heading font-semibold text-nf-white">创建活动</h1>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              className="border-nf-secondary"
              onClick={() => handleSubmit("draft")}
            >
              保存草稿
            </Button>
            <Button
              size="sm"
              className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90"
              onClick={() => handleSubmit("published")}
            >
              发布
            </Button>
          </div>
        </div>
      </div>

      {/* Form Content */}
      <main className="pt-[124px] pb-12 max-w-4xl mx-auto px-4">
        <div className="space-y-8">
          {/* Cover Image */}
          <div>
            <label className="block text-sm font-medium text-nf-white mb-2">活动封面</label>
            <div className="border-2 border-dashed border-nf-secondary rounded-xl p-8 text-center hover:border-nf-lime transition-colors cursor-pointer">
              <Upload className="h-10 w-10 text-nf-muted mx-auto mb-3" />
              <p className="text-nf-muted">点击上传封面图 (16:9)</p>
              <p className="text-xs text-nf-muted mt-1">支持 JPG, PNG, 最大 5MB</p>
            </div>
          </div>

          {/* Name */}
          <div>
            <label className="block text-sm font-medium text-nf-white mb-2">
              活动名称 <span className="text-nf-error">*</span>
            </label>
            <Input
              placeholder="输入活动名称，如「AI 创新挑战赛 2024」"
              className="bg-nf-surface border-nf-secondary"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
          </div>

          {/* Type */}
          <div>
            <label className="block text-sm font-medium text-nf-white mb-2">活动类型</label>
            <div className="flex gap-4">
              <button
                className={`flex-1 p-4 rounded-lg border-2 transition-colors ${
                  formData.type === "competition"
                    ? "border-nf-lime bg-nf-lime/10"
                    : "border-nf-secondary hover:border-nf-muted"
                }`}
                onClick={() => setFormData({ ...formData, type: "competition" })}
              >
                <span className="text-2xl mb-2 block">🏆</span>
                <span className={formData.type === "competition" ? "text-nf-lime" : "text-nf-white"}>
                  竞赛
                </span>
              </button>
              <button
                className={`flex-1 p-4 rounded-lg border-2 transition-colors ${
                  formData.type === "operation"
                    ? "border-nf-lime bg-nf-lime/10"
                    : "border-nf-secondary hover:border-nf-muted"
                }`}
                onClick={() => setFormData({ ...formData, type: "operation" })}
              >
                <span className="text-2xl mb-2 block">📋</span>
                <span className={formData.type === "operation" ? "text-nf-lime" : "text-nf-white"}>
                  运营
                </span>
              </button>
            </div>
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-nf-white mb-2">
              活动简介 <span className="text-nf-error">*</span>
            </label>
            <Textarea
              placeholder="简要描述活动内容（将显示在活动卡片上）"
              className="bg-nf-surface border-nf-secondary min-h-[100px]"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
          </div>

          {/* Content */}
          <div>
            <label className="block text-sm font-medium text-nf-white mb-2">
              活动详情 <span className="text-nf-error">*</span>
            </label>
            <Textarea
              placeholder="详细描述活动内容、奖项设置、参赛要求等（支持 Markdown）"
              className="bg-nf-surface border-nf-secondary min-h-[300px] font-mono"
              value={formData.content}
              onChange={(e) => setFormData({ ...formData, content: e.target.value })}
            />
          </div>

          {/* Tags */}
          <div>
            <label className="block text-sm font-medium text-nf-white mb-2">标签</label>
            <div className="flex gap-2 mb-2 flex-wrap">
              {formData.tags.map((tag) => (
                <Badge key={tag} variant="secondary" className="bg-nf-surface flex items-center gap-1">
                  {tag}
                  <button onClick={() => handleRemoveTag(tag)}>
                    <X className="h-3 w-3" />
                  </button>
                </Badge>
              ))}
            </div>
            <div className="flex gap-2">
              <Input
                placeholder="添加标签"
                className="bg-nf-surface border-nf-secondary"
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && (e.preventDefault(), handleAddTag())}
              />
              <Button variant="outline" className="border-nf-secondary" onClick={handleAddTag}>
                <Plus className="h-4 w-4" />
              </Button>
            </div>
          </div>

          {/* Dates */}
          <div className="border-t border-nf-secondary pt-8">
            <h2 className="font-heading text-lg font-semibold text-nf-white mb-4">📅 时间设置</h2>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-nf-white mb-2">开始时间</label>
                <Input
                  type="date"
                  className="bg-nf-surface border-nf-secondary"
                  value={formData.start_date}
                  onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-nf-white mb-2">结束时间</label>
                <Input
                  type="date"
                  className="bg-nf-surface border-nf-secondary"
                  value={formData.end_date}
                  onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
                />
              </div>
            </div>
          </div>

          {/* Rules */}
          <div className="border-t border-nf-secondary pt-8">
            <h2 className="font-heading text-lg font-semibold text-nf-white mb-4">📋 规则设置（可选）</h2>
            <Button variant="outline" className="border-nf-secondary w-full">
              <Plus className="h-4 w-4 mr-2" />
              创建活动规则
            </Button>
          </div>
        </div>
      </main>
    </div>
  )
}
