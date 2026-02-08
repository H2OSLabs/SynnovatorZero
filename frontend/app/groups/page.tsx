"use client"

import { Suspense, useEffect, useMemo, useState } from "react"
import { Search, SlidersHorizontal, Plus } from "lucide-react"
import Link from "next/link"
import { useRouter, useSearchParams } from "next/navigation"
import { PageLayout } from "@/components/layout/PageLayout"
import { GroupCard } from "@/components/cards/GroupCard"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { getGroups, getGroupMembers, getUser, type Group } from "@/lib/api-client"

function GroupsContent() {
  const router = useRouter()
  const searchParams = useSearchParams()

  const [activeTab, setActiveTab] = useState("all")
  const [searchQuery, setSearchQuery] = useState("")
  const [groups, setGroups] = useState<Group[]>([])
  const [groupMeta, setGroupMeta] = useState<Record<number, { member_count: number; members: Array<{ id: number; username: string; display_name?: string; avatar_url?: string }> }>>({})
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Initialize search query from URL
  useEffect(() => {
    const q = searchParams?.get("q") ?? ""
    setSearchQuery(q)
  }, [searchParams])

  function updateParams(patch: { q?: string | null }) {
    const next = new URLSearchParams(searchParams?.toString() ?? "")
    if (patch.q !== undefined) {
      if (!patch.q) next.delete("q")
      else next.set("q", patch.q)
    }
    const qs = next.toString()
    router.replace(qs ? `/groups?${qs}` : "/groups")
  }

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
                    return {
                      id: u.id,
                      username: u.username,
                      display_name: u.display_name ?? undefined,
                      avatar_url: u.avatar_url ?? undefined,
                    }
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

  // Client-side search and visibility filtering
  const filteredGroups = useMemo(() => {
    const q = searchQuery.trim().toLowerCase()
    return groups.filter((group) => {
      // Visibility filter
      if (activeTab === "public" && group.visibility !== "public") return false
      if (activeTab === "private" && group.visibility !== "private") return false

      // Search filter
      if (q) {
        const inName = group.name?.toLowerCase().includes(q)
        const inDesc = group.description?.toLowerCase().includes(q)
        if (!inName && !inDesc) return false
      }

      return true
    })
  }, [groups, activeTab, searchQuery])

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
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key !== "Enter") return
              updateParams({ q: searchQuery.trim() || null })
            }}
            onBlur={() => {
              updateParams({ q: searchQuery.trim() || null })
            }}
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

export default function GroupsPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-nf-dark flex items-center justify-center text-nf-muted">加载中...</div>}>
      <GroupsContent />
    </Suspense>
  )
}
