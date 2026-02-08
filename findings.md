# Findings: Header 修复 + Figma Skills 集成分析

> **更新时间**: 2026-02-08

## 1. Header 登录状态 Bug 分析

### 问题现象

Header 组件在已登录用户刷新页面时，短暂显示登录/注册按钮后才切换为用户头像。

### 根本原因

Header 组件未处理 AuthContext 的 `isLoading` 状态：

```tsx
// Before: 仅检查 user
{user ? (/* logged in UI */) : (/* login/register buttons */)}

// After: 同时检查 isLoading
{isLoading ? (/* skeleton */) : user ? (/* logged in */) : (/* login/register */)}
```

### 根因归类

| 类型 | 判定 |
|------|------|
| 测试用例缺失 | ✅ 无 TC 覆盖 Header 登录状态切换 |
| 用户旅程缺失 | ❌ J-001/J-002 已覆盖登录流程 |
| 实现问题 | ✅ 未处理 loading 状态 |

### 责任归属

| 阶段 | 问题 |
|------|------|
| Phase 7 (前端组件开发) | Header 组件未处理 loading 状态 |
| Phase 8 (E2E 测试) | 缺少 Header 状态切换测试 |

---

## 2. 用户 commit 7d54b32 分析

### URL 驱动筛选模式

用户实现了正确的 Next.js App Router 筛选模式：

```tsx
// 状态从 URL 派生
const applied = useMemo(() => {
  const q = searchParams.get("q") ?? ""
  const type = searchParams.get("type") ?? undefined
  // ...
}, [paramsKey, searchParams])

// UI 操作更新 URL
function updateParams(patch: {...}) {
  const next = new URLSearchParams(searchParams.toString())
  if (patch.q !== undefined) {...}
  router.replace(qs ? `/posts?${qs}` : "/posts")
}
```

这是 Next.js App Router 的最佳实践：
- 筛选结果可书签和分享
- 浏览器前进/后退正确工作
- 服务端渲染正确

---

## 3. Figma Skills 分析

### 可用 Skills

从 `feat/prototype-v1` 分支发现四个 Figma 相关 skills：

| Skill | 功能 | 输入 | 输出 |
|-------|------|------|------|
| `figma-resource-extractor` | 提取 Figma 设计资源 | Figma URL | `specs/design/figma/` |
| `ui-spec-generator` | 生成 UI 规格文件 | 设计资源 + 测试用例 | `specs/design/pages.yaml` |
| `ux-spec-generator` | 生成 UX 交互规格 | pages.yaml + 设计 | `specs/ux/` |
| `frontend-prototype-builder` | 构建可部署原型 | 所有上游输出 | React 页面组件 |

### Skills 工作流程

```
Figma Design
    ↓
figma-resource-extractor
    ↓
specs/design/figma/
    ↓
ui-spec-generator  ←── specs/testcases/*.md
    ↓
specs/design/pages.yaml
    ↓
ux-spec-generator
    ↓
specs/ux/ (交互规格)
    ↓
frontend-prototype-builder
    ↓
frontend/app/  +  frontend/components/pages/
```

### 当前状态

| 资源 | 状态 | 说明 |
|------|------|------|
| `specs/design/figma/` | ✅ 已存在 | 69 icons, 54 components, 104 pages |
| `specs/design/pages.yaml` | ❌ 不存在 | 需要运行 ui-spec-generator |
| `specs/ux/` | ❌ 不存在 | 需要运行 ux-spec-generator |
| Figma MCP | ❌ 未配置 | `.claude/mcp.json` 缺少 Figma 服务 |

### 依赖分析

| Skill | 依赖 | 当前状态 |
|-------|------|----------|
| figma-resource-extractor | Figma MCP | ⚠️ MCP 未配置 |
| ui-spec-generator | Figma MCP, Pencil MCP | ⚠️ MCP 未配置 |
| ux-spec-generator | pages.yaml | ❌ 需先生成 |
| frontend-prototype-builder | pages.yaml, ux specs | ❌ 需先生成 |

### MCP 配置需求

要使用 Figma skills，需要在 `.claude/mcp.json` 添加：

```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "figma-mcp"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "${FIGMA_ACCESS_TOKEN}"
      }
    }
  }
}
```

### 集成可行性评估

| 因素 | 评估 | 说明 |
|------|------|------|
| Figma 资源 | ✅ 就绪 | 已提取到 specs/design/figma/ |
| Figma MCP | ⚠️ 需配置 | 需要 Figma access token |
| Pencil MCP | ❌ 无 .pen 文件 | 项目已迁移到 Figma |
| 工作流整合 | ✅ 可行 | 可作为 Phase 4-7 的自动化 |

---

## 4. 工作流集成建议

### 短期（无 MCP 配置）

现有 Figma 资源已提取，可以：
1. 手动参考 `specs/design/figma/` 的设计文档
2. 根据测试用例手动创建 `pages.yaml`
3. 使用 `frontend-prototype-builder` 的模板生成页面

### 中期（配置 Figma MCP）

1. 配置 Figma MCP（需要 access token）
2. 将四个 skills 复制到当前分支
3. 更新 `docs/development-workflow.md` 添加设计自动化阶段

### 长期（完整集成）

修改开发工作流：

```
Phase 4: UI 设计 → 使用 Figma skills 自动化
  4.1 figma-resource-extractor
  4.2 ui-spec-generator
  4.3 ux-spec-generator

Phase 7: 前端组件开发 → 使用 frontend-prototype-builder
```

---

## 5. 待完成事项

- [x] 修复 Header isLoading 处理
- [ ] 配置 Figma MCP（需要用户提供 token）
- [ ] 复制 Figma skills 到当前分支
- [ ] 生成 specs/design/pages.yaml
- [ ] 更新开发工作流文档
