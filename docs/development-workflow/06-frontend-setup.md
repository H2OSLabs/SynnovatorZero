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

### 5.2 配置 Neon Forge 主题

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
        return [
            {
                source: '/api/:path*',
                destination: 'http://localhost:8000/api/:path*',
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
