import { PostDetail } from "@/components/pages/post-detail"

export default function PostDetailPage({ params }: { params: { id: string } }) {
  return <PostDetail postId={Number(params.id)} />
}
