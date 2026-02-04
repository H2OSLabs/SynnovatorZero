"use client"

import { useEffect, useState } from "react"
import { Search, SlidersHorizontal, Plus } from "lucide-react"
import Link from "next/link"
import { PageLayout } from "@/components/layout/PageLayout"
import { GroupCard } from "@/components/cards/GroupCard"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { getGroups, getGroupMembers, getUser, type Group } from "@/lib/api-client"

export default function GroupsPage() {
  const [activeTab, setActiveTab] = useState("all")
  const [groups, setGroups] = useState<Group[]>([])
  const [groupMeta, setGroupMeta] = useState<Record<number, { member_count: number; members: Array<{ id: number; username: string; display_name?: string; avatar_url?: string }> }>>({})
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true)
      setError(null)
      try {
        const resp = await getGroups(0, 100)
        setGroups(resp.items)

        const entries = await Promise.all(
          resp.items.map(async (g) => {
            try {
              const membersResp = await getGroupMembers(g.id, 0, 3, { status: "accepted" })
              const memberUsers = await Promise.all(
                membersResp.items.map(async (m) => {
                  try {
                    const u = await getUser(m.user_id)
                    return { id: u.id, username: u.username, display_name: u.display_name, avatar_url: u.avatar_url }
                  } catch {
                    return { id: m.user_id, username: `user_${m.user_id}` }
                  }
                })
              )
              return { groupId: g.id, meta: { member_count: membersResp.total, members: memberUsers } }
            } catch {
              return {
                groupId: g.id,
                meta: { member_count: 0, members: [] as Array<{ id: number; username: string; display_name?: string; avatar_url?: string }> },
              }
            }
          })
        )

        const meta: Record<number, { member_count: number; members: Array<{ id: number; username: string; display_name?: string; avatar_url?: string }> }> = {}
        for (const entry of entries) meta[entry.groupId] = entry.meta
        setGroupMeta(meta)
      } catch (e) {
        setError(e instanceof Error ? e.message : "加载失败")
        setGroups([])
        setGroupMeta({})
      } finally {
        setIsLoading(false)
      }
    }
    fetchData()
  }, [])

  const filteredGroups = groups.filter((group) => {
    if (activeTab === "all") return true
    if (activeTab === "public") return group.visibility === "public"
    if (activeTab === "private") return group.visibility === "private"
    return true
  })

  return (
    <PageLayout variant="compact">
      {/* Page Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="font-heading text-3xl font-bold text-nf-white mb-2">👥 团队</h1>
          <p className="text-nf-muted">发现优秀团队，寻找志同道合的伙伴</p>
        </div>
        <Link href="/groups/create">
          <Button className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
            <Plus className="h-4 w-4 mr-2" />
            创建团队
          </Button>
        </Link>
      </div>

      {/* Search & Filter */}
      <div className="flex gap-4 mb-6">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-nf-muted" />
          <Input
            placeholder="搜索团队..."
            className="pl-10 bg-nf-surface border-nf-secondary"
          />
        </div>
        <Button variant="outline" className="border-nf-secondary">
          <SlidersHorizontal className="h-4 w-4 mr-2" />
          筛选
        </Button>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="bg-nf-surface border-nf-secondary mb-6">
          <TabsTrigger value="all">全部</TabsTrigger>
          <TabsTrigger value="public">🌐 公开</TabsTrigger>
          <TabsTrigger value="private">🔒 私密</TabsTrigger>
        </TabsList>

        <TabsContent value={activeTab}>
          {isLoading ? (
            <div className="text-center py-16">
              <p className="text-nf-muted">加载中...</p>
            </div>
          ) : error ? (
            <div className="text-center py-16">
              <p className="text-nf-muted">{error}</p>
            </div>
          ) : filteredGroups.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredGroups.map((group) => (
                <GroupCard
                  key={group.id}
                  id={group.id}
                  name={group.name}
                  description={group.description ?? undefined}
                  visibility={group.visibility}
                  member_count={groupMeta[group.id]?.member_count ?? 0}
                  members={groupMeta[group.id]?.members ?? []}
                />
              ))}
            </div>
          ) : (
            <div className="text-center py-16">
              <p className="text-nf-muted">暂无团队</p>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </PageLayout>
  )
}
