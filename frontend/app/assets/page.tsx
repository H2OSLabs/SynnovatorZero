import { PageLayout } from "@/components/layout/PageLayout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { FileText, Upload, Award, Cpu } from "lucide-react"

export default function AssetLibrary() {
  return (
    <PageLayout variant="full">
      <div className="container mx-auto p-6 space-y-8">
        <div>
          <h1 className="text-3xl font-bold text-nf-white">资产管理</h1>
          <p className="text-nf-muted mt-2">管理您的数字资产，包括创作内容、上传文件、荣誉证明及算力资源</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="bg-nf-card border-nf-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-nf-white">我的文件</CardTitle>
            <FileText className="h-4 w-4 text-nf-lime" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-nf-white">0</div>
            <p className="text-xs text-nf-muted">Markdown 文档、笔记、代码片段</p>
          </CardContent>
        </Card>

        <Card className="bg-nf-card border-nf-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-nf-white">上传文件</CardTitle>
            <Upload className="h-4 w-4 text-nf-lime" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-nf-white">0</div>
            <p className="text-xs text-nf-muted">图片、PDF、数据集、压缩包</p>
          </CardContent>
        </Card>

        <Card className="bg-nf-card border-nf-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-nf-white">荣誉证明</CardTitle>
            <Award className="h-4 w-4 text-nf-lime" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-nf-white">0</div>
            <p className="text-xs text-nf-muted">数字证书、成就勋章</p>
          </CardContent>
        </Card>

        <Card className="bg-nf-card border-nf-border">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-nf-white">算力资源</CardTitle>
            <Cpu className="h-4 w-4 text-nf-lime" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-nf-white">--</div>
            <p className="text-xs text-nf-muted">CPU/GPU 时长、存储配额</p>
          </CardContent>
        </Card>
      </div>

      <div className="rounded-lg border border-nf-border bg-nf-card p-8 text-center text-nf-muted">
        <p>资产管理功能正在开发中...</p>
      </div>
    </div>
    </PageLayout>
  )
}
