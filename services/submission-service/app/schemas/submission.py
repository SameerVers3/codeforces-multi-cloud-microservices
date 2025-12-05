from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from decimal import Decimal

class SubmissionCreate(BaseModel):
    contest_id: UUID
    problem_id: UUID
    code: str = Field(..., min_length=1)
    language: str = Field(default="cpp", pattern="^cpp$")

class SubmissionUpdate(BaseModel):
    status: Optional[str] = None
    execution_time_ms: Optional[int] = None
    memory_used_mb: Optional[Decimal] = None
    test_cases_passed: Optional[int] = None
    total_test_cases: Optional[int] = None
    score: Optional[Decimal] = None
    error_message: Optional[str] = None

class SubmissionResponse(BaseModel):
    id: UUID
    contest_id: UUID
    problem_id: UUID
    user_id: UUID
    code: str
    language: str
    status: str
    execution_time_ms: Optional[int]
    memory_used_mb: Optional[Decimal]
    test_cases_passed: int
    total_test_cases: int
    score: Decimal
    error_message: Optional[str]
    submitted_at: datetime
    evaluated_at: Optional[datetime]

    class Config:
        from_attributes = True

class SubmissionResultResponse(BaseModel):
    id: UUID
    submission_id: UUID
    test_case_id: UUID
    status: str
    execution_time_ms: Optional[int]
    memory_used_mb: Optional[Decimal]
    actual_output: Optional[str]
    error_message: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class SubmissionWithResults(SubmissionResponse):
    results: List[SubmissionResultResponse] = []

