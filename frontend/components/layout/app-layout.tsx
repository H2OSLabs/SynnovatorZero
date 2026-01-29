"use client"

import { ReactNode } from "react"
import {
  Menu, Search, Zap, Bell, User, ChevronDown,
  Compass, Globe, Mountain,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"

interface NavItem {
  icon: typeof Compass
  label: string
  active?: boolean
}

const defaultNavItems: NavItem[] = [
  { icon: Compass, label: "探索" },
  { icon: Globe, label: "星球" },
  { icon: Mountain, label: "营地" },
]

interface AppLayoutProps {
  children: ReactNode
  sidebar?: ReactNode
  navMode?: "full" | "compact"
  activeNav?: string
  navItems?: NavItem[]
}

export function AppLayout({
  children,
  sidebar,
  navMode = "full",
  activeNav = "探索",
  navItems = defaultNavItems,
}: AppLayoutProps) {
  const items = navItems.map((item) => ({
    ...item,
    active: item.label === activeNav,
  }))

  return (
    <div className="flex flex-col h-screen bg-[var(--nf-near-black)]">
      {/* Header — h=60px per style.pen spec */}
      <header className="flex items-center justify-between h-[var(--nf-header-height)] px-6 border-b border-[var(--nf-dark-bg)] bg-[var(--nf-near-black)] shrink-0">
        <div className="flex items-center gap-4">
          <Menu className="w-6 h-6 text-[var(--nf-white)]" />
          <span className="font-heading text-[20px] font-bold text-[var(--nf-lime)]">
            协创者
          </span>
        </div>
        <div className="flex items-center gap-2 w-[400px] bg-[var(--nf-card-bg)] border border-[var(--nf-dark-bg)] rounded-[21px] px-5 py-2.5">
          <Search className="w-4 h-4 text-[var(--nf-muted)]" />
          <span className="text-sm text-[var(--nf-muted)]">搜索</span>
        </div>
        <div className="flex items-center gap-3">
          <Button className="bg-[var(--nf-lime)] text-[var(--nf-surface)] hover:bg-[var(--nf-lime)]/90 rounded-full px-[18px] py-2 gap-1.5">
            <Zap className="w-4 h-4" />
            <span className="text-sm font-medium">发布新内容</span>
          </Button>
          <Bell className="w-6 h-6 text-[var(--nf-white)]" />
          <Avatar className="w-8 h-8 bg-[var(--nf-blue)]">
            <AvatarFallback className="bg-[var(--nf-blue)]">
              <User className="w-4 h-4 text-[var(--nf-white)]" />
            </AvatarFallback>
          </Avatar>
          <ChevronDown className="w-4 h-4 text-[var(--nf-white)]" />
        </div>
      </header>

      {/* Body */}
      <div className="flex flex-1 overflow-hidden">
        {/* Navigation — 168px full / 60px compact per style.pen */}
        {navMode === "full" ? (
          <aside className="w-[var(--nf-nav-width)] bg-[var(--nf-near-black)] p-4 px-3 flex flex-col gap-1 shrink-0">
            {items.map((item) => (
              <div
                key={item.label}
                className={`flex items-center gap-2.5 px-3 py-2.5 rounded-full cursor-pointer ${
                  item.active
                    ? "bg-[var(--nf-lime)]"
                    : "hover:bg-[var(--nf-card-bg)]"
                }`}
              >
                <item.icon
                  className={`w-[18px] h-[18px] ${
                    item.active
                      ? "text-[var(--nf-surface)]"
                      : "text-[var(--nf-muted)]"
                  }`}
                />
                <span
                  className={`text-sm ${
                    item.active
                      ? "font-semibold text-[var(--nf-surface)]"
                      : "text-[var(--nf-muted)]"
                  }`}
                >
                  {item.label}
                </span>
              </div>
            ))}
          </aside>
        ) : (
          <aside className="w-[var(--nf-nav-compact-width)] bg-[var(--nf-near-black)] border-r border-[var(--nf-dark-bg)] flex flex-col items-center gap-2 pt-4 shrink-0">
            {items.map((item) => (
              <div
                key={item.label}
                className={`w-10 h-10 rounded-lg flex items-center justify-center cursor-pointer ${
                  item.active ? "bg-[var(--nf-lime)]" : ""
                }`}
              >
                <item.icon
                  className={`w-5 h-5 ${
                    item.active
                      ? "text-[var(--nf-surface)]"
                      : "text-[var(--nf-muted)]"
                  }`}
                />
              </div>
            ))}
          </aside>
        )}

        {/* Content + Optional Sidebar — gaps per style.pen */}
        <main className="flex flex-1 overflow-hidden">
          <div className="flex-1 overflow-y-auto p-6 px-8 flex flex-col gap-5">
            {children}
          </div>
          {sidebar && (
            <aside className="w-[var(--nf-sidebar-width)] overflow-y-auto p-4 pr-[var(--nf-sidebar-margin-right)] flex flex-col gap-4 shrink-0">
              {sidebar}
            </aside>
          )}
        </main>
      </div>
    </div>
  )
}
