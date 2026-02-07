"use client"

import Link from "next/link"
import { useParams } from "next/navigation"
import { useEffect, useState } from "react"
import { ArrowLeft, Users, UserPlus, Share2, Loader2 } from "lucide-react"
import { PageLayout } from "@/components/layout/PageLayout"
import { Panel, PanelSection, PanelCard } from "@/components/layout/Panel"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  getGroup,
  getGroupMembers,
  getUser,
  type Group,
  type Member,
  type User,
} from "@/lib/api-client"

interface MemberWithUser extends Member {
  user?: User
}

export default function GroupDetailPage() {
  const params = useParams()
  const id = Number(params.id)

  const [group, setGroup] = useState<Group | null>(null)
  const [members, setMembers] = useState<MemberWithUser[]>([])
  const [owner, setOwner] = useState<User | null>(null)

  const [isLoading, setIsLoading] = useState(true)
  const [isLoadingMembers, setIsLoadingMembers] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!Number.isFinite(id)) {
      setError("Invalid group ID")
      setIsLoading(false)
      return
    }

    // Fetch group details
    const fetchGroup = async () => {
      setIsLoading(true)
      setError(null)
      try {
        const data = await getGroup(id)
        setGroup(data)

        // Fetch owner details
        if (data.created_by) {
          try {
            const ownerData = await getUser(data.created_by)
            setOwner(ownerData)
          } catch {
            // Owner might not exist
          }
        }
      } catch (e) {
        setError(e instanceof Error ? e.message : "Failed to load group")
        setGroup(null)
      } finally {
        setIsLoading(false)
      }
    }

    // Fetch members with user details
    const fetchMembers = async () => {
      setIsLoadingMembers(true)
      try {
        const membersData = await getGroupMembers(id)
        const membersWithUsers = await Promise.all(
          membersData.items.map(async (member) => {
            try {
              const user = await getUser(member.user_id)
              return { ...member, user }
            } catch {
              return member
            }
          })
        )
        setMembers(membersWithUsers)
      } catch {
        setMembers([])
      } finally {
        setIsLoadingMembers(false)
      }
    }

    fetchGroup()
    fetchMembers()
  }, [id])

  if (isLoading) {
    return (
      <PageLayout variant="full">
        <div className="flex items-center justify-center min-h-[400px]">
          <Loader2 className="h-8 w-8 animate-spin text-nf-lime" />
        </div>
      </PageLayout>
    )
  }

  if (error || !group) {
    return (
      <PageLayout variant="full">
        <div className="text-center py-12">
          <p className="text-nf-error mb-4">{error || "Group not found"}</p>
          <Link href="/groups">
            <Button variant="outline">Back to groups</Button>
          </Link>
        </div>
      </PageLayout>
    )
  }

  const acceptedMembers = members.filter((m) => m.status === "accepted")
  const pendingMembers = members.filter((m) => m.status === "pending")

  const panelContent = (
    <Panel title="Team Actions">
      <PanelSection>
        <div className="space-y-3">
          <Button className="w-full bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
            <UserPlus className="h-4 w-4 mr-2" />
            Join Team
          </Button>
          <Button variant="outline" className="w-full border-nf-secondary">
            <Share2 className="h-4 w-4 mr-2" />
            Share Team
          </Button>
        </div>
      </PanelSection>

      <PanelSection title="Team Stats">
        <PanelCard>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-2 text-nf-muted">
                <Users className="h-4 w-4" /> Members
              </span>
              <span className="text-nf-white font-medium">{acceptedMembers.length}</span>
            </div>
            {pendingMembers.length > 0 && (
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-2 text-nf-muted">
                  Pending
                </span>
                <span className="text-nf-orange font-medium">{pendingMembers.length}</span>
              </div>
            )}
          </div>
        </PanelCard>
      </PanelSection>

      {owner && (
        <PanelSection title="Owner">
          <PanelCard>
            <div className="flex items-center gap-3">
              <Avatar className="h-10 w-10">
                <AvatarImage src={owner.avatar_url || undefined} />
                <AvatarFallback className="bg-nf-dark">
                  {owner.display_name?.charAt(0) || owner.username?.charAt(0) || "?"}
                </AvatarFallback>
              </Avatar>
              <div>
                <p className="text-nf-white font-medium">
                  {owner.display_name || owner.username}
                </p>
                <p className="text-sm text-nf-muted">@{owner.username}</p>
              </div>
            </div>
          </PanelCard>
        </PanelSection>
      )}
    </Panel>
  )

  return (
    <PageLayout variant="full" panel={panelContent}>
      {/* Back Button */}
      <Link href="/groups" className="inline-flex items-center gap-2 text-nf-muted hover:text-nf-white mb-6">
        <ArrowLeft className="h-4 w-4" />
        Back to groups
      </Link>

      {/* Group Header */}
      <div className="flex items-start gap-6 mb-8">
        <Avatar className="h-24 w-24 rounded-xl">
          <AvatarFallback className="rounded-xl bg-gradient-to-br from-nf-cyan to-nf-pink text-nf-white text-3xl font-bold">
            {group.name.charAt(0)}
          </AvatarFallback>
        </Avatar>
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h1 className="font-heading text-3xl font-bold text-nf-white">{group.name}</h1>
            <Badge variant="secondary" className="bg-nf-dark">
              {group.visibility === "public" ? "Public" : "Private"}
            </Badge>
          </div>
          <p className="text-nf-muted mb-2">
            {acceptedMembers.length} members
          </p>
        </div>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="about">
        <TabsList className="bg-nf-surface border-nf-secondary mb-6">
          <TabsTrigger value="about">About</TabsTrigger>
          <TabsTrigger value="members">Members ({acceptedMembers.length})</TabsTrigger>
        </TabsList>

        <TabsContent value="about">
          <div className="bg-nf-surface rounded-xl p-6">
            <h2 className="font-heading text-xl font-semibold text-nf-white mb-4">Description</h2>
            <p className="text-nf-light-gray whitespace-pre-wrap">
              {group.description || "No description available"}
            </p>
          </div>

          {group.require_approval && (
            <div className="mt-4 p-4 bg-nf-surface rounded-lg">
              <p className="text-sm text-nf-muted">
                This team requires approval to join
              </p>
            </div>
          )}

          {group.max_members && (
            <div className="mt-4 p-4 bg-nf-surface rounded-lg">
              <p className="text-sm text-nf-muted">
                Maximum members: {group.max_members}
              </p>
            </div>
          )}
        </TabsContent>

        <TabsContent value="members">
          {isLoadingMembers ? (
            <div className="flex items-center justify-center py-10">
              <Loader2 className="h-6 w-6 animate-spin text-nf-lime" />
            </div>
          ) : members.length === 0 ? (
            <div className="text-center py-10 text-nf-muted">No members found</div>
          ) : (
            <div className="space-y-4">
              {members.map((member) => (
                <div
                  key={member.id}
                  className="flex items-center gap-4 p-4 bg-nf-surface rounded-lg"
                >
                  <Avatar className="h-12 w-12">
                    <AvatarImage src={member.user?.avatar_url || undefined} />
                    <AvatarFallback className="bg-nf-dark">
                      {member.user?.display_name?.charAt(0) || member.user?.username?.charAt(0) || "?"}
                    </AvatarFallback>
                  </Avatar>
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-nf-white">
                        {member.user?.display_name || member.user?.username || `User ${member.user_id}`}
                      </span>
                      {member.role === "owner" && (
                        <Badge className="bg-nf-lime text-nf-near-black text-xs">Owner</Badge>
                      )}
                      {member.role === "admin" && (
                        <Badge className="bg-nf-cyan text-nf-near-black text-xs">Admin</Badge>
                      )}
                      {member.status === "pending" && (
                        <Badge variant="secondary" className="bg-nf-orange text-nf-near-black text-xs">Pending</Badge>
                      )}
                    </div>
                    {member.user?.username && (
                      <p className="text-sm text-nf-muted">@{member.user.username}</p>
                    )}
                  </div>
                  {member.status === "pending" && (
                    <div className="flex gap-2">
                      <Button size="sm" className="bg-nf-lime text-nf-near-black">Approve</Button>
                      <Button size="sm" variant="outline" className="border-nf-secondary">Reject</Button>
                    </div>
                  )}
                </div>
              ))}
              <Button variant="outline" className="w-full border-nf-secondary">
                <UserPlus className="h-4 w-4 mr-2" />
                Invite Member
              </Button>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </PageLayout>
  )
}
