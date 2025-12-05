from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
import httpx

from app.database import get_db
from app.models.submission import Submission, SubmissionStatus
from app.schemas.submission import SubmissionCreate, SubmissionResponse, SubmissionWithResults
from app.dependencies import get_current_user, verify_contest_access
from app.services.queue import submission_queue
from app.config import settings

router = APIRouter()

@router.post("/", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
async def create_submission(
    submission_data: SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Submit code for evaluation"""
    user_id = UUID(current_user["id"])
    
    # Verify contest access
    if not await verify_contest_access(submission_data.contest_id, current_user, db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be registered for this contest to submit"
        )
    
    # Verify problem exists and belongs to contest
    async with httpx.AsyncClient() as client:
        problem_response = await client.get(
            f"{settings.CONTEST_SERVICE_URL}/api/v1/problems/{submission_data.problem_id}",
            headers={"Authorization": f"Bearer {current_user.get('token', '')}"}
        )
        if problem_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Problem not found"
            )
        problem_data = problem_response.json()
        
        if str(problem_data["contest_id"]) != str(submission_data.contest_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Problem does not belong to this contest"
            )
        
        # Get test cases
        test_cases_response = await client.get(
            f"{settings.CONTEST_SERVICE_URL}/api/v1/problems/{submission_data.problem_id}",
            headers={"Authorization": f"Bearer {current_user.get('token', '')}"}
        )
        test_cases_data = test_cases_response.json().get("test_cases", [])
    
    # Create submission record
    db_submission = Submission(
        contest_id=submission_data.contest_id,
        problem_id=submission_data.problem_id,
        user_id=user_id,
        code=submission_data.code,
        language=submission_data.language,
        status=SubmissionStatus.PENDING,
        total_test_cases=len(test_cases_data)
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    # Publish to queue for execution
    try:
        submission_queue.publish_submission(
            submission_id=str(db_submission.id),
            problem_id=str(submission_data.problem_id),
            code=submission_data.code,
            test_cases=test_cases_data
        )
    except Exception as e:
        # Update submission status to error
        db_submission.status = SubmissionStatus.COMPILATION_ERROR
        db_submission.error_message = f"Failed to queue submission: {str(e)}"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to queue submission for execution"
        )
    
    return db_submission

@router.get("/", response_model=List[SubmissionResponse])
async def list_submissions(
    contest_id: Optional[UUID] = Query(None),
    problem_id: Optional[UUID] = Query(None),
    user_id: Optional[UUID] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List submissions with optional filters"""
    query = db.query(Submission)
    
    # Users can only see their own submissions unless staff
    if current_user.get("role") != "staff":
        query = query.filter(Submission.user_id == UUID(current_user["id"]))
    elif user_id:
        query = query.filter(Submission.user_id == user_id)
    
    if contest_id:
        query = query.filter(Submission.contest_id == contest_id)
    if problem_id:
        query = query.filter(Submission.problem_id == problem_id)
    
    submissions = query.order_by(Submission.submitted_at.desc()).offset(skip).limit(limit).all()
    return submissions

@router.get("/{submission_id}", response_model=SubmissionWithResults)
async def get_submission(
    submission_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get submission by ID with results"""
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
    
    # Users can only see their own submissions unless staff
    if current_user.get("role") != "staff" and submission.user_id != UUID(current_user["id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return submission

@router.get("/contest/{contest_id}/user/{user_id}", response_model=List[SubmissionResponse])
async def get_user_contest_submissions(
    contest_id: UUID,
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all submissions for a user in a contest"""
    # Users can only see their own submissions unless staff
    if current_user.get("role") != "staff" and UUID(current_user["id"]) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    submissions = db.query(Submission).filter(
        Submission.contest_id == contest_id,
        Submission.user_id == user_id
    ).order_by(Submission.submitted_at.desc()).all()
    
    return submissions

