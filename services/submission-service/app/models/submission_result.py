from sqlalchemy import Column, String, Integer, ForeignKey, Text, Numeric, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.database import Base

class TestCaseStatus(str, enum.Enum):
    PASSED = "passed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    ERROR = "error"

class SubmissionResult(Base):
    __tablename__ = "submission_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    submission_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    test_case_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    status = Column(SQLEnum(TestCaseStatus), nullable=False)
    execution_time_ms = Column(Integer)
    memory_used_mb = Column(Numeric(10, 2))
    actual_output = Column(Text)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    submission = relationship("Submission", back_populates="results")

    def __repr__(self):
        return f"<SubmissionResult {self.id}>"

