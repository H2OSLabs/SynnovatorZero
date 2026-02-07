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

## 可选 Skills（特定场景）

| Skill | 用途 | 使用场景 |
|-------|------|---------|
| **synnovator** | 管理 .synnovator/*.md 文件数据 | 需要通过文件管理测试数据时 |
| **data-importer** | 从 .synnovator 导入数据到 SQLite | 需要从文件批量导入数据时 |
| **pen-to-react** | 从 .pen 设计文件转换 React 组件 | 有 .pen 设计稿时 |
| **journey-validator** | 验证 user-journeys 文档完整性 | 阶段 0.5 前 |

## 外部工具

| 工具 | 用途 | 说明 |
|------|------|------|
| **shadcn MCP 插件** | 检查 shadcn 组件是否可用 | 前端开发时优先使用 |
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
└── ...
```
