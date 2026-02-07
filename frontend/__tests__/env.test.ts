import { getServerEnv } from '../lib/env'

describe('env', () => {
  const originalApiUrl = process.env.API_URL
  const originalInternalApiUrl = process.env.INTERNAL_API_URL
  const originalSiteOrigin = process.env.SITE_ORIGIN
  const originalNextPublicSiteOrigin = process.env.NEXT_PUBLIC_SITE_ORIGIN

  afterEach(() => {
    process.env.API_URL = originalApiUrl
    process.env.INTERNAL_API_URL = originalInternalApiUrl
    process.env.SITE_ORIGIN = originalSiteOrigin
    process.env.NEXT_PUBLIC_SITE_ORIGIN = originalNextPublicSiteOrigin
  })

  it('当 API_URL 为相对路径时，server 侧会解析为绝对地址', () => {
    process.env.API_URL = '/api'
    delete process.env.INTERNAL_API_URL
    delete process.env.SITE_ORIGIN
    delete process.env.NEXT_PUBLIC_SITE_ORIGIN

    expect(getServerEnv().API_URL).toBe('http://localhost:8000/api')
  })

  it('当提供 INTERNAL_API_URL 时，server 侧优先使用该值', () => {
    process.env.API_URL = '/api'
    process.env.INTERNAL_API_URL = 'http://backend:8000/api'

    expect(getServerEnv().API_URL).toBe('http://backend:8000/api')
  })

  it('当提供 SITE_ORIGIN 时，server 侧使用 SITE_ORIGIN 组合相对 API_URL', () => {
    process.env.API_URL = '/api'
    process.env.SITE_ORIGIN = 'https://example.test'
    delete process.env.INTERNAL_API_URL

    expect(getServerEnv().API_URL).toBe('https://example.test/api')
  })
})

