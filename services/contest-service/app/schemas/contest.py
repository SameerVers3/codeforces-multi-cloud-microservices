from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID

class ContestBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    max_participants: Optional[int] = None

class ContestCreate(ContestBase):
    pass

class ContestUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    is_active: Optional[bool] = None
    registration_open: Optional[bool] = None
    max_participants: Optional[int] = None

class ContestResponse(ContestBase):
    id: UUID
    created_by: UUID
    is_active: bool
    registration_open: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ContestWithProblems(ContestResponse):
    problems: List[Any] = []

