from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from app.models import ExerciseType, ArmType


# User schemas
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# Workout Session schemas
class WorkoutSessionCreate(BaseModel):
    notes: Optional[str] = None


class WorkoutSessionResponse(BaseModel):
    id: int
    user_id: int
    session_date: datetime
    total_duration: Optional[float] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


# Exercise Set schemas
class ExerciseSetCreate(BaseModel):
    exercise_type: ExerciseType
    arm_used: ArmType
    reps_completed: int
    set_number: int
    duration: Optional[float] = None
    avg_angle_range: Optional[float] = None
    form_quality_score: Optional[float] = None
    rep_consistency_score: Optional[float] = None
    avg_rep_speed: Optional[float] = None
    min_angle_achieved: Optional[float] = None
    max_angle_achieved: Optional[float] = None


class ExerciseSetResponse(ExerciseSetCreate):
    id: int
    session_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Personal Best schemas
class PersonalBestResponse(BaseModel):
    id: int
    user_id: int
    exercise_type: ExerciseType
    arm_used: ArmType
    max_reps_single_set: Optional[int] = None
    max_total_reps_session: Optional[int] = None
    best_form_score: Optional[float] = None
    longest_session_duration: Optional[float] = None
    achieved_date: datetime
    last_updated: datetime

    class Config:
        from_attributes = True


# Streak schemas
class UserStreakResponse(BaseModel):
    id: int
    user_id: int
    current_streak: int
    longest_streak: int
    last_workout_date: Optional[datetime] = None
    streak_start_date: Optional[datetime] = None

    class Config:
        from_attributes = True


# Progress schemas
class ExerciseProgressResponse(BaseModel):
    id: int
    user_id: int
    exercise_type: ExerciseType
    arm_used: ArmType
    week_start_date: datetime
    total_reps: int
    total_sets: int
    total_duration: float
    avg_form_score: Optional[float] = None
    workout_count: int

    class Config:
        from_attributes = True
