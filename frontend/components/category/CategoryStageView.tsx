'use client'

import { Badge } from '@/components/ui/badge'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

type CategoryStage = 'draft' | 'registration' | 'in_progress' | 'judging' | 'completed' | 'cancelled'

interface StageConfig {
  label: string
  description: string
  color: string
  bgColor: string
  borderColor: string
}

const STAGE_CONFIGS: Record<CategoryStage, StageConfig> = {
  draft: {
    label: '草稿',
    description: '活动正在准备中，尚未对外开放',
    color: 'text-nf-muted',
    bgColor: 'bg-nf-muted/10',
    borderColor: 'border-nf-muted/20',
  },
  registration: {
    label: '报名中',
    description: '活动已开放报名，欢迎参与',
    color: 'text-nf-lime',
    bgColor: 'bg-nf-lime/10',
    borderColor: 'border-nf-lime/20',
  },
  in_progress: {
    label: '进行中',
    description: '活动正在进行，参赛者可提交作品',
    color: 'text-nf-cyan',
    bgColor: 'bg-nf-cyan/10',
    borderColor: 'border-nf-cyan/20',
  },
  judging: {
    label: '评审中',
    description: '作品提交已截止，评委正在评审',
    color: 'text-nf-warning',
    bgColor: 'bg-nf-warning/10',
    borderColor: 'border-nf-warning/20',
  },
  completed: {
    label: '已结束',
    description: '活动已圆满结束',
    color: 'text-nf-success',
    bgColor: 'bg-nf-success/10',
    borderColor: 'border-nf-success/20',
  },
  cancelled: {
    label: '已取消',
    description: '活动已取消',
    color: 'text-nf-error',
    bgColor: 'bg-nf-error/10',
    borderColor: 'border-nf-error/20',
  },
}

const STAGE_ORDER: CategoryStage[] = [
  'draft',
  'registration',
  'in_progress',
  'judging',
  'completed',
]

interface CategoryStageViewProps {
  stage: CategoryStage
  showTimeline?: boolean
  showDescription?: boolean
  variant?: 'badge' | 'card' | 'timeline'
  className?: string
}

function StageBadge({ stage }: { stage: CategoryStage }) {
  const config = STAGE_CONFIGS[stage]
  return (
    <Badge
      variant="outline"
      className={`${config.color} ${config.bgColor} ${config.borderColor} font-medium`}
    >
      {config.label}
    </Badge>
  )
}

function StageTimeline({ currentStage }: { currentStage: CategoryStage }) {
  const currentIndex = STAGE_ORDER.indexOf(currentStage)

  return (
    <div className="flex items-center space-x-2">
      {STAGE_ORDER.filter(s => s !== 'cancelled').map((stage, index) => {
        const config = STAGE_CONFIGS[stage]
        const isCurrent = stage === currentStage
        const isPast = currentIndex > index
        const isFuture = currentIndex < index

        return (
          <div key={stage} className="flex items-center">
            <div
              className={`flex items-center justify-center w-8 h-8 rounded-full text-xs font-medium transition-all ${
                isCurrent
                  ? `${config.bgColor} ${config.color} ${config.borderColor} border-2`
                  : isPast
                  ? 'bg-nf-success/20 text-nf-success border border-nf-success/30'
                  : 'bg-nf-dark-bg text-nf-muted border border-nf-dark-bg'
              }`}
            >
              {isPast ? '✓' : index + 1}
            </div>
            {index < STAGE_ORDER.length - 1 && (
              <div
                className={`w-8 h-0.5 mx-1 ${
                  isPast ? 'bg-nf-success/30' : 'bg-nf-dark-bg'
                }`}
              />
            )}
          </div>
        )
      })}
    </div>
  )
}

export function CategoryStageView({
  stage,
  showTimeline = false,
  showDescription = true,
  variant = 'badge',
  className = '',
}: CategoryStageViewProps) {
  const config = STAGE_CONFIGS[stage]

  if (variant === 'badge') {
    return (
      <div className={className}>
        <StageBadge stage={stage} />
      </div>
    )
  }

  if (variant === 'timeline') {
    return (
      <div className={`space-y-2 ${className}`}>
        <StageTimeline currentStage={stage} />
        {showDescription && (
          <p className={`text-sm ${config.color}`}>{config.description}</p>
        )}
      </div>
    )
  }

  // card variant
  return (
    <Card className={`bg-nf-card-bg border-nf-dark-bg ${className}`}>
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-heading text-nf-white">
            活动状态
          </CardTitle>
          <StageBadge stage={stage} />
        </div>
        {showDescription && (
          <CardDescription className={config.color}>
            {config.description}
          </CardDescription>
        )}
      </CardHeader>
      {showTimeline && (
        <CardContent>
          <StageTimeline currentStage={stage} />
        </CardContent>
      )}
    </Card>
  )
}

// Export utilities for external use
export { STAGE_CONFIGS, STAGE_ORDER, StageBadge, StageTimeline }
export type { CategoryStage, StageConfig }
