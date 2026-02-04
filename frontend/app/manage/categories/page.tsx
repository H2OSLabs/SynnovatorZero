'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { getCategories, Category } from '@/lib/api-client'
import { Button } from '@/components/ui/button'

export default function ManageCategories() {
  const [categories, setCategories] = useState<Category[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    async function fetchCategories() {
      try {
        const result = await getCategories(0, 100)
        setCategories(result.items)
      } catch (error) {
        console.error('Failed to fetch categories:', error)
      } finally {
        setIsLoading(false)
      }
    }
    fetchCategories()
  }, [])

  const getStatusBadge = (status: Category['status']) => {
    const styles = {
      draft: 'bg-nf-muted/20 text-nf-muted',
      published: 'bg-nf-lime/20 text-nf-lime',
      closed: 'bg-nf-error/20 text-nf-error',
    }
    const labels = {
      draft: '草稿',
      published: '已发布',
      closed: '已结束',
    }
    return (
      <span className={`px-2 py-1 rounded text-xs ${styles[status]}`}>
        {labels[status]}
      </span>
    )
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-pulse text-nf-muted">加载中...</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-heading font-bold text-nf-white">
            活动管理
          </h1>
          <p className="text-nf-muted mt-1">
            管理你创建的活动和黑客马拉松
          </p>
        </div>
        <Link href="/events/create">
          <Button className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
            创建活动
          </Button>
        </Link>
      </div>

      {/* Categories Table */}
      <div className="bg-nf-secondary rounded-lg border border-nf-dark-bg overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-nf-dark-bg">
              <th className="text-left p-4 text-sm font-medium text-nf-muted">活动名称</th>
              <th className="text-left p-4 text-sm font-medium text-nf-muted">类型</th>
              <th className="text-left p-4 text-sm font-medium text-nf-muted">状态</th>
              <th className="text-left p-4 text-sm font-medium text-nf-muted">参与人数</th>
              <th className="text-right p-4 text-sm font-medium text-nf-muted">操作</th>
            </tr>
          </thead>
          <tbody>
            {categories.length === 0 ? (
              <tr>
                <td colSpan={5} className="p-8 text-center text-nf-muted">
                  暂无活动。
                  <Link href="/events/create" className="text-nf-lime hover:underline ml-1">
                    创建第一个活动
                  </Link>
                </td>
              </tr>
            ) : (
              categories.map((category) => (
                <tr key={category.id} className="border-b border-nf-dark-bg last:border-0 hover:bg-nf-dark-bg/50">
                  <td className="p-4">
                    <div className="font-medium text-nf-white">{category.name}</div>
                    <div className="text-sm text-nf-muted truncate max-w-xs">
                      {category.description}
                    </div>
                  </td>
                  <td className="p-4 text-nf-light-gray">
                    {category.type === 'competition' ? '竞赛' : '运营活动'}
                  </td>
                  <td className="p-4">{getStatusBadge(category.status)}</td>
                  <td className="p-4 text-nf-light-gray">{category.participant_count}</td>
                  <td className="p-4 text-right">
                    <Link
                      href={`/events/${category.id}`}
                      className="text-nf-lime hover:underline text-sm"
                    >
                      查看
                    </Link>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
