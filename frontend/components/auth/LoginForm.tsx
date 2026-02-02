'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { login } from '@/lib/api-client'

interface LoginFormProps {
  onSuccess?: (user: { user_id: number; username: string; role: string }) => void
  onRegisterClick?: () => void
}

export function LoginForm({ onSuccess, onRegisterClick }: LoginFormProps) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setIsLoading(true)

    try {
      const result = await login(username, password || undefined)
      onSuccess?.(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card className="w-full max-w-md bg-nf-card-bg border-nf-dark-bg">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl font-heading text-nf-white">
          登录
        </CardTitle>
        <CardDescription className="text-nf-muted">
          登录你的协创者账号
        </CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          {error && (
            <div className="p-3 rounded-md bg-nf-error/10 border border-nf-error/20 text-nf-error text-sm">
              {error}
            </div>
          )}
          <div className="space-y-2">
            <label
              htmlFor="username"
              className="text-sm font-medium text-nf-light-gray"
            >
              用户名
            </label>
            <Input
              id="username"
              type="text"
              placeholder="输入用户名"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="bg-nf-near-black border-nf-dark-bg text-nf-white placeholder:text-nf-muted focus:border-nf-lime focus:ring-nf-lime/20"
            />
          </div>
          <div className="space-y-2">
            <label
              htmlFor="password"
              className="text-sm font-medium text-nf-light-gray"
            >
              密码
            </label>
            <Input
              id="password"
              type="password"
              placeholder="输入密码（可选）"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="bg-nf-near-black border-nf-dark-bg text-nf-white placeholder:text-nf-muted focus:border-nf-lime focus:ring-nf-lime/20"
            />
            <p className="text-xs text-nf-muted">
              当前为测试模式，密码为可选项
            </p>
          </div>
        </CardContent>
        <CardFooter className="flex flex-col space-y-3">
          <Button
            type="submit"
            className="w-full bg-nf-lime text-nf-near-black hover:bg-nf-lime/90 font-medium"
            disabled={isLoading || !username}
          >
            {isLoading ? '登录中...' : '登录'}
          </Button>
          {onRegisterClick && (
            <Button
              type="button"
              variant="ghost"
              className="w-full text-nf-muted hover:text-nf-white hover:bg-nf-dark-bg"
              onClick={onRegisterClick}
            >
              没有账号？立即注册
            </Button>
          )}
        </CardFooter>
      </form>
    </Card>
  )
}
