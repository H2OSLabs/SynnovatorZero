'use client'

import { RequireRole } from '@/components/auth/RequireRole'
import { Header } from '@/components/layout/Header'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

const navItems = [
  { href: '/manage', label: '概览', icon: '📊' },
  { href: '/manage/events', label: '活动管理', icon: '🎯' },
]

export default function ManageLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()

  return (
    <RequireRole roles={['organizer', 'admin']}>
      <div className="min-h-screen bg-nf-dark">
        <Header />

        <div className="pt-[60px] flex">
          {/* Sidebar */}
          <aside className="w-64 border-r border-nf-dark-bg min-h-[calc(100vh-60px)] bg-nf-secondary">
            <div className="p-4">
              <h2 className="text-lg font-heading font-bold text-nf-lime mb-4">
                管理中心
              </h2>
              <nav className="space-y-1">
                {navItems.map((item) => {
                  const isActive = pathname === item.href
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                        isActive
                          ? 'bg-nf-lime/10 text-nf-lime'
                          : 'text-nf-muted hover:text-nf-white hover:bg-nf-dark-bg'
                      }`}
                    >
                      <span>{item.icon}</span>
                      <span>{item.label}</span>
                    </Link>
                  )
                })}
              </nav>
            </div>
          </aside>

          {/* Main content */}
          <main className="flex-1 p-6">
            {children}
          </main>
        </div>
      </div>
    </RequireRole>
  )
}
