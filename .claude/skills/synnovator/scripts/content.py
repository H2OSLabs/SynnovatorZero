#!/usr/bin/env python3
"""
Synnovator Data Engine - Generic content CRUD dispatch.

Routes to per-endpoint modules for type-specific behavior.
"""

import os

from core import (
    validate_required, validate_enum, validate_uniqueness,
    gen_id, now_iso, find_record, load_record, save_record, list_records,
    PREFIX_MAP,
)
from endpoints import get_endpoint


def create_content(data_dir, content_type, data, current_user=None):
    validate_required(content_type, data)

    for field in ["type", "status", "role", "visibility", "target_type"]:
        if field in data:
            validate_enum(content_type, field, data[field])

    # Global uniqueness (user is handled by endpoint too, but keep top-level
    # call for non-endpoint-aware callers)
    endpoint = get_endpoint(content_type)
    if endpoint and hasattr(endpoint, 'on_create'):
        endpoint.on_create(data_dir, data, current_user)
    else:
        validate_uniqueness(data_dir, content_type, data)

    record_id = gen_id(PREFIX_MAP.get(content_type, content_type))
    data["id"] = record_id
    data["created_at"] = data.get("created_at") or now_iso()
    data["updated_at"] = data["created_at"]
    data["deleted_at"] = None

    if current_user and content_type != "user":
        data.setdefault("created_by", current_user)

    # Apply endpoint defaults
    if endpoint and hasattr(endpoint, 'DEFAULTS'):
        for k, v in endpoint.DEFAULTS.items():
            if isinstance(v, list):
                data.setdefault(k, list(v))  # copy mutable defaults
            else:
                data.setdefault(k, v)

    filepath = data_dir / content_type / f"{record_id}.md"
    body = data.pop("_body", "")
    save_record(filepath, data, body=body)
    data["_body"] = body

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

    # Endpoint-specific pre-update hooks
    endpoint = get_endpoint(content_type)
    if endpoint and hasattr(endpoint, 'on_pre_update'):
        endpoint.on_pre_update(data_dir, record_id, rec, updates)

    for field in ["type", "status", "role", "visibility", "target_type"]:
        if field in updates:
            validate_enum(content_type, field, updates[field])

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

    # Endpoint-specific cascade
    endpoint = get_endpoint(content_type)
    if endpoint and hasattr(endpoint, 'on_delete_cascade'):
        endpoint.on_delete_cascade(data_dir, record_id)

    return {"deleted": record_id, "mode": "soft"}
