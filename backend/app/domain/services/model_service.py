"""
Model management service
"""

import logging
from typing import Dict, Any, List
from app.domain.interfaces.llm_interface import LLMProvider
from app.core.exceptions import ModelNotFoundError

logger = logging.getLogger(__name__)

class ModelService:
    """Service for managing LLM models"""
    
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider
    
    async def get_current_model(self) -> Dict[str, Any]:
        """Get current model information"""
        return self.llm_provider.get_info()
    
    async def list_available_models(self) -> List[Dict[str, Any]]:
        """List all available models"""
        return [
            {
                "name": "microsoft/DialoGPT-small",
                "size": "124M",
                "speed": "fast",
                "quality": "good",
                "recommended": True
            },
            {
                "name": "microsoft/DialoGPT-medium",
                "size": "355M",
                "speed": "medium",
                "quality": "better",
                "recommended": False
            },
            {
                "name": "microsoft/DialoGPT-large",
                "size": "762M",
                "speed": "slow",
                "quality": "best",
                "recommended": False
            }
        ]
    
    async def switch_model(self, model_name: str) -> Dict[str, Any]:
        """Switch to a different model"""
        # Check if model is in available list
        available_models = await self.list_available_models()
        model_names = [m["name"] for m in available_models]
        
        if model_name not in model_names:
            raise ModelNotFoundError(model_name)
        
        # Note: Model switching requires reinitialization
        # This is handled by the factory
        logger.info(f"Model switch requested to {model_name}")
        
        return {
            "message": f"Switched to {model_name}",
            "previous_model": self.llm_provider.get_info()["model"],
            "new_model": model_name,
            "note": "Model will be loaded on next request"
        }