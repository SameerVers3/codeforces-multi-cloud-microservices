from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base

class ContestRegistration(Base):
    __tablename__ = "contest_registrations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contest_id = Column(UUID(as_uuid=True), ForeignKey("contests.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    registered_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    contest = relationship("Contest", back_populates="registrations")

    def __repr__(self):
        return f"<ContestRegistration contest={self.contest_id} user={self.user_id}>"

