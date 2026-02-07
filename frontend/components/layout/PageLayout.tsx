"use client"

import { useState, useEffect } from "react"
import { Header } from "./Header"
import { Sidebar } from "./Sidebar"
import { cn } from "@/lib/utils"

export type LayoutVariant = "full" | "compact" | "focus" | "landing"

interface PageLayoutProps {
  children: React.ReactNode
  variant?: LayoutVariant
  panel?: React.ReactNode
}

export function PageLayout({
  children,
  variant = "compact",
  panel,
}: PageLayoutProps) {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(variant === "compact")
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  // Update sidebar state when variant changes
  useEffect(() => {
    setSidebarCollapsed(variant === "compact")
  }, [variant])

  const showSidebar = variant !== "focus" && variant !== "landing"
  const showPanel = (variant === "full" || variant === "compact") && panel

  // Calculate main content margins based on layout
  const getMainStyles = () => {
    const base = "min-h-screen bg-nf-dark"

    if (variant === "landing" || variant === "focus") {
      return cn(base, "pt-[60px]")
    }

    const sidebarWidth = sidebarCollapsed ? "60px" : "168px"
    const panelWidth = showPanel ? "328px" : "0px"

    return cn(
      base,
      "pt-[60px]",
      `ml-[${sidebarWidth}]`,
      showPanel && `mr-[${panelWidth}]`
    )
  }

  return (
    <div className="min-h-screen bg-nf-dark">
      {/* Header */}
      <Header
        showMenuButton={showSidebar}
        onMenuClick={() => setSidebarCollapsed(!sidebarCollapsed)}
      />

      {/* Sidebar (only for full/compact variants) */}
      {showSidebar && (
        <Sidebar
          collapsed={sidebarCollapsed}
          onToggle={() => setSidebarCollapsed(!sidebarCollapsed)}
        />
      )}

      {/* Main Content */}
      <main
        className={cn(
          "min-h-screen bg-nf-dark pt-[60px] transition-all duration-300",
          variant === "landing" && "flex flex-col items-center",
          variant === "focus" && "max-w-4xl mx-auto px-4",
          showSidebar && (sidebarCollapsed ? "ml-[60px]" : "ml-[168px]"),
          showPanel && "mr-[328px]"
        )}
      >
        <div
          className={cn(
            "p-8",
            variant === "landing" && "max-w-6xl w-full",
            variant === "focus" && "py-8"
          )}
        >
          {children}
        </div>
      </main>

      {/* Panel (only for full/compact variants when panel content provided) */}
      {showPanel && panel}
    </div>
  )
}
