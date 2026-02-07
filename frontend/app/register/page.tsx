'use client'

import Link from "next/link"
import { useRouter } from "next/navigation"
import { useState, useEffect } from "react"
import { Header } from "@/components/layout/Header"
import { useAuth } from "@/contexts/AuthContext"
import { register } from "@/lib/api-client"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export default function RegisterPage() {
  const { user, login } = useAuth()
  const router = useRouter()

  // Redirect if already logged in
  useEffect(() => {
    if (user) {
      router.push('/')
    }
  }, [user, router])

  return (
    <div className="min-h-screen bg-nf-dark">
      <Header />

      <main className="pt-[60px] flex items-center justify-center min-h-screen">
        <div className="w-full max-w-md mx-4">
          <div className="bg-nf-secondary rounded-2xl p-8">
            {/* Logo */}
            <div className="text-center mb-8">
              <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-nf-lime to-nf-cyan flex items-center justify-center mx-auto mb-4">
                <span className="text-nf-near-black font-bold text-2xl">S</span>
              </div>
              <h1 className="font-heading text-2xl font-bold text-nf-white">创建账号</h1>
              <p className="text-nf-muted mt-2">加入协创者，开启你的创新之旅</p>
            </div>

            {/* Register Form */}
            <RegisterFormWithAuth onSuccess={() => router.push('/')} />

            {/* Divider */}
            <div className="relative my-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-nf-dark" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="bg-nf-secondary px-2 text-nf-muted">或</span>
              </div>
            </div>

            {/* Social Login - placeholder */}
            <div className="space-y-3">
              <button className="w-full flex items-center justify-center gap-3 h-11 rounded-lg border border-nf-dark bg-nf-dark hover:bg-nf-dark/80 transition-colors">
                <svg className="h-5 w-5" viewBox="0 0 24 24">
                  <path
                    fill="currentColor"
                    d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                  />
                  <path
                    fill="currentColor"
                    d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                  />
                  <path
                    fill="currentColor"
                    d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                  />
                  <path
                    fill="currentColor"
                    d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                  />
                </svg>
                <span className="text-nf-white">使用 Google 注册</span>
              </button>
              <button className="w-full flex items-center justify-center gap-3 h-11 rounded-lg border border-nf-dark bg-nf-dark hover:bg-nf-dark/80 transition-colors">
                <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                </svg>
                <span className="text-nf-white">使用 GitHub 注册</span>
              </button>
            </div>

            {/* Login Link */}
            <p className="text-center text-sm text-nf-muted mt-6">
              已有账号？{" "}
              <Link href="/login" className="text-nf-lime hover:underline">
                登录
              </Link>
            </p>

            {/* Terms */}
            <p className="text-center text-xs text-nf-muted mt-4">
              注册即表示你同意我们的{" "}
              <Link href="/terms" className="text-nf-lime hover:underline">
                服务条款
              </Link>{" "}
              和{" "}
              <Link href="/privacy" className="text-nf-lime hover:underline">
                隐私政策
              </Link>
            </p>
          </div>
        </div>
      </main>
    </div>
  )
}

function RegisterFormWithAuth({ onSuccess }: { onSuccess: () => void }) {
  const { login } = useAuth()
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState<'participant' | 'organizer'>('participant')
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setIsLoading(true)

    try {
      // Register the user
      await register({ username, email, password, role })
      // Then log them in
      await login(username, password)
      onSuccess()
    } catch (err) {
      setError(err instanceof Error ? err.message : '注册失败')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="p-3 rounded-md bg-nf-error/10 border border-nf-error/20 text-nf-error text-sm">
          {error}
        </div>
      )}

      <div className="space-y-2">
        <label htmlFor="username" className="text-sm font-medium text-nf-light-gray">
          用户名
        </label>
        <Input
          id="username"
          type="text"
          placeholder="输入用户名"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          className="bg-nf-near-black border-nf-dark text-nf-white placeholder:text-nf-muted focus:border-nf-lime focus:ring-nf-lime/20"
        />
      </div>

      <div className="space-y-2">
        <label htmlFor="email" className="text-sm font-medium text-nf-light-gray">
          邮箱
        </label>
        <Input
          id="email"
          type="email"
          placeholder="输入邮箱"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="bg-nf-near-black border-nf-dark text-nf-white placeholder:text-nf-muted focus:border-nf-lime focus:ring-nf-lime/20"
        />
      </div>

      <div className="space-y-2">
        <label htmlFor="password" className="text-sm font-medium text-nf-light-gray">
          密码
        </label>
        <Input
          id="password"
          type="password"
          placeholder="输入密码"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="bg-nf-near-black border-nf-dark text-nf-white placeholder:text-nf-muted focus:border-nf-lime focus:ring-nf-lime/20"
        />
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium text-nf-light-gray">
          我是
        </label>
        <div className="grid grid-cols-2 gap-3">
          <button
            type="button"
            onClick={() => setRole('participant')}
            className={`p-3 rounded-lg border text-center transition-colors ${
              role === 'participant'
                ? 'border-nf-lime bg-nf-lime/10 text-nf-lime'
                : 'border-nf-dark bg-nf-dark text-nf-muted hover:border-nf-light-gray'
            }`}
          >
            <div className="font-medium">参赛者</div>
            <div className="text-xs mt-1 opacity-70">参加活动、组队、提交作品</div>
          </button>
          <button
            type="button"
            onClick={() => setRole('organizer')}
            className={`p-3 rounded-lg border text-center transition-colors ${
              role === 'organizer'
                ? 'border-nf-lime bg-nf-lime/10 text-nf-lime'
                : 'border-nf-dark bg-nf-dark text-nf-muted hover:border-nf-light-gray'
            }`}
          >
            <div className="font-medium">组织者</div>
            <div className="text-xs mt-1 opacity-70">创建活动、审核作品</div>
          </button>
        </div>
      </div>

      <Button
        type="submit"
        className="w-full bg-nf-lime text-nf-near-black hover:bg-nf-lime/90 font-medium"
        disabled={isLoading || !username || !email || !password}
      >
        {isLoading ? '注册中...' : '注册'}
      </Button>
    </form>
  )
}
