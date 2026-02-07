"use client"

import { useEffect, useState } from "react"
import { Search, SlidersHorizontal, Loader2 } from "lucide-react"
import { PageLayout } from "@/components/layout/PageLayout"
import { CategoryCard } from "@/components/cards/CategoryCard"
import { PostCard } from "@/components/cards/PostCard"
import { GroupCard } from "@/components/cards/GroupCard"
import { UserCard } from "@/components/cards/UserCard"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  getCategories,
  getPosts,
  getGroups,
  listUsers,
  getUser,
  type Event,
  type Post,
  type Group,
  type User,
} from "@/lib/api-client"

interface PostWithAuthor extends Post {
  author?: User
}

export default function ExplorePage() {
  const [activeTab, setActiveTab] = useState("all")

  // Events state
  const [events, setEvents] = useState<Event[]>([])
  const [isLoadingEvents, setIsLoadingEvents] = useState(true)
  const [eventsError, setEventsError] = useState<string | null>(null)

  // Posts state
  const [posts, setPosts] = useState<PostWithAuthor[]>([])
  const [isLoadingPosts, setIsLoadingPosts] = useState(true)
  const [postsError, setPostsError] = useState<string | null>(null)

  // Groups state
  const [groups, setGroups] = useState<Group[]>([])
  const [isLoadingGroups, setIsLoadingGroups] = useState(true)
  const [groupsError, setGroupsError] = useState<string | null>(null)

  // Users state
  const [users, setUsers] = useState<User[]>([])
  const [isLoadingUsers, setIsLoadingUsers] = useState(true)
  const [usersError, setUsersError] = useState<string | null>(null)

  useEffect(() => {
    // Fetch events
    const fetchEvents = async () => {
      setIsLoadingEvents(true)
      setEventsError(null)
      try {
        const resp = await getCategories(0, 6, { status: "published" })
        setEvents(resp.items)
      } catch (e) {
        setEventsError(e instanceof Error ? e.message : "加载活动失败")
        setEvents([])
      } finally {
        setIsLoadingEvents(false)
      }
    }

    // Fetch posts with author info
    const fetchPosts = async () => {
      setIsLoadingPosts(true)
      setPostsError(null)
      try {
        const resp = await getPosts(0, 6, { status: "published" })
        // Fetch author details for each post
        const postsWithAuthors = await Promise.all(
          resp.items.map(async (post) => {
            if (post.created_by) {
              try {
                const author = await getUser(post.created_by)
                return { ...post, author }
              } catch {
                return post
              }
            }
            return post
          })
        )
        setPosts(postsWithAuthors)
      } catch (e) {
        setPostsError(e instanceof Error ? e.message : "加载帖子失败")
        setPosts([])
      } finally {
        setIsLoadingPosts(false)
      }
    }

    // Fetch groups
    const fetchGroups = async () => {
      setIsLoadingGroups(true)
      setGroupsError(null)
      try {
        const resp = await getGroups(0, 6, { visibility: "public" })
        setGroups(resp.items)
      } catch (e) {
        setGroupsError(e instanceof Error ? e.message : "加载团队失败")
        setGroups([])
      } finally {
        setIsLoadingGroups(false)
      }
    }

    // Fetch users
    const fetchUsers = async () => {
      setIsLoadingUsers(true)
      setUsersError(null)
      try {
        const resp = await listUsers(0, 6)
        setUsers(resp.items)
      } catch (e) {
        setUsersError(e instanceof Error ? e.message : "加载用户失败")
        setUsers([])
      } finally {
        setIsLoadingUsers(false)
      }
    }

    fetchEvents()
    fetchPosts()
    fetchGroups()
    fetchUsers()
  }, [])

  const renderLoading = () => (
    <div className="flex items-center justify-center py-10">
      <Loader2 className="h-6 w-6 animate-spin text-nf-lime" />
    </div>
  )

  const renderError = (error: string) => (
    <div className="text-center py-10 text-nf-muted">{error}</div>
  )

  const renderEmpty = (message: string) => (
    <div className="text-center py-10 text-nf-muted">{message}</div>
  )

  return (
    <PageLayout variant="compact">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="font-heading text-3xl font-bold text-nf-white mb-2">探索</h1>
        <p className="text-nf-muted">发现最新活动与项目</p>
      </div>

      {/* Search & Filter */}
      <div className="flex gap-4 mb-6">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-nf-muted" />
          <Input
            placeholder="搜索活动、帖子、团队、用户..."
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
          <TabsTrigger value="events">活动</TabsTrigger>
          <TabsTrigger value="posts">帖子</TabsTrigger>
          <TabsTrigger value="groups">团队</TabsTrigger>
          <TabsTrigger value="users">用户</TabsTrigger>
        </TabsList>

        <TabsContent value="all">
          <div className="space-y-8">
            {/* Events Section */}
            <section>
              <h2 className="font-heading text-xl font-semibold text-nf-white mb-4">活动</h2>
              {isLoadingEvents ? (
                renderLoading()
              ) : eventsError ? (
                renderError(eventsError)
              ) : events.length === 0 ? (
                renderEmpty("暂无活动")
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {events.map((event) => (
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
            </section>

            {/* Posts Section */}
            <section>
              <h2 className="font-heading text-xl font-semibold text-nf-white mb-4">帖子</h2>
              {isLoadingPosts ? (
                renderLoading()
              ) : postsError ? (
                renderError(postsError)
              ) : posts.length === 0 ? (
                renderEmpty("暂无帖子")
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
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
            </section>

            {/* Groups Section */}
            <section>
              <h2 className="font-heading text-xl font-semibold text-nf-white mb-4">团队</h2>
              {isLoadingGroups ? (
                renderLoading()
              ) : groupsError ? (
                renderError(groupsError)
              ) : groups.length === 0 ? (
                renderEmpty("暂无团队")
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
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
            </section>
          </div>
        </TabsContent>

        <TabsContent value="events">
          {isLoadingEvents ? (
            renderLoading()
          ) : eventsError ? (
            renderError(eventsError)
          ) : events.length === 0 ? (
            renderEmpty("暂无活动")
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {events.map((event) => (
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

        <TabsContent value="posts">
          {isLoadingPosts ? (
            renderLoading()
          ) : postsError ? (
            renderError(postsError)
          ) : posts.length === 0 ? (
            renderEmpty("暂无帖子")
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
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

        <TabsContent value="groups">
          {isLoadingGroups ? (
            renderLoading()
          ) : groupsError ? (
            renderError(groupsError)
          ) : groups.length === 0 ? (
            renderEmpty("暂无团队")
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
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

        <TabsContent value="users">
          {isLoadingUsers ? (
            renderLoading()
          ) : usersError ? (
            renderError(usersError)
          ) : users.length === 0 ? (
            renderEmpty("暂无用户")
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {users.map((user) => (
                <UserCard
                  key={user.id}
                  id={user.id}
                  username={user.username}
                  display_name={user.display_name || undefined}
                  bio={user.bio || undefined}
                  avatar_url={user.avatar_url || undefined}
                />
              ))}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </PageLayout>
  )
}
