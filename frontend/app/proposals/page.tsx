import { Suspense } from "react"
import { ProposalList } from "@/components/pages/proposal-list"

export default function ProposalsPage() {
  return (
    <Suspense fallback={null}>
      <ProposalList />
    </Suspense>
  )
}
