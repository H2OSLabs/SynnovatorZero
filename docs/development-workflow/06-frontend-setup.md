# 阶段 5-6: 前端框架配置与 API 客户端

## 阶段 5: 前端样式框架配置

### 5.1 安装 Tailwind CSS + shadcn/ui

```bash
cd frontend

# 安装 Tailwind CSS
npm install -D tailwindcss @tailwindcss/postcss postcss

# 初始化 shadcn/ui
npx shadcn@latest init
```

### 5.2 Next.js 配置检查清单 ⭐

> 即使使用 App Router，某些场景仍需要 pages 目录文件。

**必须存在的文件：**

```
frontend/
├── pages/
│   ├── _app.tsx        # 自定义 App 组件
│   ├── _document.tsx   # 自定义 Document（HTML 结构）
│   └── _error.tsx      # 自定义错误页面
├── next.config.js      # Next.js 配置
└── next-env.d.ts       # TypeScript 类型声明
```

**pages/_document.tsx 示例：**

```typescript
import { Head, Html, Main, NextScript } from "next/document"

export default function Document() {
  return (
    <Html lang="zh-CN" className="dark">
      <Head />
      <body className="font-body antialiased">
        <Main />
        <NextScript />
      </body>
    </Html>
  )
}
```

**验证配置：**

```bash
# 检查必要文件存在
ls frontend/pages/_app.tsx frontend/pages/_document.tsx frontend/pages/_error.tsx

# 验证 Next.js 构建成功
cd frontend && npm run build
```

**常见问题：**

| 错误 | 原因 | 解决 |
|------|------|------|
| `ENOENT: _document.js` | 缺少 pages 目录文件 | 创建 `pages/_document.tsx` |
| Hydration mismatch | SSR/CSR 不一致 | 检查 useEffect 内的状态更新 |
| TypeScript 类型错误 | `next-env.d.ts` 过时 | 运行 `npm run build` 自动更新 |

### 5.3 配置 Neon Forge 主题

**tailwind.config.ts：**

```typescript
const colors = {
  primary: '#BBFD3B',    // Lime Green
  surface: '#181818',    // 最深背景
  dark: '#222222',       // 深色背景
  secondary: '#333333',  // 次级背景
  muted: '#666666',      // 弱化文字
  foreground: '#FFFFFF', // 主文字
};
```

**字体配置：**
- Space Grotesk — 标题
- Inter — 正文
- Poppins — 数字/代码
- Noto Sans SC — 中文

说明：为兼容离线/受限网络的预览与 CI 环境，前端默认不从 Google Fonts 在线加载字体，以上字体会自动回退到系统字体；如需固定字体效果，建议使用 `next/font`（构建期拉取并本地化）或自托管字体文件。

---

## 阶段 6: 前端 API 客户端生成

### 6.1 生成 TypeScript 客户端

```bash
uv run python .claude/skills/api-builder/scripts/cli.py \
  --spec .synnovator/openapi.yaml \
  --output app \
  --generate-client \
  --client-output frontend/lib/
```

**生成文件：**
- `frontend/lib/api-client.ts` — API 方法
- `frontend/lib/types.ts` — TypeScript 类型

### 6.2 验证 API 客户端完整性 ⭐

```bash
# 检查 CRUD 操作存在
grep -E "method: '(POST|PATCH|DELETE)'" frontend/lib/api-client.ts | wc -l

# 验证关键方法
grep -q "createPost" frontend/lib/api-client.ts && echo "✅ createPost"
grep -q "updatePost" frontend/lib/api-client.ts && echo "✅ updatePost"
grep -q "deletePost" frontend/lib/api-client.ts && echo "✅ deletePost"
```

### 6.3 配置环境变量

```bash
# frontend/.env.development
API_URL=/api
INTERNAL_API_URL=http://localhost:8000/api
```

> 环境变量通过 `lib/env.ts` 读取，注入到 `window.__ENV__`。

### 6.4 配置 Next.js API 代理 ⭐ 必须配置

> 前端使用 `/api` 作为基础路径，需要配置 rewrites 代理到后端。

**frontend/next.config.js：**

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
    output: "standalone",
    async rewrites() {
        const internalApiUrl = process.env.INTERNAL_API_URL || "http://localhost:8000/api"
        const base = internalApiUrl.replace(/\/$/, "")
        return [
            {
                source: '/api/:path*',
                destination: `${base}/:path*`,
            },
        ];
    },
};

module.exports = nextConfig;
```

**验证代理：**

```bash
make start

# 通过前端访问后端 API
curl http://localhost:3000/api/users
# 应返回与 http://localhost:8000/api/users 相同的数据
```

### 6.5 API 客户端单元测试

**测试架构：**

| 文件 | 用途 |
|------|------|
| `__tests__/api-client.test.ts` | API 客户端单元测试 |
| `__mocks__/api-client.ts` | 组件测试使用的 mock |

**绕过 moduleNameMapper 的自动 mock：**

---

## 常见问题排查

### 看到 `GET /@vite/client 404`（或预览控制台报 Vite Client）

这不是本仓库前端（Next.js）主动发出的请求。一般意味着你当前打开的页面 HTML 里被注入了 Vite 的 HMR 脚本，或你访问到了错误的上游/端口。

建议按以下顺序排查：

1. 在浏览器对首页执行 View Source，搜索是否包含 `/@vite/client`：
   - 如果包含：说明当前服务出来的 HTML 不是 Next.js 产物（或被某层反代/静态服务器替换），检查 Nginx 反代与启动命令是否指向本仓库的 `frontend`。
   - 如果不包含：更可能是浏览器插件、缓存或开发工具引入，尝试禁用相关插件并进行 Hard Reload。
2. 确认启动方式为 `make frontend` 或 `cd frontend && npm run dev`，不要在其它目录误启动 Vite 项目。

项目中提供了一个兼容兜底：`frontend/middleware.ts` 会对 `/@vite/client` 返回空模块，避免在受限预览环境产生 404 噪音；如果你的环境不会出现该请求，可以直接删除该 middleware。

```typescript
// __tests__/api-client.test.ts
jest.mock('../lib/env', () => ({
  getEnv: () => ({ API_URL: 'http://localhost:8000' }),
}))

// 获取真实模块
const apiClient = jest.requireActual('../lib/api-client')

describe('api-client', () => {
  const mockFetch = jest.fn()
  beforeAll(() => { global.fetch = mockFetch })

  test('getUser fetches user by ID', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ id: 1, username: 'test' }),
    })
    const result = await apiClient.getUser(1)
    expect(result.username).toBe('test')
  })
})
```

**运行测试：**

```bash
npm test -- --testPathPatterns="api-client"
```

## 下一步

完成前端配置后，进入 [阶段 7: 前端组件开发](07-frontend-components.md)。
