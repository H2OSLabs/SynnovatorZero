"""Batch status update schema"""
from pydantic import BaseModel
from typing import List


class BatchStatusUpdate(BaseModel):
    ids: List[int]
    status: str
