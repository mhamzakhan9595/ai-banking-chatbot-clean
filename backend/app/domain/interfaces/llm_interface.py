"""
Abstract interface for LLM providers
Allows swapping different LLM implementations
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, AsyncGenerator

class LLMProvider(ABC):
    """Interface for LLM providers"""
    
    @abstractmethod
    async def generate(
        self, 
        prompt: str, 
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response from LLM"""
        pass
    
    @abstractmethod
    async def generate_stream(
        self, 
        prompt: str, 
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Stream response from LLM"""
        pass
    
    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """Get provider information"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available"""
        pass