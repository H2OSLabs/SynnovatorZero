"use client"

import { useEffect, useMemo, useState } from "react"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import type { PostStatus } from "@/lib/api-client"

export type PostsFilterValues = {
  type?: string
  status?: PostStatus
  tags?: string[]
}

function normalizeTags(tagsText: string): string[] {
  return tagsText
    .split(",")
    .map((t) => t.trim())
    .filter(Boolean)
}

export function PostsFilterDialog({
  open,
  onOpenChange,
  value,
  onApply,
  onReset,
}: {
  open: boolean
  onOpenChange: (open: boolean) => void
  value: PostsFilterValues
  onApply: (next: PostsFilterValues) => void
  onReset: () => void
}) {
  const initialTagsText = useMemo(() => (value.tags?.length ? value.tags.join(",") : ""), [value.tags])
  const [draftType, setDraftType] = useState<string>(value.type ?? "all")
  const [draftStatus, setDraftStatus] = useState<string>(value.status ?? "all")
  const [draftTagsText, setDraftTagsText] = useState<string>(initialTagsText)

  useEffect(() => {
    if (!open) return
    setDraftType(value.type ?? "all")
    setDraftStatus(value.status ?? "all")
    setDraftTagsText(initialTagsText)
  }, [open, value.type, value.status, initialTagsText])

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="bg-nf-surface border-nf-secondary">
        <DialogHeader>
          <DialogTitle className="text-nf-white">筛选</DialogTitle>
        </DialogHeader>

        <div className="grid gap-4">
          <div className="grid gap-2">
            <div className="text-sm text-nf-muted">类型</div>
            <Select value={draftType} onValueChange={setDraftType}>
              <SelectTrigger className="w-full bg-nf-surface border-nf-secondary">
                <SelectValue placeholder="选择类型" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">全部</SelectItem>
                <SelectItem value="proposal">💡 提案</SelectItem>
                <SelectItem value="team">👥 找队友</SelectItem>
                <SelectItem value="general">📝 日常</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="grid gap-2">
            <div className="text-sm text-nf-muted">状态</div>
            <Select value={draftStatus} onValueChange={setDraftStatus}>
              <SelectTrigger className="w-full bg-nf-surface border-nf-secondary">
                <SelectValue placeholder="选择状态" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">全部</SelectItem>
                <SelectItem value="draft">草稿</SelectItem>
                <SelectItem value="pending_review">待审核</SelectItem>
                <SelectItem value="published">已发布</SelectItem>
                <SelectItem value="rejected">已拒绝</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="grid gap-2">
            <div className="text-sm text-nf-muted">标签</div>
            <Input
              value={draftTagsText}
              onChange={(e) => setDraftTagsText(e.target.value)}
              placeholder="用逗号分隔，如 AI,Web3"
              className="bg-nf-surface border-nf-secondary"
            />
          </div>
        </div>

        <DialogFooter className="mt-2">
          <Button
            variant="outline"
            className="border-nf-secondary"
            onClick={() => {
              onReset()
              onOpenChange(false)
            }}
          >
            重置
          </Button>
          <Button
            className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90"
            onClick={() => {
              onApply({
                type: draftType === "all" ? undefined : draftType,
                status: draftStatus === "all" ? undefined : (draftStatus as PostStatus),
                tags: normalizeTags(draftTagsText),
              })
              onOpenChange(false)
            }}
          >
            应用筛选
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

