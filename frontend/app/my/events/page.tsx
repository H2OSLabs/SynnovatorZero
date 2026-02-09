"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { Calendar, Loader2 } from "lucide-react"
import { PageLayout } from "@/components/layout/PageLayout"
import { CategoryCard } from "@/components/cards/CategoryCard"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { getMyGroups, getEventGroups, getCategory, type Event, type Group } from "@/lib/api-client"
import { useAuth } from "@/contexts/AuthContext"

export default function MyEventsPage() {
  const { user } = useAuth()
  const [events, setEvents] = useState<Event[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [activeTab, setActiveTab] = useState("all")

  useEffect(() => {
    if (!user) return

    const fetchEvents = async () => {
      setIsLoading(true)
      try {
        // 1. Get user's groups
        const groupsResp = await getMyGroups(0, 100, "accepted")
        const myGroups: Group[] = groupsResp.items

        // 2. For each group, get events they're registered for
        const eventIds = new Set<number>()
        for (const group of myGroups) {
          try {
            const eventGroups = await getEventGroups(group.id)
            // Note: getEventGroups returns event_id, not event
            for (const eg of eventGroups) {
              if (eg.event_id) eventIds.add(eg.event_id)
            }
          } catch {
            // Group might not be registered to any event
          }
        }

        // 3. Fetch event details
        const eventsList: Event[] = []
        for (const eventId of eventIds) {
          try {
            const event = await getCategory(eventId)
            eventsList.push(event)
          } catch {
            // Event might not exist
          }
        }

        setEvents(eventsList)
      } catch {
        setEvents([])
      } finally {
        setIsLoading(false)
      }
    }
    fetchEvents()
  }, [user])

  const filteredEvents = events.filter((event) => {
    if (activeTab === "ongoing") return event.status === "published"
    if (activeTab === "ended") return event.status === "closed"
    if (activeTab === "draft") return event.status === "draft"
    return true
  })

  if (!user) {
    return (
      <PageLayout variant="compact">
        <div className="text-center py-16">
          <Calendar className="h-16 w-16 text-nf-muted mx-auto mb-4" />
          <h1 className="text-xl font-semibold text-nf-white mb-2">请先登录</h1>
          <p className="text-nf-muted mb-6">登录后查看您参与的活动</p>
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
            我参与的活动
          </h1>
          <p className="text-nf-muted">查看您通过团队报名的所有活动</p>
        </div>
        <Link href="/events">
          <Button variant="outline" className="border-nf-secondary">
            浏览更多活动
          </Button>
        </Link>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="bg-nf-surface border-nf-secondary mb-6">
          <TabsTrigger value="all">全部 ({events.length})</TabsTrigger>
          <TabsTrigger value="ongoing">
            进行中 ({events.filter((e) => e.status === "published").length})
          </TabsTrigger>
          <TabsTrigger value="ended">
            已结束 ({events.filter((e) => e.status === "closed").length})
          </TabsTrigger>
        </TabsList>

        <TabsContent value={activeTab}>
          {isLoading ? (
            <div className="flex items-center justify-center py-16">
              <Loader2 className="h-8 w-8 animate-spin text-nf-lime" />
            </div>
          ) : filteredEvents.length === 0 ? (
            <div className="text-center py-16">
              <Calendar className="h-16 w-16 text-nf-muted mx-auto mb-4" />
              <p className="text-nf-muted mb-4">暂无参与的活动</p>
              <Link href="/events">
                <Button className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
                  浏览活动
                </Button>
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredEvents.map((event) => (
                <CategoryCard
                  key={event.id}
                  id={event.id}
                  name={event.name}
                  description={event.description}
                  type={event.type}
                  status={event.status}
                  tags={event.tags ?? []}
                  cover_image={event.cover_image ?? undefined}
                  start_date={event.start_date ?? undefined}
                  end_date={event.end_date ?? undefined}
                  participant_count={event.participant_count ?? 0}
                />
              ))}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </PageLayout>
  )
}
