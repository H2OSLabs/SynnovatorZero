import { DEFAULT_POST_TYPE, getPostTypeIcon, getPostTypeLabel, isPostType, POST_TYPE_OPTIONS } from '@/lib/post-type'

describe('post-type', () => {
  test('isPostType recognizes all configured values', () => {
    for (const option of POST_TYPE_OPTIONS) {
      expect(isPostType(option.value)).toBe(true)
    }
    expect(isPostType('not-a-type')).toBe(false)
  })

  test('label/icon fallback is stable', () => {
    expect(getPostTypeLabel('not-a-type')).toBe(getPostTypeLabel(DEFAULT_POST_TYPE))
    expect(getPostTypeIcon('not-a-type')).toBe(getPostTypeIcon(DEFAULT_POST_TYPE))
  })
})

