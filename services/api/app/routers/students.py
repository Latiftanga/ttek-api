from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from typing import List
from datetime import date

from app.core.database import get_db
from app.core.deps import get_current_user, get_current_teacher
from app.models.student import Student
from app.models.user import User

router = APIRouter()


class StudentCreate(BaseModel):
    student_id: str
    school_id: str
    first_name: str
    last_name: str
    other_names: str | None = None
    date_of_birth: date | None = None
    gender: str
    guardian_name: str | None = None
    guardian_phone: str | None = None
    guardian_email: str | None = None
    guardian_relation: str | None = None
    address: str | None = None
    admission_date: date | None = None
    academic_year: str | None = None
    class_id: str | None = None


class StudentResponse(BaseModel):
    id: str
    student_id: str
    school_id: str
    first_name: str
    last_name: str
    gender: str
    class_id: str | None
    guardian_name: str | None
    guardian_phone: str | None
    is_active: bool

    class Config:
        from_attributes = True


@router.get("/", response_model=List[StudentResponse])
async def list_students(
    school_id: str | None = Query(None),
    class_id: str | None = Query(None),
    search: str | None = Query(None),
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_teacher),
):
    query = select(Student).where(Student.is_active == True)

    if current_user.role != "superadmin":
        query = query.where(Student.school_id == current_user.school_id)
    elif school_id:
        query = query.where(Student.school_id == school_id)

    if class_id:
        query = query.where(Student.class_id == class_id)

    if search:
        query = query.where(
            (Student.first_name.ilike(f"%{search}%")) |
            (Student.last_name.ilike(f"%{search}%")) |
            (Student.student_id.ilike(f"%{search}%"))
        )

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/", response_model=StudentResponse, status_code=201)
async def create_student(
    payload: StudentCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_teacher),
):
    existing = await db.execute(
        select(Student).where(Student.student_id == payload.student_id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Student ID already exists")

    student = Student(**payload.model_dump())
    db.add(student)
    await db.flush()
    return student


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_teacher),
):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
