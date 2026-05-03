from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "ttek_sis",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.reports",
        "app.tasks.notifications",
        "app.tasks.sync",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Africa/Accra",
    enable_utc=True,
    beat_schedule={
        "daily-attendance-report": {
            "task": "app.tasks.reports.daily_attendance_report",
            "schedule": 86400.0,  # every 24 hours
        },
    },
)
