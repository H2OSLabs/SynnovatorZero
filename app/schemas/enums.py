"""Shared enum definitions for API schemas"""

from enum import StrEnum


class PostType(StrEnum):
    profile = "profile"
    team = "team"
    event = "event"
    proposal = "proposal"  # 提案（可独立存在，也可关联活动参赛）
    certificate = "certificate"
    general = "general"

