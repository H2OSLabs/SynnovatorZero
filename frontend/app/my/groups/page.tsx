"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { Users, Plus, Loader2 } from "lucide-react"
import { PageLayout } from "@/components/layout/PageLayout"
import { GroupCard } from "@/components/cards/GroupCard"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { getMyGroups, type Group } from "@/lib/api-client"
import { useAuth } from "@/contexts/AuthContext"

export default function MyGroupsPage() {
  const { user } = useAuth()
  const [groups, setGroups] = useState<Group[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [activeTab, setActiveTab] = useState("all")

  useEffect(() => {
    if (!user) return

    const fetchGroups = async () => {
      setIsLoading(true)
      try {
        // getMyGroups returns groups where user is a member with accepted status
        const resp = await getMyGroups(0, 100, "accepted")
        setGroups(resp.items)
      } catch {
        setGroups([])
      } finally {
        setIsLoading(false)
      }
    }
    fetchGroups()
  }, [user])

  // Filter by visibility (as a proxy for different views)
  const filteredGroups = groups.filter((group) => {
    if (activeTab === "public") return group.visibility === "public"
    if (activeTab === "private") return group.visibility === "private"
    return true
  })

  if (!user) {
    return (
      <PageLayout variant="compact">
        <div className="text-center py-16">
          <Users className="h-16 w-16 text-nf-muted mx-auto mb-4" />
          <h1 className="text-xl font-semibold text-nf-white mb-2">请先登录</h1>
          <p className="text-nf-muted mb-6">登录后查看您的团队</p>
          <Link href="/login">
            <Button className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
              立即登录
            </Button>
          </Link>
        </div>
      </PageLayout>
    )
  }

  return (
    <PageLayout variant="compact">
      {/* Page Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="font-heading text-3xl font-bold text-nf-white mb-2">
            我的团队
          </h1>
          <p className="text-nf-muted">管理您加入的团队</p>
        </div>
        <Link href="/groups/create">
          <Button className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
            <Plus className="h-4 w-4 mr-2" />
            创建团队
          </Button>
        </Link>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="bg-nf-surface border-nf-secondary mb-6">
          <TabsTrigger value="all">全部 ({groups.length})</TabsTrigger>
          <TabsTrigger value="public">
            公开团队 ({groups.filter((g) => g.visibility === "public").length})
          </TabsTrigger>
          <TabsTrigger value="private">
            私密团队 ({groups.filter((g) => g.visibility === "private").length})
          </TabsTrigger>
        </TabsList>

        <TabsContent value={activeTab}>
          {isLoading ? (
            <div className="flex items-center justify-center py-16">
              <Loader2 className="h-8 w-8 animate-spin text-nf-lime" />
            </div>
          ) : filteredGroups.length === 0 ? (
            <div className="text-center py-16">
              <Users className="h-16 w-16 text-nf-muted mx-auto mb-4" />
              <p className="text-nf-muted mb-4">暂无团队</p>
              <Link href="/groups/create">
                <Button className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
                  创建第一个团队
                </Button>
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredGroups.map((group) => (
                <GroupCard
                  key={group.id}
                  id={group.id}
                  name={group.name}
                  visibility={group.visibility}
                  description={group.description ?? undefined}
                />
              ))}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </PageLayout>
  )
}
