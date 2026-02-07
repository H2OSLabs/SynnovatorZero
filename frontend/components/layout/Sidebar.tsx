"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  Home,
  Compass,
  Calendar,
  FileText,
  Users,
  Pin,
  Edit3,
  User,
  Heart,
  UserPlus,
  Settings,
  ChevronLeft,
  ChevronRight,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { cn } from "@/lib/utils"
import { useAuth } from "@/contexts/AuthContext"

interface SidebarProps {
  collapsed?: boolean
  onToggle?: () => void
}

interface NavItem {
  label: string
  icon: React.ReactNode
  href: string
  requireAuth?: boolean
}

const mainNavItems: NavItem[] = [
  { label: "首页", icon: <Home className="h-5 w-5" />, href: "/" },
  { label: "探索", icon: <Compass className="h-5 w-5" />, href: "/explore" },
  { label: "活动", icon: <Calendar className="h-5 w-5" />, href: "/events" },
  { label: "帖子", icon: <FileText className="h-5 w-5" />, href: "/posts" },
  { label: "团队", icon: <Users className="h-5 w-5" />, href: "/groups" },
]

const myNavItems: NavItem[] = [
  { label: "我参与的活动", icon: <Pin className="h-5 w-5" />, href: "/my/events", requireAuth: true },
  { label: "我的帖子", icon: <Edit3 className="h-5 w-5" />, href: "/my/posts", requireAuth: true },
  { label: "我的团队", icon: <User className="h-5 w-5" />, href: "/my/groups", requireAuth: true },
  { label: "我的收藏", icon: <Heart className="h-5 w-5" />, href: "/my/favorites", requireAuth: true },
  { label: "关注", icon: <UserPlus className="h-5 w-5" />, href: "/my/following", requireAuth: true },
]

export function Sidebar({ collapsed = false, onToggle }: SidebarProps) {
  const pathname = usePathname() ?? ""
  const { user } = useAuth()

  const NavLink = ({ item }: { item: NavItem }) => {
    const isActive = pathname === item.href || pathname.startsWith(item.href + "/")

    if (item.requireAuth && !user) return null

    const linkContent = (
      <Link
        href={item.href}
        className={cn(
          "flex items-center gap-3 h-11 px-3 rounded-lg transition-colors",
          collapsed ? "justify-center" : "justify-start",
          isActive
            ? "bg-nf-dark text-nf-lime"
            : "text-nf-muted hover:bg-nf-dark hover:text-nf-white"
        )}
      >
        <span className={cn(isActive && "text-nf-lime")}>{item.icon}</span>
        {!collapsed && <span className="text-sm">{item.label}</span>}
      </Link>
    )

    if (collapsed) {
      return (
        <TooltipProvider delayDuration={0}>
          <Tooltip>
            <TooltipTrigger asChild>{linkContent}</TooltipTrigger>
            <TooltipContent side="right" className="bg-nf-secondary border-nf-dark">
              {item.label}
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
      )
    }

    return linkContent
  }

  return (
    <aside
      className={cn(
        "fixed left-0 top-[60px] bottom-0 bg-nf-surface border-r border-nf-secondary transition-all duration-300 z-40",
        collapsed ? "w-[60px]" : "w-[168px]"
      )}
    >
      <div className="flex flex-col h-full py-4">
        {/* Toggle Button */}
        <div className={cn("px-3 mb-4", collapsed ? "flex justify-center" : "flex justify-end")}>
          <Button
            variant="ghost"
            size="icon"
            onClick={onToggle}
            className="h-8 w-8 text-nf-muted hover:text-nf-white"
          >
            {collapsed ? (
              <ChevronRight className="h-4 w-4" />
            ) : (
              <ChevronLeft className="h-4 w-4" />
            )}
          </Button>
        </div>

        {/* Main Navigation */}
        <nav className="flex-1 px-2 space-y-1">
          {mainNavItems.map((item) => (
            <NavLink key={item.href} item={item} />
          ))}

          {/* Divider */}
          {user && (
            <>
              <div className="py-4">
                {!collapsed && (
                  <span className="px-3 text-[10px] font-medium text-nf-muted uppercase tracking-wider">
                    我的
                  </span>
                )}
                {collapsed && <div className="h-px bg-nf-secondary mx-3" />}
              </div>

              {myNavItems.map((item) => (
                <NavLink key={item.href} item={item} />
              ))}
            </>
          )}
        </nav>

        {/* Settings at bottom */}
        <div className="px-2 mt-auto">
          <NavLink item={{ label: "设置", icon: <Settings className="h-5 w-5" />, href: "/settings" }} />
        </div>
      </div>
    </aside>
  )
}
