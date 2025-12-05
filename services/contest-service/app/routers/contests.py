from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from app.database import get_db
from app.models.contest import Contest
from app.schemas.contest import ContestCreate, ContestUpdate, ContestResponse, ContestWithProblems
from app.dependencies import get_current_user, require_staff

router = APIRouter()

@router.post("/", response_model=ContestResponse, status_code=status.HTTP_201_CREATED)
async def create_contest(
    contest_data: ContestCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_staff)
):
    """Create a new contest (staff only)"""
    if contest_data.end_time <= contest_data.start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time must be after start time"
        )
    
    db_contest = Contest(
        **contest_data.dict(),
        created_by=UUID(current_user["id"])
    )
    db.add(db_contest)
    db.commit()
    db.refresh(db_contest)
    return db_contest

@router.get("/", response_model=List[ContestResponse])
async def list_contests(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    active_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    """List all contests"""
    query = db.query(Contest)
    
    if active_only:
        query = query.filter(Contest.is_active == True)
    
    contests = query.order_by(Contest.start_time.desc()).offset(skip).limit(limit).all()
    return contests

@router.get("/{contest_id}", response_model=ContestWithProblems)
async def get_contest(
    contest_id: UUID,
    db: Session = Depends(get_db)
):
    """Get contest by ID with problems"""
    contest = db.query(Contest).filter(Contest.id == contest_id).first()
    if not contest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contest not found"
        )
    return contest

@router.put("/{contest_id}", response_model=ContestResponse)
async def update_contest(
    contest_id: UUID,
    contest_update: ContestUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_staff)
):
    """Update contest (staff only)"""
    contest = db.query(Contest).filter(Contest.id == contest_id).first()
    if not contest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contest not found"
        )
    
    update_data = contest_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(contest, field, value)
    
    db.commit()
    db.refresh(contest)
    return contest

@router.delete("/{contest_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contest(
    contest_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_staff)
):
    """Delete contest (staff only)"""
    contest = db.query(Contest).filter(Contest.id == contest_id).first()
    if not contest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contest not found"
        )
    
    db.delete(contest)
    db.commit()
    return None

@router.post("/{contest_id}/open-registration", response_model=ContestResponse)
async def open_registration(
    contest_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_staff)
):
    """Open contest registration (staff only)"""
    contest = db.query(Contest).filter(Contest.id == contest_id).first()
    if not contest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contest not found"
        )
    
    contest.registration_open = True
    db.commit()
    db.refresh(contest)
    return contest

@router.post("/{contest_id}/close-registration", response_model=ContestResponse)
async def close_registration(
    contest_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_staff)
):
    """Close contest registration (staff only)"""
    contest = db.query(Contest).filter(Contest.id == contest_id).first()
    if not contest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contest not found"
        )
    
    contest.registration_open = False
    db.commit()
    db.refresh(contest)
    return contest

