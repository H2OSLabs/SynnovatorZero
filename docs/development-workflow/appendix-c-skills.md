# 附录 C: Skills 参考

## 核心 Skills（必须使用）

| Skill | 用途 | 阶段 |
|-------|------|------|
| **planning-with-files** | 文件化规划：task_plan.md / findings.md / progress.md | 贯穿全流程 |
| **domain-modeler** | 从 user-journeys 提取领域模型 | 阶段 0.5 |
| **schema-to-openapi** | 从 docs/ + specs/ 生成 OpenAPI 规范 | 阶段 1 |
| **api-builder** | 从 OpenAPI 生成 FastAPI 后端 + TypeScript 客户端 | 阶段 2, 6 |
| **seed-designer** | 从 testcases 提取种子数据需求 | 阶段 2.5 |
| **tests-kit** | 测试用例管理：Guard 验证 / Insert 添加 | 贯穿全流程 |

## UI/UX 设计 Skills（阶段 4）

根据项目是否有 Figma 设计，选择对应分支的 skills：

### 分支 A: 有 Figma 设计

| Skill | 用途 | 输入 → 输出 |
|-------|------|-------------|
| **figma-resource-extractor** | 提取 Figma 设计资源 | Figma URL → `specs/design/figma/*.md` |
| **ui-spec-generator** | 生成 UI 规范 | Figma + testcases → `specs/design/pages.yaml` |
| **ux-spec-generator** | 生成 UX 交互规范 | pages.yaml → `specs/ux/` |
| **frontend-prototype-builder** | 构建前端原型 | pages.yaml + ux specs → 前端组件 |

### 分支 B: 无 Figma 设计

| Skill | 用途 | 输入 → 输出 |
|-------|------|-------------|
| **ai-ui-generator** | 从 User Journey 生成 UI/UX 设计 | user-journeys + testcases → `specs/design/pages.yaml` + `specs/ux/` |

> **分支选择逻辑**: 检查 `specs/design/figma/` 目录是否存在，或项目是否有 Figma 设计链接。

## 可选 Skills（特定场景）

| Skill | 用途 | 使用场景 |
|-------|------|---------|
| **synnovator** | 管理 .synnovator/*.md 文件数据 | 需要通过文件管理测试数据时 |
| **data-importer** | 从 .synnovator 导入数据到 SQLite | 需要从文件批量导入数据时 |
| **openapi-to-components** | 将 OpenAPI spec 连接到前端组件 | 需要自动生成 API 调用代码时 |
| **journey-validator** | 验证 user-journeys 文档完整性 | 阶段 0.5 前 |

> **注意**: `pen-to-react` skill 已废弃。项目设计资源已迁移到 Figma，位于 `specs/design/figma/`。

## 外部工具

| 工具 | 用途 | 说明 |
|------|------|------|
| **shadcn MCP 插件** | 检查 shadcn 组件是否可用 | 前端开发时优先使用 |
| **Figma MCP 插件** | 连接 Figma API | 需要配置 Figma Access Token |
| **Playwright** | E2E 端到端测试 | 阶段 8 |

## Skill 使用示例

### planning-with-files

```bash
# 初始化会话
bash .claude/skills/planning-with-files/scripts/init-session.sh ProjectName

# 会话恢复
python3 .claude/skills/planning-with-files/scripts/session-catchup.py "$(pwd)"

# 完成检查
bash .claude/skills/planning-with-files/scripts/check-complete.sh
```

### api-builder

```bash
# 生成后端
uv run python .claude/skills/api-builder/scripts/cli.py \
  --spec .synnovator/openapi.yaml \
  --output app \
  --setup-alembic \
  --run-migrations

# 生成前端客户端
uv run python .claude/skills/api-builder/scripts/cli.py \
  --spec .synnovator/openapi.yaml \
  --output app \
  --generate-client \
  --client-output frontend/lib/

# 冲突处理
--conflict-strategy skip|backup|overwrite
--dry-run  # 预览
```

### tests-kit

```bash
# Guard 模式：验证测试用例
uv run python .claude/skills/tests-kit/scripts/check_testcases.py

# Insert 模式：添加测试用例（交互式）
```

### schema-to-openapi

```bash
uv run python .claude/skills/schema-to-openapi/scripts/generate_openapi.py \
  --output .synnovator/openapi.yaml \
  --title "Synnovator API" \
  --version "1.0.0" \
  --format yaml
```

### seed-designer

```bash
uv run python .claude/skills/seed-designer/scripts/extract_requirements.py
```

### figma-resource-extractor (分支 A)

```bash
# 调用 skill，提供 Figma URL
# 输出到 specs/design/figma/
```

### ai-ui-generator (分支 B)

```bash
# 调用 skill
# 读取: docs/user-journeys/*.md, specs/testcases/*.md
# 输出: specs/design/pages.yaml, specs/ux/
```

## 文件结构

```
.claude/skills/
├── planning-with-files/
│   ├── README.md
│   ├── templates/
│   └── scripts/
├── api-builder/
│   ├── README.md
│   ├── assets/
│   └── scripts/
├── schema-to-openapi/
│   └── scripts/
├── domain-modeler/
│   └── scripts/
├── seed-designer/
│   └── scripts/
├── tests-kit/
│   └── scripts/
├── figma-resource-extractor/    # 分支 A
│   └── SKILL.md
├── ui-spec-generator/           # 分支 A
│   └── SKILL.md
├── ux-spec-generator/           # 分支 A
│   └── SKILL.md
├── frontend-prototype-builder/  # 分支 A
│   └── SKILL.md
└── ai-ui-generator/             # 分支 B
    ├── SKILL.md
    └── references/
        ├── component-catalog.md
        ├── layout-patterns.md
        ├── interaction-patterns.md
        └── neon-forge-tokens.md
```

## 双分支工作流图

```
阶段 0-3: 后端开发 (domain-modeler, api-builder, seed-designer)
                    ↓
┌───────────────────────────────────────────────────────┐
│ 阶段 4: UI/UX 设计检测                                  │
│ 检查: specs/design/figma/ 或 Figma URL 存在?           │
└───────────────────────────┬───────────────────────────┘
                            │
         ┌──────────────────┴──────────────────┐
         ↓                                     ↓
┌────────────────────┐              ┌────────────────────┐
│ 分支 A: 有 Figma    │              │ 分支 B: 无 Figma    │
│                    │              │                    │
│ figma-resource-    │              │ ai-ui-generator    │
│   extractor        │              │                    │
│       ↓            │              └─────────┬──────────┘
│ ui-spec-generator  │                        │
│       ↓            │                        │
│ ux-spec-generator  │                        │
└─────────┬──────────┘                        │
          │                                   │
          └───────────────┬───────────────────┘
                          │
                specs/design/pages.yaml
                specs/ux/
                          │
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 阶段 7: 前端组件开发                                      │
│ frontend-prototype-builder (统一使用 pages.yaml)         │
└─────────────────────────────────────────────────────────┘
                          ↓
阶段 8-9: E2E 测试、集成验证
```
