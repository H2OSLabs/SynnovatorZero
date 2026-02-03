'use client'

import { useState } from 'react'
import { LoginForm, RegisterForm } from '@/components/auth'
import { UserFollowButton, FollowersList, FollowingList } from '@/components/user'
import { CategoryStageView, CategoryTrackView } from '@/components/category'
import { NotificationDropdown } from '@/components/notification'
import { SearchModal } from '@/components/search'
import { PlatformStats } from '@/components/home'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Separator } from '@/components/ui/separator'

export default function DemoPage() {
  const [currentUser, setCurrentUser] = useState<{
    user_id: number
    username: string
    role: string
  } | null>(null)

  const [showLogin, setShowLogin] = useState(true)

  const handleLoginSuccess = (user: { user_id: number; username: string; role: string }) => {
    setCurrentUser(user)
  }

  const handleRegisterSuccess = (user: { id: number; username: string; email: string; role: string }) => {
    setCurrentUser({ user_id: user.id, username: user.username, role: user.role })
  }

  return (
    <div className="min-h-screen bg-nf-near-black py-8 px-4">
      {/* Global Search Modal - triggered by ⌘K */}
      <SearchModal />

      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-heading text-nf-white">
              <span className="text-nf-lime">协创者</span> 组件演示
            </h1>
            <p className="text-nf-muted mt-1">Phase 12 前端组件预览 <kbd className="ml-2 rounded bg-nf-dark-bg px-2 py-0.5 text-xs">⌘K</kbd> 搜索</p>
          </div>
          {currentUser && (
            <div className="flex items-center gap-4">
              <NotificationDropdown userId={currentUser.user_id} />
              <span className="text-nf-light-gray">
                {currentUser.username} ({currentUser.role})
              </span>
            </div>
          )}
        </div>

        <Separator className="bg-nf-dark-bg" />

        {/* Auth Components */}
        <section>
          <h2 className="text-xl font-heading text-nf-white mb-4">认证组件</h2>
          {currentUser ? (
            <Card className="bg-nf-card-bg border-nf-dark-bg max-w-md">
              <CardHeader>
                <CardTitle className="text-nf-white">已登录</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <p className="text-nf-light-gray">用户 ID: {currentUser.user_id}</p>
                <p className="text-nf-light-gray">用户名: {currentUser.username}</p>
                <p className="text-nf-light-gray">角色: {currentUser.role}</p>
                <button
                  onClick={() => setCurrentUser(null)}
                  className="text-nf-error hover:underline text-sm mt-2"
                >
                  退出登录
                </button>
              </CardContent>
            </Card>
          ) : (
            <div className="max-w-md">
              {showLogin ? (
                <LoginForm
                  onSuccess={handleLoginSuccess}
                  onRegisterClick={() => setShowLogin(false)}
                />
              ) : (
                <RegisterForm
                  onSuccess={handleRegisterSuccess}
                  onLoginClick={() => setShowLogin(true)}
                />
              )}
            </div>
          )}
        </section>

        <Separator className="bg-nf-dark-bg" />

        {/* User Components */}
        <section>
          <h2 className="text-xl font-heading text-nf-white mb-4">用户关系组件</h2>
          <div className="grid gap-6 md:grid-cols-2">
            <Card className="bg-nf-card-bg border-nf-dark-bg">
              <CardHeader>
                <CardTitle className="text-nf-white">关注按钮</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center gap-4">
                  <span className="text-nf-light-gray">用户 1:</span>
                  <UserFollowButton
                    currentUserId={currentUser?.user_id || 1}
                    targetUserId={2}
                  />
                </div>
                <div className="flex items-center gap-4">
                  <span className="text-nf-light-gray">用户 2:</span>
                  <UserFollowButton
                    currentUserId={currentUser?.user_id || 1}
                    targetUserId={3}
                    size="sm"
                  />
                </div>
                <p className="text-xs text-nf-muted">
                  点击关注按钮测试关注/取关功能 (需要后端运行)
                </p>
              </CardContent>
            </Card>

            <Card className="bg-nf-card-bg border-nf-dark-bg">
              <CardHeader>
                <CardTitle className="text-nf-white">粉丝/关注列表</CardTitle>
              </CardHeader>
              <CardContent>
                <Tabs defaultValue="followers">
                  <TabsList className="bg-nf-dark-bg">
                    <TabsTrigger value="followers" className="data-[state=active]:bg-nf-lime data-[state=active]:text-nf-near-black">
                      粉丝
                    </TabsTrigger>
                    <TabsTrigger value="following" className="data-[state=active]:bg-nf-lime data-[state=active]:text-nf-near-black">
                      关注
                    </TabsTrigger>
                  </TabsList>
                  <TabsContent value="followers" className="mt-4">
                    <FollowersList
                      userId={currentUser?.user_id || 1}
                      currentUserId={currentUser?.user_id}
                    />
                  </TabsContent>
                  <TabsContent value="following" className="mt-4">
                    <FollowingList
                      userId={currentUser?.user_id || 1}
                      currentUserId={currentUser?.user_id}
                    />
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>
          </div>
        </section>

        <Separator className="bg-nf-dark-bg" />

        {/* Category Components */}
        <section>
          <h2 className="text-xl font-heading text-nf-white mb-4">活动阶段组件</h2>
          <div className="space-y-6">
            <Card className="bg-nf-card-bg border-nf-dark-bg">
              <CardHeader>
                <CardTitle className="text-nf-white">阶段徽章</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-3">
                  <CategoryStageView stage="draft" variant="badge" />
                  <CategoryStageView stage="registration" variant="badge" />
                  <CategoryStageView stage="in_progress" variant="badge" />
                  <CategoryStageView stage="judging" variant="badge" />
                  <CategoryStageView stage="completed" variant="badge" />
                  <CategoryStageView stage="cancelled" variant="badge" />
                </div>
              </CardContent>
            </Card>

            <Card className="bg-nf-card-bg border-nf-dark-bg">
              <CardHeader>
                <CardTitle className="text-nf-white">阶段时间线</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <p className="text-sm text-nf-muted mb-2">报名阶段:</p>
                  <CategoryStageView stage="registration" variant="timeline" />
                </div>
                <div>
                  <p className="text-sm text-nf-muted mb-2">进行中:</p>
                  <CategoryStageView stage="in_progress" variant="timeline" />
                </div>
                <div>
                  <p className="text-sm text-nf-muted mb-2">已完成:</p>
                  <CategoryStageView stage="completed" variant="timeline" />
                </div>
              </CardContent>
            </Card>

            <Card className="bg-nf-card-bg border-nf-dark-bg">
              <CardHeader>
                <CardTitle className="text-nf-white">活动卡片</CardTitle>
              </CardHeader>
              <CardContent>
                <CategoryStageView
                  stage="in_progress"
                  variant="card"
                  showTimeline={true}
                  showDescription={true}
                />
              </CardContent>
            </Card>
          </div>
        </section>

        <Separator className="bg-nf-dark-bg" />

        {/* Category Track View */}
        <section>
          <h2 className="text-xl font-heading text-nf-white mb-4">活动列表</h2>
          <CategoryTrackView
            showStageFilter={true}
            onCategorySelect={(category) => {
              alert(`选中活动: ${category.name}`)
            }}
          />
        </section>

        <Separator className="bg-nf-dark-bg" />

        {/* Platform Stats */}
        <section>
          <h2 className="text-xl font-heading text-nf-white mb-4">平台统计</h2>
          <PlatformStats />
        </section>

        {/* Footer */}
        <div className="text-center text-nf-muted text-sm pt-8">
          <p>Phase 12: 前端组件实现 - P0/P1/P2 组件完成</p>
          <p className="mt-1">使用 shadcn/ui + Neon Forge 主题</p>
        </div>
      </div>
    </div>
  )
}
