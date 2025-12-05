from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.problem import Problem
from app.models.contest import Contest
from app.schemas.problem import ProblemCreate, ProblemUpdate, ProblemResponse, ProblemWithTestCases
from app.dependencies import get_current_user, require_staff

router = APIRouter()

@router.post("/", response_model=ProblemResponse, status_code=status.HTTP_201_CREATED)
async def create_problem(
    problem_data: ProblemCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_staff)
):
    """Create a new problem (staff only)"""
    # Verify contest exists
    contest = db.query(Contest).filter(Contest.id == problem_data.contest_id).first()
    if not contest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contest not found"
        )
    
    db_problem = Problem(**problem_data.dict())
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem

@router.get("/contest/{contest_id}", response_model=List[ProblemResponse])
async def list_problems_by_contest(
    contest_id: UUID,
    db: Session = Depends(get_db)
):
    """List all problems for a contest"""
    problems = db.query(Problem).filter(
        Problem.contest_id == contest_id
    ).order_by(Problem.order_index).all()
    return problems

@router.get("/{problem_id}", response_model=ProblemWithTestCases)
async def get_problem(
    problem_id: UUID,
    db: Session = Depends(get_db)
):
    """Get problem by ID with test cases"""
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found"
        )
    return problem

@router.put("/{problem_id}", response_model=ProblemResponse)
async def update_problem(
    problem_id: UUID,
    problem_update: ProblemUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_staff)
):
    """Update problem (staff only)"""
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found"
        )
    
    update_data = problem_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(problem, field, value)
    
    db.commit()
    db.refresh(problem)
    return problem

@router.delete("/{problem_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_problem(
    problem_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_staff)
):
    """Delete problem (staff only)"""
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found"
        )
    
    db.delete(problem)
    db.commit()
    return None

