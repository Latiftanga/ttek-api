from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def list_classes():
    return {"message": "classes endpoint - coming soon"}
