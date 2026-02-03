'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Separator } from '@/components/ui/separator'
import {
  getNotifications,
  getUnreadCount,
  markNotificationAsRead,
  markAllNotificationsAsRead,
} from '@/lib/api-client'

interface Notification {
  id: number
  type: string
  title?: string
  content: string
  related_url?: string
  is_read: boolean
  created_at: string
}

interface NotificationDropdownProps {
  userId: number
  className?: string
}

const NOTIFICATION_ICONS: Record<string, string> = {
  follow: '👤',
  comment: '💬',
  mention: '@',
  team_request: '📩',
  award: '🏆',
  system: '📢',
}

function formatTime(dateStr: string): string {
  const date = new Date(dateStr)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return '刚刚'
  if (diffMins < 60) return `${diffMins}分钟前`
  if (diffHours < 24) return `${diffHours}小时前`
  if (diffDays < 7) return `${diffDays}天前`
  return date.toLocaleDateString('zh-CN')
}

export function NotificationDropdown({ userId, className = '' }: NotificationDropdownProps) {
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [unreadCount, setUnreadCount] = useState(0)
  const [isLoading, setIsLoading] = useState(false)
  const [isOpen, setIsOpen] = useState(false)

  const fetchUnreadCount = async () => {
    try {
      const { unread_count } = await getUnreadCount(userId)
      setUnreadCount(unread_count)
    } catch (err) {
      console.error('Failed to fetch unread count:', err)
    }
  }

  const fetchNotifications = async () => {
    setIsLoading(true)
    try {
      const { items } = await getNotifications(userId, 0, 20)
      setNotifications(items)
    } catch (err) {
      console.error('Failed to fetch notifications:', err)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchUnreadCount()
    // Poll every 30 seconds
    const interval = setInterval(fetchUnreadCount, 30000)
    return () => clearInterval(interval)
  }, [userId])

  useEffect(() => {
    if (isOpen) {
      fetchNotifications()
    }
  }, [isOpen, userId])

  const handleMarkAsRead = async (notificationId: number) => {
    try {
      await markNotificationAsRead(userId, notificationId)
      setNotifications(prev =>
        prev.map(n => (n.id === notificationId ? { ...n, is_read: true } : n))
      )
      setUnreadCount(prev => Math.max(0, prev - 1))
    } catch (err) {
      console.error('Failed to mark as read:', err)
    }
  }

  const handleMarkAllAsRead = async () => {
    try {
      await markAllNotificationsAsRead(userId)
      setNotifications(prev => prev.map(n => ({ ...n, is_read: true })))
      setUnreadCount(0)
    } catch (err) {
      console.error('Failed to mark all as read:', err)
    }
  }

  return (
    <Popover open={isOpen} onOpenChange={setIsOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="ghost"
          size="icon"
          className={`relative text-nf-muted hover:text-nf-white hover:bg-nf-dark-bg ${className}`}
        >
          <span className="text-xl">🔔</span>
          {unreadCount > 0 && (
            <Badge
              className="absolute -top-1 -right-1 h-5 min-w-[20px] px-1 bg-nf-error text-nf-white text-xs"
            >
              {unreadCount > 99 ? '99+' : unreadCount}
            </Badge>
          )}
        </Button>
      </PopoverTrigger>
      <PopoverContent
        className="w-80 p-0 bg-nf-card-bg border-nf-dark-bg"
        align="end"
      >
        <div className="flex items-center justify-between px-4 py-3 border-b border-nf-dark-bg">
          <h4 className="font-medium text-nf-white">通知</h4>
          {unreadCount > 0 && (
            <Button
              variant="ghost"
              size="sm"
              onClick={handleMarkAllAsRead}
              className="text-xs text-nf-lime hover:text-nf-lime/80 hover:bg-transparent"
            >
              全部已读
            </Button>
          )}
        </div>
        <ScrollArea className="h-[400px]">
          {isLoading ? (
            <div className="flex items-center justify-center h-20 text-nf-muted">
              加载中...
            </div>
          ) : notifications.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-20 text-nf-muted">
              <span className="text-2xl mb-2">📭</span>
              <span className="text-sm">暂无通知</span>
            </div>
          ) : (
            <div className="divide-y divide-nf-dark-bg">
              {notifications.map(notification => (
                <div
                  key={notification.id}
                  className={`px-4 py-3 cursor-pointer transition-colors hover:bg-nf-dark-bg/50 ${
                    !notification.is_read ? 'bg-nf-lime/5' : ''
                  }`}
                  onClick={() => {
                    if (!notification.is_read) {
                      handleMarkAsRead(notification.id)
                    }
                    if (notification.related_url) {
                      window.location.href = notification.related_url
                    }
                  }}
                >
                  <div className="flex items-start gap-3">
                    <span className="text-lg flex-shrink-0">
                      {NOTIFICATION_ICONS[notification.type] || '📌'}
                    </span>
                    <div className="flex-1 min-w-0">
                      {notification.title && (
                        <p className="font-medium text-sm text-nf-white truncate">
                          {notification.title}
                        </p>
                      )}
                      <p className="text-sm text-nf-light-gray line-clamp-2">
                        {notification.content}
                      </p>
                      <p className="text-xs text-nf-muted mt-1">
                        {formatTime(notification.created_at)}
                      </p>
                    </div>
                    {!notification.is_read && (
                      <div className="w-2 h-2 rounded-full bg-nf-lime flex-shrink-0 mt-1.5" />
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </ScrollArea>
      </PopoverContent>
    </Popover>
  )
}
