import { UserProfile } from "@/components/pages/user-profile"

export default function ProfileByIdPage({ params }: { params: { id: string } }) {
  return <UserProfile userId={Number(params.id)} />
}
