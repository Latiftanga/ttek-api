import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    school_id: Mapped[str] = mapped_column(String, ForeignKey("schools.id"), nullable=False, index=True)
    student_id: Mapped[str] = mapped_column(String, ForeignKey("students.id"), nullable=False, index=True)
    class_id: Mapped[str] = mapped_column(String, ForeignKey("classes.id"), nullable=False)
    subject: Mapped[str] = mapped_column(String(100), nullable=False)
    term: Mapped[str] = mapped_column(String(20), nullable=False)         # Term 1, Term 2, Term 3
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False)
    class_score: Mapped[float | None] = mapped_column(Float, nullable=True)   # 30%
    exam_score: Mapped[float | None] = mapped_column(Float, nullable=True)    # 70%
    total_score: Mapped[float | None] = mapped_column(Float, nullable=True)   # 100%
    grade: Mapped[str | None] = mapped_column(String(5), nullable=True)       # A, B, C...
    position: Mapped[int | None] = mapped_column(Integer, nullable=True)
    remarks: Mapped[str | None] = mapped_column(String(255), nullable=True)
    recorded_by: Mapped[str | None] = mapped_column(String, ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
