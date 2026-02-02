import Link from 'next/link'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6">
      <h1 className="text-4xl font-heading text-nf-lime">协创者</h1>
      <p className="text-nf-muted">Creative Collaboration Platform</p>
      <Link
        href="/demo"
        className="mt-4 rounded-lg bg-nf-lime px-6 py-3 font-medium text-nf-near-black transition-colors hover:bg-nf-lime/90"
      >
        查看组件演示
      </Link>
    </main>
  )
}
