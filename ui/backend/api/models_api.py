"""
Models API endpoints
"""

from typing import List, Dict
from fastapi import APIRouter

router = APIRouter()


@router.get("/types")
async def get_model_types():
    """Get available model types"""
    return {
        "types": [
            {
                "id": "flux",
                "name": "Flux",
                "description": "Flux AI models with advanced features",
                "default_resolution": "1024x1024",
            },
            {
                "id": "sdxl",
                "name": "SDXL",
                "description": "Stable Diffusion XL models",
                "default_resolution": "1024x1024",
            },
            {
                "id": "pony",
                "name": "Pony",
                "description": "Pony Diffusion models",
                "default_resolution": "1024x1024",
            },
            {
                "id": "sd1.5",
                "name": "SD 1.5",
                "description": "Stable Diffusion 1.5 models",
                "default_resolution": "512x512",
            },
        ]
    }


@router.get("/loras")
async def get_available_loras():
    """Get available LoRA models"""
    # This would scan the actual models directory in production
    return {
        "loras": [
            {"name": "detail_enhancer", "path": "detail_enhancer.safetensors"},
            {"name": "style_anime", "path": "anime_style.safetensors"},
            {"name": "quality_boost", "path": "quality_boost.safetensors"},
        ]
    }


@router.get("/resolutions")
async def get_common_resolutions():
    """Get common resolution presets"""
    return {
        "resolutions": [
            {"width": 512, "height": 512, "name": "SD 1.5 Square", "ratio": "1:1"},
            {"width": 768, "height": 512, "name": "SD 1.5 Landscape", "ratio": "3:2"},
            {"width": 512, "height": 768, "name": "SD 1.5 Portrait", "ratio": "2:3"},
            {"width": 1024, "height": 1024, "name": "SDXL Square", "ratio": "1:1"},
            {
                "width": 1216,
                "height": 832,
                "name": "SDXL Landscape",
                "ratio": "3:2",
            },
            {"width": 832, "height": 1216, "name": "SDXL Portrait", "ratio": "2:3"},
            {"width": 1344, "height": 768, "name": "Wide", "ratio": "16:9"},
            {"width": 768, "height": 1344, "name": "Tall", "ratio": "9:16"},
        ]
    }
