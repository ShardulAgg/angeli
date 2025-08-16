from fastapi import APIRouter
from datetime import datetime

router = APIRouter(
    prefix="/api",
    tags=["api"]
)


@router.get("/status")
async def get_status():
    return {
        "status": "operational",
        "timestamp": datetime.now(),
        "service": "api"
    }

@router.post("/generate_scene")
async def generate_scene():
    pass

@router.get("/info")
async def get_info():
    return {
        "name": "FastAPI Backend",
        "version": "1.0.0",
        "description": "API service"
    }