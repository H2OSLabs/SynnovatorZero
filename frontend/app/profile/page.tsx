"use client"

import { UserProfile } from "@/components/pages/user-profile"

export default function ProfilePage() {
  // TODO: Get userId from auth context; defaulting to 1 for prototype
  return <UserProfile userId={1} />
}
