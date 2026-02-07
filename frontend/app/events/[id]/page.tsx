"use client"

import Link from "next/link"
import { useParams } from "next/navigation"
import { useEffect, useState } from "react"
import { ArrowLeft, Calendar, FileText, UserPlus, Loader2 } from "lucide-react"
import { PageLayout } from "@/components/layout/PageLayout"
import { Panel, PanelSection, PanelCard } from "@/components/layout/Panel"
import { PostCard } from "@/components/cards/PostCard"
import { GroupCard } from "@/components/cards/GroupCard"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  getCategory,
  getEventPosts,
  getEventGroups,
  getEventRules,
  getPost,
  getGroup,
  getRule,
  getUser,
  type Event,
  type Post,
  type Group,
  type Rule,
  type User,
} from "@/lib/api-client"

interface PostWithAuthor extends Post {
  author?: User
}

interface GroupWithDetails extends Group {
  member_count?: number
}

export default function EventDetailPage() {
  const params = useParams()
  const id = params.id as string
  const eventId = Number(id)

  const [event, setEvent] = useState<Event | null>(null)
  const [posts, setPosts] = useState<PostWithAuthor[]>([])
  const [groups, setGroups] = useState<GroupWithDetails[]>([])
  const [rules, setRules] = useState<Rule[]>([])

  const [isLoading, setIsLoading] = useState(true)
  const [isLoadingPosts, setIsLoadingPosts] = useState(true)
  const [isLoadingGroups, setIsLoadingGroups] = useState(true)
  const [, setIsLoadingRules] = useState(true)

  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!Number.isFinite(eventId)) {
      setError("Invalid event ID")
      setIsLoading(false)
      return
    }

    // Fetch event details
    const fetchEvent = async () => {
      setIsLoading(true)
      setError(null)
      try {
        const data = await getCategory(eventId)
        setEvent(data)
      } catch (e) {
        setError(e instanceof Error ? e.message : "Failed to load event")
        setEvent(null)
      } finally {
        setIsLoading(false)
      }
    }

    // Fetch event posts with author details
    const fetchPosts = async () => {
      setIsLoadingPosts(true)
      try {
        const eventPosts = await getEventPosts(eventId)
        const postsWithDetails = await Promise.all(
          eventPosts.map(async (ep) => {
            try {
              const post = await getPost(ep.post_id)
              if (post.created_by) {
                try {
                  const author = await getUser(post.created_by)
                  return { ...post, author }
                } catch {
                  return post
                }
              }
              return post
            } catch {
              return null
            }
          })
        )
        setPosts(postsWithDetails.filter((p): p is PostWithAuthor => p !== null))
      } catch {
        setPosts([])
      } finally {
        setIsLoadingPosts(false)
      }
    }

    // Fetch event groups
    const fetchGroups = async () => {
      setIsLoadingGroups(true)
      try {
        const eventGroups = await getEventGroups(eventId)
        const groupsWithDetails = await Promise.all(
          eventGroups.map(async (eg) => {
            try {
              const group = await getGroup(eg.group_id)
              return group
            } catch {
              return null
            }
          })
        )
        setGroups(groupsWithDetails.filter((g): g is GroupWithDetails => g !== null))
      } catch {
        setGroups([])
      } finally {
        setIsLoadingGroups(false)
      }
    }

    // Fetch event rules
    const fetchRules = async () => {
      setIsLoadingRules(true)
      try {
        const eventRules = await getEventRules(eventId)
        const rulesWithDetails = await Promise.all(
          eventRules.map(async (er) => {
            try {
              return await getRule(er.rule_id)
            } catch {
              return null
            }
          })
        )
        setRules(rulesWithDetails.filter((r): r is Rule => r !== null))
      } catch {
        setRules([])
      } finally {
        setIsLoadingRules(false)
      }
    }

    fetchEvent()
    fetchPosts()
    fetchGroups()
    fetchRules()
  }, [eventId])

  const statusConfig = {
    published: { label: "Active", className: "bg-nf-lime text-nf-near-black" },
    draft: { label: "Draft", className: "bg-nf-orange text-nf-near-black" },
    closed: { label: "Closed", className: "bg-nf-muted text-nf-white" },
  }

  const statusInfo = statusConfig[(event?.status || "draft") as keyof typeof statusConfig]

  const startDate = event?.start_date ? new Date(event.start_date).toLocaleDateString("en-US") : null
  const endDate = event?.end_date ? new Date(event.end_date).toLocaleDateString("en-US") : null
  const dateRange = startDate && endDate ? `${startDate} - ${endDate}` : null

  if (isLoading) {
    return (
      <PageLayout variant="full">
        <div className="flex items-center justify-center min-h-[400px]">
          <Loader2 className="h-8 w-8 animate-spin text-nf-lime" />
        </div>
      </PageLayout>
    )
  }

  if (error || !event) {
    return (
      <PageLayout variant="full">
        <div className="text-center py-12">
          <p className="text-nf-error mb-4">{error || "Event not found"}</p>
          <Link href="/events">
            <Button variant="outline">Back to events</Button>
          </Link>
        </div>
      </PageLayout>
    )
  }

  const panelContent = (
    <Panel title="Event Overview">
      <PanelSection>
        <PanelCard>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-nf-muted">Status</span>
              <Badge className={statusInfo.className}>{statusInfo.label}</Badge>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-nf-muted">Participants</span>
              <span className="text-nf-white font-medium">{event.participant_count ?? 0}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-nf-muted">Submissions</span>
              <span className="text-nf-white font-medium">{posts.length}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-nf-muted">Teams</span>
              <span className="text-nf-white font-medium">{groups.length}</span>
            </div>
          </div>
        </PanelCard>
      </PanelSection>

      <PanelSection title="Important Dates">
        <PanelCard>
          <div className="space-y-3">
            <div>
              <p className="text-xs text-nf-muted">Start Date</p>
              <p className="text-nf-white">{startDate || "-"}</p>
            </div>
            <div>
              <p className="text-xs text-nf-muted">End Date</p>
              <p className="text-nf-white">{endDate || "-"}</p>
            </div>
          </div>
        </PanelCard>
      </PanelSection>

      {rules.length > 0 && (
        <PanelSection title="Rules">
          <PanelCard>
            <ul className="space-y-2 text-sm">
              {rules.map((rule) => (
                <li key={rule.id} className="flex items-center gap-2">
                  <FileText className="h-4 w-4 text-nf-muted" />
                  <span className="text-nf-white">{rule.name}</span>
                </li>
              ))}
            </ul>
          </PanelCard>
        </PanelSection>
      )}

      <Button className="w-full bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
        <UserPlus className="h-4 w-4 mr-2" />
        Join Event
      </Button>
    </Panel>
  )

  return (
    <PageLayout variant="full" panel={panelContent}>
      {/* Back Button */}
      <Link href="/events" className="inline-flex items-center gap-2 text-nf-muted hover:text-nf-white mb-6">
        <ArrowLeft className="h-4 w-4" />
        Back to events
      </Link>

      {/* Cover Image */}
      <div className="relative aspect-video bg-nf-surface rounded-xl mb-6 overflow-hidden">
        {event.cover_image ? (
          <img src={event.cover_image} alt={event.name} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-nf-secondary to-nf-dark">
            <Calendar className="h-20 w-20 text-nf-muted" />
          </div>
        )}
        <Badge className={`absolute top-4 left-4 ${statusInfo.className}`}>
          {statusInfo.label}
        </Badge>
      </div>

      {/* Title & Meta */}
      <div className="mb-6">
        <h1 className="font-heading text-3xl font-bold text-nf-white mb-2">
          {event.name}
        </h1>
        <div className="flex items-center gap-4 text-nf-muted">
          <span>Hosted by User #{event.created_by || "Unknown"}</span>
          <span>·</span>
          <span>{dateRange || "-"}</span>
        </div>
        {event.tags && event.tags.length > 0 && (
          <div className="flex gap-2 mt-4">
            {event.tags.map((tag) => (
              <Badge key={tag} variant="secondary" className="bg-nf-dark">
                {tag}
              </Badge>
            ))}
          </div>
        )}
      </div>

      {/* Tabs */}
      <Tabs defaultValue="details">
        <TabsList className="bg-nf-surface border-nf-secondary mb-6">
          <TabsTrigger value="details">Details</TabsTrigger>
          <TabsTrigger value="submissions">Submissions ({posts.length})</TabsTrigger>
          <TabsTrigger value="teams">Teams ({groups.length})</TabsTrigger>
          <TabsTrigger value="ranking">Ranking</TabsTrigger>
        </TabsList>

        <TabsContent value="details">
          <div className="prose prose-invert max-w-none">
            <div className="whitespace-pre-wrap text-nf-light-gray">
              {event.content || event.description || "No details available"}
            </div>
          </div>

          {/* Rules Section */}
          {rules.length > 0 && (
            <div className="mt-8">
              <h2 className="font-heading text-xl font-semibold text-nf-white mb-4">Event Rules</h2>
              <div className="space-y-4">
                {rules.map((rule) => (
                  <div key={rule.id} className="bg-nf-surface rounded-lg p-4">
                    <h3 className="font-medium text-nf-white mb-2">{rule.name}</h3>
                    {rule.description && (
                      <p className="text-sm text-nf-muted">{rule.description}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </TabsContent>

        <TabsContent value="submissions">
          {isLoadingPosts ? (
            <div className="flex items-center justify-center py-10">
              <Loader2 className="h-6 w-6 animate-spin text-nf-lime" />
            </div>
          ) : posts.length === 0 ? (
            <div className="text-center py-10 text-nf-muted">No submissions yet</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {posts.map((post) => (
                <PostCard
                  key={post.id}
                  id={post.id}
                  title={post.title}
                  type={post.type}
                  status={post.status}
                  tags={post.tags ?? []}
                  like_count={post.like_count}
                  comment_count={post.comment_count}
                  created_by={post.author ? {
                    id: post.author.id,
                    username: post.author.username,
                    display_name: post.author.display_name || post.author.username,
                  } : undefined}
                />
              ))}
            </div>
          )}
        </TabsContent>

        <TabsContent value="teams">
          {isLoadingGroups ? (
            <div className="flex items-center justify-center py-10">
              <Loader2 className="h-6 w-6 animate-spin text-nf-lime" />
            </div>
          ) : groups.length === 0 ? (
            <div className="text-center py-10 text-nf-muted">No teams registered</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {groups.map((group) => (
                <GroupCard
                  key={group.id}
                  id={group.id}
                  name={group.name}
                  visibility={group.visibility}
                  description={group.description || undefined}
                />
              ))}
            </div>
          )}
        </TabsContent>

        <TabsContent value="ranking">
          {isLoadingPosts ? (
            <div className="flex items-center justify-center py-10">
              <Loader2 className="h-6 w-6 animate-spin text-nf-lime" />
            </div>
          ) : posts.length === 0 ? (
            <div className="text-center py-10 text-nf-muted">No rankings available</div>
          ) : (
            <div className="space-y-4">
              {posts.map((post, index) => (
                <div key={post.id} className="flex items-center gap-4 bg-nf-surface rounded-lg p-4">
                  <div className="text-2xl font-bold text-nf-lime">#{index + 1}</div>
                  <div className="flex-1">
                    <h3 className="font-medium text-nf-white">{post.title}</h3>
                    <p className="text-sm text-nf-muted">
                      {post.author?.display_name || post.author?.username || "Unknown"}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-lg font-bold text-nf-white">
                      {post.average_rating ? `⭐ ${post.average_rating.toFixed(1)}` : "-"}
                    </p>
                    <p className="text-xs text-nf-muted">Avg. Score</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </PageLayout>
  )
}
