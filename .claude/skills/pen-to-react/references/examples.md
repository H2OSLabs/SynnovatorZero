# 代码生成示例

## 表格列表页面

从包含表格结构的 .pen 文件生成：

```tsx
"use client"

import { Search, Plus, Pencil, Trash2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Table, TableBody, TableCell, TableHead,
  TableHeader, TableRow,
} from "@/components/ui/table"

interface Item {
  id: number
  name: string
  created_at: string
}

const sampleData: Item[] = [
  { id: 1, name: "Sample Item 1", created_at: "2025-01-01" },
  { id: 2, name: "Sample Item 2", created_at: "2025-01-02" },
  { id: 3, name: "Sample Item 3", created_at: "2025-01-03" },
]

export function ItemsList() {
  return (
    <div className="flex flex-col gap-6 p-8 bg-[var(--nf-near-black)] min-h-screen">
      {/* 页头 */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-heading text-[36px] font-bold text-[var(--nf-white)]">
            Items / 项目列表
          </h1>
          <p className="text-[14px] text-[var(--nf-light-gray)]">
            Manage all items / 管理所有项目
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--nf-muted)]" />
            <Input
              placeholder="Search / 搜索..."
              className="pl-10 bg-[var(--nf-card-bg)] border-[var(--nf-muted)] text-[var(--nf-white)]"
            />
          </div>
          <Button className="bg-[var(--nf-lime)] text-[var(--nf-surface)] hover:bg-[var(--nf-lime)]/90">
            <Plus className="w-4 h-4 mr-2" />
            Create / 新建
          </Button>
        </div>
      </div>

      {/* 表格 */}
      <div className="rounded-[12px] border border-[var(--nf-dark-bg)] overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow className="bg-[var(--nf-dark-bg)] border-[var(--nf-dark-bg)]">
              <TableHead className="text-[var(--nf-white)]">ID</TableHead>
              <TableHead className="text-[var(--nf-white)]">Name / 名称</TableHead>
              <TableHead className="text-[var(--nf-white)]">Created / 创建时间</TableHead>
              <TableHead className="text-[var(--nf-white)] text-right">Actions / 操作</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {sampleData.map((item) => (
              <TableRow key={item.id} className="border-[var(--nf-dark-bg)]">
                <TableCell className="text-[var(--nf-light-gray)]">{item.id}</TableCell>
                <TableCell className="text-[var(--nf-light-gray)]">{item.name}</TableCell>
                <TableCell className="text-[var(--nf-light-gray)]">{item.created_at}</TableCell>
                <TableCell className="text-right">
                  <Button variant="ghost" size="icon">
                    <Pencil className="w-4 h-4 text-[var(--nf-muted)]" />
                  </Button>
                  <Button variant="ghost" size="icon">
                    <Trash2 className="w-4 h-4 text-[var(--nf-error)]" />
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}
```

## 表单页面

从包含表单结构的 .pen 文件生成：

```tsx
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import {
  Form, FormControl, FormField, FormItem, FormLabel, FormMessage,
} from "@/components/ui/form"
import {
  Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList,
  BreadcrumbPage, BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"

const formSchema = z.object({
  name: z.string().min(1, "Name is required"),
})

export function ItemsForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { name: "" },
  })

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values)
  }

  return (
    <div className="flex flex-col gap-6 p-8 bg-[var(--nf-near-black)] min-h-screen">
      <Breadcrumb>
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbLink href="/items" className="text-[var(--nf-muted)]">
              Items / 项目列表
            </BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbPage className="text-[var(--nf-white)]">
              Create / 新建
            </BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>

      <h2 className="font-heading text-[28px] font-bold text-[var(--nf-white)]">
        Create Item / 新建项目
      </h2>

      <Card className="bg-[var(--nf-card-bg)] border-[var(--nf-dark-bg)]">
        <CardHeader>
          <CardTitle className="text-[var(--nf-white)]">
            Item Information / 项目信息
          </CardTitle>
        </CardHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)}>
            <CardContent className="space-y-4">
              <FormField
                control={form.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="text-[var(--nf-white)]">
                      Name / 名称
                    </FormLabel>
                    <FormControl>
                      <Input
                        placeholder="Enter name..."
                        className="bg-[var(--nf-card-bg)] border-[var(--nf-muted)] text-[var(--nf-white)]"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </CardContent>
            <CardFooter className="flex justify-end gap-3">
              <Button variant="outline" className="border-[var(--nf-muted)] text-[var(--nf-white)]">
                Cancel / 取消
              </Button>
              <Button
                type="submit"
                className="bg-[var(--nf-lime)] text-[var(--nf-surface)] hover:bg-[var(--nf-lime)]/90"
              >
                Submit / 提交
              </Button>
            </CardFooter>
          </form>
        </Form>
      </Card>
    </div>
  )
}
```

## 关键样式模式

| 元素 | Tailwind 类 |
|------|-------------|
| 页面背景 | `bg-[var(--nf-near-black)] min-h-screen` |
| 卡片背景 | `bg-[var(--nf-card-bg)] border-[var(--nf-dark-bg)]` |
| 主按钮 | `bg-[var(--nf-lime)] text-[var(--nf-surface)]` |
| 输入框 | `bg-[var(--nf-card-bg)] border-[var(--nf-muted)] text-[var(--nf-white)]` |
| H1 标题 | `font-heading text-[36px] font-bold text-[var(--nf-white)]` |
| H2 标题 | `font-heading text-[28px] font-bold text-[var(--nf-white)]` |
| 正文 | `text-[14px] text-[var(--nf-light-gray)]` |
| 占位符/辅助文字 | `text-[var(--nf-muted)]` |
| 表格圆角 | `rounded-[12px] border border-[var(--nf-dark-bg)] overflow-hidden` |
