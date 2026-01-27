# shadcn/ui 配置与 Neon Forge 主题

## 检查 components.json

```bash
ls frontend/components.json
```

不存在则初始化：

```bash
cd frontend && npx shadcn@latest init
```

## 项目配置

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "config": "",
    "css": "app/globals.css",
    "baseColor": "neutral",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  },
  "iconLibrary": "lucide"
}
```

## Neon Forge 主题 CSS 变量

在 `globals.css` 中添加：

```css
@import "tailwindcss";

:root {
  --nf-lime: #BBFD3B;
  --nf-surface: #00000E;
  --nf-dark-bg: #333333;
  --nf-near-black: #181818;
  --nf-card-bg: #222222;
  --nf-muted: #8E8E8E;
  --nf-light-gray: #DCDCDC;
  --nf-white: #FFFFFF;
  --nf-error: #FA541C;
  --nf-success: #74FFBB;
  --nf-warning: #FAAD14;
  --nf-cyan: #41FAF4;
  --nf-blue: #4C78FF;
  --nf-pink: #FF74A7;
  --nf-orange: #FB7A38;
}
```

## 文件结构

```
frontend/
├── app/
│   ├── globals.css          # Neon Forge 主题变量
│   └── layout.tsx           # 根布局（含字体加载）
├── components/
│   ├── ui/                  # shadcn/ui 组件（自动生成）
│   └── pages/               # 生成的页面组件
│       ├── home.tsx          # ← home.pen
│       ├── category-detail.tsx
│       ├── items-list.tsx
│       ├── items-form.tsx
│       ├── items-edit.tsx
│       ├── user-profile.tsx
│       ├── team.tsx
│       └── assets.tsx
├── lib/
│   └── utils.ts             # cn() 工具函数
└── components.json
```

## 按页面类型安装组件

```bash
# 列表/表格页面
npx shadcn@latest add table button input badge pagination dropdown-menu

# 表单页面
npx shadcn@latest add form input textarea select switch button card breadcrumb

# 详情页面
npx shadcn@latest add card badge button tabs separator avatar

# 仪表盘/首页
npx shadcn@latest add card sidebar navigation-menu avatar badge button
```
