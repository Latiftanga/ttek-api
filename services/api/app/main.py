from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.routers import auth, schools, students, staff, classes, attendance, grades, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables ready")
    yield
    # Shutdown
    await engine.dispose()
    print("✅ Database connections closed")


app = FastAPI(
    title="TTEK Ghana SIS API",
    description="Student Information System for Ghanaian Schools",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router, tags=["Health"])
app.include_router(auth.router,       prefix="/auth",       tags=["Auth"])
app.include_router(schools.router,    prefix="/schools",    tags=["Schools"])
app.include_router(students.router,   prefix="/students",   tags=["Students"])
app.include_router(staff.router,      prefix="/staff",      tags=["Staff"])
app.include_router(classes.router,    prefix="/classes",    tags=["Classes"])
app.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])
app.include_router(grades.router,     prefix="/grades",     tags=["Grades"])


@app.get("/")
async def root():
    return {
        "system": "TTEK Ghana SIS",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }
