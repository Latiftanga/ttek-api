from app.core.celery_app import celery_app

@celery_app.task
def send_sms_notification(phone: str, message: str):
    print(f"Sending SMS to {phone}: {message}")
    return {"status": "sent"}
