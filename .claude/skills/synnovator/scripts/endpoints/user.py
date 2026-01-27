"""User endpoint: user profiles with uniqueness constraints."""

from core import validate_uniqueness

DEFAULTS = {
    "role": "participant",
}


def on_create(data_dir, data, current_user):
    validate_uniqueness(data_dir, "user", data)


def on_pre_update(data_dir, record_id, rec, updates):
    validate_uniqueness(data_dir, "user", {**rec, **updates}, exclude_id=record_id)


def on_delete_cascade(data_dir, record_id):
    from cascade import (
        _cascade_soft_delete_user_interactions,
        _cascade_delete_relations,
        _cascade_delete_user_user_relations,
    )
    _cascade_delete_relations(data_dir, "group_user", "user_id", record_id)
    _cascade_delete_user_user_relations(data_dir, record_id)
    _cascade_soft_delete_user_interactions(data_dir, record_id)
