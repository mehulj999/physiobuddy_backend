from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import models
from app.database import get_db
from app.schemas.exercise import ExerciseCreate, ExerciseOut
from app.auth.auth_handler import get_current_user

router = APIRouter()


@router.post("/", response_model=ExerciseOut)
def create_exercise(
    exercise: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_exercise = models.Exercise(**exercise.dict(), user_id=current_user.id)
    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)
    return new_exercise


@router.get("/", response_model=list[ExerciseOut])
def get_exercises(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return (
        db.query(models.Exercise)
        .filter(models.Exercise.user_id == current_user.id)
        .all()
    )
