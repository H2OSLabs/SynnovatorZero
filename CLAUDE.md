# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Synnovator is a creative collaboration platform (协创者) being rebuilt from scratch. The project is in the **prototype development phase** — the data model, user journeys, design system, and development workflow are fully documented. A working FastAPI backend (SQLite + SQLAlchemy), Next.js frontend, and username/password authentication system are implemented.

- **Language:** Python 3.12 + TypeScript (Next.js 14)
- **Package manager:** UV (Python, with Tsinghua PyPI mirror in `uv.toml`) + npm (frontend)
- **Database:** SQLite + SQLAlchemy + Alembic migrations
- **Repository:** H2OSLabs/SynnovatorZero

## Commands

```bash
# Start all services (backend + frontend)
make start

# Start backend only (FastAPI on port 8000)
make backend

# Start frontend only (Next.js on port 3000)
make frontend

# Add a Python dependency
uv add <package>

# Sync dependencies from lock file
uv sync

# Reset database and inject seed data
make resetdb && make seed

# Run tests
uv run pytest
```

## Project Structure

```
app/            # FastAPI backend (models, schemas, routers, crud, services, tests)
frontend/       # Next.js 14 frontend (App Router, shadcn/ui, Neon Forge theme)
docs/           # Functional documentation (data model, user journeys, workflow)
specs/          # Development standards, test cases, seed data requirements
specs/ui/       # Design system (.pen files: style guide + components)
scripts/        # Utility scripts (seed_dev_data.py)
alembic/        # Database migrations
e2e/            # Playwright E2E tests
.claude/        # Claude Code configuration, skills (20+), plugins
.synnovator/    # Platform data engine (YAML+Markdown) and generated OpenAPI spec
deploy/         # Docker & deployment configs
data/           # SQLite database files
pyproject.toml  # Python project config
uv.toml         # UV package manager config (Tsinghua mirror)
Makefile        # Build automation (make start/stop/clean/resetdb/seed)
```

## Architecture

### Data Model (docs/data-types.md, docs/relationships.md)

Seven content types defined in domain model docs, implemented as SQLAlchemy ORM models (`app/models/`) backed by SQLite:

| Type | Purpose |
|------|---------|
| `event` | Competition or operational events, linked to rules |
| `post` | User-submitted content with tags and custom rendering |
| `resource` | Uploaded file attachments |
| `rule` | Event rules created by organizers |
| `user` | User profiles (with username/password auth) |
| `group` | Teams / permission groups |
| `interaction` | Likes, comments, ratings on any content type |

Nine relationship types (with junction tables): `event:rule`, `event:post`, `event:group`, `event:event`, `post:post`, `post:resource`, `group:user`, `user:user`, `target:interaction`.

All content types use **soft delete** (`deleted_at` field). Cached counters (`like_count`, `comment_count`, `average_rating`) are auto-maintained on `post`.

> **Note:** The `.synnovator/` directory uses YAML+Markdown as a file-based data engine. The actual application stores data in SQLite via SQLAlchemy. The domain model docs (`docs/data-types.md` etc.) are the single source of truth for both.

### Roles

- **Participant (参赛者):** Browse, register, submit posts, join teams
- **Organizer (组织者):** Create/manage events and rules, review content
- **Admin (管理员):** Platform-level user and content management

### User Journeys (docs/user-journeys.md)

13 documented user flows covering registration, event creation, team formation, post lifecycle (create/edit/delete with version management), and community interactions (like/comment/rate).

### Design System (specs/ui/)

Theme: **"Neon Forge"** — dark theme with neon accents.

- **Primary accent:** Lime Green `#BBFD3B`
- **Backgrounds:** Surface `#181818`, Dark `#222222`, Secondary `#333333`
- **Fonts:** Space Grotesk (headings), Inter (body), Poppins (numbers/code), Noto Sans SC (Chinese)
- **Spacing tokens:** XS 4px, SM 8px, MD 16px, LG 24px, XL 32px
- **Border radius:** SM 4px, MD 8px, LG 12px, XL 21px, Pill 50px

## Development Approach

This project follows **spec-driven, skill-automated development** with a 12-phase workflow documented in `docs/development-workflow/` (see README.md for index).

### Core Principles

- **领域模型优先 (Domain-Model-First):** Domain model (docs/) is the single source of truth. Both database schema and API contract are downstream consumers.
- **Skill-driven automation:** Each workflow phase has a corresponding Claude Code skill that defines inputs, process, and outputs.
- **Incremental testing:** Use tests-kit after each phase, not just at the end.
- **Plan before implement:** Use Plan Mode (Shift+Tab) before implementing features. Use planning-with-files for multi-phase work.

### 12-Phase Workflow (summary)

```
Phase 0:   项目初始化
Phase 0.5: 领域建模与数据架构  [domain-modeler]
Phase 1:   API 设计 (OpenAPI)   [schema-to-openapi]
Phase 2:   后端代码生成          [api-builder]
Phase 2.5: 种子数据设计          [seed-designer]
Phase 3:   种子数据注入          make resetdb && make seed
Phase 4:   UI 设计文档生成
Phase 5:   前端样式框架配置      shadcn/ui + Neon Forge
Phase 6:   前端 API 客户端生成   [api-builder --generate-client]
Phase 7:   前端组件开发          [Figma 参考 + shadcn 组件]
Phase 8:   E2E 测试             Playwright
Phase 9:   最终集成验证          [tests-kit Guard]
```

### Key Skills

| Skill | Purpose |
|-------|---------|
| **domain-modeler** | Extract entities, relationships, constraints from user-journeys → domain model docs |
| **schema-to-openapi** | Generate OpenAPI 3.0 spec from domain model docs |
| **api-builder** | Generate FastAPI backend + TypeScript client from OpenAPI spec. Default `--conflict-strategy skip` protects existing files; use `--dry-run` to preview |
| **seed-designer** | Derive seed data requirements from test case preconditions |
| **tests-kit** | Guard mode (verify test cases) + Insert mode (add test cases) |
| **openapi-to-components** | Wire frontend components to backend API |
| **planning-with-files** | File-based planning (task_plan.md, findings.md, progress.md) for context persistence |

## Conventions

- All field names use `snake_case`; all content types use `created_by` for the author/creator field
- Domain model docs are the source of truth; `.synnovator/` uses YAML+Markdown file engine; `app/` uses SQLite+SQLAlchemy
- Documentation is bilingual (Chinese primary, English where applicable)
- Use `uv` for all Python commands (not pip/poetry)
- Frontend auth defaults to Mock login (`X-User-Id` header); real auth only when explicitly requested
- **回答问题时使用中文**（代码注释和变量名除外）
- **前端 UI 文本使用中文**：页面标题、按钮、表单标签、错误提示、Toast 消息等用户可见文本必须使用中文
- **前端路由验证**：所有 `<Link href="...">` 必须指向 `app/` 目录中实际存在的路由

## Boundaries

- Never read or commit `.env` or `secrets/**`
- Never use `curl` in bash commands (denied in settings)
- Reference `docs/data-types.md` and `docs/relationships.md` for the canonical data schema before implementing any CRUD operations
- Reference `docs/crud-operations.md` for CRUD operation definitions and permissions
- Reference `docs/user-journeys.md` before implementing user-facing flows
- Reference `specs/data-integrity.md` for data constraints and soft delete behavior

## 问题追溯规则 (Root Cause Analysis)

发现 bug 或缺失功能时，**必须**进行根因分析：

### 追溯流程

1. **定位问题阶段**
   - 对照 `docs/development-workflow/` 的 12 个阶段
   - 判断问题属于哪个阶段的产出物

2. **检查工作流覆盖**
   - 该阶段的检查点是否覆盖了这类问题？
   - 测试用例（`specs/testcases/`）是否有对应场景？

3. **检查 Skill 实现**
   - 相关 Skill 是否正确执行？
   - Skill 的输出是否被正确验证？

4. **记录分析结果**
   - 在修复 bug 的 commit message 中记录 root cause
   - 格式：`fix: [问题描述] (root cause: [阶段X] [具体原因])`

### 追溯映射表

| 问题类型 | 追溯阶段 | 检查项 |
|---------|---------|-------|
| 领域模型缺陷 | 阶段 0.5 (领域建模) | domain-modeler 输出、user-journeys 覆盖 |
| 缺少 API endpoint | 阶段 1 (API 设计) | OpenAPI spec、schema-to-openapi 输出 |
| API 返回错误数据 | 阶段 2 (后端生成) | schema 定义、api-builder 输出 |
| 种子数据需求不匹配 | 阶段 2.5 (种子设计) | seed-designer 输出、测试用例覆盖 |
| 数据不一致 | 阶段 3 (种子注入) | 种子脚本、业务校验 |
| UI 流程缺失 | 阶段 4 (UI 设计) | user-journey 覆盖度检查 |
| 前端显示异常 | 阶段 7 (组件开发) | UI 设计文档、shadcn 组件使用 |
| E2E 测试失败 | 阶段 8 (E2E 测试) | 测试用例完整性 |
| 测试用例与需求不符 | user-journeys 更新后 | tests-kit Insert 同步、种子数据更新 |

### 修复后改进

修复 bug 后，**必须**更新相关文档/流程：

- [ ] 补充测试用例到 `specs/testcases/`
- [ ] 更新 `docs/development-workflow/` 的检查点（如需要）
- [ ] 更新相关 Skill 的验证逻辑（如需要）
- [ ] 在 `findings.md` 记录经验教训（如使用 planning-with-files）
