"""
Abstract interface for cache providers
"""

from abc import ABC, abstractmethod
from typing import Optional, Any, Dict  # ADD THIS LINE

class CacheProvider(ABC):
    """Interface for cache providers"""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        pass
    
    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache"""
        pass
    
    @abstractmethod
    async def delete(self, key: str):
        """Delete from cache"""
        pass
    
    @abstractmethod
    async def clear(self):
        """Clear entire cache"""
        pass
    
    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:  # This line needs Dict
        """Get cache statistics"""
        pass