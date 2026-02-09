'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth, AuthUser } from '@/contexts/AuthContext'

interface RequireRoleProps {
  children: React.ReactNode
  roles: AuthUser['role'][]
  fallback?: React.ReactNode
  redirectTo?: string
}

/**
 * Protect pages/components based on user role.
 *
 * Usage:
 * <RequireRole roles={['organizer', 'admin']}>
 *   <OrganizerDashboard />
 * </RequireRole>
 */
export function RequireRole({
  children,
  roles,
  fallback,
  redirectTo = '/login'
}: RequireRoleProps) {
  const { user, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && !user) {
      router.push(redirectTo)
    }
  }, [user, isLoading, router, redirectTo])

  // Loading state
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-nf-dark">
        <div className="animate-pulse text-nf-muted">加载中...</div>
      </div>
    )
  }

  // Not logged in
  if (!user) {
    return null
  }

  // Check role
  if (!roles.includes(user.role)) {
    if (fallback) {
      return <>{fallback}</>
    }

    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-nf-dark">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-nf-white mb-2">无权访问</h1>
          <p className="text-nf-muted mb-4">
            此页面仅限 {roles.map(r =>
              r === 'organizer' ? '组织者' :
              r === 'admin' ? '管理员' : '参赛者'
            ).join('、')} 访问
          </p>
          <button
            onClick={() => router.push('/')}
            className="text-nf-lime hover:underline"
          >
            返回首页
          </button>
        </div>
      </div>
    )
  }

  return <>{children}</>
}

/**
 * Show content only for specific roles (inline version).
 * Does not redirect, just hides content.
 */
export function ShowForRole({
  children,
  roles
}: {
  children: React.ReactNode
  roles: AuthUser['role'][]
}) {
  const { user } = useAuth()

  if (!user || !roles.includes(user.role)) {
    return null
  }

  return <>{children}</>
}
