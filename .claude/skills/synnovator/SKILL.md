---
name: synnovator
description: >
  Manage Synnovator platform data: 7 content types (category, post, resource, rule, user, group, interaction)
  and 7 relationship types via a file-based YAML+Markdown engine. Data stored in PROJECT_DIR/.synnovator/.
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
- `interaction` - Likes, comments, ratings (YAML frontmatter only)

**7 relationship types** stored in `.synnovator/relations/<type>/`:
- `category_rule` - Activity-to-rule bindings
- `category_post` - Activity-to-post submissions
- `category_group` - Team activity registration
- `post_post` - Post references/embeds/replies
- `post_resource` - Post-to-attachment links
- `group_user` - Group membership (with approval workflow)
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
- **Cache stats**: `like_count`, `comment_count`, `average_rating` on posts auto-recalculate when interactions change.
- **Group approval**: `require_approval=true` sets join status to `pending`; owner approves via `UPDATE group_user`.
- **Uniqueness**: Enforced for user `(username)`, `(email)`; like `(user, target)`; relation duplicates.
- **Cascades**: Deleting content cascades to relations and interactions per the schema spec.

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
