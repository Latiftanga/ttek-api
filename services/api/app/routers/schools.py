from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List

from app.core.database import get_db
from app.core.deps import get_current_user, get_current_superadmin
from app.models.school import School
from app.models.user import User

router = APIRouter()


class SchoolCreate(BaseModel):
    name: str
    code: str
    region: str
    district: str
    address: str | None = None
    phone: str | None = None
    email: str | None = None
    school_type: str = "basic"


class SchoolResponse(BaseModel):
    id: str
    name: str
    code: str
    region: str
    district: str
    school_type: str
    is_active: bool

    class Config:
        from_attributes = True


@router.get("/", response_model=List[SchoolResponse])
async def list_schools(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == "superadmin":
        result = await db.execute(select(School).where(School.is_active == True))
    else:
        result = await db.execute(
            select(School).where(
                School.id == current_user.school_id,
                School.is_active == True,
            )
        )
    return result.scalars().all()


@router.post("/", response_model=SchoolResponse, status_code=201)
async def create_school(
    payload: SchoolCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_superadmin),
):
    existing = await db.execute(select(School).where(School.code == payload.code))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="School code already exists")

    school = School(**payload.model_dump())
    db.add(school)
    await db.flush()
    return school


@router.get("/{school_id}", response_model=SchoolResponse)
async def get_school(
    school_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(School).where(School.id == school_id))
    school = result.scalar_one_or_none()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school
