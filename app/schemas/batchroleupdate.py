"""Batch role update schema"""
from pydantic import BaseModel
from typing import List


class BatchRoleUpdate(BaseModel):
    ids: List[int]
    role: str
