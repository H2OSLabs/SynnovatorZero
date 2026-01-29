"""Batch operation schemas"""
from pydantic import BaseModel
from typing import List


class BatchIds(BaseModel):
    ids: List[int]
