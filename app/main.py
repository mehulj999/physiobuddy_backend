from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.auth import router as auth_router
from app.routers.workouts import router as workouts_router

app = FastAPI(
    title="PhysioBuddy API",
    description="Backend API for physiotherapy exercise tracking",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(workouts_router, prefix="/workouts", tags=["Workouts"])


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the PhysioBuddy API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
