from sqlalchemy import Column, String, Integer, ForeignKey, Text, Numeric, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.database import Base

class SubmissionStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    ACCEPTED = "accepted"
    WRONG_ANSWER = "wrong_answer"
    TIME_LIMIT_EXCEEDED = "time_limit_exceeded"
    RUNTIME_ERROR = "runtime_error"
    COMPILATION_ERROR = "compilation_error"

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contest_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    problem_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    code = Column(Text, nullable=False)
    language = Column(String(10), nullable=False, default="cpp")
    status = Column(SQLEnum(SubmissionStatus), nullable=False, default=SubmissionStatus.PENDING, index=True)
    execution_time_ms = Column(Integer)
    memory_used_mb = Column(Numeric(10, 2))
    test_cases_passed = Column(Integer, default=0)
    total_test_cases = Column(Integer, default=0)
    score = Column(Numeric(10, 2), default=0)
    error_message = Column(Text)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    evaluated_at = Column(DateTime(timezone=True))

    # Relationships
    results = relationship("SubmissionResult", back_populates="submission", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Submission {self.id}>"

