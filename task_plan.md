# Task Plan: 前端开发工作流双分支设计

> **目标**: 设计支持有/无 Figma 两种情况的前端开发工作流
> **创建时间**: 2026-02-08
> **状态**: `in_progress`

## 背景

前端开发需要 UI/UX 设计输入，但并非所有项目都有 Figma 设计。需要设计双分支工作流：

1. **分支 A (有 Figma)**：使用 4 个 Figma skills 自动化
2. **分支 B (无 Figma)**：使用 AI 工具生成 UI/UX 设计

## 阶段列表

| Phase | 描述 | 状态 |
|-------|------|------|
| Phase 1 | 复制 Figma skills 到当前分支 | `complete` |
| Phase 2 | 研究 AI 生成 UI/UX 的替代工具 | `complete` |
| Phase 3 | 设计 AI UI Generator skill | `complete` |
| Phase 4 | 更新工作流文档（双分支） | `complete` |
| Phase 5 | 集成测试 | `pending` |
| Phase 6 | 提交与文档化 | `pending` |

---

## Phase 1: 复制 Figma skills 到当前分支 `complete`

### 目标

从 `feat/prototype-v1` 分支复制以下 skills：

| Skill | 来源路径 |
|-------|----------|
| `figma-resource-extractor` | `.claude/skills/figma-resource-extractor/` |
| `ui-spec-generator` | `.claude/skills/ui-spec-generator/` |
| `ux-spec-generator` | `.claude/skills/ux-spec-generator/` |
| `frontend-prototype-builder` | `.claude/skills/frontend-prototype-builder/` |

### 执行命令

```bash
# 复制 skills
git checkout feat/prototype-v1 -- .claude/skills/figma-resource-extractor
git checkout feat/prototype-v1 -- .claude/skills/ui-spec-generator
git checkout feat/prototype-v1 -- .claude/skills/ux-spec-generator
git checkout feat/prototype-v1 -- .claude/skills/frontend-prototype-builder
```

---

## Phase 2: 研究 AI 生成 UI/UX 的替代工具 `complete`

### 研究目标

| 工具类型 | 候选 | 评估要点 |
|----------|------|----------|
| 设计工具 MCP | Pixso, Sketch | API 可用性、MCP 支持 |
| AI 设计生成 | v0.dev, Galileo AI | 输入格式、输出质量 |
| 开源库 | Penpot, Excalidraw | 自托管、API 能力 |
| LLM 直接生成 | Claude + shadcn/ui | 无需外部工具 |

### 评估标准

1. **输入兼容性**：能否从 User Journey / 需求文档生成
2. **输出格式**：能否生成 pages.yaml 或等效结构
3. **可集成性**：MCP / API / CLI 可用
4. **成本**：免费/付费、API 配额

---

## Phase 3: 设计 AI UI Generator skill `complete`

### 功能需求

```
输入:
  - docs/user-journeys/*.md
  - specs/testcases/*.md
  - Design system (shadcn/ui + Neon Forge theme)

输出:
  - specs/design/pages.yaml (与 ui-spec-generator 输出兼容)
  - specs/ux/ (与 ux-spec-generator 输出兼容)
```

### Skill 结构

```
.claude/skills/ai-ui-generator/
├── SKILL.md
├── references/
│   ├── component-catalog.md    # 可用组件列表
│   ├── layout-patterns.md      # 常见布局模式
│   └── interaction-patterns.md # 交互模式库
└── templates/
    ├── pages.yaml.j2
    └── ux-spec.yaml.j2
```

---

## Phase 4: 更新工作流文档（双分支） `complete`

### 目标

修改 `docs/development-workflow.md`，在 Phase 4-7 添加条件分支：

```
Phase 4: UI/UX 设计
├── IF Figma 设计存在 (specs/design/figma/ 或 Figma URL)
│   ├── 4.1 figma-resource-extractor
│   ├── 4.2 ui-spec-generator
│   └── 4.3 ux-spec-generator
│
└── ELSE 无 Figma 设计
    └── 4.1 ai-ui-generator (从 User Journey 生成)

Phase 7: 前端组件开发
└── 7.1 frontend-prototype-builder (统一使用 pages.yaml)
```

---

## Phase 5: 集成测试 `pending`

### 测试场景

1. **有 Figma 分支**：使用现有 `specs/design/figma/` 测试完整流程
2. **无 Figma 分支**：从 `docs/user-journeys/` 生成 UI 设计

---

## Phase 6: 提交与文档化 `pending`

- [ ] 提交所有新 skills
- [ ] 更新 CLAUDE.md
- [ ] 更新工作流文档
- [ ] 添加使用示例

---

## 双分支工作流设计图

```
                    ┌─────────────────────────────┐
                    │ Phase 0-3: 后端开发         │
                    │ (domain-modeler, api-builder)│
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │ Phase 4: UI/UX 设计检测      │
                    │ 检查: specs/design/figma/    │
                    │       或 Figma URL 存在?     │
                    └──────────────┬──────────────┘
                                   │
              ┌────────────────────┴────────────────────┐
              │                                         │
    ┌─────────▼─────────┐                     ┌────────▼─────────┐
    │ 分支 A: 有 Figma   │                     │ 分支 B: 无 Figma  │
    ├───────────────────┤                     ├──────────────────┤
    │ figma-resource-   │                     │ ai-ui-generator  │
    │   extractor       │                     │ (从 User Journey │
    │        ↓          │                     │  生成 UI 设计)   │
    │ ui-spec-generator │                     │                  │
    │        ↓          │                     │                  │
    │ ux-spec-generator │                     │                  │
    └─────────┬─────────┘                     └────────┬─────────┘
              │                                        │
              │     specs/design/pages.yaml            │
              │     specs/ux/                          │
              └────────────────┬───────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Phase 7: 前端实现    │
                    │ frontend-prototype- │
                    │   builder           │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Phase 8-9: 测试验证  │
                    └─────────────────────┘
```
