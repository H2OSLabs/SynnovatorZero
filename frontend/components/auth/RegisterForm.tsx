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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { createUser } from '@/lib/api-client'

interface RegisterFormProps {
  onSuccess?: (user: { id: number; username: string; email: string; role: string }) => void
  onLoginClick?: () => void
}

export function RegisterForm({ onSuccess, onLoginClick }: RegisterFormProps) {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [role, setRole] = useState<'participant' | 'organizer'>('participant')
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setIsLoading(true)

    try {
      const result = await createUser({ username, email, role })
      onSuccess?.(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card className="w-full max-w-md bg-nf-card-bg border-nf-dark-bg">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl font-heading text-nf-white">
          注册
        </CardTitle>
        <CardDescription className="text-nf-muted">
          创建你的协创者账号
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
              htmlFor="email"
              className="text-sm font-medium text-nf-light-gray"
            >
              邮箱
            </label>
            <Input
              id="email"
              type="email"
              placeholder="输入邮箱地址"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="bg-nf-near-black border-nf-dark-bg text-nf-white placeholder:text-nf-muted focus:border-nf-lime focus:ring-nf-lime/20"
            />
          </div>
          <div className="space-y-2">
            <label
              htmlFor="role"
              className="text-sm font-medium text-nf-light-gray"
            >
              身份
            </label>
            <Select value={role} onValueChange={(v) => setRole(v as typeof role)}>
              <SelectTrigger className="bg-nf-near-black border-nf-dark-bg text-nf-white">
                <SelectValue placeholder="选择身份" />
              </SelectTrigger>
              <SelectContent className="bg-nf-card-bg border-nf-dark-bg">
                <SelectItem value="participant" className="text-nf-white hover:bg-nf-dark-bg">
                  参赛者
                </SelectItem>
                <SelectItem value="organizer" className="text-nf-white hover:bg-nf-dark-bg">
                  组织者
                </SelectItem>
              </SelectContent>
            </Select>
            <p className="text-xs text-nf-muted">
              参赛者可参加比赛和提交作品，组织者可创建和管理活动
            </p>
          </div>
        </CardContent>
        <CardFooter className="flex flex-col space-y-3">
          <Button
            type="submit"
            className="w-full bg-nf-lime text-nf-near-black hover:bg-nf-lime/90 font-medium"
            disabled={isLoading || !username || !email}
          >
            {isLoading ? '注册中...' : '注册'}
          </Button>
          {onLoginClick && (
            <Button
              type="button"
              variant="ghost"
              className="w-full text-nf-muted hover:text-nf-white hover:bg-nf-dark-bg"
              onClick={onLoginClick}
            >
              已有账号？立即登录
            </Button>
          )}
        </CardFooter>
      </form>
    </Card>
  )
}
