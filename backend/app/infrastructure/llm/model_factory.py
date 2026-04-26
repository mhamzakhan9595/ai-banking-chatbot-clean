"""
Factory for creating LLM providers
"""

from app.domain.interfaces.llm_interface import LLMProvider
from app.infrastructure.llm.huggingface_llm import HuggingFaceLLM

class LLMFactory:
    """Factory to create LLM providers"""
    
    @staticmethod
    def create(model_type: str = "huggingface", **kwargs) -> LLMProvider:
        """Create an LLM provider instance"""
        if model_type == "huggingface":
            model_name = kwargs.get("model_name", "microsoft/DialoGPT-small")
            return HuggingFaceLLM(model_name=model_name)
        else:
            raise ValueError(f"Unknown model type: {model_type}")