# Synnovator 完整开发流程

## 概述

从需求设计到前后端实现和测试的完整开发流程。本流程涵盖数据建模、代码生成、数据注入、后端实现、前端集成（不含 UI 组件）和全栈测试。

> **重要约定：**
> - 后端包名为 `app/`（与 api-builder 模板一致，标准 FastAPI 项目结构）。所有 Python 命令使用 `uv run python` 执行。
> - 本流程较长，建议使用 **planning-with-files** skill 将流程拆分为更小的可管理阶段，防止上下文用尽或意外中断导致进度丢失。
> - 每个阶段开发完成后，使用 **tests-kit** skill 进行增量测试，及时发现和修复问题，不要积压到最后统一测试。

## 本地开发数据（Seed）

前端页面（如活动卡片列表）依赖后端返回的内容。仓库提供了可重复执行的本地种子数据脚本：

```bash
make resetdb
make seed
```

前端默认会请求 `http://127.0.0.1:8000/api`，请确保后端服务已启动（`make backend` 或 `make start`）。

## 完整工作流图

```
═══════════════════════════════════════════════════════════════════
║ 贯穿全流程: planning-with-files skill                           ║
║  - 每个阶段开始前: 更新 task_plan.md (规划当前阶段)               ║
║  - 每个阶段结束后: 更新 progress.md (记录完成情况)               ║
║  - 研究发现时: 更新 findings.md (保存发现和决策)                 ║
║  - 意外中断后: 从文件恢复上下文，继续执行                        ║
═══════════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────────┐
│ 阶段 0: 项目初始化                                              │
│  - 定义技术栈                                                   │
│  - 创建项目结构                                                 │
│  - 配置开发环境                                                 │
│  - [planning-with-files] 初始化规划文件                         │
└────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────┐
│ 阶段 1: 需求设计与数据建模                                      │
│  数据源:                                                       │
│      ├─→ synnovator skill (完整原型能力参考)                   │
│      ├─→ docs/ (功能说明文档)                                  │
│      └─→ specs/ (开发规范文档)                                 │
│                                                                │
│  [手工] 创建示例数据                                            │
│      ↓ [synnovator skill]                                     │
│  .synnovator/*.md (测试数据)                                   │
│                                                                │
│  [schema-to-openapi skill] ← 读取 synnovator + docs + specs   │
│      ↓                                                        │
│  OpenAPI 3.x 规范 (.synnovator/openapi.yaml)                  │
│                                                                │
│  ✅ [tests-kit] 验证数据模型测试用例                             │
└────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────┐
│ 阶段 2: 后端代码生成                                            │
│  [api-builder skill]                                          │
│      ↓                                                        │
│  FastAPI 后端 (app/)                                           │
│      ├─→ models/ (SQLAlchemy ORM)                            │
│      ├─→ schemas/ (Pydantic 验证)                            │
│      ├─→ routers/ (FastAPI 路由)                             │
│      ├─→ crud/ (CRUD 操作)                                   │
│      └─→ tests/ (pytest 测试)                                │
│                                                                │
│  [api-builder --setup-alembic --run-migrations]               │
│      ↓                                                        │
│  SQLite database (空表结构)                                    │
│                                                                │
│  ✅ [tests-kit] 按模块增量测试后端代码                           │
│      ├─→ 用户模块完成 → 测试用户模块                           │
│      ├─→ 活动模块完成 → 测试活动模块                           │
│      └─→ 每完成一个模块，立即运行对应测试                       │
└────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────┐
│ 阶段 3: 数据注入                                                │
│  .synnovator/*.md                                              │
│      ↓ [data-importer skill]                                  │
│  SQLite database (填充测试数据)                                │
│      ├─→ 按依赖顺序导入 (user → post → relations)             │
│      ├─→ 类型转换 (datetime, JSON, enum)                     │
│      └─→ 跳过重复记录                                         │
│                                                                │
│  ✅ [tests-kit] 验证导入数据与测试用例一致                       │
└────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────┐
│ 阶段 4: 前端客户端生成                                          │
│  [前置] 安装 Tailwind CSS + shadcn/ui                          │
│                                                                │
│  [api-builder --generate-client]                              │
│      ↓                                                        │
│  TypeScript API Client                                        │
│      ├─→ 类型定义 (从 OpenAPI schemas)                       │
│      ├─→ API 方法 (从 OpenAPI paths)                         │
│      └─→ 错误处理                                             │
│                                                                │
│  集成到 Next.js                                                │
│      ↓                                                        │
│  frontend/lib/api/api-client.ts                               │
│                                                                │
│  ✅ [tests-kit] 验证前端集成测试用例                             │
└────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────┐
│ 阶段 5: 最终集成验证                                            │
│  全栈集成测试（前面各阶段已完成模块级测试）                       │
│      ├─→ 启动 FastAPI + Next.js 服务                         │
│      ├─→ 端到端用户旅程测试                                   │
│      └─→ 数据一致性验证                                       │
│                                                                │
│  ✅ [tests-kit] 最终 Guard 检查，确保所有测试用例通过            │
└────────────────────────────────────────────────────────────────┘
```

## 使用的 Skills

| Skill | 用途 | 状态 |
|-------|------|------|
| **planning-with-files** | 文件化规划：创建 task_plan.md / findings.md / progress.md，防止上下文丢失和中断失忆 | ✅ 可用 |
| **synnovator** | 管理 .synnovator/*.md 文件数据（CRUD），是平台原型能力的完整参考实现 | ✅ 可用 |
| **schema-to-openapi** | 从 synnovator skill + docs/ + specs/ 综合生成 OpenAPI 3.0 规范 | ✅ 可用 |
| **api-builder** | 从 OpenAPI 生成 FastAPI 后端 + 迁移 + 测试 + TypeScript 客户端 | ✅ 可用 |
| **data-importer** | 从 .synnovator 导入数据到 SQLite | ✅ 可用 |
| **tests-kit** | 增量测试管理：Guard 模式验证已有测试用例，Insert 模式添加新测试用例 | ✅ 可用 |

---

## 模块开发顺序（底层到上层依赖图）

> **核心原则：从零依赖的底层模块开始，逐层向上开发。每完成一层，立即测试该层对应的测试用例。**
> 本节定义了模块间的依赖关系和推荐开发顺序。具体的执行进度追踪请使用 `task_plan.md`（由 planning-with-files 管理）。

### 依赖关系图

```
┌─────────────── Layer 0: 零依赖基础 ───────────────┐
│   user (用户)          resource (资源)              │
│   零外部依赖            零外部依赖                   │
└──────────┬─────────────────┬──────────────────────┘
           │                 │
           ▼                 │
┌─────────────── Layer 1: 仅依赖 user ──────────────┐
│   rule (规则)   group (团队)   category (活动)     │
│   ← user        ← user        ← user              │
└──────────┬─────────┬──────────┬───────────────────┘
           │         │          │
           ▼         ▼          ▼
┌─────────────── Layer 2: 依赖 Layer 0-1 ───────────┐
│   post (帖子)          interaction (交互)           │
│   ← user, resource     ← user                     │
└──────────┬──────────────┬─────────────────────────┘
           │              │
           ▼              ▼
┌─────────────── Layer 3: 简单关系 ─────────────────┐
│   group_user     user_user      post_resource     │
│   post_post      (无规则引擎, 无复杂校验)           │
└──────────┬────────────────────────────────────────┘
           │
           ▼
┌─────────────── Layer 4: 复杂关系 ─────────────────┐
│   category_rule       target_interaction           │
│   category_post (含规则引擎校验)                    │
│   category_group (含前置条件检查)                   │
└──────────┬────────────────────────────────────────┘
           │
           ▼
┌─────────────── Layer 5: 高级图关系 ───────────────┐
│   category_category                                │
│   (阶段/赛道/前置条件, 含环检测)                    │
└──────────┬────────────────────────────────────────┘
           │
           ▼
┌─────────────── Layer 6: 跨切面功能 ───────────────┐
│   软删除 + 级联删除      权限层                    │
│   声明式规则引擎          缓存字段维护              │
└──────────┬────────────────────────────────────────┘
           │
           ▼
┌─────────────── Layer 7: 集成验证 ─────────────────┐
│   13 个用户旅程端到端测试                           │
│   高级功能: 资源转移、评分排名、证书发放            │
└───────────────────────────────────────────────────┘
```

### 各层详细内容与测试映射

| Layer | 模块 | 依赖 | 测试用例 |
|-------|------|------|----------|
| **0** | user CRUD + 唯一性校验 | 无 | TC-USER-001~020, 900~903 |
| **0** | resource CRUD + 文件存储 | 无 | TC-RES-001~011, 900~901 |
| **1** | rule CRUD + scoring_criteria | user | TC-RULE-001~011, 900~901 |
| **1** | group CRUD + 成员角色定义 | user | TC-GRP-001~011, 900~901 |
| **1** | category CRUD + 状态机 | user | TC-CAT-001~011, 900~902 |
| **2** | post CRUD + 缓存字段 + 状态机 | user, resource | TC-POST-001~076, 900~903 |
| **2** | interaction CRUD (点赞/评论/评分) | user | TC-IACT-001~063, 900~905 |
| **3** | group_user 关系 + 审批流程 | group, user | TC-REL-GU-*, TC-GRP-020~025 |
| **3** | user_user 关系 (关注/屏蔽) | user | TC-FRIEND-001~010, 900~902 |
| **3** | post_resource 关系 | post, resource | TC-REL-PR-* |
| **3** | post_post 关系 (引用/回复/嵌入) | post | TC-REL-PP-* |
| **4** | category_rule 关系 | category, rule | TC-REL-CR-* |
| **4** | target_interaction (多态绑定 + 缓存更新) | interaction, post/category/resource | TC-REL-TI-*, TC-IACT-020~025 |
| **4** | category_post (含规则引擎校验) | category, post, rule | TC-REL-CP-*, TC-RULE-100~109, TC-ENTRY-* |
| **4** | category_group (含前置条件) | category, group | TC-REL-CG-*, TC-PERM-020~025 |
| **5** | category_category (阶段/赛道/前置条件 + 环检测) | category | TC-STAGE-*, TC-TRACK-*, TC-PREREQ-*, TC-CATREL-* |
| **6** | 软删除 + 级联删除 | 全部内容类型和关系 | TC-DEL-001~022 |
| **6** | 权限层 + 可见性控制 | user, 全部类型 | TC-PERM-001~025 |
| **6** | 声明式规则引擎 | rule, category | TC-ENGINE-001~061 |
| **7** | 用户旅程集成测试 | 全部 | TC-JOUR-002~013 |
| **7** | 闭幕规则 | category, rule | TC-CLOSE-001~040, 900~902 |
| **7** | 资源转移 | resource, post | TC-TRANSFER-001~004 |

### 开发节奏

```
每个 Layer 的开发循环:

  1. [planning-with-files] 更新 task_plan.md → 标记当前 Layer
  2. [api-builder 或手工] 开发该 Layer 的模块代码
  3. [tests-kit Guard] 运行该 Layer 对应的测试用例
  4. [planning-with-files] 更新 progress.md → 记录结果
  5. 如有失败 → 修复 → 重新测试 → 记录到 findings.md
  6. 全部通过 → 进入下一个 Layer
```

---

## 详细步骤

### 阶段 0: 项目初始化

#### 0.1 创建项目结构

```bash
# 项目目录结构
SynnovatorZero/
├── app/                  # FastAPI 后端（由 api-builder 生成，包名 app）
├── frontend/             # Next.js 前端
├── .synnovator/          # 文件数据存储 + OpenAPI spec
├── .claude/skills/       # Claude Code skills（synnovator 是原型参考实现）
├── docs/                 # 功能说明文档
│   ├── data-types.md     #   7 种内容类型字段定义
│   ├── relationships.md  #   9 种关系类型定义
│   ├── crud-operations.md #  CRUD 操作与权限矩阵
│   ├── user-journeys.md  #   13 个用户旅程
│   ├── rule-engine.md    #   声明式规则引擎规范
│   ├── examples.md       #   数据操作示例
│   └── development-workflow.md  # 本文档
├── specs/                # 开发规范文档
│   ├── data-integrity.md #   数据完整性约束
│   ├── data-indexing.md  #   数据库索引建议
│   ├── data-normalization.md # 反范式化决策
│   ├── cache-strategy.md #   缓存字段维护策略
│   ├── spec-guideline.md #   AI agent 规范编写指南
│   ├── testcases/        #   246 个测试用例（17 个模块）
│   └── ui/               #   Neon Forge 设计系统
├── deploy/               # Docker & 部署配置
├── pyproject.toml        # Python 依赖
├── uv.toml               # UV 包管理器配置
└── Makefile              # 构建命令
```

> **为什么是 `app/` 而不是 `backend/`？**
> api-builder 的 Jinja2 模板在 17 处硬编码了 `from app.xxx` 的导入路径。
> 使用 `app/` 作为包名可以零修改地使用 api-builder 生成的代码，是原型开发最高效的方案。
> 这也是 FastAPI 官方教程使用的标准命名。

#### 0.2 配置开发环境

```bash
# 安装 Python 依赖管理工具
# curl -LsSf https://astral.sh/uv/install.sh | sh  (已安装则跳过)

# 安装 Node.js (使用 nvm)
nvm install 18
nvm use 18

# 同步所有 Python 依赖
uv sync

# 安装前端依赖
cd frontend && npm install
```

**已安装的 Python 依赖：**
- fastapi, uvicorn, sqlalchemy (后端核心)
- pyyaml, jinja2 (skill 脚本依赖)
- alembic (数据库迁移)
- pytest, httpx (测试)

#### 0.3 初始化开发规划（planning-with-files）

> **每次开始新的开发会话时执行**，确保进度不会因上下文用尽或意外中断而丢失。

使用 **planning-with-files** skill 创建三个规划文件：

```bash
# 初始化规划文件（在项目根目录）
bash .claude/skills/planning-with-files/scripts/init-session.sh SynnovatorZero
```

生成三个文件：

| 文件 | 用途 | 更新时机 |
|------|------|----------|
| `task_plan.md` | 阶段规划与进度追踪 | 每个阶段开始/结束时 |
| `findings.md` | 研究发现与技术决策记录 | 每次有新发现时（2-Action 规则） |
| `progress.md` | 会话执行日志 | 每完成一个操作时 |

**会话恢复（中断后继续）：**

```bash
# 从规划文件恢复上下文
python3 .claude/skills/planning-with-files/scripts/session-catchup.py "$(pwd)"
```

**使用要点：**
- 每个阶段开始前，更新 `task_plan.md` 中的 `Current Phase`
- 每个阶段结束后，标记该阶段为 `complete`，记录到 `progress.md`
- 遇到错误时，记录到 `task_plan.md` 的 `Errors Encountered` 部分
- 3 次尝试失败后升级处理（3-Strike Protocol）

---

### 阶段 1: 需求设计与数据建模

#### 1.1 定义数据模型

数据模型的完整定义分布在三个位置，schema-to-openapi 会综合读取：

| 数据源 | 位置 | 内容 |
|--------|------|------|
| **synnovator skill** | `.claude/skills/synnovator/` | 原型参考实现（SKILL.md + references/ + scripts/endpoints/） |
| **功能说明文档** | `docs/` | data-types.md、relationships.md、crud-operations.md、rule-engine.md 等 |
| **开发规范文档** | `specs/` | data-integrity.md、cache-strategy.md、testcases/ 等 |

> synnovator skill 的能力就是我们想要的原型能力，它包含 7 种内容类型、9 种关系类型、
> 规则引擎、级联删除、缓存维护、权限系统等完整实现。

**7 种内容类型：**
- **user**: 用户账户
- **category**: 活动/竞赛
- **post**: 用户帖子（支持多种 type）
- **rule**: 活动规则（含声明式规则引擎）
- **resource**: 文件资源
- **group**: 团队/分组
- **interaction**: 交互记录（点赞、评论、评分）

**9 种关系类型：**
- **category_rule**: 活动-规则绑定
- **category_post**: 活动-帖子关联（报名/提交）
- **category_group**: 团队-活动报名
- **category_category**: 活动间关联（阶段/赛道/前置条件）
- **post_post**: 帖子间关联（引用/回复/嵌入）
- **post_resource**: 帖子-资源关联
- **group_user**: 成员-团队关系（含审批流程）
- **user_user**: 用户间关系（关注/屏蔽）
- **target_interaction**: 内容-交互绑定

详细字段定义见 `docs/data-types.md` 和 `docs/relationships.md`。
CRUD 操作与权限见 `docs/crud-operations.md`。
数据完整性约束见 `specs/data-integrity.md`。

#### 1.2 创建示例数据

使用 **synnovator skill** 创建测试数据：

```bash
# 创建用户
uv run python .claude/skills/synnovator/scripts/engine.py \
  --user admin create user \
  --data '{"username": "alice", "email": "alice@example.com", "display_name": "Alice", "role": "participant"}'

uv run python .claude/skills/synnovator/scripts/engine.py \
  --user admin create user \
  --data '{"username": "bob", "email": "bob@example.com", "display_name": "Bob", "role": "organizer"}'

# 创建活动
uv run python .claude/skills/synnovator/scripts/engine.py \
  --user user_xxx create category \
  --data '{"name": "2025 AI Hackathon", "description": "AI innovation competition", "type": "competition", "status": "published"}' \
  --body "# Welcome\n\nJoin us for an AI innovation competition!"

# 创建帖子
uv run python .claude/skills/synnovator/scripts/engine.py \
  --user user_xxx create post \
  --data '{"title": "My AI Project", "type": "for_category", "tags": ["ai", "demo"], "status": "published"}' \
  --body "## Project Description\n\nThis is my AI project."

# 创建团队
uv run python .claude/skills/synnovator/scripts/engine.py \
  --user user_xxx create group \
  --data '{"name": "Team Synnovator", "description": "Our team", "visibility": "public", "require_approval": false}'

# 创建关系（团队成员）
uv run python .claude/skills/synnovator/scripts/engine.py \
  --user user_xxx create group_user \
  --data '{"group_id": "grp_xxx", "user_id": "user_xxx", "role": "owner", "status": "accepted"}'
```

数据文件存储在 `.synnovator/` 目录：

```
.synnovator/
├── user/
│   ├── user_alice.md
│   └── user_bob.md
├── category/
│   └── cat_hackathon.md
├── post/
│   └── post_myproject.md
├── group/
│   └── grp_team.md
└── relations/
    └── group_user/
        └── grp_team_user_alice.md
```

#### 1.3 生成 OpenAPI 规范

> **每次进入阶段 2 前必须重新生成**，确保 OpenAPI spec 与数据模型保持同步。

**使用 schema-to-openapi skill**

schema-to-openapi 现在综合读取整个 synnovator skill 以及 docs/ 和 specs/ 文档来生成 OpenAPI 规范：

**输入数据源（按优先级）：**
1. **synnovator skill** — 完整原型参考实现
   - `SKILL.md`: 能力描述和触发条件
   - `references/schema.md`: 字段定义表格（结构化数据源）
   - `references/endpoints.md`: API 端点和用法示例
   - `scripts/endpoints/*.py`: 7 个内容类型的具体实现（默认值、验证、级联）
2. **docs/ 功能文档** — 业务需求
   - `data-types.md`: 内容类型完整字段定义
   - `relationships.md`: 关系类型定义
   - `crud-operations.md`: CRUD 操作与权限矩阵
   - `rule-engine.md`: 声明式规则引擎规范
   - `user-journeys.md`: 13 个用户旅程
3. **specs/ 规范文档** — 技术约束
   - `data-integrity.md`: 唯一性约束、软删除、级联规则
   - `cache-strategy.md`: 缓存字段维护策略

```bash
# 从 synnovator skill + docs/ + specs/ 综合生成 OpenAPI 规范
uv run python .claude/skills/schema-to-openapi/scripts/generate_openapi.py

# 指定输出路径和格式
uv run python .claude/skills/schema-to-openapi/scripts/generate_openapi.py \
  --output .synnovator/openapi.yaml \
  --title "Synnovator API" \
  --version "1.0.0" \
  --format yaml
```

**输出：** `.synnovator/openapi.yaml`

生成的规范包括:
- 7 种内容类型的 CRUD endpoints (`/users`, `/categories`, `/posts`, 等)
- 9 种关系类型的嵌套 endpoints (`/categories/{id}/posts`, `/posts/{id}/comments`, 等)
- 交互 endpoints (点赞、评论、评分)
- 用户关系 endpoints（关注/屏蔽）
- 活动关联 endpoints（阶段/赛道/前置条件）
- 管理批量操作
- OAuth2 认证配置

#### 1.4 增量测试：验证数据模型（tests-kit）

> 阶段 1 完成后，立即运行 tests-kit Guard 模式验证测试用例。

```bash
# 验证所有测试用例格式和一致性
uv run python .claude/skills/tests-kit/scripts/check_testcases.py
```

**测试范围：** 验证 `specs/testcases/` 中的数据模型相关测试用例（01-07）是否与当前 schema 一致。

如果修改了数据模型，需检查受影响的测试用例：

| 修改内容 | 受影响的测试用例前缀 |
|----------|---------------------|
| 内容类型字段 | TC-USER, TC-CAT, TC-RULE, TC-GRP, TC-POST, TC-RES, TC-IACT |
| 关系类型 | TC-REL-* |
| 权限规则 | TC-PERM-* |
| 规则引擎 | TC-ENGINE-*, TC-ENTRY-*, TC-CLOSE-* |

---

### 阶段 2: 后端代码生成

#### 2.1 使用 api-builder 生成后端

**前提**: 已使用 schema-to-openapi 重新生成 OpenAPI 规范

```bash
# 从生成的 OpenAPI 规范创建后端（输出到 app/ 目录）
uv run python .claude/skills/api-builder/scripts/cli.py \
  --spec .synnovator/openapi.yaml \
  --output app \
  --setup-alembic \
  --run-migrations
```

**生成内容：**

```
app/
├── models/               # SQLAlchemy ORM 模型
│   ├── __init__.py
│   ├── user.py
│   ├── category.py
│   ├── post.py
│   └── ...
├── schemas/              # Pydantic 验证 schemas
│   ├── __init__.py
│   ├── user.py
│   ├── category.py
│   └── ...
├── routers/              # FastAPI 路由
│   ├── __init__.py
│   ├── users.py
│   ├── categories.py
│   └── ...
├── crud/                 # CRUD 操作
│   ├── __init__.py
│   ├── base.py
│   └── user.py
├── tests/                # pytest 测试
│   ├── conftest.py
│   ├── test_api/
│   └── test_crud/
├── alembic/              # 数据库迁移
│   ├── versions/
│   └── env.py
├── main.py               # FastAPI 应用入口
├── database.py           # 数据库配置
└── alembic.ini           # Alembic 配置
```

#### 2.2 验证生成的代码

```bash
# 查看数据库表
sqlite3 data/synnovator.db ".tables"

# 预期输出: user category post rule resource group interaction ...

# 启动开发服务器
uv run uvicorn app.main:app --reload --port 8000

# 或使用 Makefile
make backend
```

访问 http://localhost:8000/docs 查看 Swagger API 文档。

#### 2.3 补充业务逻辑

生成的代码包含 TODO 注释，标记需要补充的部分：

```python
# app/routers/users.py
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # TODO: 添加业务逻辑
    # - 验证用户名/邮箱唯一性
    # - 密码哈希
    # - 发送欢迎邮件
    return crud_user.create(db, user)
```

补充要点：
- 认证/授权逻辑（JWT、OAuth）
- 业务验证规则
- 错误处理
- 日志记录

#### 2.4 增量测试：按模块测试后端代码（tests-kit）

> **核心原则：每完成一个模块，立即测试该模块，不要积压到最后。**

```bash
# 用户模块开发完成后，测试用户相关用例
uv run pytest app/tests/test_api/test_users_api.py -v
# 同时运行 tests-kit Guard 检查 TC-USER-* 用例
uv run python .claude/skills/tests-kit/scripts/check_testcases.py

# 活动模块开发完成后，测试活动相关用例
uv run pytest app/tests/test_api/test_categories_api.py -v

# 帖子模块开发完成后，测试帖子相关用例
uv run pytest app/tests/test_api/test_posts_api.py -v

# 依次类推...每个模块完成后立即测试
```

**增量测试顺序（推荐）：**

| 开发顺序 | 模块 | 对应测试用例 |
|----------|------|-------------|
| 1 | 用户 (user) | TC-USER-001~020, TC-PERM-001~025 |
| 2 | 活动 (category) | TC-CAT-001~020 |
| 3 | 规则 (rule) | TC-RULE-001~020, TC-ENGINE-* |
| 4 | 团队 (group) | TC-GRP-001~020 |
| 5 | 帖子 (post) | TC-POST-001~076 |
| 6 | 资源 (resource) | TC-RES-001~045 |
| 7 | 交互 (interaction) | TC-IACT-001~063 |
| 8 | 关系 (relations) | TC-REL-* |
| 9 | 级联删除 | TC-DEL-* |
| 10 | 用户旅程 | TC-JOUR-* |

> 更新 `progress.md` 记录每个模块的测试结果。

---

### 阶段 3: 数据注入

#### 3.1 使用 data-importer 导入测试数据

```bash
# 导入所有数据
uv run python .claude/skills/data-importer/scripts/cli.py import \
  --source .synnovator \
  --db data/synnovator.db \
  --models app/models

# 只导入特定类型
uv run python .claude/skills/data-importer/scripts/cli.py import \
  --source .synnovator \
  --db data/synnovator.db \
  --models app/models \
  --types user,post,category
```

**导入过程：**
1. 解析 `.synnovator/*.md` 文件（YAML frontmatter + Markdown body）
2. 按依赖顺序导入：
   - Phase 1: user, category, rule
   - Phase 2: group, post, resource
   - Phase 3: interaction
   - Phase 4: 所有关系类型
3. 自动类型转换（datetime, JSON, enum）
4. 跳过已存在记录（基于 ID）
5. 生成导入报告

#### 3.2 验证导入结果

```bash
# 查看导入的数据
sqlite3 data/synnovator.db << EOF
SELECT COUNT(*) FROM user;
SELECT COUNT(*) FROM post;
SELECT COUNT(*) FROM category;
SELECT * FROM user LIMIT 3;
EOF
```

#### 3.3 数据更新流程

**场景 1: 添加新的测试数据**

```bash
# 1. 使用 synnovator engine 创建新数据
uv run python .claude/skills/synnovator/scripts/engine.py \
  --user user_xxx create post \
  --data '{"title": "New Post", "type": "general"}' \
  --body "New content..."

# 2. 重新导入（增量模式，自动跳过已存在记录）
uv run python .claude/skills/data-importer/scripts/cli.py import \
  --source .synnovator \
  --db data/synnovator.db \
  --models app/models
```

**场景 2: 更新现有数据**

```bash
# 1. 使用 synnovator engine 更新
uv run python .claude/skills/synnovator/scripts/engine.py \
  update post --id post_xxx \
  --data '{"status": "published"}'

# 2. 清空数据库重新导入
rm data/synnovator.db
cd app && uv run alembic upgrade head && cd ..
uv run python .claude/skills/data-importer/scripts/cli.py import \
  --source .synnovator \
  --db data/synnovator.db \
  --models app/models
```

#### 3.4 增量测试：验证导入数据（tests-kit）

> 数据注入完成后，验证导入的数据是否与测试用例中描述的场景一致。

```bash
# 运行后端 API 测试（验证导入数据可通过 API 正确访问）
uv run pytest app/tests/ -v

# 运行 tests-kit Guard 检查
uv run python .claude/skills/tests-kit/scripts/check_testcases.py
```

**重点验证：**
- 外键关系是否正确建立（TC-REL-*）
- 级联删除是否正常工作（TC-DEL-*）
- 缓存字段是否正确计算（TC-IACT 中的计数器测试）

> 更新 `progress.md` 记录数据注入阶段的测试结果。

---

### 阶段 4: 前端客户端生成

#### 4.0 前置：安装前端样式框架

> **必须在开始前端 UI 开发前完成！**

```bash
cd frontend

# 安装 Tailwind CSS
npm install -D tailwindcss @tailwindcss/postcss postcss

# 初始化 shadcn/ui（按提示配置）
npx shadcn@latest init

cd ..
```

Neon Forge 设计系统配色（参考 `specs/ui/style.pen`）：
- Primary accent: `#BBFD3B` (Lime Green)
- Surface: `#181818`, Dark: `#222222`, Secondary: `#333333`
- Fonts: Space Grotesk (headings), Inter (body), Poppins (numbers), Noto Sans SC (Chinese)

#### 4.1 生成 TypeScript API 客户端

```bash
# 使用 schema-to-openapi 生成的规范
uv run python .claude/skills/api-builder/scripts/cli.py \
  --spec .synnovator/openapi.yaml \
  --output app \
  --generate-client \
  --client-output frontend/lib/api/api-client.ts
```

**生成内容：**

```typescript
// frontend/lib/api/api-client.ts

// 类型定义（从 OpenAPI schemas 生成）
export interface User {
  id: string;
  username: string;
  email: string;
  display_name?: string;
  role: 'participant' | 'organizer' | 'admin';
  created_at: string;
  updated_at: string;
}

export interface UserCreate {
  username: string;
  email: string;
  display_name?: string;
  role?: 'participant' | 'organizer' | 'admin';
}

// API 客户端类
class ApiClient {
  private baseURL: string;

  constructor(baseURL?: string) {
    // 使用运行时环境变量，通过 lib/env.ts 的 getEnv() 获取
    // 开发环境: http://localhost:8000 (来自 .env.development)
    // 生产环境: /api (来自 Docker 环境变量)
    this.baseURL = baseURL || 'http://localhost:8000';
  }

  // User endpoints
  async listUsers(): Promise<User[]> {
    const response = await fetch(`${this.baseURL}/users`);
    if (!response.ok) throw new Error('Failed to fetch users');
    return response.json();
  }

  async createUser(data: UserCreate): Promise<User> {
    const response = await fetch(`${this.baseURL}/users`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to create user');
    return response.json();
  }

  async getUser(id: string): Promise<User> {
    const response = await fetch(`${this.baseURL}/users/${id}`);
    if (!response.ok) throw new Error('Failed to fetch user');
    return response.json();
  }

  // ... 其他 endpoints
}

export const apiClient = new ApiClient();
```

#### 4.2 集成到 Next.js

**配置环境变量：**

```bash
# frontend/.env.development (开发环境，已提交到仓库)
API_URL=http://localhost:8000/api

# frontend/.env.local (本地覆盖，不提交)
API_URL=https://custom-api.example.com/api
```

> 注意：环境变量通过 `lib/env.ts` 在服务端读取，并通过 `layout.tsx` 注入到 `window.__ENV__` 供客户端使用。

**在 Server Component 中使用：**

```typescript
// frontend/app/users/page.tsx
import { apiClient } from '@/lib/api/api-client';

export default async function UsersPage() {
  const users = await apiClient.listUsers();

  return (
    <div>
      <h1>Users</h1>
      <ul>
        {users.map(user => (
          <li key={user.id}>
            {user.username} ({user.email})
          </li>
        ))}
      </ul>
    </div>
  );
}
```

**在 Client Component 中使用：**

```typescript
// frontend/app/users/create/page.tsx
'use client';

import { useState } from 'react';
import { apiClient } from '@/lib/api/api-client';

export default function CreateUserPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const user = await apiClient.createUser({ username, email });
      alert(`User created: ${user.id}`);
    } catch (error) {
      alert('Failed to create user');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input value={username} onChange={e => setUsername(e.target.value)} placeholder="Username" />
      <input value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" />
      <button type="submit">Create User</button>
    </form>
  );
}
```

#### 4.3 错误处理和类型安全

生成的客户端提供：
- TypeScript 类型安全
- 自动 JSON 序列化/反序列化
- 统一的错误处理
- 环境变量配置

#### 4.4 增量测试：验证前端集成（tests-kit）

```bash
# 启动后端服务
make backend &

# 验证 TypeScript 编译通过
cd frontend && npx tsc --noEmit

# 运行前端测试
npx playwright test
```

**重点验证：**
- API 客户端类型定义与后端 schema 一致
- 基本 CRUD 操作能正常调用
- 错误处理正常工作

> 更新 `progress.md` 记录前端集成测试结果。

---

### 阶段 5: 最终集成验证

> **前面各阶段已完成模块级增量测试**，本阶段聚焦于全栈端到端集成验证。

#### 5.1 tests-kit 最终 Guard 检查

```bash
# 运行 tests-kit Guard 模式，确保所有 246 个测试用例未被破坏
uv run python .claude/skills/tests-kit/scripts/check_testcases.py
```

确保所有 17 个测试模块的用例都已覆盖：
- 01-07: 内容类型 CRUD
- 08: 关系操作
- 09: 级联删除
- 10: 权限控制
- 11: 用户旅程
- 12-13: 资源转移、关注
- 14: 活动关联
- 15-17: 规则引擎

#### 5.2 后端完整测试

```bash
# 运行所有后端测试
uv run pytest app/tests/ -v

# 测试覆盖率
uv run pytest app/tests/ --cov=app --cov-report=html
```

#### 5.3 端到端集成测试

**完整的用户旅程测试（参考 `docs/user-journeys.md` 的 13 个用户旅程）：**

```bash
# 启动后端和前端
make start

# 确保测试数据已导入
uv run python .claude/skills/data-importer/scripts/cli.py import \
  --source .synnovator --db data/synnovator.db --models app/models

# 运行前端端到端测试
cd frontend && npx playwright test

# 手动验证
open http://localhost:3000
open http://localhost:8000/docs
```

#### 5.4 完成会话记录

```bash
# 更新 progress.md，标记所有阶段完成
# 运行完成检查脚本
bash .claude/skills/planning-with-files/scripts/check-complete.sh
```

---

## 数据模型更新流程

### 场景 1: 添加新字段

```bash
# 0. [tests-kit Guard] 先检查现有测试用例
uv run python .claude/skills/tests-kit/scripts/check_testcases.py

# 1. 更新 docs/data-types.md（内容类型字段定义）
# 2. 同步更新 synnovator skill 相关文件（references/schema.md、endpoints/*.py）

# 3. 重新生成 OpenAPI spec（自动读取 synnovator skill + docs/ + specs/）
uv run python .claude/skills/schema-to-openapi/scripts/generate_openapi.py

# 4. 重新生成后端代码
uv run python .claude/skills/api-builder/scripts/cli.py \
  --spec .synnovator/openapi.yaml --output app

# 5. 生成数据库迁移
cd app && uv run alembic revision --autogenerate -m "Add new field"
uv run alembic upgrade head && cd ..

# 6. 更新 .synnovator 测试数据
uv run python .claude/skills/synnovator/scripts/engine.py \
  update user --id user_xxx --data '{"new_field": "value"}'

# 7. 重新导入数据
uv run python .claude/skills/data-importer/scripts/cli.py import \
  --source .synnovator --db data/synnovator.db --models app/models

# 8. [tests-kit Guard] 验证受影响的测试用例仍然通过
uv run python .claude/skills/tests-kit/scripts/check_testcases.py

# 9. 运行后端测试
uv run pytest app/tests/ -v
```

### 场景 2: 添加新的内容类型

```bash
# 0. [tests-kit Guard] 先检查现有测试用例
uv run python .claude/skills/tests-kit/scripts/check_testcases.py

# 1. 更新 docs/data-types.md 和 docs/relationships.md
# 2. 同步更新 synnovator skill（references/schema.md、新增 endpoints/*.py）
# 3. 重新生成 OpenAPI spec
uv run python .claude/skills/schema-to-openapi/scripts/generate_openapi.py
# 4. 重新生成后端
uv run python .claude/skills/api-builder/scripts/cli.py \
  --spec .synnovator/openapi.yaml --output app
# 5. 更新 data-importer（在 IMPORT_ORDER 中添加新类型）
# 6. 创建测试数据
# 7. 导入并测试

# 8. [tests-kit Insert] 为新内容类型添加测试用例到 specs/testcases/
# 9. [tests-kit Guard] 验证所有测试用例通过
uv run python .claude/skills/tests-kit/scripts/check_testcases.py
```

### 场景 3: 修改关系类型

```bash
# 0. [tests-kit Guard] 先检查现有测试用例（重点关注 TC-REL-*）
uv run python .claude/skills/tests-kit/scripts/check_testcases.py

# 1. 更新 docs/relationships.md
# 2. 同步更新 synnovator skill（references/schema.md）
# 3. 重新生成 OpenAPI spec
uv run python .claude/skills/schema-to-openapi/scripts/generate_openapi.py
# 4. 重新生成后端
uv run python .claude/skills/api-builder/scripts/cli.py \
  --spec .synnovator/openapi.yaml --output app
# 5. 生成迁移（可能需要手动调整）
cd app && uv run alembic revision --autogenerate -m "Update relations"
uv run alembic upgrade head && cd ..
# 6. 更新测试数据
# 7. 重新导入
uv run python .claude/skills/data-importer/scripts/cli.py import \
  --source .synnovator --db data/synnovator.db --models app/models

# 8. [tests-kit Guard] 验证关系相关测试用例
uv run python .claude/skills/tests-kit/scripts/check_testcases.py
```

---

## 常见问题

### Q: 如何清空数据库重新开始？

```bash
rm data/synnovator.db
cd app && uv run alembic upgrade head && cd ..
uv run python .claude/skills/data-importer/scripts/cli.py import \
  --source .synnovator --db data/synnovator.db --models app/models
```

### Q: 数据导入失败怎么办？

1. 查看错误报告
2. 验证 .md 文件格式
3. 检查外键依赖
4. 使用 `--types` 单独导入失败的类型

### Q: 生产环境请求 `/api/*` 返回 404，但后端日志显示收到的是 `/*`？

现象示例：浏览器请求 `GET /api/categories`，但后端日志却是 `GET /categories`，从而触发 404。

常见原因是 Nginx 反向代理的 `proxy_pass` 写法导致路径前缀被剥离：

- 错误写法：`location /api/ { proxy_pass http://backend/; }`（会把 `/api/...` 转发成 `/...`）
- 正确写法：`location /api/ { proxy_pass http://backend; }`（保留原始 URI，后端可匹配 `/api/...`）

本仓库的对应配置文件在 `deploy/nginx.conf`，修改后需要 reload/restart Nginx 容器或主机 Nginx 才会生效。

### Q: 如何添加认证？

```python
# app/auth.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    # TODO: 验证 token
    return user

# app/routers/users.py
@router.get("/me")
def get_current_user_info(user: User = Depends(get_current_user)):
    return user
```

### Q: 如何处理文件上传？

```python
# app/routers/resources.py
from fastapi import File, UploadFile

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # 保存文件
    contents = await file.read()
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(contents)

    # 创建 resource 记录
    resource = crud_resource.create(db, {
        "filename": file.filename,
        "mime_type": file.content_type,
        "size": len(contents),
        "url": file_path
    })
    return resource
```

---

## 最佳实践

### 1. 数据一致性
- 优先在 `.synnovator/` 中维护测试数据
- 使用 data-importer 同步到数据库
- 避免直接修改数据库

### 2. 版本控制
- `.synnovator/` 纳入 Git
- `data/*.db` 添加到 .gitignore
- 迁移文件纳入版本控制

### 3. 增量开发与增量测试
- 设计 → 生成 → 导入 → **测试** → 下一模块
- 每次迭代只修改必要部分
- 保持数据与 schema 同步
- **每完成一个模块，立即使用 tests-kit 验证**，不要积压到最后

### 4. 测试策略
- 使用 **tests-kit Guard** 模式在修改前检查现有测试用例
- 使用 **tests-kit Insert** 模式为新功能添加测试用例
- 按模块增量测试：用户 → 活动 → 规则 → 团队 → 帖子 → 资源 → 交互 → 关系
- 使用真实的 .synnovator 数据
- 测试外键约束和级联删除
- 最终阶段运行全量集成测试

### 5. 会话管理（planning-with-files）
- 每次开始新会话时初始化或恢复规划文件
- 每 2 次搜索/浏览操作后保存发现到 `findings.md`
- 重大决策前重新阅读 `task_plan.md` 保持目标在注意力中
- 错误记录到规划文件，避免重复同样的失败
- 3 次尝试失败后升级处理方式

### 6. 环境隔离
- 开发环境: SQLite
- 测试环境: SQLite（独立数据库）
- 生产环境: PostgreSQL/MySQL

---

## 技术栈总结

### 后端
- **语言**: Python 3.12+
- **框架**: FastAPI
- **ORM**: SQLAlchemy
- **数据库**: SQLite（开发）/ PostgreSQL（生产）
- **迁移**: Alembic
- **验证**: Pydantic
- **测试**: pytest, httpx
- **包管理**: uv

### 前端
- **框架**: Next.js 14 (App Router)
- **语言**: TypeScript
- **样式**: Tailwind CSS + shadcn/ui (Neon Forge 主题)
- **API 客户端**: 自动生成（TypeScript）
- **测试**: Playwright
- **包管理**: npm

### 工具链（Skills）
- **planning-with-files**: 文件化规划与会话管理（task_plan.md / findings.md / progress.md）
- **synnovator**: 平台原型参考实现 + 文件数据管理（CRUD 操作）
- **schema-to-openapi**: 从 synnovator skill + docs/ + specs/ 综合生成 OpenAPI 3.0 规范
- **api-builder**: 后端代码生成（FastAPI + SQLAlchemy + Alembic + 测试 + TypeScript 客户端）
- **data-importer**: 数据导入（.synnovator → SQLite）
- **tests-kit**: 增量测试管理（Guard 验证 + Insert 添加，246 个测试用例）

---

## 总结

完整开发流程 6 个阶段（贯穿 planning-with-files 规划管理）：

0. **项目初始化** - 创建结构、配置环境、初始化规划文件（planning-with-files）
1. **需求设计** - synnovator skill 为原型参考，综合 docs/ + specs/ 生成 OpenAPI spec → **tests-kit 验证数据模型**
2. **后端生成** - 使用 api-builder 生成 FastAPI 到 `app/` + 迁移 → **tests-kit 按模块增量测试**
3. **数据注入** - 使用 data-importer 导入测试数据 → **tests-kit 验证导入数据**
4. **前端集成** - 安装 Tailwind+shadcn → 生成 TypeScript 客户端 → 集成到 Next.js → **tests-kit 验证前端集成**
5. **最终集成验证** - tests-kit 全量 Guard 检查 + 端到端用户旅程测试

这个流程确保：
- 从设计到实现的一致性
- 自动化代码生成，减少重复工作
- **增量测试，每个模块完成后立即验证**，不积压问题
- **文件化规划，防止上下文丢失和中断失忆**
- 测试数据与生产 schema 同步
- 类型安全的全栈开发
- 快速迭代和验证
