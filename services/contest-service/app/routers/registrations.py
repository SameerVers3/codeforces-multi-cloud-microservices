from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.registration import ContestRegistration
from app.models.contest import Contest
from app.schemas.registration import RegistrationResponse
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/contest/{contest_id}/register", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register_for_contest(
    contest_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Register for a contest"""
    # Check if contest exists
    contest = db.query(Contest).filter(Contest.id == contest_id).first()
    if not contest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contest not found"
        )
    
    # Check if registration is open
    if not contest.registration_open:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration is closed for this contest"
        )
    
    # Check if already registered
    existing_registration = db.query(ContestRegistration).filter(
        ContestRegistration.contest_id == contest_id,
        ContestRegistration.user_id == UUID(current_user["id"])
    ).first()
    
    if existing_registration:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already registered for this contest"
        )
    
    # Check max participants
    if contest.max_participants:
        current_registrations = db.query(ContestRegistration).filter(
            ContestRegistration.contest_id == contest_id
        ).count()
        if current_registrations >= contest.max_participants:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contest is full"
            )
    
    # Create registration
    registration = ContestRegistration(
        contest_id=contest_id,
        user_id=UUID(current_user["id"])
    )
    db.add(registration)
    db.commit()
    db.refresh(registration)
    return registration

@router.get("/contest/{contest_id}/registrations", response_model=List[RegistrationResponse])
async def list_contest_registrations(
    contest_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List all registrations for a contest"""
    registrations = db.query(ContestRegistration).filter(
        ContestRegistration.contest_id == contest_id
    ).all()
    return registrations

@router.get("/user/{user_id}/registrations", response_model=List[RegistrationResponse])
async def list_user_registrations(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List all contests a user is registered for"""
    # Users can only view their own registrations unless staff
    if UUID(current_user["id"]) != user_id and current_user.get("role") != "staff":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    registrations = db.query(ContestRegistration).filter(
        ContestRegistration.user_id == user_id
    ).all()
    return registrations

@router.delete("/contest/{contest_id}/unregister", status_code=status.HTTP_204_NO_CONTENT)
async def unregister_from_contest(
    contest_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Unregister from a contest"""
    registration = db.query(ContestRegistration).filter(
        ContestRegistration.contest_id == contest_id,
        ContestRegistration.user_id == UUID(current_user["id"])
    ).first()
    
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    
    db.delete(registration)
    db.commit()
    return None

@router.get("/contest/{contest_id}/is-registered")
async def check_registration(
    contest_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Check if user is registered for a contest"""
    registration = db.query(ContestRegistration).filter(
        ContestRegistration.contest_id == contest_id,
        ContestRegistration.user_id == UUID(current_user["id"])
    ).first()
    
    return {"is_registered": registration is not None}

