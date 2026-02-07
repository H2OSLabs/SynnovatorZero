"use client"

import { useState, Suspense } from "react"
import Link from "next/link"
import { useRouter, useSearchParams } from "next/navigation"
import { X, Upload, Plus, Loader2 } from "lucide-react"
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Header } from "@/components/layout/Header"
import { DEFAULT_POST_TYPE, isPostType, POST_TYPE_OPTIONS } from "@/lib/post-type"
import { createPost, type PostStatus } from "@/lib/api-client"

function CreatePostForm() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const typeParam = searchParams?.get("type") || ""
  const defaultType = isPostType(typeParam) ? typeParam : DEFAULT_POST_TYPE

  const [formData, setFormData] = useState({
    title: "",
    body: "",
    type: defaultType,
    tags: [] as string[],
    event_id: null as number | null,
  })
  const [tagInput, setTagInput] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleAddTag = () => {
    if (tagInput.trim() && !formData.tags.includes(tagInput.trim())) {
      setFormData({ ...formData, tags: [...formData.tags, tagInput.trim()] })
      setTagInput("")
    }
  }

  const handleRemoveTag = (tag: string) => {
    setFormData({ ...formData, tags: formData.tags.filter((t) => t !== tag) })
  }

  const handleSubmit = async (status: PostStatus) => {
    if (!formData.title.trim()) {
      toast.error("请输入帖子标题")
      return
    }

    setIsSubmitting(true)
    try {
      const post = await createPost({
        title: formData.title,
        content: formData.body,
        type: formData.type,
        tags: formData.tags.length > 0 ? formData.tags : undefined,
        status,
        event_id: formData.event_id,
      })
      toast.success(status === "published" ? "帖子发布成功" : "草稿保存成功")
      router.push(`/posts/${post.id}`)
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "发布失败，请重试")
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen bg-nf-dark">
      <Header />

      {/* Top Bar */}
      <div className="fixed top-[60px] left-0 right-0 h-14 bg-nf-surface border-b border-nf-secondary z-40">
        <div className="max-w-4xl mx-auto h-full flex items-center justify-between px-4">
          <Link href="/posts" className="flex items-center gap-2 text-nf-muted hover:text-nf-white">
            <X className="h-5 w-5" />
            <span>取消</span>
          </Link>
          <h1 className="font-heading font-semibold text-nf-white">创建帖子</h1>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              className="border-nf-secondary"
              onClick={() => handleSubmit("draft")}
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="h-4 w-4 mr-1 animate-spin" />
                  保存中...
                </>
              ) : (
                "保存草稿"
              )}
            </Button>
            <Button
              size="sm"
              className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90"
              onClick={() => handleSubmit("published")}
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="h-4 w-4 mr-1 animate-spin" />
                  发布中...
                </>
              ) : (
                "发布"
              )}
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
            <div className="flex gap-4 flex-wrap">
              {POST_TYPE_OPTIONS.map((type) => (
                <button
                  key={type.value}
                  className={`flex-1 min-w-[140px] p-3 rounded-lg border-2 transition-colors text-left ${
                    formData.type === type.value
                      ? "border-nf-lime bg-nf-lime/10"
                      : "border-nf-secondary hover:border-nf-muted"
                  }`}
                  onClick={() => setFormData({ ...formData, type: type.value })}
                >
                  <span className="text-lg">
                    {type.icon} {type.label}
                  </span>
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
            <div className="border-2 border-dashed border-nf-secondary rounded-xl p-6 text-center hover:border-nf-lime transition-colors cursor-pointer">
              <Upload className="h-8 w-8 text-nf-muted mx-auto mb-2" />
              <p className="text-nf-muted">拖拽文件到此处或点击上传</p>
              <p className="text-xs text-nf-muted mt-1">支持 PDF, ZIP, 图片, 最大 10MB</p>
            </div>
          </div>

          {/* Event Selection (for proposals) */}
          {formData.type === "proposal" && (
            <div className="border-t border-nf-secondary pt-8">
              <h2 className="font-heading text-lg font-semibold text-nf-white mb-4">🎯 关联活动</h2>
              <Button variant="outline" className="border-nf-secondary w-full text-left justify-start">
                选择要提交的活动...
              </Button>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default function CreatePostPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-nf-dark flex items-center justify-center text-nf-muted">加载中...</div>}>
      <CreatePostForm />
    </Suspense>
  )
}
