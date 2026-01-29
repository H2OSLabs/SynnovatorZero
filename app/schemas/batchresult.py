"""Batch result schema"""
from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class BatchResult(BaseModel):
    success_count: int
    failed_count: int
    failed_ids: Optional[List[int]] = None
    errors: Optional[Dict[str, Any]] = None
