from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base

class Contest(Base):
    __tablename__ = "contests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    # Store creator user id without enforcing FK to decouple from auth schema
    created_by = Column(UUID(as_uuid=True), nullable=False, index=True)
    start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    end_time = Column(DateTime(timezone=True), nullable=False, index=True)
    duration_minutes = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    registration_open = Column(Boolean, default=True)
    max_participants = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    problems = relationship("Problem", back_populates="contest", cascade="all, delete-orphan")
    registrations = relationship("ContestRegistration", back_populates="contest", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Contest {self.title}>"

