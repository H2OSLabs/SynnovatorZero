"use client"

import Link from "next/link"
import { useState } from "react"
import { Search, Bell, Plus, Menu, Home, Compass, Calendar, Users, FileText, Settings } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { SearchModal } from "@/components/search/SearchModal"
import { NotificationDropdown } from "@/components/notification/NotificationDropdown"
import { useAuth } from "@/contexts/AuthContext"
import { cn } from "@/lib/utils"

interface HeaderProps {
  onMenuClick?: () => void
  showMenuButton?: boolean
}

export function Header({ onMenuClick, showMenuButton = false }: HeaderProps) {
  const [searchOpen, setSearchOpen] = useState(false)
  const { user, logout, isOrganizer, isAdmin } = useAuth()

  const handleLogout = async () => {
    await logout()
  }

  return (
    <header className="fixed top-0 left-0 right-0 z-50 h-[60px] bg-nf-surface border-b border-nf-secondary">
      <div className="flex items-center justify-between h-full px-6">
        {/* Left: Logo + Menu Button */}
        <div className="flex items-center gap-4">
          {showMenuButton && (
            <Button
              variant="ghost"
              size="icon"
              onClick={onMenuClick}
              className="text-nf-muted hover:text-nf-white"
            >
              <Menu className="h-5 w-5" />
            </Button>
          )}
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-nf-lime to-nf-cyan flex items-center justify-center">
              <span className="text-nf-near-black font-bold text-sm">S</span>
            </div>
            <span className="font-heading font-bold text-lg text-nf-white hidden sm:block">
              协创者
            </span>
          </Link>
        </div>

        {/* Center: Search Bar */}
        <div className="flex-1 max-w-md mx-4 hidden md:block">
          <Button
            variant="outline"
            className="w-full justify-start text-nf-muted bg-nf-dark border-nf-secondary hover:border-nf-lime rounded-full"
            onClick={() => setSearchOpen(true)}
          >
            <Search className="h-4 w-4 mr-2" />
            <span>搜索活动、帖子、用户...</span>
            <kbd className="ml-auto text-xs bg-nf-secondary px-2 py-0.5 rounded">⌘K</kbd>
          </Button>
        </div>

        {/* Right: Navigation + Actions */}
        <div className="flex items-center gap-2">
          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center gap-1">
            <Link href="/explore">
              <Button variant="ghost" className="text-nf-light-gray hover:text-nf-white">
                <Compass className="h-4 w-4 mr-2" />
                探索
              </Button>
            </Link>
            <Link href="/events">
              <Button variant="ghost" className="text-nf-light-gray hover:text-nf-white">
                <Calendar className="h-4 w-4 mr-2" />
                活动
              </Button>
            </Link>
            {/* Manage link for organizers/admins */}
            {(isOrganizer || isAdmin) && (
              <Link href="/manage">
                <Button variant="ghost" className="text-nf-lime hover:text-nf-lime/80">
                  <Settings className="h-4 w-4 mr-2" />
                  管理
                </Button>
              </Link>
            )}
          </nav>

          {user ? (
            <>
              {/* Search Icon (Mobile) */}
              <Button
                variant="ghost"
                size="icon"
                className="md:hidden text-nf-light-gray hover:text-nf-white"
                onClick={() => setSearchOpen(true)}
              >
                <Search className="h-5 w-5" />
              </Button>

              {/* Notification Bell */}
              <NotificationDropdown userId={user.user_id} />

              {/* Add New Button */}
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button
                    size="icon"
                    className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90 rounded-full"
                  >
                    <Plus className="h-5 w-5" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="bg-nf-secondary border-nf-dark">
                  <DropdownMenuItem asChild>
                    <Link href="/posts/create" className="flex items-center gap-2">
                      <FileText className="h-4 w-4" />
                      发布日常帖
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem asChild>
                    <Link href="/posts/create?type=proposal" className="flex items-center gap-2">
                      <FileText className="h-4 w-4" />
                      发布提案
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem asChild>
                    <Link href="/groups/create" className="flex items-center gap-2">
                      <Users className="h-4 w-4" />
                      创建团队
                    </Link>
                  </DropdownMenuItem>
                  {(isOrganizer || isAdmin) && (
                    <DropdownMenuItem asChild>
                      <Link href="/events/create" className="flex items-center gap-2">
                        <Calendar className="h-4 w-4" />
                        创建活动
                      </Link>
                    </DropdownMenuItem>
                  )}
                </DropdownMenuContent>
              </DropdownMenu>

              {/* User Avatar */}
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="relative h-9 w-9 rounded-full">
                    <Avatar className="h-9 w-9 border-2 border-nf-secondary">
                      <AvatarFallback className="bg-gradient-to-br from-nf-lime to-nf-cyan text-nf-near-black">
                        {user.username.charAt(0).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="bg-nf-secondary border-nf-dark w-48">
                  <div className="px-2 py-1.5">
                    <p className="text-sm font-medium text-nf-white">{user.username}</p>
                    <p className="text-xs text-nf-muted">
                      {user.role === 'organizer' ? '组织者' : user.role === 'admin' ? '管理员' : '参赛者'}
                    </p>
                  </div>
                  <DropdownMenuSeparator className="bg-nf-dark" />
                  <DropdownMenuItem asChild>
                    <Link href={`/users/${user.user_id}`} className="flex items-center gap-2">
                      我的主页
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem asChild>
                    <Link href="/posts" className="flex items-center gap-2">
                      我的帖子
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem asChild>
                    <Link href="/groups" className="flex items-center gap-2">
                      我的团队
                    </Link>
                  </DropdownMenuItem>
                  {(isOrganizer || isAdmin) && (
                    <>
                      <DropdownMenuSeparator className="bg-nf-dark" />
                      <DropdownMenuItem asChild>
                        <Link href="/manage" className="flex items-center gap-2 text-nf-lime">
                          <Settings className="h-4 w-4" />
                          管理中心
                        </Link>
                      </DropdownMenuItem>
                    </>
                  )}
                  <DropdownMenuSeparator className="bg-nf-dark" />
                  <DropdownMenuItem asChild>
                    <Link href="/settings" className="flex items-center gap-2">
                      设置
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuSeparator className="bg-nf-dark" />
                  <DropdownMenuItem
                    className="text-nf-error cursor-pointer"
                    onClick={handleLogout}
                  >
                    退出登录
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </>
          ) : (
            <>
              <Link href="/login">
                <Button variant="ghost" className="text-nf-white">
                  登录
                </Button>
              </Link>
              <Link href="/register">
                <Button className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
                  注册
                </Button>
              </Link>
            </>
          )}
        </div>
      </div>

      {/* Search Modal */}
      <SearchModal defaultOpen={searchOpen} onOpenChange={setSearchOpen} />
    </header>
  )
}
