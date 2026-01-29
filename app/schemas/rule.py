"""Rule Pydantic schemas"""
from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Any, Dict, List, Optional


class ScoringCriterion(BaseModel):
    name: str
    weight: float
    description: Optional[str] = None


class CheckCondition(BaseModel):
    type: str
    params: Optional[Dict[str, Any]] = None


class CheckDefinition(BaseModel):
    trigger: str
    phase: str  # "pre" or "post"
    condition: Optional[CheckCondition] = None
    on_fail: Optional[str] = "deny"  # "deny" | "warn" | "flag"
    action: Optional[str] = None
    action_params: Optional[Dict[str, Any]] = None
    message: Optional[str] = None


class RuleBase(BaseModel):
    name: str
    description: str
    allow_public: Optional[bool] = False
    require_review: Optional[bool] = False
    reviewers: Optional[List[int]] = None
    submission_start: Optional[datetime] = None
    submission_deadline: Optional[datetime] = None
    submission_format: Optional[List[str]] = None
    max_submissions: Optional[int] = None
    min_team_size: Optional[int] = None
    max_team_size: Optional[int] = None
    scoring_criteria: Optional[List[ScoringCriterion]] = None
    checks: Optional[List[CheckDefinition]] = None
    content: Optional[str] = None


class RuleCreate(RuleBase):
    name: str
    description: str

    @model_validator(mode="after")
    def validate_scoring_criteria_weights(self) -> "RuleCreate":
        if self.scoring_criteria:
            total = sum(c.weight for c in self.scoring_criteria)
            if abs(total - 100) > 0.01:
                raise ValueError(
                    f"scoring_criteria weights must sum to 100, got {total}"
                )
        return self


class RuleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    allow_public: Optional[bool] = None
    require_review: Optional[bool] = None
    reviewers: Optional[List[int]] = None
    submission_start: Optional[datetime] = None
    submission_deadline: Optional[datetime] = None
    submission_format: Optional[List[str]] = None
    max_submissions: Optional[int] = None
    min_team_size: Optional[int] = None
    max_team_size: Optional[int] = None
    scoring_criteria: Optional[List[ScoringCriterion]] = None
    checks: Optional[List[CheckDefinition]] = None
    content: Optional[str] = None

    @model_validator(mode="after")
    def validate_scoring_criteria_weights(self) -> "RuleUpdate":
        if self.scoring_criteria is not None:
            total = sum(c.weight for c in self.scoring_criteria)
            if abs(total - 100) > 0.01:
                raise ValueError(
                    f"scoring_criteria weights must sum to 100, got {total}"
                )
        return self


class RuleInDBBase(RuleBase):
    id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class Rule(RuleInDBBase):
    pass
