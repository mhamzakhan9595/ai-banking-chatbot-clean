"""
Abstract interface for rate limiters
"""

from abc import ABC, abstractmethod
from typing import Tuple  # ADD THIS LINE

class RateLimiter(ABC):
    """Interface for rate limiters"""
    
    @abstractmethod
    async def is_allowed(self, key: str) -> Tuple[bool, int]:  # Tuple needed
        """Check if request is allowed"""
        pass
    
    @abstractmethod
    async def get_remaining(self, key: str) -> int:
        """Get remaining requests"""
        pass
    
    @abstractmethod
    async def reset(self, key: str):
        """Reset rate limit for key"""
        pass