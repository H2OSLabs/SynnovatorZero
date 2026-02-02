"use client"

import { useState } from "react"
import Link from "next/link"
import { useRouter, useParams } from "next/navigation"
import { X, Upload, Plus, Trash2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Header } from "@/components/layout/Header"

// Mock existing post data
const mockPost = {
  id: 1,
  title: "基于大模型的智能教育平台",
  body: "## 项目介绍\n\n我们开发了一个基于大语言模型的个性化学习平台...",
  type: "for_category",
  tags: ["AI", "Education", "LLM"],
  resources: [
    { id: 1, filename: "proposal.pdf", display_name: "项目提案" },
    { id: 2, filename: "demo.zip", display_name: "演示文件" },
  ],
}

export default function EditPostPage() {
  const params = useParams()
  const id = params.id as string
  const router = useRouter()
  const [formData, setFormData] = useState({
    title: mockPost.title,
    body: mockPost.body,
    type: mockPost.type,
    tags: mockPost.tags,
  })
  const [tagInput, setTagInput] = useState("")
  const [resources, setResources] = useState(mockPost.resources)

  const handleAddTag = () => {
    if (tagInput.trim() && !formData.tags.includes(tagInput.trim())) {
      setFormData({ ...formData, tags: [...formData.tags, tagInput.trim()] })
      setTagInput("")
    }
  }

  const handleRemoveTag = (tag: string) => {
    setFormData({ ...formData, tags: formData.tags.filter((t) => t !== tag) })
  }

  const handleRemoveResource = (resourceId: number) => {
    setResources(resources.filter((r) => r.id !== resourceId))
  }

  const handleSubmit = (status: "draft" | "published") => {
    // TODO: API call
    console.log({ ...formData, status })
    router.push(`/posts/${id}`)
  }

  return (
    <div className="min-h-screen bg-nf-dark">
      <Header user={{ id: 1, username: "test", role: "participant" }} />

      {/* Top Bar */}
      <div className="fixed top-[60px] left-0 right-0 h-14 bg-nf-surface border-b border-nf-secondary z-40">
        <div className="max-w-4xl mx-auto h-full flex items-center justify-between px-4">
          <Link href={`/posts/${id}`} className="flex items-center gap-2 text-nf-muted hover:text-nf-white">
            <X className="h-5 w-5" />
            <span>取消</span>
          </Link>
          <h1 className="font-heading font-semibold text-nf-white">编辑帖子</h1>
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
              更新
            </Button>
          </div>
        </div>
      </div>

      {/* Form Content */}
      <main className="pt-[124px] pb-12 max-w-4xl mx-auto px-4">
        <div className="space-y-8">
          {/* Post Type */}
          <div>
            <label className="block text-sm font-medium text-nf-white mb-2">帖子类型</label>
            <div className="flex gap-4">
              {[
                { value: "general", label: "📝 日常", desc: "分享日常想法" },
                { value: "for_category", label: "💡 提案", desc: "参赛作品" },
                { value: "team", label: "👥 团队", desc: "找队友" },
                { value: "profile", label: "👤 个人", desc: "个人简介" },
              ].map((type) => (
                <button
                  key={type.value}
                  className={`flex-1 p-3 rounded-lg border-2 transition-colors text-left ${
                    formData.type === type.value
                      ? "border-nf-lime bg-nf-lime/10"
                      : "border-nf-secondary hover:border-nf-muted"
                  }`}
                  onClick={() => setFormData({ ...formData, type: type.value })}
                >
                  <span className="text-lg">{type.label}</span>
                  <p className="text-xs text-nf-muted mt-1">{type.desc}</p>
                </button>
              ))}
            </div>
          </div>

          {/* Title */}
          <div>
            <label className="block text-sm font-medium text-nf-white mb-2">
              标题 <span className="text-nf-error">*</span>
            </label>
            <Input
              placeholder="输入帖子标题"
              className="bg-nf-surface border-nf-secondary"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            />
          </div>

          {/* Content */}
          <div>
            <label className="block text-sm font-medium text-nf-white mb-2">
              内容 <span className="text-nf-error">*</span>
            </label>
            <Textarea
              placeholder="帖子内容（支持 Markdown）"
              className="bg-nf-surface border-nf-secondary min-h-[300px] font-mono"
              value={formData.body}
              onChange={(e) => setFormData({ ...formData, body: e.target.value })}
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

          {/* Attachments */}
          <div className="border-t border-nf-secondary pt-8">
            <h2 className="font-heading text-lg font-semibold text-nf-white mb-4">📎 附件</h2>

            {/* Existing Resources */}
            {resources.length > 0 && (
              <div className="space-y-2 mb-4">
                {resources.map((res) => (
                  <div
                    key={res.id}
                    className="flex items-center gap-3 p-3 bg-nf-surface rounded-lg"
                  >
                    <span className="text-lg">📄</span>
                    <span className="flex-1 text-nf-white">{res.display_name}</span>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="text-nf-error hover:bg-nf-error/10"
                      onClick={() => handleRemoveResource(res.id)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                ))}
              </div>
            )}

            {/* Upload */}
            <div className="border-2 border-dashed border-nf-secondary rounded-xl p-6 text-center hover:border-nf-lime transition-colors cursor-pointer">
              <Upload className="h-8 w-8 text-nf-muted mx-auto mb-2" />
              <p className="text-nf-muted">拖拽文件到此处或点击上传</p>
              <p className="text-xs text-nf-muted mt-1">支持 PDF, ZIP, 图片, 最大 10MB</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
