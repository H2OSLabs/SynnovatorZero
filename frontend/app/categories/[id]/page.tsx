import { CategoryDetail } from "@/components/pages/category-detail"

export default function CategoryDetailPage({ params }: { params: { id: string } }) {
  return <CategoryDetail categoryId={Number(params.id)} />
}
