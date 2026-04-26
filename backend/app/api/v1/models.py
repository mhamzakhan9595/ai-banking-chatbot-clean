"""
Model management endpoints - Version 1
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.core.containers import container

router = APIRouter(prefix="/api/v1/models", tags=["models"])

class ModelSwitchRequest(BaseModel):
    model_name: str

def get_model_info():
    """Get current model information"""
    return container.llm_provider.get_info()

@router.get("")
async def list_models():
    """List all available models"""
    current = get_model_info()
    
    available_models = [
        {
            "name": "microsoft/DialoGPT-small",
            "size": "124M",
            "speed": "fast",
            "quality": "good",
            "recommended": True,
            "is_current": current.get("model") == "microsoft/DialoGPT-small"
        },
        {
            "name": "microsoft/DialoGPT-medium",
            "size": "355M", 
            "speed": "medium",
            "quality": "better",
            "recommended": False,
            "is_current": current.get("model") == "microsoft/DialoGPT-medium"
        },
        {
            "name": "microsoft/DialoGPT-large",
            "size": "762M",
            "speed": "slow",
            "quality": "best",
            "recommended": False,
            "is_current": current.get("model") == "microsoft/DialoGPT-large"
        }
    ]
    
    return {
        "current_model": current,
        "available_models": available_models
    }

@router.get("/current")
async def get_current_model():
    """Get current model information"""
    return get_model_info()

@router.post("/switch")
async def switch_model(request: ModelSwitchRequest):
    """
    Switch to a different model
    Note: This will take time to load the new model
    """
    try:
        # Store the requested model in settings
        from app.core.config import settings
        settings.model_name = request.model_name
        
        # Reinitialize the LLM provider
        from app.infrastructure.llm.model_factory import LLMFactory
        container._llm_provider = None  # Clear existing
        container._chat_service = None  # Clear chat service
        new_provider = LLMFactory.create(
            model_type="huggingface",
            model_name=request.model_name
        )
        container._llm_provider = new_provider
        
        return {
            "message": f"Switched to {request.model_name}",
            "status": "success",
            "model_info": new_provider.get_info()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to switch model: {str(e)}")