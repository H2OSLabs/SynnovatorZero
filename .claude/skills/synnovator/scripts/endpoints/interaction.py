"""Interaction endpoint: likes, comments, ratings."""

DEFAULTS = {}


def on_create(data_dir, data, current_user):
    pass


def on_pre_update(data_dir, record_id, rec, updates):
    pass


def on_delete_cascade(data_dir, record_id):
    from cascade import _cascade_delete_child_comments, _cascade_delete_relations
    from relations import read_relation
    from cache import _update_cache_stats

    _cascade_delete_child_comments(data_dir, record_id)
    # Find target before deleting relation (needed for cache update)
    target_rels = read_relation(data_dir, "target_interaction", {"interaction_id": record_id})
    _cascade_delete_relations(data_dir, "target_interaction", "interaction_id", record_id)
    for rel in target_rels:
        _update_cache_stats(data_dir, rel.get("target_type"), rel.get("target_id"))
