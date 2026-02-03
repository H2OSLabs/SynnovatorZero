const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

export type PostType = 'profile' | 'team' | 'category' | 'for_category' | 'certificate' | 'general'

export type PostTypeOption = {
  value: PostType
  icon: string
  label: string
  desc: string
}

export const DEFAULT_POST_TYPE: PostType = 'general'

export const POST_TYPE_OPTIONS: PostTypeOption[] = [
  { value: 'general', icon: '📝', label: '日常', desc: '分享日常想法' },
  { value: 'for_category', icon: '💡', label: '提案', desc: '参赛作品' },
  { value: 'team', icon: '👥', label: '团队', desc: '找队友' },
  { value: 'profile', icon: '👤', label: '个人', desc: '个人简介' },
  { value: 'category', icon: '🏷️', label: '活动', desc: '活动相关内容' },
  { value: 'certificate', icon: '🏆', label: '证书', desc: '获奖/证书展示' },
]

export function isPostType(value: string): value is PostType {
  return POST_TYPE_OPTIONS.some(option => option.value === value)
}

export function getPostTypeOption(value: string): PostTypeOption {
  return POST_TYPE_OPTIONS.find(option => option.value === value) || POST_TYPE_OPTIONS[0]
}

export function getPostTypeIcon(value: string): string {
  return getPostTypeOption(value).icon
}

export function getPostTypeLabel(value: string): string {
  return getPostTypeOption(value).label
}

export type PostTypesMeta = {
  items: PostType[]
  default: PostType
}

export async function fetchPostTypesMeta(): Promise<PostTypesMeta> {
  const response = await fetch(`${API_BASE}/meta/post-types`, { cache: 'no-store' })
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`)
  }
  return response.json()
}

