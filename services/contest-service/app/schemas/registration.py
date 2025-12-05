from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class RegistrationResponse(BaseModel):
    id: UUID
    contest_id: UUID
    user_id: UUID
    registered_at: datetime

    class Config:
        from_attributes = True

