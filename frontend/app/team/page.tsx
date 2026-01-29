"use client"

import { Team } from "@/components/pages/team"

export default function TeamPage() {
  // TODO: Get groupId from route or context; defaulting to 1 for prototype
  return <Team groupId={1} />
}
