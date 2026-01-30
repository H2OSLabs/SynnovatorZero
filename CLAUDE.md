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
app/                # FastAPI backend (package name matches api-builder templates)
frontend/           # Next.js 14 frontend
docs/               # Human-readable project documentation
  user-journeys.md  #   13 user flow documents
  examples.md       #   Data operation examples
  development-workflow.md  # Development process and conventions
specs/              # Technical specifications
  data/             #   Data model specs (types, relationships, CRUD, integrity)
  design/           #   UI/UX design (Figma, .pen files, pages.yaml)
  testcases/        #   Test case specifications
  guidelines/       #   Development guidelines (spec-guideline.md)
.claude/            # Claude Code configuration, skills, plugins
.synnovator/        # Platform data (YAML+Markdown test fixtures)
  generated/        #   Generated artifacts (openapi.yaml)
.project/           # Project management files
  task_plan.md      #   High-level task tracking
  progress.md       #   Detailed session progress
  findings.md       #   Key discoveries and decisions
deploy/             # Docker & deployment configs
pyproject.toml      # Python project config
uv.toml             # UV package manager config (Tsinghua mirror)
Makefile            # Build automation (make start/stop/clean)
```

## Architecture

### Data Model (specs/data/types.md, specs/data/relationships.md)

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

### Design System (specs/design/)

Theme: **"Neon Forge"** — dark theme with neon accents.

- **Primary accent:** Lime Green `#BBFD3B`
- **Backgrounds:** Surface `#181818`, Dark `#222222`, Secondary `#333333`
- **Fonts:** Space Grotesk (headings), Inter (body), Poppins (numbers/code), Noto Sans SC (Chinese)
- **Spacing tokens:** XS 4px, SM 8px, MD 16px, LG 24px, XL 32px
- **Border radius:** SM 4px, MD 8px, LG 12px, XL 21px, Pill 50px

## Development Approach

This project follows **spec-driven development** (see `specs/guidelines/spec-guideline.md`):

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
- Reference `specs/data/types.md` and `specs/data/relationships.md` for the canonical data schema before implementing any CRUD operations
- Reference `specs/data/crud-operations.md` for CRUD operation definitions and permissions
- Reference `docs/user-journeys.md` before implementing user-facing flows
- Reference `specs/data/integrity.md` for data constraints and soft delete behavior
