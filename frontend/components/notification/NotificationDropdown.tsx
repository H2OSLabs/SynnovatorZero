'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { toast } from 'sonner'
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
  updateGroupMemberStatus,
  approveCopyResource,
  rejectCopyResource,
  approveLinkResource,
  rejectLinkResource,
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
  friend: '🤝',
  comment: '💬',
  mention: '@',
  team_request: '📩',
  team_apply: '👋',
  team_apply_result: '📝',
  team_invite: '📨',
  team_invite_result: '📝',
  asset_copy_req: '📄',
  asset_copy_result: '📝',
  asset_link_req: '🔗',
  asset_link_result: '📝',
  like: '👍',
  bookmark: '🔖',
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
  const router = useRouter()
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

  const handleTeamApplyAction = async (notification: Notification, action: 'accepted' | 'rejected') => {
    try {
      if (!notification.related_url) return
      // Parse related_url: /users/{userId}?apply_group_id={groupId}
      // Note: new URL() requires a base for relative URLs
      const url = new URL(notification.related_url, 'http://dummy.com')
      
      const groupIdParam = url.searchParams.get('apply_group_id')
      if (!groupIdParam) {
        console.error("Missing group ID in notification URL")
        return
      }
      
      // Extract user ID from path (last segment)
      const pathParts = url.pathname.split('/')
      const applicantIdStr = pathParts[pathParts.length - 1]
      
      const groupId = parseInt(groupIdParam)
      const applicantId = parseInt(applicantIdStr)
      
      if (isNaN(groupId) || isNaN(applicantId)) {
        console.error("Invalid IDs in notification data")
        return
      }

      await updateGroupMemberStatus(groupId, applicantId, action)
      toast.success(action === 'accepted' ? '已批准加入' : '已拒绝申请')
      
      // Mark as read and refresh
      if (!notification.is_read) {
        await handleMarkAsRead(notification.id)
      }
      fetchNotifications()
    } catch (err) {
      toast.error('操作失败')
      console.error(err)
    }
  }

  const handleTeamInviteAction = async (notification: Notification, action: 'accepted' | 'rejected') => {
    try {
      if (!notification.related_url) return
      // Parse related_url: /groups/{groupId}?invite_id={groupId}
      const url = new URL(notification.related_url, 'http://dummy.com')
      
      // The group ID is in the path
      const pathParts = url.pathname.split('/')
      const groupIdStr = pathParts[pathParts.length - 1]
      const groupId = parseInt(groupIdStr)
      
      if (isNaN(groupId)) {
        console.error("Invalid Group ID in notification URL")
        return
      }
      
      // For invites, the "member" record already exists with status "invited".
      // We are the current user, so we update our own status in that group.
      await updateGroupMemberStatus(groupId, userId, action)
      
      toast.success(action === 'accepted' ? '已加入团队' : '已拒绝邀请')
      
      if (!notification.is_read) await handleMarkAsRead(notification.id)
      fetchNotifications()
    } catch (err) {
      toast.error('操作失败')
      console.error(err)
    }
  }

  const handleAssetCopyAction = async (notification: Notification, action: 'accepted' | 'rejected') => {
    try {
      if (!notification.related_url) return
      // /assets/{resource_id}?requester_id={requester_id}
      const url = new URL(notification.related_url, 'http://dummy.com')
      
      const requesterIdParam = url.searchParams.get('requester_id')
      if (!requesterIdParam) return
      
      const pathParts = url.pathname.split('/')
      const resourceIdStr = pathParts[pathParts.length - 1]
      
      const resourceId = parseInt(resourceIdStr)
      const requesterId = parseInt(requesterIdParam)
      
      if (isNaN(resourceId) || isNaN(requesterId)) return
      
      if (action === 'accepted') {
        await approveCopyResource(resourceId, requesterId)
        toast.success('已同意复制')
      } else {
        await rejectCopyResource(resourceId, requesterId)
        toast.success('已拒绝复制')
      }
      
      if (!notification.is_read) await handleMarkAsRead(notification.id)
      fetchNotifications()
    } catch (err) {
      toast.error('操作失败')
      console.error(err)
    }
  }

  const handleAssetLinkAction = async (notification: Notification, action: 'accepted' | 'rejected') => {
    try {
      if (!notification.related_url) return
      // /posts/{post_id}?link_resource_id={resource_id}
      const url = new URL(notification.related_url, 'http://dummy.com')
      
      const resourceIdParam = url.searchParams.get('link_resource_id')
      if (!resourceIdParam) return
      
      const pathParts = url.pathname.split('/')
      const postIdStr = pathParts[pathParts.length - 1]
      
      const postId = parseInt(postIdStr)
      const resourceId = parseInt(resourceIdParam)
      
      // Notification actor_id is the requester
      const requesterId = notification.actor_id 
      if (!requesterId) return 
      
      if (isNaN(postId) || isNaN(resourceId)) return
      
      if (action === 'accepted') {
        await approveLinkResource(postId, resourceId, requesterId)
        toast.success('已同意关联')
      } else {
        await rejectLinkResource(postId, resourceId, requesterId)
        toast.success('已拒绝关联')
      }
      
      if (!notification.is_read) await handleMarkAsRead(notification.id)
      fetchNotifications()
    } catch (err) {
      toast.error('操作失败')
      console.error(err)
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
                      router.push(notification.related_url)
                      setIsOpen(false)
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
                      <p className="text-sm text-nf-muted line-clamp-2">
                        {notification.content}
                      </p>
                      
                      {/* Action Buttons */}
                      {notification.type === 'team_apply' && (
                        <div className="flex gap-2 mt-2">
                          <Button 
                            size="sm" 
                            className="h-7 text-xs bg-nf-lime text-nf-black hover:bg-nf-lime/90"
                            onClick={(e) => {
                              e.stopPropagation()
                              handleTeamApplyAction(notification, 'accepted')
                            }}
                          >
                            同意
                          </Button>
                          <Button 
                            size="sm" 
                            variant="outline"
                            className="h-7 text-xs border-nf-muted text-nf-muted hover:text-nf-white hover:border-nf-white bg-transparent"
                            onClick={(e) => {
                              e.stopPropagation()
                              handleTeamApplyAction(notification, 'rejected')
                            }}
                          >
                            拒绝
                          </Button>
                        </div>
                      )}
                      
                      {notification.type === 'team_invite' && (
                        <div className="flex gap-2 mt-2">
                          <Button 
                            size="sm" 
                            className="h-7 text-xs bg-nf-lime text-nf-black hover:bg-nf-lime/90"
                            onClick={(e) => {
                              e.stopPropagation()
                              handleTeamInviteAction(notification, 'accepted')
                            }}
                          >
                            接受邀请
                          </Button>
                          <Button 
                            size="sm" 
                            variant="outline"
                            className="h-7 text-xs border-nf-muted text-nf-muted hover:text-nf-white hover:border-nf-white bg-transparent"
                            onClick={(e) => {
                              e.stopPropagation()
                              handleTeamInviteAction(notification, 'rejected')
                            }}
                          >
                            忽略
                          </Button>
                        </div>
                      )}

                      {notification.type === 'asset_copy_req' && (
                        <div className="flex gap-2 mt-2">
                          <Button 
                            size="sm" 
                            className="h-7 text-xs bg-nf-lime text-nf-black hover:bg-nf-lime/90"
                            onClick={(e) => {
                              e.stopPropagation()
                              handleAssetCopyAction(notification, 'accepted')
                            }}
                          >
                            允许复制
                          </Button>
                          <Button 
                            size="sm" 
                            variant="outline"
                            className="h-7 text-xs border-nf-muted text-nf-muted hover:text-nf-white hover:border-nf-white bg-transparent"
                            onClick={(e) => {
                              e.stopPropagation()
                              handleAssetCopyAction(notification, 'rejected')
                            }}
                          >
                            拒绝
                          </Button>
                        </div>
                      )}

                      {notification.type === 'asset_link_req' && (
                        <div className="flex gap-2 mt-2">
                          <Button 
                            size="sm" 
                            className="h-7 text-xs bg-nf-lime text-nf-black hover:bg-nf-lime/90"
                            onClick={(e) => {
                              e.stopPropagation()
                              handleAssetLinkAction(notification, 'accepted')
                            }}
                          >
                            允许关联
                          </Button>
                          <Button 
                            size="sm" 
                            variant="outline"
                            className="h-7 text-xs border-nf-muted text-nf-muted hover:text-nf-white hover:border-nf-white bg-transparent"
                            onClick={(e) => {
                              e.stopPropagation()
                              handleAssetLinkAction(notification, 'rejected')
                            }}
                          >
                            拒绝
                          </Button>
                        </div>
                      )}
                      
                      <span className="text-xs text-nf-muted/60 mt-1 block">
                        {formatTime(notification.created_at)}
                      </span>
                    </div>
                    {!notification.is_read && (
                      <div className="w-2 h-2 rounded-full bg-nf-lime flex-shrink-0 mt-2" />
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
