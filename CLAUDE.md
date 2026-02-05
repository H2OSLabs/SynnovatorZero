# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Synnovator is a creative collaboration platform (协创者) being rebuilt from scratch. The project is currently in the **specification and design phase** — the data model, user journeys, and design system are fully documented, but production code has not yet been written.

- **Language:** Python 3.12
- **Package manager:** UV (with Tsinghua PyPI mirror configured in `uv.toml`)
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

# Run tests
uv run pytest
```

## Project Structure

```
app/            # FastAPI backend (package name matches api-builder templates)
frontend/       # Next.js 14 frontend
docs/           # Functional documentation (data model, user journeys)
specs/          # Development standards and guidelines
specs/ui/       # Design system (.pen files: style guide + components)
.claude/        # Claude Code configuration, skills, plugins
.synnovator/    # Platform data (YAML+Markdown) and generated OpenAPI spec
deploy/         # Docker & deployment configs
pyproject.toml  # Python project config
uv.toml         # UV package manager config (Tsinghua mirror)
Makefile        # Build automation (make start/stop/clean)
```

## Architecture

### Data Model (docs/data-types.md, docs/relationships.md)

Seven content types stored as **YAML frontmatter + Markdown body**:

| Type | Purpose |
|------|---------|
| `category` | Competition or operational events, linked to rules |
| `post` | User-submitted content with tags and custom rendering |
| `resource` | Uploaded file attachments |
| `rule` | Event rules created by organizers |
| `user` | User profiles |
| `group` | Teams / permission groups |
| `interaction` | Likes, comments, ratings on any content type |

Nine relationship types: `category:rule`, `category:post`, `category:group`, `category:category`, `post:post`, `post:resource`, `group:user`, `user:user`, `target:interaction`.

All content types use **soft delete** (`deleted_at` field). Cached counters (`like_count`, `comment_count`, `average_rating`) are auto-maintained on `post`.

### Roles

- **Participant (参赛者):** Browse, register, submit posts, join teams
- **Organizer (组织者):** Create/manage categories and rules, review content
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

This project follows **spec-driven development** (see `specs/spec-guideline.md`):

1. Start with high-level vision, let AI draft details
2. Use structured PRD framework covering 6 domains: Commands, Testing, Project Structure, Code Style, Git Workflow, Boundaries
3. Modularize tasks — break large specs into small, focused pieces
4. Build self-checking constraints into specs
5. Test, iterate, and evolve specs over time

Use **Plan Mode** (Shift+Tab) before implementing features. Read the relevant `docs/` files before writing code that touches the data model or user flows.

## Conventions

- All field names use `snake_case`; all content types use `created_by` for the author/creator field
- Content is stored as YAML frontmatter + Markdown body
- Documentation is bilingual (Chinese primary, English where applicable)
- Use `uv` for all Python commands (not pip/poetry)

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
   - 对照 `docs/development-workflow.md` 的 10 个阶段
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
| API 返回错误数据 | 阶段 2 (后端生成) | schema 定义、api-builder 输出 |
| 前端显示异常 | 阶段 7 (组件开发) | UI 设计文档、shadcn 组件使用 |
| 缺少 API endpoint | 阶段 1 (需求设计) | OpenAPI spec、user-journeys 覆盖 |
| E2E 测试失败 | 阶段 8 (E2E 测试) | 测试用例完整性 |
| 数据不一致 | 阶段 3 (种子数据) | 种子脚本、业务校验 |
| UI 流程缺失 | 阶段 4 (UI 设计) | user-journey 覆盖度检查 |

### 修复后改进

修复 bug 后，**必须**更新相关文档/流程：

- [ ] 补充测试用例到 `specs/testcases/`
- [ ] 更新 `docs/development-workflow.md` 的检查点（如需要）
- [ ] 更新相关 Skill 的验证逻辑（如需要）
- [ ] 在 `findings.md` 记录经验教训（如使用 planning-with-files）
