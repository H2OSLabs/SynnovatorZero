"use client"

import { X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface PanelProps {
  title?: string
  children: React.ReactNode
  onClose?: () => void
  className?: string
}

export function Panel({ title, children, onClose, className }: PanelProps) {
  return (
    <aside
      className={cn(
        "fixed right-0 top-[60px] bottom-0 w-[328px] bg-nf-surface border-l border-nf-secondary overflow-y-auto z-40",
        className
      )}
    >
      {title && (
        <div className="sticky top-0 bg-nf-surface border-b border-nf-secondary px-4 py-3 flex items-center justify-between">
          <h2 className="text-sm font-medium text-nf-muted">{title}</h2>
          {onClose && (
            <Button
              variant="ghost"
              size="icon"
              onClick={onClose}
              className="h-6 w-6 text-nf-muted hover:text-nf-white"
            >
              <X className="h-4 w-4" />
            </Button>
          )}
        </div>
      )}
      <div className="p-4">{children}</div>
    </aside>
  )
}

interface PanelSectionProps {
  title?: string
  children: React.ReactNode
  className?: string
}

export function PanelSection({ title, children, className }: PanelSectionProps) {
  return (
    <div className={cn("mb-6", className)}>
      {title && (
        <h3 className="text-sm font-medium text-nf-muted mb-3">{title}</h3>
      )}
      {children}
    </div>
  )
}

interface PanelCardProps {
  children: React.ReactNode
  className?: string
}

export function PanelCard({ children, className }: PanelCardProps) {
  return (
    <div className={cn("bg-nf-dark rounded-xl p-4", className)}>
      {children}
    </div>
  )
}
