import Link from "next/link"
import { ArrowRight, Rocket, Users, Trophy, Lightbulb } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Header } from "@/components/layout/Header"
import { CategoryCard } from "@/components/cards/CategoryCard"
import { PostCard } from "@/components/cards/PostCard"
import { PlatformStats } from "@/components/home/PlatformStats"

// Mock data for development
const mockCategories = [
  {
    id: 1,
    name: "AI 创新挑战赛 2024",
    description: "探索人工智能的无限可能",
    type: "competition" as const,
    status: "published" as const,
    tags: ["AI", "Machine Learning"],
    participant_count: 128,
    start_date: "2024-03-01",
    end_date: "2024-03-30",
  },
  {
    id: 2,
    name: "Web3 黑客马拉松",
    description: "构建去中心化的未来",
    type: "competition" as const,
    status: "published" as const,
    tags: ["Web3", "Blockchain"],
    participant_count: 86,
    start_date: "2024-04-01",
    end_date: "2024-04-15",
  },
  {
    id: 3,
    name: "绿色科技创新大赛",
    description: "用科技守护地球家园",
    type: "competition" as const,
    status: "published" as const,
    tags: ["Climate", "Sustainability"],
    participant_count: 64,
    start_date: "2024-05-01",
    end_date: "2024-05-31",
  },
  {
    id: 4,
    name: "开源社区贡献月",
    description: "参与开源，共建技术生态",
    type: "operation" as const,
    status: "published" as const,
    tags: ["Open Source"],
    participant_count: 256,
    start_date: "2024-03-01",
    end_date: "2024-03-31",
  },
]

const mockPosts = [
  {
    id: 1,
    title: "基于大模型的智能教育平台",
    body: "我们开发了一个基于大语言模型的个性化学习平台，能够根据学生的学习进度自动调整教学内容...",
    type: "for_category",
    status: "published",
    tags: ["AI", "Education", "LLM"],
    like_count: 128,
    comment_count: 32,
    created_by: { id: 1, username: "alice", display_name: "Alice" },
  },
  {
    id: 2,
    title: "去中心化身份认证系统",
    body: "利用区块链技术构建的下一代身份认证系统，让用户真正掌控自己的数据...",
    type: "for_category",
    status: "published",
    tags: ["Web3", "DID", "Privacy"],
    like_count: 96,
    comment_count: 24,
    created_by: { id: 2, username: "bob", display_name: "Bob" },
  },
  {
    id: 3,
    title: "碳足迹追踪应用",
    body: "帮助用户记录和减少日常生活中的碳排放，通过游戏化机制激励环保行动...",
    type: "for_category",
    status: "published",
    tags: ["Climate", "Mobile", "Gamification"],
    like_count: 72,
    comment_count: 18,
    created_by: { id: 3, username: "carol", display_name: "Carol" },
  },
  {
    id: 4,
    title: "开源代码审查工具",
    body: "AI 驱动的代码审查助手，帮助开发者发现潜在 bug 和安全漏洞...",
    type: "for_category",
    status: "published",
    tags: ["DevTools", "AI", "Security"],
    like_count: 156,
    comment_count: 42,
    created_by: { id: 4, username: "dave", display_name: "Dave" },
  },
]

export default function HomePage() {
  return (
    <div className="min-h-screen bg-nf-dark">
      {/* Header */}
      <Header user={null} />

      {/* Hero Section */}
      <section className="pt-[60px]">
        <div className="max-w-6xl mx-auto px-4 py-20 text-center">
          <div className="flex justify-center mb-6">
            <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-nf-lime to-nf-cyan flex items-center justify-center">
              <Rocket className="h-10 w-10 text-nf-near-black" />
            </div>
          </div>
          <h1 className="font-heading text-4xl md:text-5xl lg:text-6xl font-bold text-nf-white mb-4">
            创意在这里起飞
          </h1>
          <p className="text-lg md:text-xl text-nf-muted mb-8 max-w-2xl mx-auto">
            发现最激动人心的 Hackathon，与志同道合的人组队，将创意变为现实
          </p>
          <div className="flex flex-wrap gap-4 justify-center">
            <Link href="/explore">
              <Button size="lg" className="bg-nf-lime text-nf-near-black hover:bg-nf-lime/90">
                探索活动
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link href="/events/create">
              <Button size="lg" variant="outline" className="border-nf-secondary text-nf-white hover:bg-nf-secondary">
                发起活动
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-12 bg-nf-surface">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="w-14 h-14 rounded-xl bg-nf-lime/20 flex items-center justify-center mx-auto mb-4">
                <Trophy className="h-7 w-7 text-nf-lime" />
              </div>
              <h3 className="font-heading text-xl font-semibold text-nf-white mb-2">参与竞赛</h3>
              <p className="text-nf-muted">
                参加各类 Hackathon 和创新大赛，展示你的技术实力
              </p>
            </div>
            <div className="text-center p-6">
              <div className="w-14 h-14 rounded-xl bg-nf-cyan/20 flex items-center justify-center mx-auto mb-4">
                <Users className="h-7 w-7 text-nf-cyan" />
              </div>
              <h3 className="font-heading text-xl font-semibold text-nf-white mb-2">组建团队</h3>
              <p className="text-nf-muted">
                找到志同道合的伙伴，组建你的梦想团队
              </p>
            </div>
            <div className="text-center p-6">
              <div className="w-14 h-14 rounded-xl bg-nf-pink/20 flex items-center justify-center mx-auto mb-4">
                <Lightbulb className="h-7 w-7 text-nf-pink" />
              </div>
              <h3 className="font-heading text-xl font-semibold text-nf-white mb-2">分享创意</h3>
              <p className="text-nf-muted">
                发布你的项目作品，获取社区反馈和支持
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Hot Events */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex items-center justify-between mb-8">
            <h2 className="font-heading text-2xl font-bold text-nf-white">🔥 热门活动</h2>
            <Link href="/events" className="text-nf-lime hover:underline text-sm">
              查看更多 →
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {mockCategories.map((category) => (
              <CategoryCard key={category.id} {...category} />
            ))}
          </div>
        </div>
      </section>

      {/* Featured Projects */}
      <section className="py-16 bg-nf-surface">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex items-center justify-between mb-8">
            <h2 className="font-heading text-2xl font-bold text-nf-white">💡 精选项目</h2>
            <Link href="/posts" className="text-nf-lime hover:underline text-sm">
              查看更多 →
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {mockPosts.map((post) => (
              <PostCard key={post.id} {...post} />
            ))}
          </div>
        </div>
      </section>

      {/* Platform Stats */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="font-heading text-2xl font-bold text-nf-white text-center mb-8">📊 平台数据</h2>
          <PlatformStats />
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-nf-surface border-t border-nf-secondary">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center gap-6">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-nf-lime to-nf-cyan flex items-center justify-center">
                <span className="text-nf-near-black font-bold text-sm">S</span>
              </div>
              <span className="font-heading font-bold text-nf-white">协创者</span>
            </div>
            <div className="flex gap-6 text-sm text-nf-muted">
              <Link href="/about" className="hover:text-nf-white">关于我们</Link>
              <Link href="/help" className="hover:text-nf-white">帮助中心</Link>
              <Link href="/contact" className="hover:text-nf-white">联系我们</Link>
              <Link href="/privacy" className="hover:text-nf-white">隐私政策</Link>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-nf-secondary text-center text-sm text-nf-muted">
            © 2024 Synnovator. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  )
}
