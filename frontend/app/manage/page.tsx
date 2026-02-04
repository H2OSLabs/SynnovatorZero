'use client'

import { useAuth } from '@/contexts/AuthContext'
import Link from 'next/link'

export default function ManageDashboard() {
  const { user } = useAuth()

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-heading font-bold text-nf-white">
          欢迎回来，{user?.username}
        </h1>
        <p className="text-nf-muted mt-1">
          你的角色：{user?.role === 'organizer' ? '组织者' : '管理员'}
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-nf-secondary rounded-lg p-4 border border-nf-dark-bg">
          <div className="text-nf-muted text-sm">我创建的活动</div>
          <div className="text-2xl font-bold text-nf-white mt-1">-</div>
        </div>
        <div className="bg-nf-secondary rounded-lg p-4 border border-nf-dark-bg">
          <div className="text-nf-muted text-sm">待审核作品</div>
          <div className="text-2xl font-bold text-nf-white mt-1">-</div>
        </div>
        <div className="bg-nf-secondary rounded-lg p-4 border border-nf-dark-bg">
          <div className="text-nf-muted text-sm">参与团队</div>
          <div className="text-2xl font-bold text-nf-white mt-1">-</div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-nf-secondary rounded-lg p-6 border border-nf-dark-bg">
        <h2 className="text-lg font-heading font-bold text-nf-white mb-4">
          快速操作
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Link
            href="/manage/categories"
            className="flex items-center gap-3 p-4 rounded-lg border border-nf-dark-bg hover:border-nf-lime transition-colors"
          >
            <span className="text-2xl">🎯</span>
            <div>
              <div className="font-medium text-nf-white">管理活动</div>
              <div className="text-sm text-nf-muted">查看和编辑你创建的活动</div>
            </div>
          </Link>
          <Link
            href="/events/create"
            className="flex items-center gap-3 p-4 rounded-lg border border-nf-dark-bg hover:border-nf-lime transition-colors"
          >
            <span className="text-2xl">➕</span>
            <div>
              <div className="font-medium text-nf-white">创建活动</div>
              <div className="text-sm text-nf-muted">发起新的黑客马拉松或活动</div>
            </div>
          </Link>
        </div>
      </div>
    </div>
  )
}
