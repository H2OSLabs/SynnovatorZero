"use client"

import { useEffect, useState } from "react"
import { Search, SlidersHorizontal, Loader2, ChevronLeft, ChevronRight } from "lucide-react"
import { PageLayout } from "@/components/layout/PageLayout"
import { CategoryCard } from "@/components/cards/CategoryCard"
import { PostCard } from "@/components/cards/PostCard"
import { GroupCard } from "@/components/cards/GroupCard"
import { UserCard } from "@/components/cards/UserCard"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { useDebounce } from "@/hooks/use-debounce"
import {
  getCategories,
  getPosts,
  getProposals,
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
  const [searchQuery, setSearchQuery] = useState("")
  const [sort, setSort] = useState<'newest' | 'hottest'>('newest')
  const debouncedSearchQuery = useDebounce(searchQuery, 500)

  // Events state
  const [events, setEvents] = useState<Event[]>([])
  const [isLoadingEvents, setIsLoadingEvents] = useState(true)
  const [eventsError, setEventsError] = useState<string | null>(null)

  // Posts state
  const [posts, setPosts] = useState<PostWithAuthor[]>([])
  const [isLoadingPosts, setIsLoadingPosts] = useState(true)
  const [postsError, setPostsError] = useState<string | null>(null)

  // Proposals state
  const [proposals, setProposals] = useState<PostWithAuthor[]>([])
  const [isLoadingProposals, setIsLoadingProposals] = useState(true)
  const [proposalsError, setProposalsError] = useState<string | null>(null)

  // Hero Carousel State
  const [currentSlide, setCurrentSlide] = useState(0)

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
        const resp = await getCategories(0, 6, { status: "published", q: debouncedSearchQuery, sort })
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
        const resp = await getPosts(0, 6, { status: "published", q: debouncedSearchQuery, sort })
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

    // Fetch proposals
    const fetchProposals = async () => {
      setIsLoadingProposals(true)
      setProposalsError(null)
      try {
        const resp = await getProposals(0, 6, { status: "published", q: debouncedSearchQuery, sort })
        const proposalsWithAuthors = await Promise.all(
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
        setProposals(proposalsWithAuthors)
      } catch (e) {
        setProposalsError(e instanceof Error ? e.message : "加载提案失败")
        setProposals([])
      } finally {
        setIsLoadingProposals(false)
      }
    }

    // Fetch groups
    const fetchGroups = async () => {
      setIsLoadingGroups(true)
      setGroupsError(null)
      try {
        const resp = await getGroups(0, 6, { visibility: "public", q: debouncedSearchQuery })
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
        const resp = await listUsers(0, 6, undefined, debouncedSearchQuery)
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
    fetchProposals()
    fetchGroups()
    fetchUsers()
  }, [debouncedSearchQuery, sort])

  // Auto-rotate carousel
  useEffect(() => {
    if (events.length === 0) return
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % Math.min(events.length, 5))
    }, 5000)
    return () => clearInterval(timer)
  }, [events.length])

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % Math.min(events.length, 5))
  }

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + Math.min(events.length, 5)) % Math.min(events.length, 5))
  }

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
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="border-nf-secondary min-w-[100px]">
              <SlidersHorizontal className="h-4 w-4 mr-2" />
              {sort === 'newest' ? '最新' : '最热'}
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={() => setSort('newest')}>
              最新发布
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => setSort('hottest')}>
              最热内容
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      {/* Hero Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8 h-[360px]">
        {/* Left: Carousel */}
        <div className="lg:col-span-2 relative rounded-xl overflow-hidden bg-nf-card border border-nf-border group">
          {isLoadingEvents ? (
            <div className="w-full h-full flex items-center justify-center bg-nf-surface">
              <Loader2 className="h-8 w-8 animate-spin text-nf-lime" />
            </div>
          ) : events.length > 0 ? (
            <>
              {events.slice(0, 5).map((event, index) => (
                <div
                  key={event.id}
                  className={`absolute inset-0 transition-opacity duration-500 ${
                    index === currentSlide ? "opacity-100 z-10" : "opacity-0 z-0"
                  }`}
                >
                  <img
                    src={event.cover_image || "/placeholder-event.jpg"}
                    alt={event.name}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />
                  <div className="absolute bottom-0 left-0 p-8 w-full">
                    <span className="inline-block px-3 py-1 mb-3 text-xs font-medium bg-nf-lime/90 text-nf-dark rounded-full">
                      {event.type === 'competition' ? '竞赛' : '活动'}
                    </span>
                    <h2 className="text-3xl font-bold text-white mb-2">{event.name}</h2>
                    <p className="text-gray-200 line-clamp-2 max-w-2xl">{event.description}</p>
                  </div>
                </div>
              ))}
              
              {/* Carousel Controls */}
              <button 
                onClick={prevSlide}
                className="absolute left-4 top-1/2 -translate-y-1/2 z-20 p-2 rounded-full bg-black/30 hover:bg-black/50 text-white opacity-0 group-hover:opacity-100 transition-opacity"
              >
                <ChevronLeft className="h-6 w-6" />
              </button>
              <button 
                onClick={nextSlide}
                className="absolute right-4 top-1/2 -translate-y-1/2 z-20 p-2 rounded-full bg-black/30 hover:bg-black/50 text-white opacity-0 group-hover:opacity-100 transition-opacity"
              >
                <ChevronRight className="h-6 w-6" />
              </button>
              
              {/* Indicators */}
              <div className="absolute bottom-4 right-8 z-20 flex gap-2">
                {events.slice(0, 5).map((_, index) => (
                  <button
                    key={index}
                    onClick={() => setCurrentSlide(index)}
                    className={`w-2 h-2 rounded-full transition-all ${
                      index === currentSlide ? "w-6 bg-nf-lime" : "bg-white/50 hover:bg-white"
                    }`}
                  />
                ))}
              </div>
            </>
          ) : (
            <div className="w-full h-full flex items-center justify-center bg-nf-surface text-nf-muted">
              暂无推荐活动
            </div>
          )}
        </div>

        {/* Right: Pinned Content */}
        <div className="hidden lg:flex flex-col gap-4 h-full">
          {isLoadingPosts ? (
            <>
              <div className="flex-1 rounded-xl bg-nf-card border border-nf-border animate-pulse" />
              <div className="flex-1 rounded-xl bg-nf-card border border-nf-border animate-pulse" />
            </>
          ) : (
            <>
              {/* Slot 1 */}
              <div className="flex-1 relative rounded-xl overflow-hidden bg-nf-card border border-nf-border p-5 hover:border-nf-lime/50 transition-colors group cursor-pointer">
                <div className="absolute top-0 right-0 p-2">
                  <span className="px-2 py-0.5 text-[10px] font-bold bg-nf-lime/20 text-nf-lime rounded border border-nf-lime/30">置顶</span>
                </div>
                <h3 className="font-bold text-nf-white text-lg mb-2 line-clamp-2 group-hover:text-nf-lime transition-colors">
                  {posts[0]?.title || "官方公告：Synnovator 平台正式上线"}
                </h3>
                <p className="text-sm text-nf-muted line-clamp-3">
                  {posts[0]?.content || "欢迎来到 Synnovator！这是一个连接创新者、开发者与企业的协作平台..."}
                </p>
                <div className="absolute bottom-4 left-5 flex items-center text-xs text-nf-muted/60">
                  <span>{posts[0]?.created_at ? new Date(posts[0].created_at).toLocaleDateString() : "2024-03-20"}</span>
                </div>
              </div>

              {/* Slot 2 */}
              <div className="flex-1 relative rounded-xl overflow-hidden bg-nf-card border border-nf-border p-5 hover:border-nf-lime/50 transition-colors group cursor-pointer">
                 <div className="absolute top-0 right-0 p-2">
                  <span className="px-2 py-0.5 text-[10px] font-bold bg-red-500/20 text-red-400 rounded border border-red-500/30">热门</span>
                </div>
                <h3 className="font-bold text-nf-white text-lg mb-2 line-clamp-2 group-hover:text-nf-lime transition-colors">
                  {posts[1]?.title || "新手指南：如何创建你的第一个提案"}
                </h3>
                <p className="text-sm text-nf-muted line-clamp-3">
                  {posts[1]?.content || "详细教程带你了解从构思到发布的完整流程，获取更多社区支持..."}
                </p>
                <div className="absolute bottom-4 left-5 flex items-center text-xs text-nf-muted/60">
                  <span>{posts[1]?.created_at ? new Date(posts[1].created_at).toLocaleDateString() : "2024-03-19"}</span>
                </div>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="bg-nf-surface border-nf-secondary mb-6">
          <TabsTrigger value="all">全部</TabsTrigger>
          <TabsTrigger value="events">活动</TabsTrigger>
          <TabsTrigger value="proposals">提案</TabsTrigger>
          <TabsTrigger value="posts">帖子</TabsTrigger>
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

            {/* Proposals Section */}
            <section>
              <h2 className="font-heading text-xl font-semibold text-nf-white mb-4">提案</h2>
              {isLoadingProposals ? (
                renderLoading()
              ) : proposalsError ? (
                renderError(proposalsError)
              ) : proposals.length === 0 ? (
                renderEmpty("暂无提案")
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {proposals.map((post) => (
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
                      description={group.description}
                      visibility={group.visibility}
                      member_count={group.member_count}
                    />
                  ))}
                </div>
              )}
            </section>

            {/* Users Section */}
            <section>
              <h2 className="font-heading text-xl font-semibold text-nf-white mb-4">用户</h2>
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
                      display_name={user.display_name}
                      avatar_url={user.avatar_url}
                      bio={user.bio}
                      follower_count={user.follower_count}
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

        <TabsContent value="proposals">
          {isLoadingProposals ? (
            renderLoading()
          ) : proposalsError ? (
            renderError(proposalsError)
          ) : proposals.length === 0 ? (
            renderEmpty("暂无提案")
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {proposals.map((post) => (
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
      </Tabs>
    </PageLayout>
  )
}
