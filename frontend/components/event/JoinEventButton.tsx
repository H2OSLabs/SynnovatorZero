"use client"

import { useState, useEffect } from "react"
import { UserPlus, Check, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  getMyGroups,
  getEventGroups,
  registerGroupToEvent,
  type Group,
  type EventGroup,
} from "@/lib/api-client"
import { useAuth } from "@/contexts/AuthContext"
import { toast } from "sonner"

interface JoinEventButtonProps {
  eventId: number
  onJoined?: () => void
  className?: string
}

export function JoinEventButton({ eventId, onJoined, className }: JoinEventButtonProps) {
  const { user } = useAuth()
  const [open, setOpen] = useState(false)
  const [myGroups, setMyGroups] = useState<Group[]>([])
  const [registeredGroupIds, setRegisteredGroupIds] = useState<Set<number>>(new Set())
  const [selectedGroupId, setSelectedGroupId] = useState<string>("")
  const [isLoading, setIsLoading] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)

  useEffect(() => {
    if (!open || !user) return

    const fetchData = async () => {
      setIsLoading(true)
      try {
        // Fetch user's groups (accepted membership only)
        const groupsResp = await getMyGroups(0, 100, "accepted")
        setMyGroups(groupsResp.items)

        // Fetch already registered groups for this event
        const eventGroups = await getEventGroups(eventId)
        setRegisteredGroupIds(new Set(eventGroups.map((eg: EventGroup) => eg.group_id)))
      } catch {
        setMyGroups([])
        setRegisteredGroupIds(new Set())
      } finally {
        setIsLoading(false)
      }
    }
    fetchData()
  }, [open, user, eventId])

  // Filter out already registered groups
  const availableGroups = myGroups.filter((g) => !registeredGroupIds.has(g.id))

  const handleJoin = async () => {
    if (!selectedGroupId) return
    const groupId = Number(selectedGroupId)

    setIsSubmitting(true)
    try {
      await registerGroupToEvent(eventId, groupId)
      toast.success("报名成功")
      setOpen(false)
      setSelectedGroupId("")
      onJoined?.()
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "报名失败")
    } finally {
      setIsSubmitting(false)
    }
  }

  // Check if all user's groups are already registered
  const allGroupsRegistered = myGroups.length > 0 && availableGroups.length === 0

  if (!user) {
    return (
      <Button className={className} disabled>
        <UserPlus className="h-4 w-4 mr-2" />
        登录后报名
      </Button>
    )
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button className={`bg-nf-lime text-nf-near-black hover:bg-nf-lime/90 ${className}`}>
          <UserPlus className="h-4 w-4 mr-2" />
          报名参加
        </Button>
      </DialogTrigger>
      <DialogContent className="bg-nf-surface border-nf-secondary">
        <DialogHeader>
          <DialogTitle className="text-nf-white">报名参加活动</DialogTitle>
          <DialogDescription className="text-nf-muted">
            选择一个团队来报名参加此活动
          </DialogDescription>
        </DialogHeader>

        {isLoading ? (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="h-6 w-6 animate-spin text-nf-lime" />
          </div>
        ) : myGroups.length === 0 ? (
          <div className="text-center py-6">
            <p className="text-nf-muted mb-4">你还没有加入任何团队</p>
            <Button
              variant="outline"
              className="border-nf-secondary"
              onClick={() => {
                setOpen(false)
                window.location.href = "/groups/create"
              }}
            >
              创建团队
            </Button>
          </div>
        ) : allGroupsRegistered ? (
          <div className="text-center py-6">
            <Check className="h-12 w-12 text-nf-lime mx-auto mb-4" />
            <p className="text-nf-white font-medium mb-2">已全部报名</p>
            <p className="text-nf-muted text-sm">你的所有团队都已报名此活动</p>
          </div>
        ) : (
          <div className="space-y-4">
            <div>
              <label className="text-sm text-nf-muted mb-2 block">选择团队</label>
              <Select value={selectedGroupId} onValueChange={setSelectedGroupId}>
                <SelectTrigger className="bg-nf-dark border-nf-secondary">
                  <SelectValue placeholder="选择要报名的团队" />
                </SelectTrigger>
                <SelectContent className="bg-nf-dark border-nf-secondary">
                  {availableGroups.map((group) => (
                    <SelectItem key={group.id} value={String(group.id)}>
                      {group.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="flex justify-end gap-2">
              <Button
                variant="outline"
                className="border-nf-secondary"
                onClick={() => setOpen(false)}
              >
                取消
              </Button>
              <Button
                className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90"
                onClick={handleJoin}
                disabled={!selectedGroupId || isSubmitting}
              >
                {isSubmitting ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  "确认报名"
                )}
              </Button>
            </div>
          </div>
        )}
      </DialogContent>
    </Dialog>
  )
}
