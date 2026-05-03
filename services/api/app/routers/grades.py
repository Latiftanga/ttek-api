from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def list_grades():
    return {"message": "grades endpoint - coming soon"}
