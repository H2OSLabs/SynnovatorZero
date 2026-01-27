"""Cascade delete service — orchestrates related record cleanup before soft delete.

Each function handles the cascade chain for a specific content type.
Relationship records are hard-deleted; content types are soft-deleted.
"""
from sqlalchemy.orm import Session

from app import crud
from app.models.interaction import Interaction
from app.models.post import Post


def _hard_delete_interactions(db: Session, interaction_ids: list[int]):
    """Hard-delete interaction records by IDs (used after target_interaction bindings removed)."""
    for iid in interaction_ids:
        obj = db.query(Interaction).filter(Interaction.id == iid).first()
        if obj:
            db.delete(obj)
    db.commit()


def _cascade_delete_interactions_for_target(db: Session, target_type: str, target_id: int):
    """Remove all target_interaction bindings and hard-delete the linked interactions."""
    interaction_ids = crud.target_interactions.remove_all_by_target(
        db, target_type=target_type, target_id=target_id,
    )
    _hard_delete_interactions(db, interaction_ids)


def _update_post_cache(db: Session, post_id: int):
    """Recalculate post cache counters."""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return
    post.like_count = crud.target_interactions.count_by_target_and_type(
        db, target_type="post", target_id=post_id, interaction_type="like",
    )
    post.comment_count = crud.target_interactions.count_by_target_and_type(
        db, target_type="post", target_id=post_id, interaction_type="comment",
    )
    rating_tis = crud.target_interactions.get_multi_by_target(
        db, target_type="post", target_id=post_id, interaction_type="rating",
    )
    if rating_tis:
        total = 0.0
        count = 0
        for ti in rating_tis:
            interaction = crud.interactions.get(db, id=ti.interaction_id)
            if interaction and interaction.value and isinstance(interaction.value, dict):
                scores = list(interaction.value.values())
                if scores:
                    total += sum(scores) / len(scores)
                    count += 1
        post.average_rating = round(total / count, 2) if count > 0 else None
    else:
        post.average_rating = None
    db.commit()


def cascade_delete_category(db: Session, category_id: int):
    """TC-DEL-001, TC-DEL-010: Delete category with cascade.

    Cascade chain:
    - category_rule relations (hard delete)
    - category_post relations (hard delete)
    - category_group relations (hard delete)
    - category_category relations — both source and target (hard delete)
    - target_interaction bindings + interactions on this category (hard delete)
    - category itself (soft delete)
    """
    crud.category_rules.remove_all_by_category(db, category_id=category_id)
    crud.category_posts.remove_all_by_category(db, category_id=category_id)
    crud.category_groups.remove_all_by_category(db, category_id=category_id)
    crud.category_categories.remove_all_by_category(db, category_id=category_id)
    _cascade_delete_interactions_for_target(db, "category", category_id)
    crud.categories.remove(db, id=category_id)


def cascade_delete_user(db: Session, user_id: int):
    """TC-DEL-003, TC-DEL-011: Delete user with cascade.

    Cascade chain:
    - All user's interactions (hard delete, with cache update on affected posts)
    - group:user (member) relations (hard delete)
    - user:user relations — both directions (hard delete)
    - user itself (soft delete)
    """
    # Find all interactions created by this user, hard-delete them + bindings
    interactions = db.query(Interaction).filter(
        Interaction.created_by == user_id,
        Interaction.deleted_at.is_(None),
    ).all()

    affected_post_ids = set()
    for interaction in interactions:
        # Find target_interaction bindings for this interaction
        tis = crud.target_interactions.get_all_by_interaction(db, interaction_id=interaction.id)
        for ti in tis:
            if ti.target_type == "post":
                affected_post_ids.add(ti.target_id)
        crud.target_interactions.remove_all_by_interaction(db, interaction_id=interaction.id)
        db.delete(interaction)
    db.commit()

    # Update caches on affected posts
    for post_id in affected_post_ids:
        _update_post_cache(db, post_id)

    crud.members.remove_all_by_user(db, user_id=user_id)
    crud.user_users.remove_all_for_user(db, user_id=user_id)
    crud.users.remove(db, id=user_id)


def cascade_delete_post(db: Session, post_id: int):
    """TC-DEL-012: Delete post with full cascade chain.

    Cascade chain:
    - category_post relations (hard delete)
    - post_post relations — both source and target (hard delete)
    - post_resource relations (hard delete)
    - target_interaction bindings + interactions on this post (hard delete)
    - post itself (soft delete)
    """
    crud.category_posts.remove_all_by_post(db, post_id=post_id)
    crud.post_posts.remove_all_by_post(db, post_id=post_id)
    crud.post_resources.remove_all_by_post(db, post_id=post_id)
    _cascade_delete_interactions_for_target(db, "post", post_id)
    crud.posts.remove(db, id=post_id)


def cascade_delete_rule(db: Session, rule_id: int):
    """TC-DEL-002, TC-DEL-013: Delete rule with cascade.

    Cascade chain:
    - category_rule relations (hard delete)
    - rule itself (soft delete)
    """
    crud.category_rules.remove_all_by_rule(db, rule_id=rule_id)
    crud.rules.remove(db, id=rule_id)


def cascade_delete_group(db: Session, group_id: int):
    """TC-DEL-004, TC-DEL-014: Delete group with cascade.

    Cascade chain:
    - member (group_user) relations (hard delete)
    - category_group relations (hard delete)
    - group itself (soft delete)
    """
    crud.members.remove_all_by_group(db, group_id=group_id)
    crud.category_groups.remove_all_by_group(db, group_id=group_id)
    crud.groups.remove(db, id=group_id)


def cascade_delete_interaction(db: Session, interaction_id: int):
    """TC-DEL-005, TC-DEL-015: Delete interaction with cascade.

    For likes: removes target_interaction binding, updates post cache.
    For comments: cascades to child comments (recursive), updates post cache.
    For ratings: removes target_interaction binding, updates post cache.
    """
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        return

    # Collect all interaction IDs to delete (recursive for comments)
    ids_to_delete = _collect_interaction_tree(db, interaction_id)

    # Find affected posts for cache update
    affected_post_ids = set()
    for iid in ids_to_delete:
        tis = crud.target_interactions.get_all_by_interaction(db, interaction_id=iid)
        for ti in tis:
            if ti.target_type == "post":
                affected_post_ids.add(ti.target_id)
        crud.target_interactions.remove_all_by_interaction(db, interaction_id=iid)

    # Hard-delete all interactions in the tree
    for iid in ids_to_delete:
        obj = db.query(Interaction).filter(Interaction.id == iid).first()
        if obj:
            db.delete(obj)
    db.commit()

    # Update caches
    for post_id in affected_post_ids:
        _update_post_cache(db, post_id)


def _collect_interaction_tree(db: Session, interaction_id: int) -> list[int]:
    """Collect interaction and all descendant interactions (for comment trees)."""
    ids = []
    stack = [interaction_id]
    while stack:
        current = stack.pop()
        ids.append(current)
        # Find children (comments with parent_id == current)
        children = db.query(Interaction).filter(
            Interaction.parent_id == current,
            Interaction.deleted_at.is_(None),
        ).all()
        for child in children:
            stack.append(child.id)
    return ids
