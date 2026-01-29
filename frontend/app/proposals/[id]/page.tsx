import { ProposalDetail } from "@/components/pages/proposal-detail"

export default function ProposalDetailPage({ params }: { params: { id: string } }) {
  return <ProposalDetail postId={Number(params.id)} />
}
