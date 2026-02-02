'use client'

import * as React from 'react'
import { UsersIcon, FolderIcon, FileTextIcon, TrendingUpIcon } from 'lucide-react'
import { Card, CardContent } from '@/components/ui/card'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

interface Stats {
  user_count: number
  category_count: number
  post_count: number
}

interface StatCardProps {
  icon: React.ReactNode
  label: string
  value: number
  loading?: boolean
}

function StatCard({ icon, label, value, loading }: StatCardProps) {
  return (
    <Card className="bg-nf-card-bg border-nf-dark-bg">
      <CardContent className="flex items-center gap-4 p-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-nf-dark-bg">
          {icon}
        </div>
        <div>
          <p className="text-sm text-nf-muted">{label}</p>
          {loading ? (
            <div className="h-8 w-16 animate-pulse rounded bg-nf-dark-bg" />
          ) : (
            <p className="text-2xl font-heading font-bold text-nf-white">
              {value.toLocaleString()}
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  )
}

interface PlatformStatsProps {
  /** Refresh interval in milliseconds (0 to disable) */
  refreshInterval?: number
}

export function PlatformStats({ refreshInterval = 0 }: PlatformStatsProps) {
  const [stats, setStats] = React.useState<Stats | null>(null)
  const [loading, setLoading] = React.useState(true)
  const [error, setError] = React.useState<string | null>(null)

  const fetchStats = React.useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE}/stats`)
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }
      const data = await response.json()
      setStats(data)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load stats')
    } finally {
      setLoading(false)
    }
  }, [])

  React.useEffect(() => {
    fetchStats()

    if (refreshInterval > 0) {
      const interval = setInterval(fetchStats, refreshInterval)
      return () => clearInterval(interval)
    }
  }, [fetchStats, refreshInterval])

  if (error) {
    return (
      <Card className="bg-nf-card-bg border-nf-dark-bg">
        <CardContent className="p-4 text-center text-nf-error">
          <p>加载统计数据失败</p>
          <button
            onClick={fetchStats}
            className="mt-2 text-sm text-nf-lime hover:underline"
          >
            重试
          </button>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <TrendingUpIcon className="h-5 w-5 text-nf-lime" />
        <h3 className="text-lg font-heading text-nf-white">平台统计</h3>
      </div>
      <div className="grid gap-4 sm:grid-cols-3">
        <StatCard
          icon={<UsersIcon className="h-6 w-6 text-nf-lime" />}
          label="注册用户"
          value={stats?.user_count ?? 0}
          loading={loading}
        />
        <StatCard
          icon={<FolderIcon className="h-6 w-6 text-nf-lime" />}
          label="活动数量"
          value={stats?.category_count ?? 0}
          loading={loading}
        />
        <StatCard
          icon={<FileTextIcon className="h-6 w-6 text-nf-lime" />}
          label="作品数量"
          value={stats?.post_count ?? 0}
          loading={loading}
        />
      </div>
    </div>
  )
}

export default PlatformStats
