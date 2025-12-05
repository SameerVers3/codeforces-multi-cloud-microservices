from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.database import Base

class LeaderboardEntry(Base):
    __tablename__ = "leaderboard_entries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contest_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    total_score = Column(Numeric(10, 2), default=0)
    total_submissions = Column(Integer, default=0)
    total_accepted = Column(Integer, default=0)
    last_submission_at = Column(DateTime(timezone=True))
    rank = Column(Integer, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

