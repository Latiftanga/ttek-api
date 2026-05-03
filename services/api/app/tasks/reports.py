from app.core.celery_app import celery_app

@celery_app.task
def daily_attendance_report():
    print("Running daily attendance report...")
    return {"status": "done"}
