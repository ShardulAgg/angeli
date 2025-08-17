from fastapi import APIRouter, UploadFile, File, Form
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/api",
    tags=["api"]
)

class SceneGeneratorInput(BaseModel):
    product_name: Optional[str] = None
    brand_name: Optional[str] = None
    brand_personality: Optional[str] = None
    influencer_name: Optional[str] = None
    meme_type: Optional[str] = "GRWM"

@router.get("/status")
async def get_status():
    return {
        "status": "operational",
        "timestamp": datetime.now(),
        "service": "api"
    }

@router.post("/generate_scene")
async def generate_scene(
    product_image: Optional[UploadFile] = File(None),
    product_name: Optional[str] = Form(None),
    brand_name: Optional[str] = Form(None),
    brand_personality: Optional[str] = Form(None),
    influencer_name: Optional[str] = Form(None),
    meme_type: Optional[str] = Form("GRWM")
):
    image_info = None
    if product_image:
        image_info = {
            "filename": product_image.filename,
            "content_type": product_image.content_type,
            "size": product_image.size
        }
    
    return {
        "status": "success",
        "message": "Scene generation initiated",
        "input": {
            "product_image": image_info,
            "product_name": product_name,
            "brand_name": brand_name,
            "brand_personality": brand_personality,
            "influencer_name": influencer_name,
            "meme_type": meme_type
        }
    }

@router.get("/info")
async def get_info():
    return {
        "name": "FastAPI Backend",
        "version": "1.0.0",
        "description": "API service"
    }