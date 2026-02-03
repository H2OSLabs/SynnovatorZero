'use client'

import { useState, useEffect } from 'react'
import { Badge } from '@/components/ui/badge'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'
import { getCategories } from '@/lib/api-client'
import { CategoryStageView, STAGE_CONFIGS, type CategoryStage } from './CategoryStageView'

interface CategoryTrack {
  id: number
  name: string
  type: string
  stage: CategoryStage
  description?: string
  participant_count: number
}

interface CategoryTrackViewProps {
  parentCategoryId?: number
  showStageFilter?: boolean
  onCategorySelect?: (category: CategoryTrack) => void
  className?: string
}

const TYPE_LABELS: Record<string, string> = {
  competition: '比赛',
  event: '活动',
  campaign: '活动',
  program: '项目',
}

export function CategoryTrackView({
  parentCategoryId,
  showStageFilter = true,
  onCategorySelect,
  className = '',
}: CategoryTrackViewProps) {
  const [categories, setCategories] = useState<CategoryTrack[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [selectedStage, setSelectedStage] = useState<CategoryStage | 'all'>('all')

  useEffect(() => {
    const fetchCategories = async () => {
      setIsLoading(true)
      try {
        const { items } = await getCategories(0, 100)
        setCategories(items as unknown as CategoryTrack[])
      } catch (err) {
        console.error('Failed to fetch categories:', err)
      } finally {
        setIsLoading(false)
      }
    }
    fetchCategories()
  }, [parentCategoryId])

  const filteredCategories = selectedStage === 'all'
    ? categories
    : categories.filter(c => c.stage === selectedStage)

  const stageCounts = categories.reduce((acc, c) => {
    acc[c.stage] = (acc[c.stage] || 0) + 1
    return acc
  }, {} as Record<string, number>)

  if (isLoading) {
    return (
      <div className={`space-y-4 ${className}`}>
        <div className="flex gap-2 mb-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <Skeleton key={i} className="h-8 w-20 bg-nf-dark-bg" />
          ))}
        </div>
        {Array.from({ length: 3 }).map((_, i) => (
          <Skeleton key={i} className="h-24 w-full bg-nf-dark-bg" />
        ))}
      </div>
    )
  }

  return (
    <div className={className}>
      {showStageFilter && (
        <div className="flex flex-wrap gap-2 mb-4">
          <Badge
            variant={selectedStage === 'all' ? 'default' : 'outline'}
            className={`cursor-pointer ${
              selectedStage === 'all'
                ? 'bg-nf-lime text-nf-near-black'
                : 'border-nf-dark-bg text-nf-muted hover:text-nf-white'
            }`}
            onClick={() => setSelectedStage('all')}
          >
            全部 ({categories.length})
          </Badge>
          {(['registration', 'in_progress', 'judging', 'completed'] as CategoryStage[]).map(stage => {
            const config = STAGE_CONFIGS[stage]
            const count = stageCounts[stage] || 0
            return (
              <Badge
                key={stage}
                variant={selectedStage === stage ? 'default' : 'outline'}
                className={`cursor-pointer ${
                  selectedStage === stage
                    ? `${config.bgColor} ${config.color}`
                    : `border-nf-dark-bg text-nf-muted hover:${config.color}`
                }`}
                onClick={() => setSelectedStage(stage)}
              >
                {config.label} ({count})
              </Badge>
            )
          })}
        </div>
      )}

      {filteredCategories.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-12 text-nf-muted">
          <span className="text-4xl mb-3">📋</span>
          <span className="text-sm">暂无{selectedStage === 'all' ? '' : STAGE_CONFIGS[selectedStage as CategoryStage].label}活动</span>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {filteredCategories.map(category => (
            <Card
              key={category.id}
              className={`bg-nf-card-bg border-nf-dark-bg cursor-pointer transition-all hover:border-nf-lime/30 hover:shadow-lg hover:shadow-nf-lime/5 ${
                onCategorySelect ? '' : ''
              }`}
              onClick={() => onCategorySelect?.(category)}
            >
              <CardHeader className="pb-2">
                <div className="flex items-start justify-between gap-2">
                  <div className="min-w-0 flex-1">
                    <CardTitle className="text-base font-medium text-nf-white truncate">
                      {category.name}
                    </CardTitle>
                    <CardDescription className="text-nf-muted text-sm mt-1">
                      {TYPE_LABELS[category.type] || category.type}
                    </CardDescription>
                  </div>
                  <CategoryStageView stage={category.stage} variant="badge" />
                </div>
              </CardHeader>
              <CardContent>
                {category.description && (
                  <p className="text-sm text-nf-light-gray line-clamp-2 mb-3">
                    {category.description}
                  </p>
                )}
                <div className="flex items-center gap-4 text-sm text-nf-muted">
                  <span className="flex items-center gap-1">
                    <span>👥</span>
                    <span>{category.participant_count} 参与</span>
                  </span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
