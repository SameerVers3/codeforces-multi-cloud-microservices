from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.leaderboard_entry import LeaderboardEntry

router = APIRouter()

@router.get("/contest/{contest_id}")
async def get_leaderboard(
    contest_id: UUID,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get leaderboard for a contest"""
    entries = db.query(LeaderboardEntry).filter(
        LeaderboardEntry.contest_id == contest_id
    ).order_by(
        LeaderboardEntry.total_score.desc(),
        LeaderboardEntry.last_submission_at.asc()
    ).limit(limit).all()
    
    return [
        {
            "rank": entry.rank or idx + 1,
            "user_id": str(entry.user_id),
            "total_score": float(entry.total_score),
            "total_submissions": entry.total_submissions,
            "total_accepted": entry.total_accepted,
            "last_submission_at": entry.last_submission_at.isoformat() if entry.last_submission_at else None
        }
        for idx, entry in enumerate(entries)
    ]

