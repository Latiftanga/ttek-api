from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def list_staff():
    return {"message": "staff endpoint - coming soon"}
