from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class TestCaseBase(BaseModel):
    input_data: str
    expected_output: str
    is_sample: bool = False
    order_index: int

class TestCaseCreate(TestCaseBase):
    problem_id: UUID

class TestCaseUpdate(BaseModel):
    input_data: Optional[str] = None
    expected_output: Optional[str] = None
    is_sample: Optional[bool] = None
    order_index: Optional[int] = None

class TestCaseResponse(TestCaseBase):
    id: UUID
    problem_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

