"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { useRouter, useParams } from "next/navigation"
import { X, Upload, Plus, Trash2, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Header } from "@/components/layout/Header"
import { POST_TYPE_OPTIONS } from "@/lib/post-type"
import { getPost, updatePost, getPostResources } from "@/lib/api-client"

interface ResourceItem {
  id: number
  resource_id: number
  display_name?: string
  filename?: string
}

export default function EditPostPage() {
  const params = useParams()
  const idParam = params?.id
  const rawId = Array.isArray(idParam) ? idParam[0] : idParam
  const id = typeof rawId === "string" ? Number(rawId) : Number.NaN
  const router = useRouter()

  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [formData, setFormData] = useState({
    title: "",
    content: "",
    type: "general",
    tags: [] as string[],
  })
  const [tagInput, setTagInput] = useState("")
  const [resources, setResources] = useState<ResourceItem[]>([])

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true)
        setError(null)

        // Fetch post data
        const postData = await getPost(id)
        setFormData({
          title: postData.title || "",
          content: postData.content || "",
          type: postData.type || "general",
          tags: postData.tags || [],
        })

        // Fetch resources
        const resourcesData = await getPostResources(id)
        setResources(
          resourcesData.map((r) => ({
            id: r.id,
            resource_id: r.resource_id,
            display_name: `Resource ${r.resource_id}`,
          }))
        )
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load post")
      } finally {
        setLoading(false)
      }
    }

    if (Number.isFinite(id)) {
      fetchData()
    } else {
      setError("无效的帖子 ID")
      setLoading(false)
    }
  }, [id])

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

  const handleSubmit = async (status: "draft" | "published") => {
    try {
      setSaving(true)
      await updatePost(id, {
        title: formData.title,
        content: formData.content,
        type: formData.type,
        tags: formData.tags,
        status,
      })
      router.push(`/posts/${id}`)
    } catch (err) {
      console.error("Failed to update post:", err)
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-nf-dark">
        <Header />
        <div className="flex items-center justify-center min-h-[400px] pt-[60px]">
          <Loader2 className="h-8 w-8 animate-spin text-nf-lime" />
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-nf-dark">
        <Header />
        <div className="text-center py-12 pt-[120px]">
          <p className="text-nf-error mb-4">{error}</p>
          <Link href="/posts">
            <Button variant="outline">Back to posts</Button>
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-nf-dark">
      <Header />

      {/* Top Bar */}
      <div className="fixed top-[60px] left-0 right-0 h-14 bg-nf-surface border-b border-nf-secondary z-40">
        <div className="max-w-4xl mx-auto h-full flex items-center justify-between px-4">
          <Link href={`/posts/${id}`} className="flex items-center gap-2 text-nf-muted hover:text-nf-white">
            <X className="h-5 w-5" />
            <span>Cancel</span>
          </Link>
          <h1 className="font-heading font-semibold text-nf-white">Edit Post</h1>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              className="border-nf-secondary"
              onClick={() => handleSubmit("draft")}
              disabled={saving}
            >
              {saving ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
              Save Draft
            </Button>
            <Button
              size="sm"
              className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90"
              onClick={() => handleSubmit("published")}
              disabled={saving}
            >
              {saving ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
              Update
            </Button>
          </div>
        </div>
      </div>

      {/* Form Content */}
      <main className="pt-[124px] pb-12 max-w-4xl mx-auto px-4">
        <div className="space-y-8">
          {/* Post Type */}
          <div>
            <label className="block text-sm font-medium text-nf-white mb-2">Post Type</label>
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
              Title <span className="text-nf-error">*</span>
            </label>
            <Input
              placeholder="Enter post title"
              className="bg-nf-surface border-nf-secondary"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            />
          </div>

          {/* Content */}
          <div>
            <label className="block text-sm font-medium text-nf-white mb-2">
              Content <span className="text-nf-error">*</span>
            </label>
            <Textarea
              placeholder="Post content (supports Markdown)"
              className="bg-nf-surface border-nf-secondary min-h-[300px] font-mono"
              value={formData.content}
              onChange={(e) => setFormData({ ...formData, content: e.target.value })}
            />
          </div>

          {/* Tags */}
          <div>
            <label className="block text-sm font-medium text-nf-white mb-2">Tags</label>
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
                placeholder="Add a tag"
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
            <h2 className="font-heading text-lg font-semibold text-nf-white mb-4">Attachments</h2>

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
              <p className="text-nf-muted">Drag files here or click to upload</p>
              <p className="text-xs text-nf-muted mt-1">Supports PDF, ZIP, images, max 10MB</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
