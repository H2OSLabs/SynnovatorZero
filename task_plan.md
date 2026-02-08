# Task Plan: Header 修复 + Figma 工作流集成

> **目标**: 修复 Header 登录状态问题，研究 Figma skills 集成可行性
> **创建时间**: 2026-02-08
> **状态**: `in_progress`

## 背景

用户提交了 commit 7d54b32 实现了帖子筛选对话框和搜索功能。同时发现 Header 组件存在登录状态显示 bug。用户还希望研究 `feat/prototype-v1` 分支上的 Figma skills，评估集成到开发工作流的可行性。

## 阶段列表

| Phase | 描述 | 状态 |
|-------|------|------|
| Phase 1 | 分析用户 commit 7d54b32 | `complete` |
| Phase 2 | 修复 Header 登录状态 bug | `complete` |
| Phase 3 | 根因分析 | `complete` |
| Phase 4 | 研究 Figma skills | `in_progress` |
| Phase 5 | 评估工作流集成 | `pending` |
| Phase 6 | 验证与提交 | `pending` |

---

## Phase 1: 分析用户 commit 7d54b32 `complete`

### 变更内容

用户实现了帖子筛选功能：

| 文件 | 变更 |
|------|------|
| `app/routers/posts.py` | 添加 `q` (关键词搜索) 和 `tags` (标签筛选) 参数 |
| `app/tests/test_posts.py` | 添加 tag 和 keyword 筛选测试 |
| `docs/frontend-routes.md` | 文档化 `/posts` 查询参数 |
| `frontend/app/posts/page.tsx` | URL 参数同步 + 筛选状态管理 |
| `frontend/components/post/PostsFilterDialog.tsx` | 新建筛选对话框组件 |
| `frontend/lib/api-client.ts` | 支持 `q` 和 `tags` 筛选参数 |

### 关键模式

URL 驱动的筛选状态：通过 `useSearchParams` + `router.replace()` 同步 URL 和组件状态，使筛选结果可书签和分享。

---

## Phase 2: 修复 Header 登录状态 bug `complete`

### 问题分析

Header 组件 (lines 98-227) 使用 `user ? ... : ...` 条件渲染，但未处理 `isLoading` 状态：

1. 页面加载时，`isLoading=true`, `user=null`
2. Header 显示登录/注册按钮（错误）
3. localStorage 检查完成后，`isLoading=false`, `user=authUser`
4. Header 重新渲染（正确状态）

这导致已登录用户在页面加载时会短暂看到登录/注册按钮。

### 修复方案

```tsx
{isLoading ? (
  // 骨架占位符，避免闪烁
  <div className="flex items-center gap-2">
    <div className="h-9 w-9 rounded-full bg-nf-secondary animate-pulse" />
  </div>
) : user ? (
  // 已登录 UI
) : (
  // 未登录 UI: 登录/注册按钮
)}
```

---

## Phase 3: 根因分析 `complete`

### 问题归类

| 类型 | 判定 |
|------|------|
| 测试用例缺失 | ✅ 无 TC 覆盖 Header 登录状态切换 |
| 用户旅程缺失 | ❌ J-001/J-002 已覆盖登录流程 |
| 实现问题 | ✅ 未处理 AuthContext 的 isLoading 状态 |

### 责任归属

| 阶段 | 问题 |
|------|------|
| Phase 7 (前端组件开发) | Header 组件未处理 loading 状态 |
| Phase 8 (E2E 测试) | 无登录状态切换的 E2E 测试 |

### 改进建议

1. 在 `specs/testcases/33-frontend-integration.md` 添加登录状态切换测试用例
2. 更新 `07-frontend-components.md` 添加 AuthContext loading 状态处理规范

---

## Phase 4: 研究 Figma skills `in_progress`

### 目标

从 `feat/prototype-v1` 分支获取以下 skills：
- figma-resource-extractor
- frontend-prototype-builder
- ui-spec-generator
- ux-spec-generator

### Figma 资源位置

`specs/design/figma/` 目录

### 待完成

- [ ] 检出 feat/prototype-v1 分支的 skills
- [ ] 分析每个 skill 的功能和依赖
- [ ] 评估与现有工作流的集成点

---

## Phase 5: 评估工作流集成 `pending`

根据 Phase 4 分析结果，确定：
- 哪些 skills 可以直接使用
- 需要哪些调整或配置
- 如何整合到 `docs/development-workflow.md`

---

## Phase 6: 验证与提交 `pending`

- [ ] 验证 Header 修复
- [ ] 提交所有更改
- [ ] 更新 progress.md
