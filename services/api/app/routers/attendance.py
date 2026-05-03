from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def list_attendance():
    return {"message": "attendance endpoint - coming soon"}
