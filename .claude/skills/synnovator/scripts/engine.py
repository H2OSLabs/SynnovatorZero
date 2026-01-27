#!/usr/bin/env python3
"""
Synnovator Data Engine - CRUD operations for all content types and relationships.

Data is stored as Markdown files with YAML frontmatter under PROJECT_DIR/.synnovator/
Each content record is a .md file: YAML frontmatter (structured fields) + Markdown body.
Relations are stored as lightweight .md files in relations/ subdirectories.

Directory structure:
  .synnovator/
    category/        # .md files with YAML frontmatter + Markdown body
    post/            # .md files with YAML frontmatter + Markdown body
    resource/        # .md files with YAML frontmatter
    rule/            # .md files with YAML frontmatter + Markdown body
    user/            # .md files with YAML frontmatter
    group/           # .md files with YAML frontmatter
    interaction/     # .md files with YAML frontmatter
    relations/
      category_rule/
      category_post/
      category_group/
      post_post/
      post_resource/
      group_user/
      target_interaction/
"""

import argparse
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    class yaml:
        @staticmethod
        def safe_load(s):
            return json.loads(s)
        @staticmethod
        def dump(data, stream=None, **kwargs):
            text = json.dumps(data, indent=2, ensure_ascii=False, default=str)
            if stream:
                stream.write(text)
                return None
            return text
        @staticmethod
        def safe_dump(data, **kwargs):
            return json.dumps(data, indent=2, ensure_ascii=False, default=str)


# === Constants ===

CONTENT_TYPES = ["category", "post", "resource", "rule", "user", "group", "interaction"]

RELATION_TYPES = [
    "category_rule", "category_post", "category_group",
    "post_post", "post_resource", "group_user", "target_interaction"
]

# Content types that support Markdown body
BODY_TYPES = ["category", "post", "rule"]

ENUMS = {
    "category.type": ["competition", "operation"],
    "category.status": ["draft", "published", "closed"],
    "post.type": ["profile", "team", "category", "for_category", "certificate", "general"],
    "post.status": ["draft", "pending_review", "published", "rejected"],
    "user.role": ["participant", "organizer", "admin"],
    "group.visibility": ["public", "private"],
    "interaction.type": ["like", "comment", "rating"],
    "interaction.target_type": ["post", "category", "resource"],
    "category_post.relation_type": ["submission", "reference"],
    "post_post.relation_type": ["reference", "reply", "embed"],
    "post_resource.display_type": ["attachment", "inline"],
    "group_user.role": ["owner", "admin", "member"],
    "group_user.status": ["pending", "accepted", "rejected"],
}

REQUIRED_FIELDS = {
    "category": ["name", "description", "type"],
    "post": ["title"],
    "resource": ["filename"],
    "rule": ["name", "description"],
    "user": ["username", "email"],
    "group": ["name"],
    "interaction": ["type", "target_type", "target_id"],
}

RELATION_KEYS = {
    "category_rule": ["category_id", "rule_id"],
    "category_post": ["category_id", "post_id"],
    "category_group": ["category_id", "group_id"],
    "post_post": ["source_post_id", "target_post_id"],
    "post_resource": ["post_id", "resource_id"],
    "group_user": ["group_id", "user_id"],
    "target_interaction": ["target_type", "target_id", "interaction_id"],
}


# === Markdown + YAML Frontmatter I/O ===

def parse_frontmatter_md(content):
    """Parse a .md file with YAML frontmatter into (metadata_dict, body_str)."""
    pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n?(.*)', re.DOTALL)
    m = pattern.match(content)
    if m:
        try:
            meta = yaml.safe_load(m.group(1)) or {}
        except Exception:
            meta = {}
        body = m.group(2).strip()
        return meta, body
    # No frontmatter
    return {}, content.strip()


def serialize_frontmatter_md(meta, body=""):
    """Serialize metadata dict + body string into YAML frontmatter .md format."""
    try:
        fm = yaml.dump(meta, default_flow_style=False, allow_unicode=True, sort_keys=False)
    except (TypeError, AttributeError):
        fm = yaml.safe_dump(meta)
    parts = ["---", fm.rstrip(), "---"]
    if body:
        parts.append("")
        parts.append(body)
    parts.append("")
    return "\n".join(parts)


# === Helpers ===

def get_data_dir(project_dir=None):
    if project_dir:
        return Path(project_dir) / ".synnovator"
    return Path.cwd() / ".synnovator"


def init_dirs(data_dir):
    for ct in CONTENT_TYPES:
        (data_dir / ct).mkdir(parents=True, exist_ok=True)
    for rt in RELATION_TYPES:
        (data_dir / "relations" / rt).mkdir(parents=True, exist_ok=True)


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def gen_id(prefix=""):
    short = uuid.uuid4().hex[:12]
    return f"{prefix}_{short}" if prefix else short


def load_record(filepath):
    """Load a .md record file -> (meta_dict, body_str). Returns combined dict with _body key."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    meta, body = parse_frontmatter_md(content)
    if body:
        meta["_body"] = body
    return meta


def save_record(filepath, data, body=None):
    """Save record as .md with YAML frontmatter + optional Markdown body."""
    meta = {k: v for k, v in data.items() if k != "_body"}
    if body is None:
        body = data.get("_body", "")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(serialize_frontmatter_md(meta, body))


def find_record(data_dir, content_type, record_id):
    filepath = data_dir / content_type / f"{record_id}.md"
    if filepath.exists():
        return filepath
    return None


def list_records(data_dir, content_type, filters=None, include_deleted=False):
    """List all records of a content type, optionally filtered."""
    folder = data_dir / content_type
    if not folder.exists():
        return []
    results = []
    for f in sorted(folder.iterdir()):
        if f.suffix != ".md":
            continue
        rec = load_record(f)
        if not include_deleted and rec.get("deleted_at"):
            continue
        if filters:
            match = True
            for k, v in filters.items():
                if rec.get(k) != v:
                    match = False
                    break
            if not match:
                continue
        results.append(rec)
    return results


def validate_enum(content_type, field, value):
    key = f"{content_type}.{field}"
    if key in ENUMS:
        if value not in ENUMS[key]:
            raise ValueError(f"Invalid value '{value}' for {key}. Allowed: {ENUMS[key]}")


def validate_required(content_type, data):
    for field in REQUIRED_FIELDS.get(content_type, []):
        if field not in data or data[field] is None:
            raise ValueError(f"Missing required field '{field}' for {content_type}")


def validate_uniqueness(data_dir, content_type, data, exclude_id=None):
    if content_type == "user":
        for rec in list_records(data_dir, "user"):
            if exclude_id and rec.get("id") == exclude_id:
                continue
            if rec.get("username") == data.get("username"):
                raise ValueError(f"Username '{data['username']}' already exists")
            if rec.get("email") == data.get("email"):
                raise ValueError(f"Email '{data['email']}' already exists")


def validate_reference_exists(data_dir, content_type, record_id):
    fp = find_record(data_dir, content_type, record_id)
    if not fp:
        raise ValueError(f"Referenced {content_type} '{record_id}' not found")
    rec = load_record(fp)
    if rec.get("deleted_at"):
        raise ValueError(f"Referenced {content_type} '{record_id}' is soft-deleted")
    return rec


# === CRUD: Content Types ===

def create_content(data_dir, content_type, data, current_user=None):
    validate_required(content_type, data)

    for field in ["type", "status", "role", "visibility", "target_type"]:
        if field in data:
            validate_enum(content_type, field, data[field])

    validate_uniqueness(data_dir, content_type, data)

    prefix_map = {
        "category": "cat", "post": "post", "resource": "res",
        "rule": "rule", "user": "user", "group": "grp", "interaction": "iact"
    }
    record_id = data.get("id") or gen_id(prefix_map.get(content_type, content_type))
    data["id"] = record_id
    data["created_at"] = data.get("created_at") or now_iso()
    data["updated_at"] = data["created_at"]
    data["deleted_at"] = None

    if current_user and content_type != "user":
        data.setdefault("created_by", current_user)

    # Content-type defaults
    if content_type == "category":
        data.setdefault("status", "draft")
    elif content_type == "post":
        data.setdefault("type", "general")
        data.setdefault("status", "draft")
        data.setdefault("tags", [])
        data.setdefault("like_count", 0)
        data.setdefault("comment_count", 0)
        data.setdefault("average_rating", None)
    elif content_type == "user":
        data.setdefault("role", "participant")
    elif content_type == "group":
        data.setdefault("visibility", "public")
        data.setdefault("require_approval", False)
    elif content_type == "interaction":
        validate_reference_exists(data_dir, data["target_type"], data["target_id"])
        if data["type"] == "like" and current_user:
            for rec in list_records(data_dir, "interaction"):
                if (rec.get("type") == "like" and
                    rec.get("target_type") == data["target_type"] and
                    rec.get("target_id") == data["target_id"] and
                    rec.get("created_by") == current_user):
                    raise ValueError("User already liked this target")

    filepath = data_dir / content_type / f"{record_id}.md"
    body = data.pop("_body", "")
    save_record(filepath, data, body=body)
    data["_body"] = body

    # Side effects
    if content_type == "interaction":
        _update_cache_stats(data_dir, data)

    return data


def read_content(data_dir, content_type, record_id=None, filters=None, include_deleted=False):
    if record_id:
        fp = find_record(data_dir, content_type, record_id)
        if not fp:
            raise ValueError(f"{content_type} '{record_id}' not found")
        rec = load_record(fp)
        if not include_deleted and rec.get("deleted_at"):
            raise ValueError(f"{content_type} '{record_id}' is soft-deleted")
        return rec
    return list_records(data_dir, content_type, filters=filters, include_deleted=include_deleted)


def update_content(data_dir, content_type, record_id, updates):
    fp = find_record(data_dir, content_type, record_id)
    if not fp:
        raise ValueError(f"{content_type} '{record_id}' not found")
    rec = load_record(fp)
    if rec.get("deleted_at"):
        raise ValueError(f"{content_type} '{record_id}' is soft-deleted")

    for field in ["type", "status", "role", "visibility", "target_type"]:
        if field in updates:
            validate_enum(content_type, field, updates[field])

    if content_type == "user":
        validate_uniqueness(data_dir, content_type, {**rec, **updates}, exclude_id=record_id)

    for k, v in updates.items():
        if k == "tags" and isinstance(v, str) and v.startswith("+"):
            tag = v[1:]
            if "tags" not in rec:
                rec["tags"] = []
            if tag not in rec["tags"]:
                rec["tags"].append(tag)
        elif k == "tags" and isinstance(v, str) and v.startswith("-"):
            tag = v[1:]
            if "tags" in rec and tag in rec["tags"]:
                rec["tags"].remove(tag)
        else:
            rec[k] = v

    rec["updated_at"] = now_iso()
    body = rec.pop("_body", "")
    save_record(fp, rec, body=body)
    rec["_body"] = body
    return rec


def delete_content(data_dir, content_type, record_id, hard=False):
    fp = find_record(data_dir, content_type, record_id)
    if not fp:
        raise ValueError(f"{content_type} '{record_id}' not found")

    if hard:
        os.remove(fp)
        return {"deleted": record_id, "mode": "hard"}

    rec = load_record(fp)
    rec["deleted_at"] = now_iso()
    rec["updated_at"] = rec["deleted_at"]
    body = rec.pop("_body", "")
    save_record(fp, rec, body=body)

    # Cascade
    if content_type in ("category", "post", "resource"):
        _cascade_soft_delete_interactions(data_dir, content_type, record_id)
    if content_type == "category":
        _cascade_delete_relations(data_dir, "category_rule", "category_id", record_id)
        _cascade_delete_relations(data_dir, "category_post", "category_id", record_id)
        _cascade_delete_relations(data_dir, "category_group", "category_id", record_id)
    elif content_type == "post":
        _cascade_delete_relations(data_dir, "category_post", "post_id", record_id)
        _cascade_delete_relations(data_dir, "post_post", "source_post_id", record_id)
        _cascade_delete_relations(data_dir, "post_post", "target_post_id", record_id)
        _cascade_delete_relations(data_dir, "post_resource", "post_id", record_id)
    elif content_type == "resource":
        _cascade_delete_relations(data_dir, "post_resource", "resource_id", record_id)
    elif content_type == "rule":
        _cascade_delete_relations(data_dir, "category_rule", "rule_id", record_id)
    elif content_type == "user":
        _cascade_soft_delete_user_interactions(data_dir, record_id)
    elif content_type == "group":
        _cascade_delete_relations(data_dir, "category_group", "group_id", record_id)
    elif content_type == "interaction":
        _cascade_delete_child_comments(data_dir, record_id)
        _cascade_delete_relations(data_dir, "target_interaction", "interaction_id", record_id)
        rec_data = load_record(fp)
        _update_cache_stats(data_dir, rec_data, removed=True)

    return {"deleted": record_id, "mode": "soft"}


# === CRUD: Relations ===

def create_relation(data_dir, relation_type, data):
    keys = RELATION_KEYS.get(relation_type)
    if not keys:
        raise ValueError(f"Unknown relation type: {relation_type}")

    for k in keys:
        if k not in data:
            raise ValueError(f"Missing required key '{k}' for {relation_type}")

    _validate_relation_refs(data_dir, relation_type, data)
    _check_relation_uniqueness(data_dir, relation_type, data)

    if relation_type == "group_user":
        group_rec = validate_reference_exists(data_dir, "group", data["group_id"])
        if data.get("role") == "owner":
            data["status"] = "accepted"
            data["joined_at"] = now_iso()
        elif group_rec.get("require_approval", False):
            data.setdefault("status", "pending")
        else:
            data.setdefault("status", "accepted")
            data["joined_at"] = now_iso()
        data.setdefault("role", "member")

    rel_id = gen_id("rel")
    data.setdefault("_id", rel_id)
    data["created_at"] = data.get("created_at") or now_iso()

    filepath = data_dir / "relations" / relation_type / f"{rel_id}.md"
    save_record(filepath, data)
    return data


def read_relation(data_dir, relation_type, filters=None):
    folder = data_dir / "relations" / relation_type
    if not folder.exists():
        return []
    results = []
    for f in sorted(folder.iterdir()):
        if f.suffix != ".md":
            continue
        rec = load_record(f)
        if filters:
            match = True
            for k, v in filters.items():
                if rec.get(k) != v:
                    match = False
                    break
            if not match:
                continue
        results.append(rec)
    return results


def update_relation(data_dir, relation_type, filters, updates):
    folder = data_dir / "relations" / relation_type
    if not folder.exists():
        raise ValueError(f"No relations of type {relation_type}")

    updated = []
    for f in folder.iterdir():
        if f.suffix != ".md":
            continue
        rec = load_record(f)
        match = True
        for k, v in filters.items():
            if rec.get(k) != v:
                match = False
                break
        if match:
            for field in ["relation_type", "display_type", "role", "status"]:
                if field in updates:
                    enum_key = f"{relation_type}.{field}"
                    if enum_key in ENUMS and updates[field] not in ENUMS[enum_key]:
                        raise ValueError(f"Invalid value '{updates[field]}' for {enum_key}")

            for k, v in updates.items():
                rec[k] = v

            if relation_type == "group_user" and "status" in updates:
                if updates["status"] == "accepted" and not rec.get("joined_at"):
                    rec["joined_at"] = now_iso()
                rec["status_changed_at"] = now_iso()

            save_record(f, rec)
            updated.append(rec)

    return updated


def delete_relation(data_dir, relation_type, filters):
    folder = data_dir / "relations" / relation_type
    if not folder.exists():
        return []

    deleted = []
    for f in list(folder.iterdir()):
        if f.suffix != ".md":
            continue
        rec = load_record(f)
        match = True
        for k, v in filters.items():
            if rec.get(k) != v:
                match = False
                break
        if match:
            os.remove(f)
            deleted.append(rec)

    return deleted


# === Cache Stats ===

def _update_cache_stats(data_dir, interaction_data, removed=False):
    target_type = interaction_data.get("target_type")
    target_id = interaction_data.get("target_id")

    if target_type != "post":
        return

    fp = find_record(data_dir, "post", target_id)
    if not fp:
        return

    post = load_record(fp)
    all_interactions = list_records(data_dir, "interaction", filters={
        "target_type": "post", "target_id": target_id
    })

    post["like_count"] = sum(1 for i in all_interactions if i.get("type") == "like")
    post["comment_count"] = sum(1 for i in all_interactions if i.get("type") == "comment")

    ratings = [i for i in all_interactions if i.get("type") == "rating"]
    if ratings:
        scoring_criteria = _find_scoring_criteria(data_dir, target_id)
        if scoring_criteria:
            weight_map = {sc["name"]: sc["weight"] for sc in scoring_criteria}
            total_weighted_scores = []
            for r in ratings:
                val = r.get("value", {})
                if isinstance(val, dict):
                    weighted_score = 0
                    for dim_name, dim_score in val.items():
                        if dim_name.startswith("_"):
                            continue
                        if dim_name in weight_map and isinstance(dim_score, (int, float)):
                            weighted_score += dim_score * weight_map[dim_name] / 100
                    if weighted_score > 0:
                        total_weighted_scores.append(weighted_score)
            if total_weighted_scores:
                post["average_rating"] = round(
                    sum(total_weighted_scores) / len(total_weighted_scores), 2
                )
            else:
                post["average_rating"] = None
        else:
            post["average_rating"] = None
    else:
        post["average_rating"] = None

    post["updated_at"] = now_iso()
    body = post.pop("_body", "")
    save_record(fp, post, body=body)


def _find_scoring_criteria(data_dir, post_id):
    cat_post_rels = read_relation(data_dir, "category_post", {"post_id": post_id})
    for rel in cat_post_rels:
        cat_id = rel.get("category_id")
        cat_rule_rels = read_relation(data_dir, "category_rule", {"category_id": cat_id})
        for cr in cat_rule_rels:
            rule_id = cr.get("rule_id")
            fp = find_record(data_dir, "rule", rule_id)
            if fp:
                rule = load_record(fp)
                if rule.get("scoring_criteria"):
                    return rule["scoring_criteria"]
    return None


# === Cascade Helpers ===

def _cascade_soft_delete_interactions(data_dir, target_type, target_id):
    for rec in list_records(data_dir, "interaction"):
        if rec.get("target_type") == target_type and rec.get("target_id") == target_id:
            fp = find_record(data_dir, "interaction", rec["id"])
            if fp:
                rec["deleted_at"] = now_iso()
                body = rec.pop("_body", "")
                save_record(fp, rec, body=body)


def _cascade_soft_delete_user_interactions(data_dir, user_id):
    for rec in list_records(data_dir, "interaction"):
        if rec.get("created_by") == user_id:
            fp = find_record(data_dir, "interaction", rec["id"])
            if fp:
                rec["deleted_at"] = now_iso()
                body = rec.pop("_body", "")
                save_record(fp, rec, body=body)


def _cascade_delete_child_comments(data_dir, parent_id):
    for rec in list_records(data_dir, "interaction"):
        if rec.get("parent_id") == parent_id:
            fp = find_record(data_dir, "interaction", rec["id"])
            if fp:
                rec["deleted_at"] = now_iso()
                body = rec.pop("_body", "")
                save_record(fp, rec, body=body)
                _cascade_delete_child_comments(data_dir, rec["id"])


def _cascade_delete_relations(data_dir, relation_type, key_field, key_value):
    delete_relation(data_dir, relation_type, {key_field: key_value})


def _validate_relation_refs(data_dir, relation_type, data):
    ref_map = {
        "category_rule": [("category", "category_id"), ("rule", "rule_id")],
        "category_post": [("category", "category_id"), ("post", "post_id")],
        "category_group": [("category", "category_id"), ("group", "group_id")],
        "post_post": [("post", "source_post_id"), ("post", "target_post_id")],
        "post_resource": [("post", "post_id"), ("resource", "resource_id")],
        "group_user": [("group", "group_id"), ("user", "user_id")],
        "target_interaction": [("interaction", "interaction_id")],
    }
    for content_type, field in ref_map.get(relation_type, []):
        if field in data:
            validate_reference_exists(data_dir, content_type, data[field])


def _check_relation_uniqueness(data_dir, relation_type, data):
    if relation_type == "category_rule":
        existing = read_relation(data_dir, relation_type, {
            "category_id": data["category_id"], "rule_id": data["rule_id"]
        })
        if existing:
            raise ValueError("This rule is already linked to this category")
    elif relation_type == "category_group":
        existing = read_relation(data_dir, relation_type, {
            "category_id": data["category_id"], "group_id": data["group_id"]
        })
        if existing:
            raise ValueError("This group is already registered for this category")
    elif relation_type == "group_user":
        existing = read_relation(data_dir, relation_type, {
            "group_id": data["group_id"], "user_id": data["user_id"]
        })
        if existing:
            for e in existing:
                if e.get("status") == "rejected":
                    delete_relation(data_dir, relation_type, {
                        "group_id": data["group_id"], "user_id": data["user_id"]
                    })
                    return
            raise ValueError("This user is already in this group")


# === CLI Interface ===

def main():
    parser = argparse.ArgumentParser(description="Synnovator Data Engine")
    parser.add_argument("--data-dir", default=None, help="Path to project root containing .synnovator/")
    parser.add_argument("--init", action="store_true", help="Initialize data directories")
    parser.add_argument("--user", default=None, help="Current user ID for permission context")

    sub = parser.add_subparsers(dest="command")

    for cmd in ["create", "read", "update", "delete"]:
        p = sub.add_parser(cmd)
        p.add_argument("type", help="Content type or relation type")
        p.add_argument("--id", default=None, help="Record ID")
        p.add_argument("--data", default=None, help="JSON data")
        p.add_argument("--body", default=None, help="Markdown body content")
        p.add_argument("--filters", default=None, help="JSON filters")
        p.add_argument("--hard", action="store_true", help="Hard delete")
        p.add_argument("--include-deleted", action="store_true", help="Include soft-deleted")

    args = parser.parse_args()

    data_dir = get_data_dir(args.data_dir) if args.data_dir else get_data_dir()

    if args.init:
        init_dirs(data_dir)
        print(json.dumps({"status": "ok", "data_dir": str(data_dir)}))
        return

    if not args.command:
        parser.print_help()
        return

    is_relation = args.type in RELATION_TYPES or args.type.replace(":", "_") in RELATION_TYPES
    normalized_type = args.type.replace(":", "_") if is_relation else args.type

    try:
        data = json.loads(args.data) if args.data else {}
        filters = json.loads(args.filters) if args.filters else {}
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}), file=sys.stderr)
        sys.exit(1)

    # Add Markdown body if provided
    if hasattr(args, 'body') and args.body:
        data["_body"] = args.body

    try:
        if args.command == "create":
            if is_relation:
                result = create_relation(data_dir, normalized_type, data)
            else:
                result = create_content(data_dir, normalized_type, data, current_user=args.user)
        elif args.command == "read":
            if is_relation:
                result = read_relation(data_dir, normalized_type, filters=filters or None)
            else:
                result = read_content(
                    data_dir, normalized_type,
                    record_id=args.id,
                    filters=filters or None,
                    include_deleted=getattr(args, 'include_deleted', False)
                )
        elif args.command == "update":
            if is_relation:
                result = update_relation(data_dir, normalized_type, filters, data)
            else:
                if not args.id:
                    raise ValueError("--id required for update")
                result = update_content(data_dir, normalized_type, args.id, data)
        elif args.command == "delete":
            if is_relation:
                result = delete_relation(data_dir, normalized_type, filters or data)
            else:
                if not args.id:
                    raise ValueError("--id required for delete")
                result = delete_content(data_dir, normalized_type, args.id, hard=args.hard)

        # Remove _body from JSON output for cleanliness, indicate presence
        def clean_output(obj):
            if isinstance(obj, dict):
                out = {k: v for k, v in obj.items() if k != "_body"}
                if obj.get("_body"):
                    out["has_body"] = True
                return out
            if isinstance(obj, list):
                return [clean_output(i) for i in obj]
            return obj

        print(json.dumps(clean_output(result), indent=2, ensure_ascii=False, default=str))

    except ValueError as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e), "type": type(e).__name__}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
