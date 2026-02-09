"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { Bell, Check, CheckCheck, MessageCircle, Users, Star, Loader2 } from "lucide-react"
import { PageLayout } from "@/components/layout/PageLayout"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { getNotifications, markNotificationAsRead, markAllNotificationsAsRead } from "@/lib/api-client"
import { useAuth } from "@/contexts/AuthContext"
import { toast } from "sonner"

interface Notification {
  id: number
  type: string
  title?: string
  content: string
  related_url?: string
  is_read: boolean
  created_at: string
}

const TYPE_ICONS: Record<string, React.ReactNode> = {
  comment: <MessageCircle className="h-5 w-5" />,
  like: <Star className="h-5 w-5" />,
  follow: <Users className="h-5 w-5" />,
  team: <Users className="h-5 w-5" />,
  system: <Bell className="h-5 w-5" />,
}

const TYPE_COLORS: Record<string, string> = {
  comment: "text-nf-cyan",
  like: "text-nf-lime",
  follow: "text-nf-orange",
  team: "text-nf-purple",
  system: "text-nf-muted",
}

export default function NotificationsPage() {
  const { user } = useAuth()
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [activeTab, setActiveTab] = useState("all")

  useEffect(() => {
    if (!user) return

    const fetchNotifications = async () => {
      setIsLoading(true)
      try {
        const isRead = activeTab === "unread" ? false : activeTab === "read" ? true : undefined
        const resp = await getNotifications(user.user_id, 0, 100, isRead)
        setNotifications(resp.items)
      } catch {
        setNotifications([])
      } finally {
        setIsLoading(false)
      }
    }
    fetchNotifications()
  }, [user, activeTab])

  const handleMarkAsRead = async (notification: Notification) => {
    if (!user || notification.is_read) return

    try {
      await markNotificationAsRead(user.user_id, notification.id)
      setNotifications((prev) =>
        prev.map((n) => (n.id === notification.id ? { ...n, is_read: true } : n))
      )
    } catch {
      toast.error("标记失败")
    }
  }

  const handleMarkAllAsRead = async () => {
    if (!user) return

    try {
      await markAllNotificationsAsRead(user.user_id)
      setNotifications((prev) => prev.map((n) => ({ ...n, is_read: true })))
      toast.success("已全部标记为已读")
    } catch {
      toast.error("操作失败")
    }
  }

  const formatTime = (dateStr: string) => {
    const date = new Date(dateStr)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const minutes = Math.floor(diff / 60000)
    const hours = Math.floor(diff / 3600000)
    const days = Math.floor(diff / 86400000)

    if (minutes < 1) return "刚刚"
    if (minutes < 60) return `${minutes} 分钟前`
    if (hours < 24) return `${hours} 小时前`
    if (days < 7) return `${days} 天前`
    return date.toLocaleDateString("zh-CN")
  }

  const unreadCount = notifications.filter((n) => !n.is_read).length

  if (!user) {
    return (
      <PageLayout variant="compact">
        <div className="text-center py-16">
          <Bell className="h-16 w-16 text-nf-muted mx-auto mb-4" />
          <h1 className="text-xl font-semibold text-nf-white mb-2">请先登录</h1>
          <p className="text-nf-muted mb-6">登录后查看您的通知</p>
          <Link href="/login">
            <Button className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
              立即登录
            </Button>
          </Link>
        </div>
      </PageLayout>
    )
  }

  return (
    <PageLayout variant="compact">
      {/* Page Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="font-heading text-3xl font-bold text-nf-white mb-2">
            通知
            {unreadCount > 0 && (
              <Badge className="ml-3 bg-nf-lime text-nf-near-black">{unreadCount} 未读</Badge>
            )}
          </h1>
          <p className="text-nf-muted">查看系统通知和社区互动</p>
        </div>
        {unreadCount > 0 && (
          <Button
            variant="outline"
            className="border-nf-secondary"
            onClick={handleMarkAllAsRead}
          >
            <CheckCheck className="h-4 w-4 mr-2" />
            全部已读
          </Button>
        )}
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="bg-nf-surface border-nf-secondary mb-6">
          <TabsTrigger value="all">全部</TabsTrigger>
          <TabsTrigger value="unread">未读</TabsTrigger>
          <TabsTrigger value="read">已读</TabsTrigger>
        </TabsList>

        <TabsContent value={activeTab}>
          {isLoading ? (
            <div className="flex items-center justify-center py-16">
              <Loader2 className="h-8 w-8 animate-spin text-nf-lime" />
            </div>
          ) : notifications.length === 0 ? (
            <div className="text-center py-16">
              <Bell className="h-16 w-16 text-nf-muted mx-auto mb-4" />
              <p className="text-nf-muted">暂无通知</p>
            </div>
          ) : (
            <div className="space-y-3">
              {notifications.map((notification) => (
                <div
                  key={notification.id}
                  className={`flex items-start gap-4 p-4 rounded-lg transition-colors ${
                    notification.is_read
                      ? "bg-nf-surface"
                      : "bg-nf-surface/80 border border-nf-lime/20"
                  }`}
                >
                  {/* Icon */}
                  <div className={`shrink-0 ${TYPE_COLORS[notification.type] || TYPE_COLORS.system}`}>
                    {TYPE_ICONS[notification.type] || TYPE_ICONS.system}
                  </div>

                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    {notification.title && (
                      <h3 className="font-medium text-nf-white mb-1">{notification.title}</h3>
                    )}
                    <p className="text-nf-light-gray text-sm">{notification.content}</p>
                    <p className="text-nf-muted text-xs mt-2">{formatTime(notification.created_at)}</p>
                  </div>

                  {/* Actions */}
                  <div className="shrink-0 flex items-center gap-2">
                    {notification.related_url && (
                      <Link href={notification.related_url}>
                        <Button size="sm" variant="ghost" className="text-nf-muted hover:text-nf-white">
                          查看
                        </Button>
                      </Link>
                    )}
                    {!notification.is_read && (
                      <Button
                        size="sm"
                        variant="ghost"
                        className="text-nf-muted hover:text-nf-lime"
                        onClick={() => handleMarkAsRead(notification)}
                      >
                        <Check className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </PageLayout>
  )
}
