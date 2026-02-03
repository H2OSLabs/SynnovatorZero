"""Shared enum definitions for API schemas"""

from enum import StrEnum


class PostType(StrEnum):
    profile = "profile"
    team = "team"
    category = "category"
    for_category = "for_category"
    certificate = "certificate"
    general = "general"

