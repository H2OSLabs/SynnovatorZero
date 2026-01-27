# Synnovator API Endpoints Reference

All operations are executed via the engine script:
```
uv run python .claude/skills/synnovator/scripts/engine.py [OPTIONS] COMMAND TYPE [ARGS]
```

## Global Options
| Option | Description |
|--------|-------------|
| `--data-dir PATH` | Path to project root (default: cwd) |
| `--init` | Initialize `.synnovator/` directories |
| `--user USER_ID` | Set current user context for permissions |

## Content CRUD

### CREATE
```bash
engine.py create <type> --data '<json>' [--body 'markdown content'] [--user <user_id>]
```
Types: `category`, `post`, `resource`, `rule`, `user`, `group`, `interaction`

Markdown body can be passed via `--body` flag or `"_body"` key in JSON data.
Records are stored as `.md` files with YAML frontmatter + Markdown body.

### READ
```bash
# Read single record
engine.py read <type> --id <record_id>
# List with filters
engine.py read <type> --filters '<json>'
# Include soft-deleted
engine.py read <type> --include-deleted
```

### UPDATE
```bash
engine.py update <type> --id <record_id> --data '<json>'
```
Special: for post tags, use `"+tagname"` to append, `"-tagname"` to remove.

### DELETE
```bash
# Soft delete (default)
engine.py delete <type> --id <record_id>
# Hard delete
engine.py delete <type> --id <record_id> --hard
```

## Relation CRUD

Use `_` separator or `:` separator for relation type names.

### CREATE
```bash
engine.py create <relation_type> --data '<json>'
```
Relation types: `category_rule`, `category_post`, `category_group`, `post_post`, `post_resource`, `group_user`, `target_interaction`

### READ
```bash
engine.py read <relation_type> --filters '<json>'
```

### UPDATE
```bash
engine.py update <relation_type> --filters '<json>' --data '<json>'
```

### DELETE (hard delete)
```bash
engine.py delete <relation_type> --filters '<json>'
```

## Examples

### Create a user
```bash
engine.py create user --data '{"username":"alice","email":"alice@example.com","display_name":"Alice","role":"organizer"}'
```

### Create a category
```bash
engine.py --user user_alice create category --data '{"name":"AI Hackathon","description":"AI competition","type":"competition"}'
```

### Create a rule and link to category
```bash
engine.py --user user_alice create rule --data '{"name":"Submission Rule","description":"Rules for submissions","allow_public":true,"require_review":true,"scoring_criteria":[{"name":"Innovation","weight":30,"description":"Originality"},{"name":"Technical","weight":30,"description":"Code quality"},{"name":"Practical","weight":25,"description":"Usefulness"},{"name":"Demo","weight":15,"description":"Presentation"}]}'

engine.py create category_rule --data '{"category_id":"cat_xxx","rule_id":"rule_xxx","priority":1}'
```

### Create a group and add members
```bash
engine.py --user user_alice create group --data '{"name":"Team Alpha","require_approval":true}'
engine.py create group_user --data '{"group_id":"grp_xxx","user_id":"user_alice","role":"owner"}'
engine.py create group_user --data '{"group_id":"grp_xxx","user_id":"user_bob","role":"member"}'
```

### Approve group member
```bash
engine.py update group_user --filters '{"group_id":"grp_xxx","user_id":"user_bob"}' --data '{"status":"accepted"}'
```

### Create post and link to category
```bash
engine.py --user user_alice create post --data '{"title":"My Submission","type":"for_category","tags":["AI"]}'
engine.py create category_post --data '{"category_id":"cat_xxx","post_id":"post_xxx","relation_type":"submission"}'
```

### Like a post
```bash
engine.py --user user_bob create interaction --data '{"type":"like","target_type":"post","target_id":"post_xxx"}'
engine.py create target_interaction --data '{"target_type":"post","target_id":"post_xxx","interaction_id":"iact_xxx"}'
```

### Comment on a post
```bash
engine.py --user user_bob create interaction --data '{"type":"comment","target_type":"post","target_id":"post_xxx","value":"Great work!"}'
```

### Submit a rating
```bash
engine.py --user user_judge create interaction --data '{"type":"rating","target_type":"post","target_id":"post_xxx","value":{"Innovation":87,"Technical":82,"Practical":78,"Demo":91,"_comment":"Well done"}}'
```
