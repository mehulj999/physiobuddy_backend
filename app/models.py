# physiobyddy-backend/app/models.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Enum,
    Boolean,
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

# Import Base from database.py instead of creating a new one
from .database import Base


class ExerciseType(str, enum.Enum):
    BICEP_CURL = "bicep_curl"
    # Add more exercises later
    # PUSH_UP = "push_up"
    # SQUAT = "squat"


class ArmType(str, enum.Enum):
    LEFT = "left"
    RIGHT = "right"
    BOTH = "both"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    # Relationships
    workout_sessions = relationship("WorkoutSession", back_populates="user")
    personal_bests = relationship("PersonalBest", back_populates="user")


class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_date = Column(DateTime, default=datetime.now)
    total_duration = Column(Float)  # in seconds
    notes = Column(String, nullable=True)

    # Relationships
    user = relationship("User", back_populates="workout_sessions")
    exercises = relationship("ExerciseSet", back_populates="session")


class ExerciseSet(Base):
    __tablename__ = "exercise_sets"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("workout_sessions.id"), nullable=False)
    exercise_type = Column(Enum(ExerciseType), nullable=False)
    arm_used = Column(Enum(ArmType), nullable=False)

    # Core metrics
    reps_completed = Column(Integer, nullable=False)
    set_number = Column(Integer, nullable=False)  # 1st set, 2nd set, etc.
    duration = Column(Float)  # duration of this set in seconds

    # Quality metrics
    avg_angle_range = Column(Float)  # average (max_angle - min_angle)
    form_quality_score = Column(Float)  # 0.0 to 1.0
    rep_consistency_score = Column(Float)  # standard deviation of angles
    avg_rep_speed = Column(Float)  # average seconds per rep

    # Raw angle data (optional - for detailed analysis)
    min_angle_achieved = Column(Float)
    max_angle_achieved = Column(Float)

    created_at = Column(DateTime, default=datetime.now)

    # Relationships
    session = relationship("WorkoutSession", back_populates="exercises")


class PoseFrame(Base):
    __tablename__ = "pose_frames"

    id = Column(Integer, primary_key=True, index=True)
    exercise_set_id = Column(Integer, ForeignKey("exercise_sets.id"), nullable=False)

    timestamp = Column(Float, nullable=False)  # seconds from start of set
    frame_number = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.now)

    # Relationships
    exercise_set = relationship("ExerciseSet", backref="pose_frames")
    joint_positions = relationship("JointPosition", back_populates="frame")


class JointType(str, enum.Enum):
    SHOULDER = "shoulder"
    ELBOW = "elbow"
    WRIST = "wrist"
    HIP = "hip"
    KNEE = "knee"
    ANKLE = "ankle"
    # Extend as needed (including "left_" / "right_" variants)


class JointPosition(Base):
    __tablename__ = "joint_positions"

    id = Column(Integer, primary_key=True, index=True)
    frame_id = Column(Integer, ForeignKey("pose_frames.id"), nullable=False)

    joint_type = Column(Enum(JointType), nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    z = Column(Float, nullable=True)  # Optional, if using 3D data

    confidence = Column(Float, nullable=True)  # From BlazePose if available

    # Relationships
    frame = relationship("PoseFrame", back_populates="joint_positions")


class PersonalBest(Base):
    __tablename__ = "personal_bests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exercise_type = Column(Enum(ExerciseType), nullable=False)
    arm_used = Column(Enum(ArmType), nullable=False)

    # Best metrics
    max_reps_single_set = Column(Integer)
    max_total_reps_session = Column(Integer)
    best_form_score = Column(Float)
    longest_session_duration = Column(Float)

    # Tracking
    achieved_date = Column(DateTime, default=datetime.now)
    last_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    user = relationship("User", back_populates="personal_bests")


class UserStreak(Base):
    __tablename__ = "user_streaks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_workout_date = Column(DateTime)
    streak_start_date = Column(DateTime)

    # Relationships
    user = relationship("User")


class ExerciseProgress(Base):
    __tablename__ = "exercise_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exercise_type = Column(Enum(ExerciseType), nullable=False)
    arm_used = Column(Enum(ArmType), nullable=False)

    # Weekly/Monthly aggregates
    week_start_date = Column(DateTime, nullable=False)
    total_reps = Column(Integer, default=0)
    total_sets = Column(Integer, default=0)
    total_duration = Column(Float, default=0.0)
    avg_form_score = Column(Float)
    workout_count = Column(Integer, default=0)

    # Relationships
    user = relationship("User")


class VideoMetadata(Base):
    __tablename__ = "video_metadata"

    id = Column(Integer, primary_key=True)
    exercise_set_id = Column(Integer, ForeignKey("exercise_sets.id"))
    frame_rate = Column(Float)
    resolution = Column(String)
    duration = Column(Float)
    video_url = Column(String)  # if storing video externally (e.g., S3)
