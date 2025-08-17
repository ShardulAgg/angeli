from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import tempfile
import os
from logic.scene_generator import generate_storyboard_scenes_gemini
from logic.video_generator import generate_video
from logic.push_content import push_content
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
async def generate_scene(
    product_image: Optional[UploadFile] = File(None),
    product_name: Optional[str] = Form("product"),
    brand_name: Optional[str] = Form("brand"),
    brand_personality: Optional[str] = Form("trendy and modern"),
):
    """
    Generate storyboard scenes for content creation.
    
    Args:
        product_image: Product image file (optional)
        product_name: Name of the product
        brand_name: Name of the brand
        brand_personality: Brand personality description
        influencer_name: Name of the influencer (default: angeli)
        meme_type: Type of meme/content (default: GRWM)
    """
    try:
        # Save product image if provided
        influencer_name="angeli"
        meme_type="GRWM"
        product_image_file = None
        if product_image:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                content = await product_image.read()
                tmp_file.write(content)
                product_image_file = tmp_file.name
        
        # Generate storyboard
        result = generate_storyboard_scenes_gemini(
            product_image=product_image_file if product_image_file else None,
            product_name=product_name,
            brand_name=brand_name,
            brand_personality=brand_personality,
            influencer_name=influencer_name,
            meme_type=meme_type
        )
        video_path = generate_video(prompts=result[0],initial_image_path=result[1]) 
        # Clean up temp file if created

        pushed_content = push_content( video_path=video_path, title="GRWM")
        if product_image_file and os.path.exists(product_image_file):
            os.unlink(product_image_file)
        
        return {
            "status": "success",
            "message": "Storyboard generated successfully"
        }
        
    except Exception as e:
        # Clean up temp file if it exists
        if 'product_image_file' in locals() and product_image_file:
            try:
                print(str(e))
                os.unlink(product_image_file)
            except:
                pass
        
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/info")
async def get_info():
    return {
        "name": "FastAPI Backend",
        "version": "1.0.0",
        "description": "API service"
    }