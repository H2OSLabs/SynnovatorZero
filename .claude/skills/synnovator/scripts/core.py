#!/usr/bin/env python3
"""
Synnovator Data Engine - Shared infrastructure: constants, I/O, helpers, validators.
"""

import json
import os
import re
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
    "category_rule", "category_post", "category_group", "category_category",
    "post_post", "post_resource", "group_user", "user_user", "target_interaction"
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
    "category_post.relation_type": ["submission", "reference"],
    "category_category.relation_type": ["stage", "track", "prerequisite"],
    "post_post.relation_type": ["reference", "reply", "embed"],
    "post_resource.display_type": ["attachment", "inline"],
    "group_user.role": ["owner", "admin", "member"],
    "group_user.status": ["pending", "accepted", "rejected"],
    "user_user.relation_type": ["follow", "block"],
    "target_interaction.target_type": ["post", "category", "resource"],
}

REQUIRED_FIELDS = {
    "category": ["name", "description", "type"],
    "post": ["title"],
    "resource": ["filename"],
    "rule": ["name", "description"],
    "user": ["username", "email"],
    "group": ["name"],
    "interaction": ["type"],
}

RELATION_KEYS = {
    "category_rule": ["category_id", "rule_id"],
    "category_post": ["category_id", "post_id"],
    "category_group": ["category_id", "group_id"],
    "category_category": ["source_category_id", "target_category_id"],
    "post_post": ["source_post_id", "target_post_id"],
    "post_resource": ["post_id", "resource_id"],
    "group_user": ["group_id", "user_id"],
    "user_user": ["source_user_id", "target_user_id"],
    "target_interaction": ["target_type", "target_id", "interaction_id"],
}

PREFIX_MAP = {
    "category": "cat", "post": "post", "resource": "res",
    "rule": "rule", "user": "user", "group": "grp", "interaction": "iact"
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
    """Load a .md record file -> dict with optional _body key."""
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


# === Validators ===

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
