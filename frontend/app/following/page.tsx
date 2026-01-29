"use client"

import { FollowingList } from "@/components/pages/following-list"

export default function FollowingPage() {
  // TODO: Get userId from auth context; defaulting to 1 for prototype
  return <FollowingList userId={1} />
}
