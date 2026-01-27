---
name: synnovator
description: >
  Manage Synnovator platform data: 7 content types (category, post, resource, rule, user, group, interaction)
  and 9 relationship types via a file-based YAML+Markdown engine. Data stored in PROJECT_DIR/.synnovator/.
  Use when performing CRUD operations on platform content, managing activities/competitions, teams,
  posts, user interactions (likes/comments/ratings), or testing user journeys.
  Trigger: any request involving Synnovator platform data, user journey simulation, or content management.
---

# Synnovator

File-based data engine for the Synnovator platform. All records are `.md` files with YAML frontmatter + Markdown body, stored under `PROJECT_DIR/.synnovator/`.

## Quick Start

```bash
# Initialize data directory
uv run python .claude/skills/synnovator/scripts/engine.py --init

# CRUD operations
uv run python .claude/skills/synnovator/scripts/engine.py [--user USER_ID] COMMAND TYPE [OPTIONS]
```

Commands: `create`, `read`, `update`, `delete`

## Data Model

**7 content types** stored as `.md` files in `.synnovator/<type>/`:
- `category` - Activities/competitions (YAML + Markdown body)
- `post` - User posts with tags (YAML + Markdown body)
- `resource` - File attachments (YAML frontmatter only)
- `rule` - Activity rules with scoring criteria (YAML + Markdown body)
- `user` - User accounts (YAML frontmatter only)
- `group` - Teams/groups (YAML frontmatter only)
- `interaction` - Likes, comments, ratings (YAML frontmatter only). Target info is stored in `target_interaction` relation, not on the interaction itself.

**9 relationship types** stored in `.synnovator/relations/<type>/`:
- `category_rule` - Activity-to-rule bindings
- `category_post` - Activity-to-post submissions
- `category_group` - Team activity registration
- `category_category` - Activity association (stage / track / prerequisite)
- `post_post` - Post references/embeds/replies
- `post_resource` - Post-to-attachment links
- `group_user` - Group membership (with approval workflow)
- `user_user` - User follow/block relationships
- `target_interaction` - Content-to-interaction bindings

See [references/schema.md](references/schema.md) for complete field definitions.

## Content CRUD

### Create
```bash
engine.py [--user UID] create <type> --data '<json>' [--body 'markdown content']
```
Auto-generates: `id`, `created_at`, `updated_at`, `deleted_at`. Sets `created_by` from `--user`.

### Read
```bash
engine.py read <type> --id <record_id>           # Single record
engine.py read <type> --filters '<json>'          # Filtered list
engine.py read <type> --include-deleted           # Include soft-deleted
```

### Update
```bash
engine.py update <type> --id <record_id> --data '<json>'
```
For tags: `"+tagname"` appends, `"-tagname"` removes. Body: `"_body": "new markdown"`.

### Delete
```bash
engine.py delete <type> --id <record_id>          # Soft delete (default)
engine.py delete <type> --id <record_id> --hard    # Hard delete
```
Cascades: deleting a post removes its relations and soft-deletes linked interactions.

## Relation CRUD

```bash
engine.py create <rel_type> --data '<json>'                        # Create
engine.py read <rel_type> --filters '<json>'                       # Read
engine.py update <rel_type> --filters '<json>' --data '<json>'     # Update
engine.py delete <rel_type> --filters '<json>'                     # Delete (hard)
```
Use `_` or `:` separator: `category_rule` or `category:rule`.

## Key Behaviors

- **Soft delete**: Sets `deleted_at`, record stays on disk. Default for content types.
- **Hard delete**: Removes file. Default for relations.
- **Cache stats**: `like_count`, `comment_count`, `average_rating` on posts are **read-only** — auto-recalculated when `target_interaction` relations are created/deleted. Manual updates to these fields are silently ignored.
- **Two-step interactions**: Creating an interaction requires: (1) `create interaction` for the record, (2) `create target_interaction` to link it to a target. Cache updates, duplicate-like checks, and target validation happen at step 2.
- **Group approval**: `require_approval=true` sets join status to `pending`; owner approves via `UPDATE group_user`.
- **Uniqueness**: Enforced for user `(username)`, `(email)`; like `(user, target)` at `target_interaction` creation; relation duplicates; user-per-category-per-group (a user can only belong to one group per category); `user_user` `(source_user_id, target_user_id, relation_type)`; `category_category` `(source_category_id, target_category_id)`.
- **Self-reference prevention**: `user_user` and `category_category` cannot reference the same entity as both source and target.
- **Block enforcement**: If user B blocks user A, A cannot follow B.
- **Circular dependency detection**: `category_category` with `stage` or `prerequisite` relation types prevents cycles (A→B→C→A).
- **Prerequisite enforcement**: Creating a `category_group` registration checks that all prerequisite categories (via `category_category` prerequisite) are closed.
- **Cascades**: Deleting content cascades to relations and interactions per the schema spec. Notably:
  - Deleting a **group** cascades to both `group_user` and `category_group` relations.
  - Deleting a **user** cascades to `group_user` and `user_user` relations and soft-deletes all user interactions.
  - Deleting a **category** cascades to `category_rule`, `category_post`, `category_group`, and `category_category` relations and soft-deletes linked interactions.

## Rule Enforcement

Rules linked to a category via `category_rule` are **automatically enforced** as pre-operation hooks. All rules must pass (AND logic); any single violation rejects the operation with a descriptive error.

### Hook Points

| Operation | Check Type | Validations |
|-----------|-----------|-------------|
| `create category_post` | submission | Time window (`submission_start`/`submission_deadline`), max submissions per user, submission format, min team size |
| `create group_user` | team_join | Max team size (checked against all categories the group is registered for) |
| `create category_group` | prerequisite | All prerequisite categories must be closed before registration |
| `update post` (status change) | publish | `allow_public` / `require_review` path enforcement |

### Validation Chain

```
category_post: category → category_rule → rule → validate against post/user context
group_user:    group → category_group → category → category_rule → rule → validate team size
post status:   post → category_post → category → category_rule → rule → validate publish path
```

### Behavior

- **No rules linked** → no constraints, operation proceeds normally.
- **Rule field absent** → that constraint is skipped (e.g., no `submission_deadline` means no time limit).
- **Violation** → operation rejected with error: `Rule '<name>': <reason>`.
- Posts not linked to any category are unconstrained (rules only apply through `category_post`).

## File Format

Each record is a `.md` file:
```markdown
---
name: 2025 AI Hackathon
type: competition
status: published
id: cat_abc123
created_by: user_alice
created_at: '2025-01-01T00:00:00Z'
---

## Activity Description

Markdown content here.
```

## Testing

Run all user journey tests:
```bash
uv run python .claude/skills/synnovator/scripts/test_journeys.py
```

See [references/endpoints.md](references/endpoints.md) for detailed API examples.
See [references/schema.md](references/schema.md) for complete field and enum definitions.

## Documentation Sync

This skill's data model is the **implementation** of the canonical specs in `docs/` and `specs/`. When modifying the skill's schema, engine logic, or data model, **must** sync the following docs:

| Skill file | Canonical docs | Sync what |
|-----------|---------------|-----------|
| `references/schema.md` | `docs/data-types.md`, `docs/relationships.md` | Field definitions, enums, required fields, relation schemas |
| `scripts/engine.py` (CRUD logic) | `docs/crud-operations.md`, `specs/data-integrity.md` | CRUD operations, cascade strategies, uniqueness constraints |
| `scripts/engine.py` (cache) | `specs/cache-strategy.md` | Cache stats triggers, read-only enforcement |
| `scripts/test_journeys.py` | `docs/user-journeys.md` | User journey steps, data operation sequences |

**Checklist when updating the skill:**
1. Update skill code (`engine.py`) and tests (`test_journeys.py`)
2. Update skill reference docs (`references/schema.md`, `references/endpoints.md`)
3. Update canonical docs (`docs/data-types.md`, `docs/relationships.md`, `docs/crud-operations.md`, `docs/user-journeys.md`)
4. Run `uv run python .claude/skills/synnovator/scripts/test_journeys.py` to verify
