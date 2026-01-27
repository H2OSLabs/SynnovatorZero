#!/usr/bin/env python3
"""
Synnovator Data Engine - Cascade delete helpers.

Uses lazy imports for relations to avoid circular dependencies.
"""

from core import (
    find_record, load_record, save_record, list_records, now_iso,
)


def _cascade_soft_delete_interactions(data_dir, target_type, target_id):
    """Soft-delete all interactions linked to a target via target_interaction relations."""
    from relations import read_relation, delete_relation

    rels = read_relation(data_dir, "target_interaction", {
        "target_type": target_type, "target_id": target_id
    })
    for rel in rels:
        iact_id = rel.get("interaction_id")
        fp = find_record(data_dir, "interaction", iact_id)
        if fp:
            rec = load_record(fp)
            if not rec.get("deleted_at"):
                rec["deleted_at"] = now_iso()
                body = rec.pop("_body", "")
                save_record(fp, rec, body=body)
    # Clean up the target_interaction relations
    delete_relation(data_dir, "target_interaction", {
        "target_type": target_type, "target_id": target_id
    })


def _cascade_soft_delete_user_interactions(data_dir, user_id):
    """Soft-delete all interactions by a user and update affected targets' cache stats."""
    from relations import read_relation
    from cache import _update_cache_stats

    affected_targets = set()
    for rec in list_records(data_dir, "interaction"):
        if rec.get("created_by") == user_id:
            fp = find_record(data_dir, "interaction", rec["id"])
            if fp:
                # Find this interaction's target via relation
                rels = read_relation(data_dir, "target_interaction", {
                    "interaction_id": rec["id"]
                })
                for rel in rels:
                    affected_targets.add((rel.get("target_type"), rel.get("target_id")))
                rec["deleted_at"] = now_iso()
                body = rec.pop("_body", "")
                save_record(fp, rec, body=body)
    for target_type, target_id in affected_targets:
        _update_cache_stats(data_dir, target_type, target_id)


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
    from relations import delete_relation
    delete_relation(data_dir, relation_type, {key_field: key_value})


def _cascade_delete_user_user_relations(data_dir, user_id):
    """Delete all user_user relations where user is source or target."""
    from relations import read_relation, delete_relation
    for rel in read_relation(data_dir, "user_user"):
        if rel.get("source_user_id") == user_id or rel.get("target_user_id") == user_id:
            delete_relation(data_dir, "user_user", {
                "source_user_id": rel["source_user_id"],
                "target_user_id": rel["target_user_id"],
            })


def _cascade_delete_category_category_relations(data_dir, category_id):
    """Delete all category_category relations where category is source or target."""
    from relations import read_relation, delete_relation
    for rel in read_relation(data_dir, "category_category"):
        if rel.get("source_category_id") == category_id or rel.get("target_category_id") == category_id:
            delete_relation(data_dir, "category_category", {
                "source_category_id": rel["source_category_id"],
                "target_category_id": rel["target_category_id"],
            })
