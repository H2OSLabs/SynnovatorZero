"""
Endpoint registry: maps content_type name to its module.
"""

from endpoints import category, post, resource, rule, user, group, interaction

REGISTRY = {
    "category": category,
    "post": post,
    "resource": resource,
    "rule": rule,
    "user": user,
    "group": group,
    "interaction": interaction,
}


def get_endpoint(content_type):
    """Return the endpoint module for a content type, or None."""
    return REGISTRY.get(content_type)
