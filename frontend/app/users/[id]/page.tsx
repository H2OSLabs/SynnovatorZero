"use client"

import Link from "next/link"
import { useParams } from "next/navigation"
import { useEffect, useState } from "react"
import { MessageCircle, Loader2 } from "lucide-react"
import { PageLayout } from "@/components/layout/PageLayout"
import { Panel, PanelSection, PanelCard } from "@/components/layout/Panel"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { getUser, type User } from "@/lib/api-client"

export default function UserProfilePage() {
  const params = useParams()
  const id = Number(params.id)

  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [isFollowing, setIsFollowing] = useState(false)
  const [followerCount, setFollowerCount] = useState(0)
  const [followingCount, setFollowingCount] = useState(0)

  useEffect(() => {
    if (!Number.isFinite(id)) {
      setError("Invalid user ID")
      setIsLoading(false)
      return
    }

    const fetchUser = async () => {
      setIsLoading(true)
      setError(null)
      try {
        const userData = await getUser(id)
        setUser(userData)
        setFollowerCount(userData.follower_count || 0)
        setFollowingCount(userData.following_count || 0)
      } catch (e) {
        setError(e instanceof Error ? e.message : "Failed to load user")
        setUser(null)
      } finally {
        setIsLoading(false)
      }
    }

    fetchUser()
  }, [id])

  const handleFollow = async () => {
    // For demo purposes, we'll just toggle the state
    // In a real app, you'd get the current user's ID from auth context
    setIsFollowing(!isFollowing)
    setFollowerCount((c) => (isFollowing ? c - 1 : c + 1))
  }

  if (isLoading) {
    return (
      <PageLayout variant="full">
        <div className="flex items-center justify-center min-h-[400px]">
          <Loader2 className="h-8 w-8 animate-spin text-nf-lime" />
        </div>
      </PageLayout>
    )
  }

  if (error || !user) {
    return (
      <PageLayout variant="full">
        <div className="text-center py-12">
          <p className="text-nf-error mb-4">{error || "User not found"}</p>
          <Link href="/explore">
            <Button variant="outline">Back to explore</Button>
          </Link>
        </div>
      </PageLayout>
    )
  }

  const panelContent = (
    <Panel title="User Actions">
      <PanelSection>
        <div className="space-y-3">
          <Button
            className={isFollowing ? "w-full border-nf-secondary" : "w-full bg-nf-lime text-nf-near-black hover:bg-nf-lime/90"}
            variant={isFollowing ? "outline" : "default"}
            onClick={handleFollow}
          >
            {isFollowing ? "Following" : "Follow"}
          </Button>
          <Button variant="outline" className="w-full border-nf-secondary">
            <MessageCircle className="h-4 w-4 mr-2" />
            Message
          </Button>
        </div>
      </PanelSection>

      <PanelSection title="Stats">
        <PanelCard>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-nf-muted">Role</span>
              <Badge className="bg-nf-dark">{user.role}</Badge>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-nf-muted">Following</span>
              <span className="text-nf-white font-medium">{followingCount}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-nf-muted">Followers</span>
              <span className="text-nf-white font-medium">{followerCount}</span>
            </div>
          </div>
        </PanelCard>
      </PanelSection>
    </Panel>
  )

  return (
    <PageLayout variant="full" panel={panelContent}>
      {/* Cover Image */}
      <div className="relative h-48 -mx-8 -mt-8 mb-20 bg-gradient-to-br from-nf-secondary to-nf-dark">
        {/* Profile Section */}
        <div className="absolute -bottom-16 left-8 flex items-end gap-6">
          <Avatar className="h-32 w-32 border-4 border-nf-dark">
            <AvatarImage src={user.avatar_url || undefined} />
            <AvatarFallback className="bg-gradient-to-br from-nf-lime to-nf-cyan text-nf-near-black text-4xl font-bold">
              {(user.display_name || user.username).charAt(0)}
            </AvatarFallback>
          </Avatar>
        </div>
      </div>

      {/* User Info */}
      <div className="mb-8">
        <h1 className="font-heading text-3xl font-bold text-nf-white mb-1">
          {user.display_name || user.username}
        </h1>
        <p className="text-nf-muted mb-4">@{user.username}</p>

        {/* Bio */}
        {user.bio && (
          <p className="text-nf-light-gray mb-4 max-w-2xl">{user.bio}</p>
        )}

        {/* Follow Stats */}
        <div className="flex items-center gap-6 text-sm">
          <span className="text-nf-white">
            <strong>{followingCount}</strong>{" "}
            <span className="text-nf-muted">Following</span>
          </span>
          <span className="text-nf-white">
            <strong>{followerCount}</strong>{" "}
            <span className="text-nf-muted">Followers</span>
          </span>
        </div>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="about">
        <TabsList className="bg-nf-surface border-nf-secondary mb-6">
          <TabsTrigger value="about">About</TabsTrigger>
          <TabsTrigger value="posts">Posts</TabsTrigger>
        </TabsList>

        <TabsContent value="about">
          <div className="bg-nf-surface rounded-xl p-6">
            <h2 className="font-heading text-xl font-semibold text-nf-white mb-4">About</h2>
            <div className="space-y-4">
              <div>
                <p className="text-sm text-nf-muted">Email</p>
                <p className="text-nf-white">{user.email}</p>
              </div>
              <div>
                <p className="text-sm text-nf-muted">Role</p>
                <p className="text-nf-white capitalize">{user.role}</p>
              </div>
              {user.bio && (
                <div>
                  <p className="text-sm text-nf-muted">Bio</p>
                  <p className="text-nf-white">{user.bio}</p>
                </div>
              )}
              {user.created_at && (
                <div>
                  <p className="text-sm text-nf-muted">Member since</p>
                  <p className="text-nf-white">
                    {new Date(user.created_at).toLocaleDateString("en-US", {
                      year: "numeric",
                      month: "long",
                      day: "numeric",
                    })}
                  </p>
                </div>
              )}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="posts">
          <div className="text-center py-16">
            <p className="text-nf-muted">User posts would be displayed here</p>
          </div>
        </TabsContent>
      </Tabs>
    </PageLayout>
  )
}
