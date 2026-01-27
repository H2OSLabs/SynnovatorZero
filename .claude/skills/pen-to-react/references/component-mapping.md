# .pen → shadcn/ui 组件映射表

## 布局与容器

| .pen 模式 | shadcn/ui 组件 | 备注 |
|---|---|---|
| 页面级框架（页头+内容） | `Card` 或布局 div | flex 布局 |
| 卡片容器 | `Card`, `CardHeader`, `CardContent`, `CardFooter` | |
| 侧边栏导航 | `Sidebar`, `SidebarContent`, `SidebarMenu` | |
| 标签页布局 | `Tabs`, `TabsList`, `TabsTrigger`, `TabsContent` | |
| 分割线 | `Separator` | |

## 数据展示

| .pen 模式 | shadcn/ui 组件 | 备注 |
|---|---|---|
| 表格（表头+数据行） | `Table`, `TableHeader`, `TableRow`, `TableCell` | 交互式用 `DataTable` |
| 徽章/标签 | `Badge` | 映射颜色变体 |
| 头像圆形 | `Avatar`, `AvatarImage`, `AvatarFallback` | |
| 分页控件 | `Pagination`, `PaginationContent`, `PaginationItem` | |

## 表单

| .pen 模式 | shadcn/ui 组件 | 备注 |
|---|---|---|
| 带标签的表单 | `Form`, `FormField`, `FormItem`, `FormLabel`, `FormControl` | react-hook-form + zod |
| 文本输入框 | `Input` | 从 .pen 映射 placeholder |
| 多行文本框 | `Textarea` | 长文本字段 |
| 下拉选择 | `Select`, `SelectTrigger`, `SelectContent`, `SelectItem` | |
| 开关切换 | `Switch` | 布尔值字段 |
| 带图标搜索框 | `Input` + Lucide `Search` 图标 | |

## 按钮

| .pen 模式 | shadcn/ui 组件 | 备注 |
|---|---|---|
| 主按钮（lime 填充） | `Button`（默认变体） | Neon Forge lime 样式 |
| 描边按钮 | `Button variant="outline"` | |
| 幽灵按钮 | `Button variant="ghost"` | |

## 导航与弹层

| .pen 模式 | shadcn/ui 组件 | 备注 |
|---|---|---|
| 面包屑 | `Breadcrumb`, `BreadcrumbItem`, `BreadcrumbLink` | |
| 对话框/弹窗 | `Dialog`, `DialogContent`, `DialogHeader`, `DialogTitle` | |
| 下拉菜单 | `DropdownMenu`, `DropdownMenuTrigger`, `DropdownMenuContent` | |
| 悬浮提示 | `Tooltip`, `TooltipTrigger`, `TooltipContent` | |

## 图标映射

`.pen` 中 `iconFontFamily: "lucide"` + `iconFontName` 直接映射 Lucide React：

```tsx
import { Search, Plus, Trash2, Pencil, Eye, ChevronDown } from "lucide-react"
// "search" → <Search />
// "plus" → <Plus />
// "trash-2" → <Trash2 />
// "chevron-down" → <ChevronDown />
```

转换规则：kebab-case → PascalCase（如 `circle-check` → `CircleCheck`）
