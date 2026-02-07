# Task Plan: 工作流审查与修复

> **目标**: 审查整个开发工作流，修复过时的 Skills 引用，确保文档与实际一致
> **创建时间**: 2026-02-08
> **状态**: `complete`

## 背景

1. 用户修复了 19 个前端运行时错误 (d17ea88..4c8ce11)
2. 分析发现多个根本原因来自工作流和 Skills
3. 用户指出 `pen-to-react` 已废弃，项目中没有 .pen 文件
4. 需要全面审查工作流，移除过时内容

## 发现的问题

### 问题 1: pen-to-react 已废弃但仍被引用

**现状**：
- 项目中没有 .pen 文件
- 设计文档已迁移到 `specs/design/figma/*.md` (Figma 导出)
- `pen-to-react` skill 仍存在于 `.claude/skills/` 但无用

**被引用的位置**：

| 文件 | 引用内容 |
|------|---------|
| `CLAUDE.md` | Phase 7: [pen-to-react / openapi-to-components] |
| `CLAUDE.md` | Key Skills 表格 |
| `appendix-c-skills.md` | 可选 Skills 表格 |
| `findings.md` | 错误分析（我之前写的） |

### 问题 2: openapi-to-components 的实际使用

**现状**：
- `openapi-to-components` skill 仍存在
- 用途：将 OpenAPI spec 连接到前端组件
- 但目前前端组件主要手动编写或参考 Figma 设计

### 问题 3: 设计资源位置不明确

**现状**：
- 设计资源在 `specs/design/figma/` (18 个文件)
- 工作流 Phase 4 (UI 设计) 未提及 Figma 目录
- Phase 7 提到了 Figma 参考但不够清晰

## 阶段列表

| Phase | 描述 | 状态 | 完成度 |
|-------|------|------|--------|
| Phase 1 | 分析 19 个修复提交 | `complete` | 100% |
| Phase 2 | 更新工作流文档 (组件规范/国际化/路由) | `complete` | 100% |
| Phase 3 | 更新 CLAUDE.md (UI 文本规则) | `complete` | 100% |
| Phase 4 | 创建前端路由文档 | `complete` | 100% |
| Phase 5 | 移除 pen-to-react 引用 | `complete` | 100% |
| Phase 6 | 更新 Phase 4 (UI 设计) 文档 | `complete` | 100% |
| Phase 7 | 清理 findings.md 中的错误引用 | `complete` | 100% |
| Phase 8 | 验证工作流完整性 | `complete` | 100% |
| Phase 9 | 测试用例覆盖分析 | `complete` | 100% |
| Phase 10 | 总结与提交 | `complete` | 100% |

---

## Phase 5: 移除 pen-to-react 引用 `complete`

### 5.1 更新 CLAUDE.md

- [ ] 移除 Phase 7 中的 `[pen-to-react / openapi-to-components]`
- [ ] 改为 `[Figma 参考 / shadcn 组件]`
- [ ] 从 Key Skills 表格移除 `pen-to-react`

### 5.2 更新 appendix-c-skills.md

- [ ] 从可选 Skills 移除 `pen-to-react`
- [ ] 添加说明：设计资源已迁移到 Figma

### 5.3 更新 07-frontend-components.md

- [ ] 确认 7.0 Figma 设计参考正确
- [ ] 移除任何 .pen 文件引用

---

## Phase 6: 更新 Phase 4 (UI 设计) 文档 `complete`

- [ ] 6.1 明确设计资源位置 (`specs/design/figma/`)
- [ ] 6.2 添加 Figma 文件索引
- [ ] 6.3 说明设计到代码的工作流

---

## Phase 7: 清理 findings.md 中的错误引用 `complete`

- [ ] 7.1 移除 pen-to-react 相关分析
- [ ] 7.2 更正 UI 组件问题的责任归属
- [ ] 7.3 更新建议（不再建议更新 pen-to-react）

---

## Phase 8: 验证工作流完整性 `complete`

检查清单：

- [ ] 所有 skills 引用都指向实际存在的 skills
- [ ] 所有路径引用都正确
- [ ] 工作流图与文档一致
- [ ] CLAUDE.md 与 development-workflow 一致

---

## Phase 9: 测试用例覆盖分析 `complete`

**当前测试状态**：

| 测试类型 | 位置 | 状态 |
|----------|------|------|
| 后端 pytest | `app/tests/` | ✅ 390+ |
| 前端 Jest | `frontend/__tests__/` | ⚠️ 9 个 |
| E2E Playwright | 无 | ❌ 缺失 |

**specs/testcases 覆盖差距**：

| 测试用例 | 实现 |
|---------|------|
| 01-10 (后端) | ✅ 覆盖 |
| 11 (用户旅程) | ❌ 无 E2E |
| 33 (前端集成) | ⚠️ 部分 |

---

## Phase 10: 总结与提交 `complete`

- [x] 10.1 更新 progress.md
- [x] 10.2 提交所有更改 (17eac49)
- [x] 10.3 推送到远程

---

## 设计资源现状

**Figma 设计目录** (`specs/design/figma/`)：

```
specs/design/figma/
├── README.md         # 设计索引
├── assets.md         # 资源图标
├── components.md     # 组件库 (54 个)
├── icons.md          # 图标库 (69 个)
├── layouts.md        # 布局模板
└── pages/            # 页面设计 (14 个)
    ├── asset.md
    ├── auth.md
    ├── camp.md
    ├── content.md
    ├── explore.md
    ├── home.md
    ├── message.md
    ├── misc.md
    ├── planet.md
    ├── profile.md
    ├── search.md
    ├── settings.md
    └── team.md
```

---

## 错误记录

| 时间 | 错误 | 尝试 | 解决方案 |
|------|------|------|----------|
| - | - | - | - |
