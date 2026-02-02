import { Suspense } from "react"
import { PostList } from "@/components/pages/post-list"

export default function PostsPage() {
  return (
    <Suspense fallback={null}>
      <PostList />
    </Suspense>
  )
}
