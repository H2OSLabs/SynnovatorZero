"""Category endpoint: competition or operational events."""

DEFAULTS = {
    "status": "draft",
}


def on_create(data_dir, data, current_user):
    pass


def on_pre_update(data_dir, record_id, rec, updates):
    pass


def on_delete_cascade(data_dir, record_id):
    from cascade import (
        _cascade_soft_delete_interactions,
        _cascade_delete_relations,
        _cascade_delete_category_category_relations,
    )
    _cascade_soft_delete_interactions(data_dir, "category", record_id)
    _cascade_delete_relations(data_dir, "category_rule", "category_id", record_id)
    _cascade_delete_relations(data_dir, "category_post", "category_id", record_id)
    _cascade_delete_relations(data_dir, "category_group", "category_id", record_id)
    _cascade_delete_category_category_relations(data_dir, record_id)
