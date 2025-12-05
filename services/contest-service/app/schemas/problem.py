from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID

class ProblemBase(BaseModel):
    title: str
    description: str
    difficulty: Optional[str] = None
    time_limit_seconds: int = Field(default=2, ge=1)
    memory_limit_mb: int = Field(default=256, ge=1)
    points: int = Field(default=100, ge=0)
    order_index: int

class ProblemCreate(ProblemBase):
    contest_id: UUID

class ProblemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[str] = None
    time_limit_seconds: Optional[int] = Field(None, ge=1)
    memory_limit_mb: Optional[int] = Field(None, ge=1)
    points: Optional[int] = Field(None, ge=0)
    order_index: Optional[int] = None

class ProblemResponse(ProblemBase):
    id: UUID
    contest_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProblemWithTestCases(ProblemResponse):
    test_cases: List[Any] = []

