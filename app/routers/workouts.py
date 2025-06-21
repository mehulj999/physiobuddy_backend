# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.models import models
# from app.database import get_db
# from app.schemas.exercise import ExerciseCreate, ExerciseOut
# from app.auth.auth_handler import get_current_user

# router = APIRouter()


# @router.post("/", response_model=ExerciseOut)
# def create_exercise(
#     exercise: ExerciseCreate,
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(get_current_user),
# ):
#     new_exercise = models.Exercise(**exercise.dict(), user_id=current_user.id)
#     db.add(new_exercise)
#     db.commit()
#     db.refresh(new_exercise)
#     return new_exercise


# @router.get("/", response_model=list[ExerciseOut])
# def get_exercises(
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(get_current_user),
# ):
#     return (
#         db.query(models.Exercise)
#         .filter(models.Exercise.user_id == current_user.id)
#         .all()
#     )


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models import User, WorkoutSession, ExerciseSet, PersonalBest
from app.schemas import (
    WorkoutSessionCreate,
    WorkoutSessionResponse,
    ExerciseSetCreate,
    ExerciseSetResponse,
    PersonalBestResponse,
)
from app.auth.auth import get_current_user

router = APIRouter()


@router.post("/sessions", response_model=WorkoutSessionResponse)
def create_workout_session(
    session_data: WorkoutSessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new workout session."""
    db_session = WorkoutSession(user_id=current_user.id, notes=session_data.notes)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


@router.get("/sessions", response_model=List[WorkoutSessionResponse])
def get_user_sessions(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get user's workout sessions."""
    sessions = (
        db.query(WorkoutSession)
        .filter(WorkoutSession.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return sessions


@router.post("/sessions/{session_id}/exercises", response_model=ExerciseSetResponse)
def add_exercise_to_session(
    session_id: int,
    exercise_data: ExerciseSetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add an exercise set to a workout session."""
    # Verify session belongs to current user
    session = (
        db.query(WorkoutSession)
        .filter(
            WorkoutSession.id == session_id, WorkoutSession.user_id == current_user.id
        )
        .first()
    )

    if not session:
        raise HTTPException(status_code=404, detail="Workout session not found")

    db_exercise = ExerciseSet(session_id=session_id, **exercise_data.dict())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)

    # Update session total duration if provided
    if exercise_data.duration:
        if session.total_duration:
            session.total_duration += exercise_data.duration
        else:
            session.total_duration = exercise_data.duration
        db.commit()

    return db_exercise


@router.get(
    "/sessions/{session_id}/exercises", response_model=List[ExerciseSetResponse]
)
def get_session_exercises(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all exercises from a workout session."""
    # Verify session belongs to current user
    session = (
        db.query(WorkoutSession)
        .filter(
            WorkoutSession.id == session_id, WorkoutSession.user_id == current_user.id
        )
        .first()
    )

    if not session:
        raise HTTPException(status_code=404, detail="Workout session not found")

    exercises = db.query(ExerciseSet).filter(ExerciseSet.session_id == session_id).all()
    return exercises


@router.get("/personal-bests", response_model=List[PersonalBestResponse])
def get_personal_bests(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get user's personal bests."""
    personal_bests = (
        db.query(PersonalBest).filter(PersonalBest.user_id == current_user.id).all()
    )
    return personal_bests
