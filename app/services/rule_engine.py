"""Declarative Rule Engine — evaluates checks from Rules linked to a category.

The engine supports:
- Fixed-field expansion: max_submissions, submission_start/deadline, submission_format,
  min_team_size, max_team_size automatically expand to equivalent checks.
- Custom checks: declarative condition-action definitions in Rule.checks field.
- Condition types: time_window, count, exists, field_match, resource_format, resource_required, aggregate.
- on_fail behavior: deny (raise), warn (return warning), flag (tag target).
- post-phase actions: compute_ranking, flag_disqualified, award_certificate.
"""
from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy.orm import Session

from app import crud


class RuleCheckError(Exception):
    """Raised when a pre-phase check with on_fail=deny fails."""
    def __init__(self, message: str, rule_name: str = ""):
        self.message = message
        self.rule_name = rule_name
        super().__init__(message)


class RuleCheckWarning:
    """Returned when a check with on_fail=warn fails."""
    def __init__(self, message: str, rule_name: str = ""):
        self.message = message
        self.rule_name = rule_name


def _expand_fixed_fields(rule) -> list[dict]:
    """Expand Rule fixed fields into equivalent check definitions."""
    expanded = []

    # submission_start + submission_deadline → time_window
    if rule.submission_start is not None or rule.submission_deadline is not None:
        start_str = rule.submission_start.isoformat() if rule.submission_start else None
        end_str = rule.submission_deadline.isoformat() if rule.submission_deadline else None
        expanded.append({
            "trigger": "create_relation(category_post)",
            "phase": "pre",
            "condition": {
                "type": "time_window",
                "params": {"start": start_str, "end": end_str},
            },
            "on_fail": "deny",
            "message": "Submission not within allowed time window",
        })

    # max_submissions → count
    if rule.max_submissions is not None:
        expanded.append({
            "trigger": "create_relation(category_post)",
            "phase": "pre",
            "condition": {
                "type": "count",
                "params": {
                    "entity": "category_post",
                    "scope": "user",
                    "filter": {"relation_type": "submission"},
                    "op": "<",
                    "value": rule.max_submissions,
                },
            },
            "on_fail": "deny",
            "message": f"Max submissions reached ({rule.max_submissions})",
        })

    # submission_format → resource_format
    if rule.submission_format:
        expanded.append({
            "trigger": "create_relation(category_post)",
            "phase": "pre",
            "condition": {
                "type": "resource_format",
                "params": {"formats": rule.submission_format},
            },
            "on_fail": "deny",
            "message": f"Submission format must be one of: {', '.join(rule.submission_format)}",
        })

    # min_team_size → count (group_user, scope=group)
    if rule.min_team_size is not None:
        expanded.append({
            "trigger": "create_relation(category_post)",
            "phase": "pre",
            "condition": {
                "type": "count",
                "params": {
                    "entity": "group_user",
                    "scope": "group",
                    "filter": {"status": "accepted"},
                    "op": ">=",
                    "value": rule.min_team_size,
                },
            },
            "on_fail": "deny",
            "message": f"Team must have at least {rule.min_team_size} accepted members",
        })

    # max_team_size → count (group_user, scope=group)
    if rule.max_team_size is not None:
        expanded.append({
            "trigger": "create_relation(group_user)",
            "phase": "pre",
            "condition": {
                "type": "count",
                "params": {
                    "entity": "group_user",
                    "scope": "group",
                    "filter": {"status": "accepted"},
                    "op": "<",
                    "value": rule.max_team_size,
                },
            },
            "on_fail": "deny",
            "message": f"Team cannot exceed {rule.max_team_size} members",
        })

    return expanded


def _get_checks_for_trigger(rule, trigger: str, phase: str) -> list[dict]:
    """Get all checks (expanded + custom) for a given trigger and phase."""
    expanded = _expand_fixed_fields(rule)

    custom_checks = []
    if rule.checks:
        raw = rule.checks
        if isinstance(raw, list):
            custom_checks = raw
        # Otherwise ignore (invalid format)

    all_checks = expanded + custom_checks

    return [
        c for c in all_checks
        if c.get("trigger") == trigger and c.get("phase") == phase
    ]


def _evaluate_condition(db: Session, condition: dict, context: dict) -> bool:
    """Evaluate a single condition. Returns True if condition passes."""
    ctype = condition.get("type")
    params = condition.get("params", {})

    if ctype == "time_window":
        return _eval_time_window(params)
    elif ctype == "count":
        return _eval_count(db, params, context)
    elif ctype == "exists":
        return _eval_exists(db, params, context)
    elif ctype == "field_match":
        return _eval_field_match(db, params, context)
    elif ctype == "resource_format":
        return _eval_resource_format(db, params, context)
    elif ctype == "resource_required":
        return _eval_resource_required(db, params, context)
    elif ctype == "aggregate":
        return _eval_aggregate(db, params, context)
    else:
        # Unknown condition type: pass by default (don't block)
        return True


def _eval_time_window(params: dict) -> bool:
    """Check if current time is within [start, end]."""
    now = datetime.now(timezone.utc)
    start = params.get("start")
    end = params.get("end")

    if start is not None:
        if isinstance(start, str):
            start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
        else:
            start_dt = start
        if start_dt.tzinfo is None:
            start_dt = start_dt.replace(tzinfo=timezone.utc)
        if now < start_dt:
            return False

    if end is not None:
        if isinstance(end, str):
            end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))
        else:
            end_dt = end
        if end_dt.tzinfo is None:
            end_dt = end_dt.replace(tzinfo=timezone.utc)
        if now > end_dt:
            return False

    return True


def _eval_count(db: Session, params: dict, context: dict) -> bool:
    """Evaluate count condition on a relationship entity."""
    entity = params.get("entity", "")
    scope = params.get("scope", "")
    op = params.get("op", ">=")
    value = params.get("value", 0)
    filt = params.get("filter", {})

    # Resolve $rule.<field> references in value
    if isinstance(value, str) and value.startswith("$rule."):
        field_name = value[len("$rule."):]
        rule_obj = context.get("rule")
        if rule_obj:
            value = getattr(rule_obj, field_name, 0) or 0
        else:
            value = 0

    actual = 0

    if entity == "category_post":
        category_id = context.get("category_id")
        user_id = context.get("user_id")
        if category_id and scope == "user" and user_id:
            actual = crud.category_posts.count_submissions_by_user(
                db, category_id=category_id, user_id=user_id,
            )
        elif category_id:
            rels = crud.category_posts.get_multi_by_category(
                db, category_id=category_id,
                relation_type=filt.get("relation_type"),
            )
            actual = len(rels)

    elif entity == "group_user":
        group_id = context.get("group_id")
        if group_id and scope == "group":
            status_filter = filt.get("status")
            actual = crud.members.count_by_group(db, group_id=group_id, status=status_filter)

    return _compare(actual, op, value)


def _eval_exists(db: Session, params: dict, context: dict) -> bool:
    """Check if an entity exists (or doesn't exist if require=false)."""
    entity = params.get("entity", "")
    scope = params.get("scope", "")
    require = params.get("require", True)
    filt = params.get("filter", {})

    found = False

    if entity == "post_resource":
        post_id = context.get("post_id")
        if post_id and scope == "post":
            rels = crud.post_resources.get_multi_by_post(db, post_id=post_id)
            found = len(rels) > 0

    elif entity == "category_post":
        user_id = context.get("user_id")
        category_id = context.get("category_id")
        if user_id and category_id:
            relation_type = filt.get("relation_type")
            rels = crud.category_posts.get_multi_by_category(
                db, category_id=category_id, relation_type=relation_type,
            )
            # Filter by user
            for rel in rels:
                post = crud.posts.get(db, id=rel.post_id)
                if post and post.created_by == user_id:
                    found = True
                    break

    elif entity == "category_group":
        category_id = context.get("category_id")
        if category_id:
            rels = crud.category_groups.get_multi_by_category(db, category_id=category_id)
            if scope == "user_group":
                user_id = context.get("user_id")
                if user_id:
                    for rel in rels:
                        member = crud.members.get_by_group_and_user(db, group_id=rel.group_id, user_id=user_id)
                        if member:
                            found = True
                            break
            else:
                found = len(rels) > 0

    elif entity == "group_user":
        user_id = context.get("user_id")
        if user_id:
            # Check if user is in any accepted group
            from app.models.member import Member
            status_filter = filt.get("status", "accepted")
            members = db.query(Member).filter(
                Member.user_id == user_id,
                Member.status == status_filter,
            ).all()
            found = len(members) > 0

    elif entity == "post":
        user_id = context.get("user_id")
        if user_id and scope == "user":
            from app.models.post import Post
            q = db.query(Post).filter(
                Post.created_by == user_id,
                Post.deleted_at.is_(None),
            )
            if "type" in filt:
                q = q.filter(Post.type == filt["type"])
            if "status" in filt:
                q = q.filter(Post.status == filt["status"])
            found = q.first() is not None

    if require:
        return found
    else:
        return not found


def _eval_field_match(db: Session, params: dict, context: dict) -> bool:
    """Check a field value on an entity."""
    entity = params.get("entity", "")
    target = params.get("target", "$target")
    field = params.get("field", "")
    op = params.get("op", "==")
    value = params.get("value")

    obj = None
    if entity == "category":
        cat_id = context.get("category_id")
        if cat_id:
            obj = crud.categories.get(db, id=cat_id)
    elif entity == "post":
        post_id = context.get("post_id")
        if post_id:
            obj = crud.posts.get(db, id=post_id)
    elif entity == "group":
        group_id = context.get("group_id")
        if group_id:
            obj = crud.groups.get(db, id=group_id)

    if obj is None:
        return False

    actual = getattr(obj, field, None)
    return _compare_field(actual, op, value)


def _eval_resource_format(db: Session, params: dict, context: dict) -> bool:
    """Check that post resources match allowed formats."""
    formats = params.get("formats", [])
    require_any = params.get("require_any", False)
    post_id = context.get("post_id")
    if not post_id or not formats:
        return True

    rels = crud.post_resources.get_multi_by_post(db, post_id=post_id)
    if not rels:
        return True  # No resources to check

    for rel in rels:
        resource = crud.resources.get(db, id=rel.resource_id)
        if resource:
            ext = _get_extension(resource.filename) if resource.filename else ""
            if require_any:
                if ext.lower() in [f.lower() for f in formats]:
                    return True
            else:
                if ext.lower() not in [f.lower() for f in formats]:
                    return False

    if require_any:
        return False  # None matched
    return True  # All matched


def _eval_resource_required(db: Session, params: dict, context: dict) -> bool:
    """Check that post has required number of resources (optionally with format)."""
    min_count = params.get("min_count", 1)
    formats = params.get("formats")
    post_id = context.get("post_id")
    if not post_id:
        return True

    rels = crud.post_resources.get_multi_by_post(db, post_id=post_id)
    if formats:
        count = 0
        for rel in rels:
            resource = crud.resources.get(db, id=rel.resource_id)
            if resource:
                ext = _get_extension(resource.filename) if resource.filename else ""
                if ext.lower() in [f.lower() for f in formats]:
                    count += 1
        return count >= min_count
    else:
        return len(rels) >= min_count


def _eval_aggregate(db: Session, params: dict, context: dict) -> bool:
    """Aggregate check across entities in a scope."""
    entity = params.get("entity", "")
    scope = params.get("scope", "")
    filt = params.get("filter", {})
    agg_func = params.get("agg_func", "count")
    op = params.get("op", ">=")
    value = params.get("value", 0)

    # Resolve $rule references
    if isinstance(value, str) and value.startswith("$rule."):
        field_name = value[len("$rule."):]
        rule_obj = context.get("rule")
        if rule_obj:
            value = getattr(rule_obj, field_name, 0) or 0

    if scope == "each_group_in_category":
        category_id = context.get("category_id")
        if not category_id:
            return True
        # Get all groups registered to this category
        cat_groups = crud.category_groups.get_multi_by_category(db, category_id=category_id)
        for cg in cat_groups:
            status_filter = filt.get("status")
            count = crud.members.count_by_group(db, group_id=cg.group_id, status=status_filter)
            if not _compare(count, op, value):
                return False
        return True

    return True  # Unknown scope


def _compare(actual: int, op: str, value: int) -> bool:
    """Compare actual vs value using operator string."""
    if op == "<":
        return actual < value
    elif op == "<=":
        return actual <= value
    elif op == "==":
        return actual == value
    elif op == ">=":
        return actual >= value
    elif op == ">":
        return actual > value
    elif op == "!=":
        return actual != value
    return True


def _compare_field(actual: Any, op: str, value: Any) -> bool:
    """Compare field values with extended operators."""
    if op == "==":
        return actual == value
    elif op == "!=":
        return actual != value
    elif op == "in":
        return actual in (value if isinstance(value, list) else [value])
    elif op == "not_in":
        return actual not in (value if isinstance(value, list) else [value])
    elif op in ("<", "<=", ">=", ">"):
        try:
            return _compare(actual, op, value)
        except TypeError:
            return False
    return True


def _get_extension(filename: str) -> str:
    """Extract file extension without dot."""
    if "." in filename:
        return filename.rsplit(".", 1)[-1]
    return ""


# --- Public API ---

def run_pre_checks(
    db: Session,
    trigger: str,
    category_id: int,
    context: dict,
) -> list[RuleCheckWarning]:
    """Run all pre-phase checks for a trigger on a category's rules.

    Args:
        db: Database session
        trigger: The operation point (e.g., "create_relation(category_post)")
        category_id: The category to get rules from
        context: Dict with keys like user_id, post_id, group_id, etc.

    Returns:
        List of warnings (on_fail=warn). Raises RuleCheckError for on_fail=deny.
    """
    warnings = []
    cat_rules = crud.category_rules.get_multi_by_category(db, category_id=category_id)

    for cr in cat_rules:
        rule = crud.rules.get(db, id=cr.rule_id)
        if rule is None:
            continue

        ctx = {**context, "rule": rule, "category_id": category_id}
        checks = _get_checks_for_trigger(rule, trigger, "pre")

        for check in checks:
            condition = check.get("condition")
            if condition is None:
                continue

            passed = _evaluate_condition(db, condition, ctx)
            if not passed:
                on_fail = check.get("on_fail", "deny")
                message = check.get("message", "Rule check failed")
                if on_fail == "deny":
                    raise RuleCheckError(message=message, rule_name=rule.name)
                elif on_fail == "warn":
                    warnings.append(RuleCheckWarning(message=message, rule_name=rule.name))
                elif on_fail == "flag":
                    # Flag target (add tag to post/group) — simplified implementation
                    warnings.append(RuleCheckWarning(message=f"[flagged] {message}", rule_name=rule.name))

    return warnings


def run_post_hooks(
    db: Session,
    trigger: str,
    category_id: int,
    context: dict,
) -> list[str]:
    """Run all post-phase checks/actions for a trigger on a category's rules.

    Post hooks never block the operation. They execute actions when conditions are met.

    Returns:
        List of action log messages.
    """
    logs = []
    cat_rules = crud.category_rules.get_multi_by_category(db, category_id=category_id)

    for cr in cat_rules:
        rule = crud.rules.get(db, id=cr.rule_id)
        if rule is None:
            continue

        ctx = {**context, "rule": rule, "category_id": category_id}
        checks = _get_checks_for_trigger(rule, trigger, "post")

        for check in checks:
            condition = check.get("condition")
            action = check.get("action")
            action_params = check.get("action_params", {})
            message = check.get("message", "")

            # If condition exists, evaluate it; if not, action always runs
            if condition:
                passed = _evaluate_condition(db, condition, ctx)
                if not passed:
                    logs.append(f"Post-hook skipped (condition not met): {message}")
                    continue

            if action:
                try:
                    _execute_action(db, action, action_params, ctx)
                    logs.append(f"Post-hook executed: {action} — {message}")
                except Exception as e:
                    logs.append(f"Post-hook failed: {action} — {e}")

    return logs


def _execute_action(db: Session, action: str, params: dict, context: dict):
    """Execute a post-phase action."""
    if action == "compute_ranking":
        _action_compute_ranking(db, params, context)
    elif action == "flag_disqualified":
        _action_flag_disqualified(db, params, context)
    elif action == "award_certificate":
        _action_award_certificate(db, params, context)
    elif action == "notify":
        pass  # Notification not implemented
    else:
        pass  # Unknown action, skip


def _action_compute_ranking(db: Session, params: dict, context: dict):
    """Compute ranking for posts in a category based on average_rating."""
    category_id = context.get("category_id")
    if not category_id:
        return

    source_field = params.get("source_field", "average_rating")
    order = params.get("order", "desc")
    output_tag_prefix = params.get("output_tag_prefix", "rank_")

    # Get all submissions
    rels = crud.category_posts.get_multi_by_category(
        db, category_id=category_id, relation_type="submission",
    )

    scored_posts = []
    for rel in rels:
        post = crud.posts.get(db, id=rel.post_id)
        if post:
            score = getattr(post, source_field, None)
            if score is not None:
                scored_posts.append((post, score))

    # Filter out disqualified posts (posts with any disqualification tag)
    disqualification_tags = {"team_too_small", "missing_attachment", "disqualified"}
    eligible_posts = []
    for post, score in scored_posts:
        tags = post.tags or []
        if isinstance(tags, str):
            tags = [tags]
        if not any(t in disqualification_tags for t in tags):
            eligible_posts.append((post, score))

    # Sort
    reverse = (order == "desc")
    eligible_posts.sort(key=lambda x: x[1], reverse=reverse)

    # Assign ranking tags with tie handling
    rank = 1
    i = 0
    while i < len(eligible_posts):
        # Find all posts with same score (tie group)
        current_score = eligible_posts[i][1]
        tie_group = []
        while i < len(eligible_posts) and eligible_posts[i][1] == current_score:
            tie_group.append(eligible_posts[i][0])
            i += 1

        # All tied posts get the same rank
        tag = f"{output_tag_prefix}{rank}"
        for post in tie_group:
            current_tags = post.tags or []
            if isinstance(current_tags, str):
                current_tags = [current_tags]
            current_tags = [t for t in current_tags if not t.startswith(output_tag_prefix)]
            current_tags.append(tag)
            post.tags = current_tags

        # Next rank skips by tie count (e.g., 2 tied at rank 1 → next is rank 3)
        rank += len(tie_group)

    db.commit()


def _action_flag_disqualified(db: Session, params: dict, context: dict):
    """Flag disqualified groups/posts in a category."""
    category_id = context.get("category_id")
    if not category_id:
        return

    target = params.get("target", "group")
    tag = params.get("tag", "disqualified")

    # For groups: check each group's team size against rule's min_team_size
    if target == "group":
        rule = context.get("rule")
        min_size = rule.min_team_size if rule else None
        if min_size is None:
            return

        cat_groups = crud.category_groups.get_multi_by_category(db, category_id=category_id)
        for cg in cat_groups:
            count = crud.members.count_by_group(db, group_id=cg.group_id, status="accepted")
            if count < min_size:
                # Find submissions by group members and tag them
                group_members = crud.members.get_multi_by_group(db, group_id=cg.group_id)
                for member in group_members:
                    rels = crud.category_posts.get_multi_by_category(
                        db, category_id=category_id, relation_type="submission",
                    )
                    for rel in rels:
                        post = crud.posts.get(db, id=rel.post_id)
                        if post and post.created_by == member.user_id:
                            current_tags = post.tags or []
                            if isinstance(current_tags, str):
                                current_tags = [current_tags]
                            if tag not in current_tags:
                                current_tags.append(tag)
                                post.tags = current_tags
        db.commit()

    # For posts: check each submission post directly (e.g., missing resource)
    elif target == "post":
        rels = crud.category_posts.get_multi_by_category(
            db, category_id=category_id, relation_type="submission",
        )
        for rel in rels:
            post = crud.posts.get(db, id=rel.post_id)
            if not post:
                continue
            # Check condition based on tag type
            should_flag = False
            if tag == "missing_attachment":
                post_rels = crud.post_resources.get_multi_by_post(db, post_id=post.id)
                should_flag = len(post_rels) == 0
            if should_flag:
                current_tags = post.tags or []
                if isinstance(current_tags, str):
                    current_tags = [current_tags]
                if tag not in current_tags:
                    current_tags.append(tag)
                    post.tags = current_tags
        db.commit()


def _action_award_certificate(db: Session, params: dict, context: dict):
    """Award certificates based on ranking. Depends on compute_ranking having run first."""
    category_id = context.get("category_id")
    if not category_id:
        return

    rules_list = params.get("rules", [])
    output_tag_prefix = "rank_"  # Must match compute_ranking output

    rels = crud.category_posts.get_multi_by_category(
        db, category_id=category_id, relation_type="submission",
    )

    for rel in rels:
        post = crud.posts.get(db, id=rel.post_id)
        if not post:
            continue
        tags = post.tags or []
        if isinstance(tags, str):
            tags = [tags]

        # Find rank tag
        rank = None
        for t in tags:
            if t.startswith(output_tag_prefix):
                try:
                    rank = int(t[len(output_tag_prefix):])
                except ValueError:
                    pass

        if rank is None:
            continue

        # Check award rules
        for award_rule in rules_list:
            rank_range = award_rule.get("rank_range", [0, 0])
            if rank_range[0] <= rank <= rank_range[1]:
                title = award_rule.get("title", "Certificate")
                # Create certificate post
                from app.models.post import Post as PostModel
                cert_post = PostModel(
                    title=f"{title} — {post.title}",
                    content=f"Certificate awarded for rank {rank}",
                    type="certificate",
                    status="published",
                    visibility="public",
                    created_by=post.created_by,
                )
                db.add(cert_post)
                db.commit()
                db.refresh(cert_post)
                # Link to category
                crud.category_posts.create(
                    db, category_id=category_id, post_id=cert_post.id, relation_type="reference",
                )
                break  # Only first matching rule
