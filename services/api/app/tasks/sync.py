from app.core.celery_app import celery_app

@celery_app.task
def sync_offline_data(school_id: str):
    print(f"Syncing offline data for school {school_id}")
    return {"status": "synced"}
